"""Adversarial scenarios: replay, omission, reordering, evidence inflation, verifier robustness.

Tests named `test_known_limit_*` assert the CURRENT (weak) behaviour on purpose, so the limitation is
executable documentation rather than a silent gap. If one of them starts failing, the limit was fixed:
update SECURITY.md in the same change.
"""
import copy
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import agenttrust_verify as av
import pytest

from .conftest import act, make_delegation

API = "/api/v1"
CLI = Path(__file__).resolve().parents[2] / "verifier" / "agenttrust_verify.py"


def _populate(client, deleg, n=3):
    for p in ["p_headphones", "p_sofa", "p_cable"][:n]:
        act(client, deleg["delegation_id"], product=p)


def _export(client):
    return client.get(f"{API}/receipts/export").json()


def _problems(ex):
    return av.verify(ex["receipts"], ex["gateway_public_key_hex"], ex["mock_merchant_public_key_hex"])


def _rehash(r):
    core = {k: v for k, v in r.items() if k not in ("current_hash", "signature")}
    r["current_hash"] = av.sha(av.canonical(core))


# ---------- replay ----------

def test_replayed_approval_does_not_execute_twice(client):
    d = make_delegation(client, auto_purchase_allowed=False)
    t = act(client, d["delegation_id"]).json()
    first = client.post(f"{API}/transactions/{t['transaction_id']}/approve")
    assert first.json()["status"] == "EXECUTED"
    again = client.post(f"{API}/transactions/{t['transaction_id']}/approve")
    assert again.status_code >= 400
    assert client.get(f"{API}/delegations/{d['delegation_id']}").json()["current"]["spent_krw"] == 120000
    executions = [r for r in client.get(f"{API}/receipts").json() if r["event_type"] == "EXECUTION_RESULT"]
    assert len(executions) == 1


def test_replayed_cancellation_does_not_double_release_budget(client, deleg):
    t = act(client, deleg["delegation_id"]).json()
    assert client.post(f"{API}/transactions/{t['transaction_id']}/cancel", json={"reason": "x"}).status_code in (200, 201)
    spent = client.get(f"{API}/delegations/{deleg['delegation_id']}").json()["current"]["spent_krw"]
    again = client.post(f"{API}/transactions/{t['transaction_id']}/cancel", json={"reason": "x"})
    assert again.status_code >= 400
    assert client.get(f"{API}/delegations/{deleg['delegation_id']}").json()["current"]["spent_krw"] == spent
    assert spent >= 0


def test_idempotency_keys_are_scoped_per_agent(client, deleg):
    k = "shared-key-001"
    a = act(client, deleg["delegation_id"], key=k).json()
    b = act(client, deleg["delegation_id"], key=k, agent="agent_other").json()
    assert b["transaction_id"] != a["transaction_id"]
    assert "AGENT_MISMATCH" in [v["code"] for v in b["policy_reason"]["violations"]]
    assert b["status"] != "EXECUTED"


def test_replayed_receipt_appended_to_chain_is_detected(client, deleg):
    _populate(client, deleg)
    ex = _export(client)
    ex["receipts"].append(copy.deepcopy(ex["receipts"][1]))
    probs = _problems(ex)
    assert any("BROKEN_CHAIN_LINK" in p for p in probs) and any("SEQUENCE_GAP" in p for p in probs)


def test_replayed_old_delegation_version_denied(client, deleg):
    did = deleg["delegation_id"]
    r = client.post(f"{API}/delegations/{did}/revoke")
    assert r.status_code == 200
    t = act(client, did).json()
    assert t["decision"] == "DENY"
    assert any(v["code"].startswith("DELEGATION_") for v in t["policy_reason"]["violations"])


# ---------- omission / reorder / transplant ----------

def test_deleting_every_possible_single_middle_receipt_is_detected(client, deleg):
    _populate(client, deleg)
    ex = _export(client)
    n = len(ex["receipts"])
    assert n >= 4
    for i in range(0, n - 1):  # all but the last (see known-limit test)
        probs = av.verify(ex["receipts"][:i] + ex["receipts"][i + 1:], ex["gateway_public_key_hex"])
        assert probs, f"deleting receipt index {i} went unnoticed"


