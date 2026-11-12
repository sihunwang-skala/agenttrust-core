export type Language = "en" | "ko";

const ko: Record<string, string> = {
  "Dashboard": "대시보드", "Delegation": "위임 관리", "Agent Simulator": "에이전트 시뮬레이터",
  "Receipt Explorer": "영수증 탐색기", "Dispute & Recovery": "분쟁 및 복구",
  "DEMO / MOCK DATA ONLY: simulated merchant, no real payments or personal data. Approvals happen on a Demo Trusted Surface and are not cryptographically signed by the user. AgentTrust does not determine legal responsibility.":
    "데모 및 모의 데이터 전용: 가상 판매자를 사용하며 실제 결제나 개인정보는 처리하지 않습니다. 승인은 데모 신뢰 화면에서 진행되며 사용자의 암호학적 서명이 아닙니다. AgentTrust는 법적 책임을 판단하지 않습니다.",
  "Reset demo data": "데모 데이터 초기화", "Delete ALL demo data (delegations, receipts, disputes)?": "모든 데모 데이터(위임, 영수증, 분쟁)를 삭제할까요?",
  "Total agent actions": "에이전트 전체 작업", "Approved actions": "승인된 작업", "Blocked actions": "차단된 작업",
  "Awaiting user approval": "사용자 승인 대기", "Open disputes": "진행 중인 분쟁", "Recent receipts": "최근 영수증",
  "Open explorer": "영수증 탐색기 열기", "No receipts yet. Create a delegation, then run the Agent Simulator.": "영수증이 없습니다. 위임을 만든 다음 에이전트 시뮬레이터를 실행하세요.",
  "Time": "시간", "Event": "이벤트", "Decision": "판정", "Status": "상태", "Evidence level": "증거 수준",
  "Backend unreachable: ": "백엔드에 연결할 수 없습니다: ", "Loading…": "불러오는 중…",
  "Create delegation": "위임 만들기", "Agent ID": "에이전트 ID", "Total budget (KRW)": "전체 예산(원)",
  "Max per item (KRW)": "건별 최대 금액(원)", "Allowed categories (comma separated)": "허용 카테고리(쉼표로 구분)",
  "Allowed merchant IDs (comma separated)": "허용 판매자 ID(쉼표로 구분)", "Max delivery days": "최대 배송 기간(일)",
  "Valid for (minutes, counted from approval)": "유효 시간(분, 승인 시점부터)", "Require free returns": "무료 반품 필수",
  "Allow automatic purchase (otherwise each action needs your approval)": "자동 구매 허용(끄면 매 작업마다 승인 필요)",
  "Create delegation (pending)": "위임 만들기(승인 대기)", "Create new version (pending)": "새 버전 만들기(승인 대기)",
  "Cancel": "취소", "A delegation has no effect until you explicitly approve it. Approval is recorded on the Demo Trusted Surface and is NOT a cryptographic signature by you.":
    "위임은 직접 승인하기 전까지 효력이 없습니다. 승인은 데모 신뢰 화면에 기록되며 사용자의 암호학적 서명이 아닙니다.",
  "No delegations yet.": "아직 위임이 없습니다.", "Agent": "에이전트", "Budget": "예산",
  "Per item max": "건별 최대 금액", "Categories": "카테고리", "Merchants": "판매자",
  "Free returns": "무료 반품", "Auto purchase": "자동 구매", "required": "필수", "not required": "필수 아님",
  "allowed": "허용", "approval per action": "작업별 승인 필요", "Expires": "만료",
  "Approve (demo surface)": "승인(데모 화면)", "Revoke": "철회", "Revise (new version)": "수정(새 버전)",
  "Select for simulator": "시뮬레이터에서 선택", "Selected for simulator": "시뮬레이터에 선택됨",
  "New version of ": "새 버전: ", "min after approval": "분(승인 후)",
  "Mock Agent scenarios": "모의 에이전트 시나리오",
  "Acting under delegation ": "위임에 따라 실행 중: ", ". The mock agent calls the same Gateway API a real agent would.": ". 모의 에이전트는 실제 에이전트와 동일한 Gateway API를 호출합니다.",
  "Create and approve a delegation first (Delegation tab), then select it.": "먼저 위임 관리 탭에서 위임을 만들고 승인한 뒤 선택하세요.",
  "Run": "실행", "Result: ": "실행 결과: ", "idempotent replay: no second execution": "멱등 재요청: 추가 실행 없음",
  "authorized ": "승인 금액 ", "merchant charged ": "판매자 청구 금액 ", "Approve this action": "이 작업 승인",
  "Reject": "거부", "View receipts for ": "영수증 보기: ", "Mock merchant catalog (synthetic, simulated)": "모의 판매자 상품 목록(합성 데이터)",
  "Product": "상품", "Merchant": "판매자", "Category": "카테고리", "Price": "가격", "Free returns": "무료 반품",
  "Delivery": "배송", "Cancellable": "취소 가능", "yes": "예", "no": "아니요", "true": "예", "false": "아니요",
  "1. Select a transaction": "1. 거래 선택", "Transaction": "거래", "Choose…": "선택하세요…", "Dispute reason": "분쟁 사유",
  "This purchase looks wrong": "이 구매 내역이 잘못된 것 같습니다", "Open dispute": "분쟁 접수", "Disputes": "분쟁",
  "None yet.": "아직 없습니다.", "Open or select a dispute to compare evidence.": "분쟁을 접수하거나 선택해 증거를 비교하세요.",
  "Dispute ": "분쟁 ", "Transaction ": "거래 ", " is ": " 상태: ", ". Failed stage: ": ". 실패 단계: ",
  "none detected": "감지되지 않음", "Responsibility: ": "책임: ", "Violated conditions": "위반 조건",
  "None recorded.": "기록된 항목이 없습니다.", "Discrepancies between sources": "출처 간 불일치",
  "None detected.": "감지된 항목이 없습니다.", "Stage": "단계", "Field": "항목", "Expected": "예상값", "Observed": "관측값",
  "Evidence by party": "당사자별 증거", "no evidence": "증거 없음", "Not established (unknowns)": "확인되지 않은 사실",
  "Recovery (simulated)": "복구(시뮬레이션)", "Cancellation possible: ": "취소 가능 여부: ", "yes (merchant may still reject)": "가능(판매자가 거부할 수 있음)",
  "Request cancellation from mock merchant": "모의 판매자에게 취소 요청", "Close dispute": "분쟁 종료",
  "Merchant result: ": "판매자 처리 결과: ", " (no real refund, chargeback or insurance payout exists in this MVP)": " (이 MVP에는 실제 환불, 차지백, 보험금 지급 기능이 없습니다)",
  "Charged: ": "청구 금액: ", "All receipts (hash chain order)": "전체 영수증(해시 체인 순서)",
  "Receipts for ": "영수증: ", "Show all": "전체 보기", "No receipts.": "영수증이 없습니다.",
  "Verify whole chain": "전체 체인 검증", "Export JSON": "JSON 내보내기", "Chain valid (": "체인 유효 (", " receipts)": "개)",
  "Chain INVALID: ": "체인 무효: ", "Receipt ": "영수증 ", "Timeline": "타임라인", "Action: ": "작업: ",
  " on ": " 대상 ", " · agent ": " · 에이전트 ", " · delegation ": " · 위임 ", "Policy reasons (violations):": "정책 위반 사유:",
  "All ": "전체 ", " deterministic checks passed.": "개 결정론적 검사를 통과했습니다.",
  "Merchant response (": "판매자 응답(", ") type: ": ") 유형: ", "Verifiable evidence": "검증 가능한 증거",
  "Merchant confirmation comes from a simulated merchant. PAYMENT_CONFIRMED does not exist in this MVP.": "판매자 확인은 모의 판매자에서 생성됩니다. 이 MVP에는 PAYMENT_CONFIRMED 상태가 없습니다.",
  "Unverified claims / unknowns": "미검증 주장 및 미확인 정보", "None recorded in this receipt.": "이 영수증에는 기록된 항목이 없습니다.",
  "Signature & hash verification": "서명 및 해시 검증", "Verify this receipt": "이 영수증 검증",
  "Hash matches content: ": "해시와 내용 일치: ", "Ed25519 signature valid: ": "Ed25519 서명 유효: ",
  "Chain link to previous receipt: ": "이전 영수증과 체인 연결: ", "Merchant signature (simulated): ": "판매자 서명(시뮬레이션): ",
  "Offline: ": "오프라인 검증: ", "Backend unreachable": "백엔드 연결 실패",
  "ALLOW": "허용", "DENY": "거부", "REQUIRE_APPROVAL": "승인 필요", "EXECUTED": "실행됨", "DENIED": "거부됨",
  "FAILED": "실패", "UNKNOWN": "알 수 없음", "DISCREPANCY": "불일치", "CANCELLED": "취소됨", "ACTIVE": "활성",
  "REVOKED": "철회됨", "EXPIRED": "만료됨", "PENDING_APPROVAL": "승인 대기", "SUPERSEDED": "대체됨",
  "OPEN": "진행 중", "CLOSED": "종료됨", "SELF_REPORTED": "자체 보고", "GATEWAY_VERIFIED": "게이트웨이 검증",
  "MERCHANT_CONFIRMED": "판매자 확인", "AUTHORIZED": "승인됨", "REJECTED": "거부됨",
  "NOT_DETERMINED": "판단되지 않음", "n/a": "해당 없음",
  "user": "사용자", "agent": "에이전트", "gateway": "게이트웨이", "merchant": "판매자",
};

