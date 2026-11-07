"""Dispute analysis (public reference version). Groups evidence per party and never assigns responsibility."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import DisputeRow, ReceiptRow, TransactionRow
from .receipts import load

STAGE_BY_EVENT = {"POLICY_DECISION": "POLICY_CHECK", "USER_APPROVAL": "USER_APPROVAL", "EXECUTION_RESULT": "MERCHANT_EXECUTION",
                  "CANCEL_REQUESTED": "CANCELLATION", "CANCEL_APPROVED": "CANCELLATION", "CANCEL_REJECTED": "CANCELLATION",
                  "TRANSACTION_STATE_CHANGED": "STATE_CHANGE", "USER_REJECTION": "USER_APPROVAL", "DISPUTE_OPENED": "DISPUTE"}

NOT_DETERMINED = {
    "determination": "NOT_DETERMINED",
    "note": "AgentTrust records and compares evidence only. It does not determine legal responsibility, "
            "guarantee refunds, or act as an insurer or arbiter.",
}


def analyze(db: Session, dispute: DisputeRow) -> dict:
    tx = db.get(TransactionRow, dispute.transaction_id)
    receipts = [load(r) for r in db.execute(select(ReceiptRow).where(ReceiptRow.transaction_id == tx.transaction_id)
                                            .order_by(ReceiptRow.seq)).scalars()]
    stages = [{"stage": STAGE_BY_EVENT.get(r["event_type"], r["event_type"]), "event_type": r["event_type"],
               "receipt_id": r["receipt_id"], "timestamp": r["timestamp"], "execution_status": r["execution_status"],
               "policy_decision": r["policy_decision"], "verification_level": r["verification_level"]} for r in receipts]

    violated = [v for r in receipts if r["event_type"] in ("POLICY_DECISION", "USER_APPROVAL")
                for v in r["policy_reason"].get("violations", [])]

    ev = {"user": [], "agent": [], "gateway": [], "merchant": []}
    for r in receipts:
        for e in r["evidence_references"]:
            item = {"receipt_id": r["receipt_id"], "evidence_id": e["evidence_id"], "level": e["level"],
                    "type": e["type"], "summary": e["summary"]}
            if e["type"] in ("cancel_reason", "dispute_claim"):
                ev["user"].append(item)
            elif e["type"] == "user_approval":
                ev["user"].append(item)
            elif e["level"] == "SELF_REPORTED":
                ev["agent"].append(item)
            elif e["level"] == "MERCHANT_CONFIRMED":
                ev["merchant"].append(item)
            else:
                ev["gateway"].append(item)
    ev["user"].insert(0, {"receipt_id": None, "evidence_id": None, "level": "GATEWAY_VERIFIED", "type": "delegation_record",
                          "summary": f"Delegation {tx.delegation_id} v{tx.delegation_version} recorded by the gateway; approved "
                                     "on the Demo Trusted Surface, not cryptographically signed by the user"})

    discrepancies = []
    discrepancies += tx.discrepancies
    failed_stage = discrepancies[0]["stage"] if discrepancies else (
        "POLICY_CHECK" if tx.status == "DENIED" else "MERCHANT_EXECUTION" if tx.status in ("FAILED", "UNKNOWN") else None)

    cancellable = tx.status in ("EXECUTED", "DISCREPANCY")
    merchant_cancellable = tx.quote["payload"]["cancellable"] if tx.quote else None
    if cancellable:
        reason = ("Merchant-confirmed order exists. A cancellation can be requested; the merchant may still reject it"
                  + (" (the signed quote says this item is non-cancellable)" if merchant_cancellable is False else ""))
    else:
        reason = {"CANCELLED": "Already cancelled", "DENIED": "No order was placed (denied by policy)",
                  "FAILED": "Merchant reported an error; no order confirmation exists",
                  "UNKNOWN": "No merchant response was received, so there is no order reference to cancel",
                  }.get(tx.status, f"Not cancellable in status {tx.status}")

    unknowns = ["Whether any real payment settlement occurred: no payment provider is integrated (PAYMENT_CONFIRMED is never issued)",
                "Whether the human user actually intended or authorized this purchase: approval was on a Demo Trusted Surface without a user signature",
                "Whether the simulated merchant's signed statements reflect real-world fulfilment"]
    if tx.status in ("UNKNOWN", "FAILED"):
        unknowns.insert(0, "The merchant-side outcome is unknown: it is not established by the available evidence")
    if discrepancies:
        unknowns.insert(0, "Why the sources disagree is not established by the available evidence")

    return {"dispute_id": dispute.dispute_id, "transaction_id": tx.transaction_id, "dispute_status": dispute.status,
            "transaction_status": tx.status, "stages": stages, "violated_conditions": violated,
            "evidence_by_party": ev, "discrepancies": discrepancies, "failed_stage": failed_stage,
            "cancellation": {"possible": cancellable, "reason": reason, "merchant_cancellable_per_quote": merchant_cancellable},
            "unknown_facts": unknowns, "responsibility": NOT_DETERMINED, "simulation": True}