def test_reordered_receipts_are_detected(client, deleg):
    _populate(client, deleg)
    ex = _export(client)
    ex["receipts"][1], ex["receipts"][2] = ex["receipts"][2], ex["receipts"][1]
    assert _problems(ex)


def test_signature_transplant_between_receipts_fails(client, deleg):
    _populate(client, deleg)
    ex = _export(client)
    ex["receipts"][1]["signature"] = ex["receipts"][2]["signature"]
    assert any("BAD_SIGNATURE" in p for p in _problems(ex))


def test_known_limit_trailing_truncation_is_not_detected(client, deleg):
    """A single signer + hash chain cannot prove completeness: dropping the newest receipts verifies OK."""
    _populate(client, deleg)
    ex = _export(client)
    assert _problems({**ex, "receipts": ex["receipts"][:-2]}) == []


def test_known_limit_stale_export_replay_is_not_detected(client, deleg):
    """An older, genuine export looks valid forever; there is no freshness proof or external anchor."""
    act(client, deleg["delegation_id"])
    old = _export(client)
    act(client, deleg["delegation_id"], product="p_sofa")
    assert _problems(old) == []
    assert len(_export(client)["receipts"]) > len(old["receipts"])


def test_server_side_row_deletion_in_middle_detected_by_api(client, deleg, app):
    _populate(client, deleg)
    db_path = app.state.rt.settings.database_url.replace("sqlite:///", "")
    con = sqlite3.connect(db_path)
    con.execute("delete from receipts where seq=2")
    con.commit()
    con.close()
    chain = client.get(f"{API}/receipts/verify-chain").json()
    assert not chain["valid"]
    assert {p["problem"] for p in chain["problems"]} & {"SEQUENCE_GAP", "BROKEN_CHAIN_LINK"}


# ---------- evidence-level honesty ----------

def test_evidence_level_inflation_is_detected(client, deleg):
    act(client, deleg["delegation_id"], product="p_tablet")  # price mismatch -> not clean
    act(client, deleg["delegation_id"], product="p_unknown_xyz")
    ex = _export(client)
    target = next(r for r in ex["receipts"] if r["verification_level"] != "MERCHANT_CONFIRMED")
    target["verification_level"] = "MERCHANT_CONFIRMED"
    assert any("HASH_MISMATCH" in p for p in _problems(ex))
    _rehash(target)
    assert any("BAD_SIGNATURE" in p for p in _problems(ex))


def test_payment_confirmed_in_a_forged_receipt_is_rejected_by_verifier(client, deleg):
    act(client, deleg["delegation_id"])
    ex = _export(client)
    ex["receipts"][-1]["verification_level"] = "PAYMENT_CONFIRMED"
    assert any("PAYMENT_CONFIRMED" in p for p in _problems(ex))


def test_levels_never_exceed_what_evidence_supports(client):
    d = make_delegation(client)
    for p in ["p_headphones", "p_tablet", "p_flaky", "p_timeout", "p_shady", "p_nothing"]:
        act(client, d["delegation_id"], product=p)
    for r in client.get(f"{API}/receipts").json():
        levels = [e["level"] for e in r["evidence_references"]]
        assert r["verification_level"] == max(levels, key=["UNKNOWN", "SELF_REPORTED", "GATEWAY_VERIFIED", "MERCHANT_CONFIRMED"].index, default="UNKNOWN")
        if r["verification_level"] == "MERCHANT_CONFIRMED":
            assert r["merchant_response"] is not None
        if r["policy_decision"] == "DENY":
            assert r["verification_level"] != "MERCHANT_CONFIRMED"
        if r["execution_status"] == "UNKNOWN":
            assert r["verification_level"] != "MERCHANT_CONFIRMED" or r["merchant_response"]


def test_merchant_payload_tampering_is_caught_by_verifier_alone(client, deleg):
    act(client, deleg["delegation_id"])
    ex = _export(client)
    r = next(x for x in ex["receipts"] if x.get("merchant_response"))
    r["merchant_response"]["payload"]["total_krw"] = 1
    probs = _problems(ex)
    assert any("HASH_MISMATCH" in p for p in probs)