const partial: Array<[string, string]> = [
  ["Backend unreachable: ", "백엔드에 연결할 수 없습니다: "], ["New version of ", "새 버전: "],
  ["Acting under delegation ", "위임에 따라 실행 중: "], [". The mock agent calls the same Gateway API a real agent would.", ". 모의 에이전트는 실제 에이전트와 동일한 Gateway API를 호출합니다."],
  ["Result: ", "실행 결과: "], ["View receipts for ", "영수증 보기: "], ["Receipts for ", "영수증: "],
  ["Dispute ", "분쟁 "], ["Transaction ", "거래 "], ["Failed stage: ", "실패 단계: "],
  ["Responsibility: ", "책임: "], ["Cancellation possible: ", "취소 가능 여부: "], ["Merchant result: ", "판매자 처리 결과: "],
  ["Charged: ", "청구 금액: "], ["Action: ", "작업: "], [" · agent ", " · 에이전트 "], [" · delegation ", " · 위임 "],
  ["Backend unreachable", "백엔드 연결 실패"],
];

export function translate(text: string, language: Language) {
  if (language === "en") return text;
  const trimmed = text.trim();
  if (ko[trimmed]) return text.replace(trimmed, ko[trimmed]);
  return partial.reduce((out, [from, to]) => out.replaceAll(from, to), text);
}

export function localizeDom(root: HTMLElement, language: Language) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes: Text[] = [];
  while (walker.nextNode()) nodes.push(walker.currentNode as Text);
  for (const node of nodes) {
    const parent = node.parentElement;
    if (!parent || ["SCRIPT", "STYLE", "CODE", "PRE"].includes(parent.tagName)) continue;
    const next = translate(node.data, language);
    if (next !== node.data) node.data = next;
  }
  const attrs = ["aria-label", "placeholder", "title", "value"];
  root.querySelectorAll<HTMLElement>("*").forEach((el) => {
    for (const attr of attrs) {
      if (!el.hasAttribute(attr)) continue;
      const value = el.getAttribute(attr)!;
      const next = translate(value, language);
      if (next !== value) el.setAttribute(attr, next);
    }
    if (el instanceof HTMLInputElement && el.type !== "checkbox" && el.type !== "radio") {
      const next = translate(el.value, language);
      if (next !== el.value) el.value = next;
    }
    if (el instanceof HTMLTextAreaElement) {
      const next = translate(el.value, language);
      if (next !== el.value) el.value = next;
    }
  });
}