# ---------- budget / duplicate boundaries ----------

def test_budget_exact_boundary_allowed_then_one_won_denied(client):
    d = make_delegation(client, total_budget_krw=120000, per_item_max_krw=120000)
    assert act(client, d["delegation_id"], product="p_headphones").json()["status"] == "EXECUTED"
    t = act(client, d["delegation_id"], product="p_cable").json()
    assert "BUDGET_EXCEEDED" in [v["code"] for v in t["policy_reason"]["violations"]]
    assert client.get(f"{API}/delegations/{d['delegation_id']}").json()["current"]["spent_krw"] == 120000


def test_quantity_multiplication_cannot_bypass_budget(client, deleg):
    t = act(client, deleg["delegation_id"], product="p_headphones", qty=3).json()
    assert t["decision"] == "DENY"
    assert client.get(f"{API}/delegations/{deleg['delegation_id']}").json()["current"]["spent_krw"] == 0


@pytest.mark.parametrize("qty", [0, -1, 10**9])
def test_hostile_quantities_never_execute(client, deleg, qty):
    r = act(client, deleg["delegation_id"], qty=qty)
    assert r.status_code == 422 or r.json().get("decision") == "DENY"
    assert client.get(f"{API}/delegations/{deleg['delegation_id']}").json()["current"]["spent_krw"] == 0


def test_denied_transaction_cannot_be_approved_into_execution(client, deleg):
    t = act(client, deleg["delegation_id"], product="p_monitor", merchant="m_unknown").json()
    assert t["decision"] == "DENY"
    r = client.post(f"{API}/transactions/{t['transaction_id']}/approve")
    assert r.status_code >= 400
    assert client.get(f"{API}/transactions/{t['transaction_id']}").json()["status"] != "EXECUTED"


# ---------- verifier robustness ----------

@pytest.mark.parametrize("mutate", [
    lambda r: r.pop("signature"),
    lambda r: r.pop("current_hash"),
    lambda r: r.pop("seq"),
    lambda r: r.pop("previous_hash"),
    lambda r: r.update(signature="zz"),
    lambda r: r.update(signature=None),
    lambda r: r.update(seq="1"),
    lambda r: r.update(seq=True),
    lambda r: r.update(action_parameters={"x": 1.5}),
    lambda r: r.update(merchant_response={"signature": "00"}),
    lambda r: r.update(merchant_response="oops"),
])
def test_verifier_never_crashes_on_malformed_receipts(client, deleg, mutate):
    act(client, deleg["delegation_id"])
    ex = _export(client)
    mutate(ex["receipts"][-1])
    probs = _problems(ex)  # must return, not raise
    assert probs, "malformed receipt was accepted"


def test_verifier_cli_exit_codes_on_garbage(tmp_path):
    cases = {"notjson.json": "{{{", "empty.json": "[]", "scalar.json": "42", "nested.json": '{"receipts": "x"}'}
    for name, text in cases.items():
        f = tmp_path / name
        f.write_text(text)
        out = subprocess.run([sys.executable, str(CLI), str(f), "--public-key", "00" * 32], capture_output=True, text=True)
        assert out.returncode in (0, 1, 2), (name, out.stderr)
        assert "Traceback" not in out.stderr, (name, out.stderr)
    bad = tmp_path / "k.json"
    bad.write_text("[]")
    out = subprocess.run([sys.executable, str(CLI), str(bad), "--public-key", "not-hex"], capture_output=True, text=True)
    assert "Traceback" not in out.stderr


def test_committed_samples_behave_as_documented():
    root = Path(__file__).resolve().parents[2] / "samples"
    good = json.loads((root / "sample_export.json").read_text())["receipts"]
    bad = json.loads((root / "tampered_export.json").read_text())["receipts"]
    pub = (root / "gateway_public_key.hex").read_text().strip()
    mpub = (root / "mock_merchant_public_key.hex").read_text().strip()
    assert av.verify(good, pub, mpub) == []
    assert any("HASH_MISMATCH" in p for p in av.verify(bad, pub))
