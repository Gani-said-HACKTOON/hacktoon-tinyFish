# from ollama import chat
# from ollama import ChatResponse

# response: ChatResponse = chat(model='qwen2.5-coder:latest', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])
# print(response.message.content)

# # test with ollama library
# from dotenv import load_dotenv
# load_dotenv()

# from tinyfish import TinyFish
# from fastapi import FastAPI

# app = FastAPI()
# client = TinyFish()

# @app.get("/")
# def hello():
#     return {"message": "hello"}

# @app.get("/scrape")
# def scrape(url: str):

#     result = None

#     with client.agent.stream(
#         url=url,
#         goal="Summarize this website"
#     ) as stream:

#         for event in stream:
#             if event.type.value == "COMPLETE":
#                 result = event.result_json

#     return {"result": result}

# # testing fastapi combined with tinyfish

"""
How it works
==============================================
Workflow:
  1. User inputs regulation data (terminal)
  2. Save to in-memory DB
  3. TinyFish: monitor latest regulations + detect risk
  4. Generate compliance report -> JSON + PDF
  5. Automatic policy enforcement (system)
  6. Monitor & activity history

Run in terminal: python main.py or py main.py  // depends on version
Note: Make sure all libraries from requirements.txt are installed.
      Using a virtual environment is recommended.
"""

from dotenv import load_dotenv
load_dotenv()

# ─── FastAPI ──────────────────────────────────────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Compliance Regulator AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegulationInput(BaseModel):
    company_name:     str
    industry:         str
    country:          str
    regulations:      list[str]
    activity:         str
    value:            str
    parties_involved: str
    cross_border:     str
    third_party:      str
    sensitive_data:   str
    url:              str = ""

# ─────────────────────────────────────────────────────────────────────────────

import json
import os
import datetime
from tinyfish import TinyFish

# Convert output to PDF for a cleaner format
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

client = TinyFish()

# DB
DB = {
    "regulations":         [],   # regulation data entered by user
    "risk_analyses":       [],   # AI analysis results
    "compliance_reports":  [],   # compliance reports
    "policy_enforcements": [],   # enforcement log
    "activity_log":        [],   # all activity history
}

OUTPUT_DIR = "compliance_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def log_activity(action: str, detail: str, ref_id: str = ""):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action":    action,
        "detail":    detail,
        "ref_id":    ref_id,
    }
    DB["activity_log"].append(entry)


# step 1
def collect_input() -> dict:
    print("\n" + "="*62)
    print("  📋  BUSINESS REGULATION INPUT DATA")
    print("="*62)

    d = {}

    print("\n[1] Company Identity")
    d["company_name"] = input("    Company Name         : ").strip()
    d["industry"]     = input("    Industry             : ").strip()
    d["country"]      = input("    Country of Operation : ").strip()

    print("\n[2] Applicable Regulations")
    print("    (comma-separated — e.g.: UU Cipta Kerja, OJK, PPATK, GDPR)")
    raw = input("    Regulations          : ").strip()
    d["regulations"] = [r.strip() for r in raw.split(",") if r.strip()]

    print("\n[3] Activity / Transaction Under Review")
    d["activity"]         = input("    Activity Description : ").strip()
    d["value"]            = input("    Value (USD)          : ").strip()
    d["parties_involved"] = input("    Parties Involved     : ").strip()

    print("\n[4] Risk Factors")
    d["cross_border"]   = input("    Cross-border Transaction?  (yes/no): ").strip().lower()
    d["third_party"]    = input("    Third Party Involved?      (yes/no): ").strip().lower()
    d["sensitive_data"] = input("    Sensitive Data Present?    (yes/no): ").strip().lower()

    print("\n[5] Regulation Reference URL  (leave blank = auto search)")
    d["url"] = input("    Reference URL        : ").strip()

    d["id"]        = f"REG-{len(DB['regulations'])+1:04d}"
    d["timestamp"] = datetime.datetime.now().isoformat()
    return d


def save_regulation(d: dict) -> str:
    DB["regulations"].append(d)
    log_activity("INPUT", f"Regulation data saved: {d['company_name']}", d["id"])
    print(f"\n  ✅  Saved with ID: {d['id']}")
    return d["id"]


# step 2
TINYFISH_GOAL = """
You are a professional AI Compliance & Regulatory Risk Analyst with global expertise.

You have TWO tasks simultaneously:

=== TASK 1: REGULATORY MONITORING ===
Browse ONLY the trusted official sources listed below. Do NOT use random websites,
blogs, news portals, or unofficial sources. Stick strictly to government and
regulatory authority domains provided.

TRUSTED SOURCES TO BROWSE (official government & regulatory domains only):
{trusted_sources}

From these sources, check:
- Are there any recent regulatory changes or updates that affect this company?
- Are the mentioned regulations still valid and up-to-date?
- Are there any new regulations the company may not be aware of but relevant to its industry?
- Cross-check with international standards (FATF, BIS, IOSCO) where applicable.

=== TASK 2: RISK DETECTION & COMPLIANCE ANALYSIS ===
Based on company data and its activities, analyze:
- Do the activities being reviewed potentially violate applicable regulations?
- How significant is the compliance risk?
- What concrete actions should be taken?

=== SOURCE VALIDATION RULES ===
- ONLY cite information from the trusted domains listed above.
- If a regulation cannot be verified from the trusted sources, flag it as "UNVERIFIED".
- Always include the source URL when referencing a specific regulation.
- Prioritize the most recent official publications (check publication/update dates).

=== COMPANY DATA ===
- Name        : {company_name}
- Industry    : {industry}
- Country     : {country}
- Regulations : {regulations}

=== ACTIVITY UNDER REVIEW ===
- Description     : {activity}
- Value           : {value}
- Parties         : {parties_involved}
- Cross-border    : {cross_border}
- Third Parties   : {third_party}
- Sensitive Data  : {sensitive_data}

=== OUTPUT FORMAT ===
Respond ONLY with the following valid JSON (no markdown, no additional text):
{{
  "regulation_monitor": {{
    "status": "UP_TO_DATE | CHANGES_FOUND | NEEDS_REVIEW",
    "new_regulations_found": ["<regulation name> — source: <official URL>"],
    "changed_regulations": ["<regulation name> — source: <official URL>"],
    "monitor_notes": "<2-3 sentence monitoring summary citing only verified sources>"
  }},
  "risk_analysis": {{
    "risk_score": <0-100>,
    "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
    "violations_detected": ["<specific article/rule> — source: <official URL>"],
    "risk_factors": ["<factor description>"],
    "risk_summary": "<2-3 sentence risk summary>"
  }},
  "compliance_report": {{
    "compliance_status": "<COMPLIANT|NEEDS_IMPROVEMENT|NON_COMPLIANT>",
    "findings": [
      {{"number": 1, "finding": "<description>", "level": "<LOW|MEDIUM|HIGH|CRITICAL>", "related_regulation": "<regulation name>", "source_url": "<official URL>"}}
    ],
    "recommendations": [
      {{"priority": 1, "action": "<concrete action>", "deadline": "<immediate|30 days|90 days>", "responsible_party": "<dept/role>"}}
    ],
    "executive_summary": "<executive summary for management, 3-4 sentences>"
  }}
}}
"""


# =============================================================
# TRUSTED REGULATORY SOURCE REGISTRY (by country/region)
# Semua domain ini adalah sumber resmi pemerintah / regulator
# =============================================================
TRUSTED_SOURCES = {
    # ---------- INDONESIA ----------
    "indonesia": [
        "https://peraturan.go.id",           # Jaringan Dokumentasi Hukum Nasional
        "https://ojk.go.id",                 # Otoritas Jasa Keuangan
        "https://ppatk.go.id",               # Pusat Pelaporan Transaksi Keuangan
        "https://bpkp.go.id",                # Badan Pengawasan Keuangan
        "https://kemenkeu.go.id",            # Kementerian Keuangan
        "https://bi.go.id",                  # Bank Indonesia
        "https://kominfo.go.id",             # Kominfo (data & digital)
        "https://bpom.go.id",               # BPOM (makanan, obat, kosmetik)
        "https://esdm.go.id",               # Kementerian ESDM (energi)
    ],
    # ---------- UNITED STATES ----------
    "united states": [
        "https://sec.gov",                   # Securities & Exchange Commission
        "https://federalregister.gov",       # Federal Register (semua regulasi federal)
        "https://ftc.gov",                   # Federal Trade Commission
        "https://fdic.gov",                  # Federal Deposit Insurance Corp
        "https://occ.treas.gov",             # Office of the Comptroller
        "https://cfpb.gov",                  # Consumer Financial Protection Bureau
        "https://dol.gov",                   # Department of Labor
        "https://irs.gov",                   # Internal Revenue Service
    ],
    # ---------- EUROPEAN UNION ----------
    "european union": [
        "https://eur-lex.europa.eu",         # EUR-Lex (semua hukum EU)
        "https://esma.europa.eu",            # European Securities & Markets Authority
        "https://eba.europa.eu",             # European Banking Authority
        "https://edpb.europa.eu",            # European Data Protection Board (GDPR)
        "https://ec.europa.eu",              # European Commission
    ],
    # ---------- UNITED KINGDOM ----------
    "united kingdom": [
        "https://legislation.gov.uk",        # Semua legislasi UK
        "https://fca.org.uk",               # Financial Conduct Authority
        "https://pra.bankofengland.co.uk",  # Prudential Regulation Authority
        "https://ico.org.uk",               # Information Commissioner (data)
        "https://gov.uk",                   # GOV.UK (semua regulasi pemerintah)
    ],
    # ---------- SINGAPORE ----------
    "singapore": [
        "https://mas.gov.sg",               # Monetary Authority of Singapore
        "https://sso.agc.gov.sg",           # Singapore Statutes Online
        "https://acra.gov.sg",              # Accounting & Corporate Regulatory Authority
        "https://pdpc.gov.sg",              # Personal Data Protection Commission
        "https://mom.gov.sg",               # Ministry of Manpower
    ],
    # ---------- AUSTRALIA ----------
    "australia": [
        "https://legislation.gov.au",       # Federal Register of Legislation
        "https://asic.gov.au",              # Australian Securities & Investments Commission
        "https://apra.gov.au",              # Australian Prudential Regulation Authority
        "https://oaic.gov.au",              # Office of the Australian Info Commissioner
        "https://austrac.gov.au",           # AUSTRAC (anti-money laundering)
    ],
    # ---------- MALAYSIA ----------
    "malaysia": [
        "https://bnm.gov.my",               # Bank Negara Malaysia
        "https://sc.com.my",                # Securities Commission Malaysia
        "https://agc.gov.my",               # Attorney General Chambers
        "https://pdp.gov.my",               # Personal Data Protection
        "https://ssm.com.my",               # Companies Commission of Malaysia
    ],
    # ---------- JAPAN ----------
    "japan": [
        "https://fsa.go.jp",                # Financial Services Agency
        "https://meti.go.jp",               # Ministry of Economy, Trade & Industry
        "https://mof.go.jp",                # Ministry of Finance
        "https://boj.or.jp",                # Bank of Japan
        "https://cas.go.jp",                # Cabinet Secretariat
    ],
    # ---------- CHINA ----------
    "china": [
        "https://csrc.gov.cn",              # China Securities Regulatory Commission
        "https://pbc.gov.cn",               # People's Bank of China
        "https://samr.gov.cn",              # State Admin for Market Regulation
        "https://nfra.gov.cn",              # National Financial Regulatory Administration
        "https://mofcom.gov.cn",            # Ministry of Commerce
    ],
    # ---------- INDIA ----------
    "india": [
        "https://sebi.gov.in",              # Securities & Exchange Board of India
        "https://rbi.org.in",               # Reserve Bank of India
        "https://mca.gov.in",               # Ministry of Corporate Affairs
        "https://finmin.nic.in",            # Ministry of Finance
        "https://meity.gov.in",             # Ministry of Electronics & IT
    ],
    # ---------- GERMANY ----------
    "germany": [
        "https://bafin.de",                 # Federal Financial Supervisory Authority
        "https://bundesbank.de",            # Deutsche Bundesbank
        "https://gesetze-im-internet.de",   # Federal Laws (official)
        "https://bmi.bund.de",              # Federal Ministry of Interior
    ],
    # ---------- INTERNATIONAL / GLOBAL ----------
    "global": [
        "https://fatf-gafi.org",            # FATF (anti-money laundering global)
        "https://bis.org",                  # Bank for International Settlements
        "https://iosco.org",                # Int'l Org of Securities Commissions
        "https://iasb.org",                 # Int'l Accounting Standards Board
        "https://imf.org",                  # International Monetary Fund
        "https://worldbank.org",            # World Bank (regulatory reports)
        "https://unctad.org",               # UN Trade & Development
        "https://wto.org",                  # World Trade Organization
    ],
}

def get_trusted_urls(country: str, regulations: list) -> list:
    """
    Kembalikan list URL sumber terpercaya berdasarkan negara.
    Selalu tambahkan sumber global (FATF, BIS, dll) sebagai pelengkap.
    """
    country_key = country.strip().lower()

    # Cari exact match dulu
    sources = list(TRUSTED_SOURCES.get(country_key, []))

    # Kalau tidak ada exact match, cari partial match
    if not sources:
        for key in TRUSTED_SOURCES:
            if key in country_key or country_key in key:
                sources = list(TRUSTED_SOURCES[key])
                break


    if not sources:
        # Coba Google Site Search ke domain .gov atau resmi negara tsb
        country_slug = country_key.replace(" ", "+")
        sources = [
            f"https://www.google.com/search?q={country_slug}+official+regulation+site:.gov+OR+site:.go+OR+site:.gov.{country_slug[:2]}",
        ]


    sources += TRUSTED_SOURCES["global"][:3] 
    return sources


def run_tinyfish(d: dict) -> dict:
    print("\n" + "="*62)
    print("  🤖  Dreelio AI")
    print("="*62)

    # Determine target URL — prioritaskan URL manual, lalu sumber terpercaya
    if d.get("url"):
        urls = [d["url"]]
    else:
        urls = get_trusted_urls(d["country"], d["regulations"])

    url = urls[0]

    trusted_domains_str = "\n".join(f"  - {u}" for u in urls)

    goal = TINYFISH_GOAL.format(
        trusted_sources  = trusted_domains_str,
        company_name     = d["company_name"],
        industry         = d["industry"],
        country          = d["country"],
        regulations      = ", ".join(d["regulations"]),
        activity         = d["activity"],
        value            = d["value"],
        parties_involved = d["parties_involved"],
        cross_border     = d["cross_border"],
        third_party      = d["third_party"],
        sensitive_data   = d["sensitive_data"],
    )

    print(f"\n  🔍  Entry point  : {url}")
    print(f"  📋  Trusted sources ({len(urls)} domains):")
    for u in urls:
        print(f"        • {u}")
    print("  ⏳  Please wait (estimated 1-3 minutes)...\n")

    result = None
    run_id = None
    try:
        with client.agent.stream(url=url, goal=goal) as stream:
            for event in stream:
                ev = event.type.value if hasattr(event.type, "value") else str(event.type)
                if ev not in ("COMPLETE", "ERROR"):
                    print(f"  ⟳  [{ev}]", end="\r")
                if ev == "COMPLETE":
                    run_id = event.run_id
                    break
    except Exception as e:
        print(f"\n  ⚠️  Dreelio error error: {e}")

    # Fetch result from run_id because result_json is always None
    if run_id:
        try:
            run_result = client.runs.get(run_id)
            result = run_result.result
        except Exception as e:
            print(f"\n  ⚠️  Failed to fetch run result: {e}")

    if isinstance(result, str):
        try:
            clean = result.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean)
        except Exception:
            result = None

    if not isinstance(result, dict):
        print("  ℹ️  Using fallback analysis (rule-based)...")
        result = fallback_analysis(d)

    valid_levels = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    if "risk_analysis" not in result:
        print("  ⚠️  'risk_analysis' key missing from AI response — using fallback.")
        result = fallback_analysis(d)

    ra_check = result.get("risk_analysis", {})
    detected_level = ra_check.get("risk_level", "").upper()
    if detected_level not in valid_levels:
        print(f"  ⚠️  Invalid risk_level '{detected_level}' — using fallback.")
        result = fallback_analysis(d)
    else:
        result["risk_analysis"]["risk_level"] = detected_level

    result = override_risk_level(result)
    result = inject_confidence_flags(result)

    final_level = result["risk_analysis"].get("risk_level")
    print(f"\n  ✅  Analysis complete. Risk Level: {final_level}\n")
    log_activity("AI_ANALYSIS", f"Dreelio analysis done: {d['company_name']}", d["id"])
    return result

LEVEL_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
RANK_LEVEL = {v: k for k, v in LEVEL_RANK.items()}

def override_risk_level(result: dict) -> dict:
    """
    Rule-based override: kalau temuan atau violations lebih parah
    dari risk_level yang diklaim AI, paksa naik ke level yang sesuai.
    """
    ra = result.get("risk_analysis", {})
    cr = result.get("compliance_report", {})

    current_level = ra.get("risk_level", "LOW")
    current_rank  = LEVEL_RANK.get(current_level, 1)
    findings      = cr.get("findings", [])
    violations    = ra.get("violations_detected", [])

    finding_levels   = [f.get("level", "LOW").upper() for f in findings]
    max_finding_rank = max((LEVEL_RANK.get(l, 1) for l in finding_levels), default=1)

    overridden_rank  = current_rank
    override_reasons = []

    if max_finding_rank > current_rank:
        overridden_rank = max_finding_rank
        top_level = RANK_LEVEL[max_finding_rank]
        override_reasons.append(
            f"Finding level {top_level} detected — risk level upgraded from {current_level} to {top_level}."
        )

    if violations and "CRITICAL" in finding_levels and overridden_rank < 4:
        overridden_rank = 4
        override_reasons.append(
            "Active violations + CRITICAL finding detected — risk level forced to CRITICAL."
        )

    score = ra.get("risk_score", 0)
    if score > 70 and overridden_rank < 3:
        overridden_rank = 3
        override_reasons.append(
            f"Risk score {score}/100 exceeds threshold — risk level upgraded to HIGH."
        )

    if overridden_rank != current_rank:
        new_level = RANK_LEVEL[overridden_rank]
        result["risk_analysis"]["risk_level"] = new_level
        result["risk_analysis"].setdefault("override_log", []).extend(override_reasons)
        for reason in override_reasons:
            print(f"  ⚠️  OVERRIDE: {reason}")
    else:
        result["risk_analysis"].setdefault("override_log", [])

    return result


_ASSUMPTION_PATTERNS = [
    "typically", "usually", "generally", "often", "may", "might", "could",
    "assumed", "assumption", "likely", "probably", "suggest", "appears",
    "seems", "too small", "too large", "too low", "too high",
    "insufficient", "excessive", "unusual", "uncommon",
]

def inject_confidence_flags(result: dict) -> dict:
    """
    Scan semua teks di hasil analisis.
    Kalau ada kalimat yang mengandung pola asumsi, tandai sebagai
    LOW_CONFIDENCE dan tambahkan disclaimer.
    """
    ra = result.get("risk_analysis", {})
    cr = result.get("compliance_report", {})
    low_confidence_items = []

    def scan_text(text: str, source: str):
        lower = text.lower()
        for pat in _ASSUMPTION_PATTERNS:
            if pat in lower:
                low_confidence_items.append({
                    "source":  source,
                    "excerpt": text[:120] + ("..." if len(text) > 120 else ""),
                    "trigger": pat,
                })
                return

    scan_text(ra.get("risk_summary", ""), "risk_summary")
    for i, f in enumerate(cr.get("findings", [])):
        scan_text(f.get("finding", ""), f"finding #{i+1}")
    for i, r in enumerate(cr.get("recommendations", [])):
        scan_text(r.get("action", ""), f"recommendation #{i+1}")
    for v in ra.get("violations_detected", []):
        scan_text(v, "violation")

    result["risk_analysis"]["confidence"] = {
        "level": "LOW" if low_confidence_items else "HIGH",
        "flags": low_confidence_items,
        "disclaimer": (
            f"⚠️  {len(low_confidence_items)} statement(s) in this report are based on AI assumptions "
            "rather than verified regulatory text. Please cross-check with official sources before "
            "making compliance decisions."
        ) if low_confidence_items else (
            "✅  No assumption-based statements detected. Analysis references verified regulatory sources."
        ),
    }

    if low_confidence_items:
        print(f"  ⚠️  CONFIDENCE: {len(low_confidence_items)} assumption-based statement(s) flagged.")

    return result


def fallback_analysis(d: dict) -> dict:
    score = 20
    factors = []
    if d.get("cross_border") == "yes":
        score += 20; factors.append("Cross-border transaction")
    if d.get("third_party") == "yes":
        score += 15; factors.append("Third party involved")
    if d.get("sensitive_data") == "yes":
        score += 25; factors.append("Sensitive data present")
    score = min(score, 100)
    level = "LOW" if score < 40 else "MEDIUM" if score < 60 else "HIGH" if score < 80 else "CRITICAL"
    return {
        "regulation_monitor": {
            "status": "NEEDS_REVIEW",
            "new_regulations_found": [],
            "changed_regulations": [],
            "monitor_notes": "Fallback analysis — unable to access online regulation sources."
        },
        "risk_analysis": {
            "risk_score": score,
            "risk_level": level,
            "violations_detected": [],
            "risk_factors": factors,
            "risk_summary": f"Risk level {level} based on factors: {', '.join(factors) or 'standard'}."
        },
        "compliance_report": {
            "compliance_status": "NEEDS_IMPROVEMENT",
            "findings": [{"number": 1, "finding": "Manual review required", "level": level, "related_regulation": ", ".join(d["regulations"])}],
            "recommendations": [{"priority": 1, "action": "Conduct manual review with compliance officer", "deadline": "30 days", "responsible_party": "Compliance Dept"}],
            "executive_summary": "Automated analysis could not be completed. Manual review is recommended."
        }
    }


# step 3
POLICY = {
    "CRITICAL": {
        "action": "BLOCK",
        "icon":   "🔴",
        "msg":    "Process BLOCKED. Immediate escalation to Compliance Officer required.",
        "detail": (
            "This process has been BLOCKED due to critical compliance violations. "
            "No further action may be taken until all critical findings are resolved. "
            "The Compliance Officer must be notified immediately and a formal remediation "
            "plan must be approved before the process can resume."
        ),
    },
    "HIGH": {
        "action": "REVIEW_REQUIRED",
        "icon":   "🟡",
        "msg":    "Process ON HOLD. Manual review required before proceeding.",
        "detail": (
            "This process is ON HOLD pending manual review by the Compliance team. "
            "High-risk findings have been detected that require direct sign-off before "
            "the process may continue. All identified violations must be reviewed and "
            "a mitigation plan submitted within the deadlines stated in the recommendations."
        ),
    },
    "MEDIUM": {
        "action": "WARNING",
        "icon":   "🟠",
        "msg":    "WARNING recorded. Process may continue under close monitoring.",
        "detail": (
            "This process may continue, however a formal WARNING has been recorded. "
            "The identified findings must be addressed within the recommended deadlines. "
            "Progress must be reported to the Compliance team on a monthly basis until "
            "all medium-risk items are resolved and the compliance status is upgraded."
        ),
    },
    "LOW": {
        "action": "PASS",
        "icon":   "🟢",
        "msg":    "Process APPROVED. No additional action required.",
        "detail": (
            "This process has been APPROVED. No significant compliance issues were detected. "
            "Standard monitoring procedures apply. A periodic compliance review is recommended "
            "every 6 months or whenever there is a material change in business activity, "
            "applicable regulations, or the regulatory environment."
        ),
    },
}

def build_enforcement_message(risk_level: str, analysis: dict) -> str:
    """
    Bangun pesan policy enforcement yang detail dan kontekstual
    berdasarkan temuan nyata dari analisis AI.
    """
    p           = POLICY.get(risk_level, POLICY["LOW"])
    ra          = analysis.get("risk_analysis", {})
    cr          = analysis.get("compliance_report", {})
    mr          = analysis.get("regulation_monitor", {})

    score       = ra.get("risk_score", 0)
    risk_factors = ra.get("risk_factors", [])
    violations  = ra.get("violations_detected", [])
    findings    = cr.get("findings", [])
    recs        = cr.get("recommendations", [])
    reg_changes = mr.get("changed_regulations", []) + mr.get("new_regulations_found", [])

    lines = []

    # 1. Header status
    lines.append(f"{p['msg']}")
    lines.append("")

    # 2. Risk score summary
    lines.append(f"Risk Score: {score}/100  |  Risk Level: {risk_level}  |  Action: {p['action']}")
    lines.append("")

    # 3. Detail narasi sesuai level
    lines.append(p["detail"])
    lines.append("")

    # 4. Temuan utama (max 3)
    high_findings = [f for f in findings if f.get("level") in ("HIGH", "CRITICAL")]
    show_findings = high_findings if high_findings else findings
    if show_findings:
        lines.append("Key Findings Driving This Decision:")
        for f in show_findings[:3]:
            lvl = f.get("level", "?")
            txt = f.get("finding", "-")
            reg = f.get("related_regulation", "")
            lines.append(f"  [{lvl}] {txt}" + (f" ({reg})" if reg else ""))
        lines.append("")

    # 5. Regulatory changes detected
    if reg_changes:
        lines.append(f"Regulatory Changes Detected ({len(reg_changes)}):")
        for r in reg_changes[:3]:
            lines.append(f"  • {r}")
        lines.append("")

    # 6. Faktor risiko
    if risk_factors:
        lines.append("Active Risk Factors:")
        for rf in risk_factors[:3]:
            lines.append(f"  • {rf}")
        lines.append("")

    # 7. Top priority rekomendasi
    if recs:
        top = sorted(recs, key=lambda x: x.get("priority", 99))[:2]
        lines.append("Immediate Actions Required:")
        for r in top:
            deadline = r.get("deadline", "")
            action   = r.get("action", "")
            owner    = r.get("responsible_party", "")
            lines.append(f"  {r.get('priority','?')}. [{deadline}] {action}" + (f" — {owner}" if owner else ""))

    return "\n".join(lines)


def enforce_policy(risk_level: str, report_id: str, analysis: dict = None) -> dict:
    p       = POLICY.get(risk_level, POLICY["LOW"])
    message = build_enforcement_message(risk_level, analysis or {})
    entry = {
        "timestamp":  datetime.datetime.now().isoformat(),
        "report_id":  report_id,
        "risk_level": risk_level,
        "action":     p["action"],
        "message":    message,
    }
    DB["policy_enforcements"].append(entry)
    log_activity("ENFORCEMENT", f"{p['action']} applied for {report_id}", report_id)
    return {**entry, "icon": p["icon"]}


# step 4
def save_json(report_id: str, d: dict, analysis: dict, enforcement: dict) -> str:
    payload = {
        "report_id":    report_id,
        "regulation":   d,
        "analysis":     analysis,
        "enforcement":  enforcement,
        "generated_at": datetime.datetime.now().isoformat(),
    }
    path = os.path.join(OUTPUT_DIR, f"{report_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    log_activity("SAVE_JSON", f"JSON saved: {path}", report_id)
    return path


# step 5
RISK_COLORS = {
    "CRITICAL": colors.HexColor("#C0392B"),
    "HIGH":     colors.HexColor("#E67E22"),
    "MEDIUM":   colors.HexColor("#F1C40F"),
    "LOW":      colors.HexColor("#27AE60"),
}

def save_pdf(report_id: str, d: dict, analysis: dict, enforcement: dict) -> str:
    path = os.path.join(OUTPUT_DIR, f"{report_id}.pdf")
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story  = []

    title_style = ParagraphStyle("Title2", parent=styles["Title"],
                                 fontSize=18, spaceAfter=4, textColor=colors.HexColor("#1A252F"))
    h1 = ParagraphStyle("H1", parent=styles["Heading1"],
                         fontSize=13, textColor=colors.HexColor("#2C3E50"), spaceBefore=14, spaceAfter=4)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"],
                         fontSize=11, textColor=colors.HexColor("#34495E"), spaceBefore=8, spaceAfter=2)
    body = ParagraphStyle("Body2", parent=styles["Normal"],
                           fontSize=10, leading=14, spaceAfter=4)
    small = ParagraphStyle("Small", parent=styles["Normal"],
                            fontSize=9, textColor=colors.grey)

    ra  = analysis.get("risk_analysis", {})
    mr  = analysis.get("regulation_monitor", {})
    cr  = analysis.get("compliance_report", {})
    rl  = ra.get("risk_level", "LOW")
    rs  = ra.get("risk_score", 0)
    risk_color = RISK_COLORS.get(rl, colors.grey)

    story.append(Paragraph("COMPLIANCE REPORT", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2C3E50")))
    story.append(Spacer(1, 6))

    info_data = [
        ["Report ID",  report_id,           "Date",        datetime.datetime.now().strftime("%d %b %Y %H:%M")],
        ["Company",    d["company_name"],    "Industry",    d["industry"]],
        ["Country",    d["country"],         "Regulations", ", ".join(d["regulations"])],
    ]
    info_table = Table(info_data, colWidths=[3.5*cm, 6*cm, 3*cm, 5.5*cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE",       (0,0), (-1,-1), 9),
        ("FONTNAME",       (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTNAME",       (2,0), (2,-1),  "Helvetica-Bold"),
        ("BACKGROUND",     (0,0), (0,-1),  colors.HexColor("#ECF0F1")),
        ("BACKGROUND",     (2,0), (2,-1),  colors.HexColor("#ECF0F1")),
        ("GRID",           (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))

    badge_data = [[
        Paragraph(f"RISK LEVEL: {rl}", ParagraphStyle("badge", parent=styles["Normal"],
            fontSize=16, textColor=colors.white, fontName="Helvetica-Bold")),
        Paragraph(f"SCORE: {rs} / 100", ParagraphStyle("badge2", parent=styles["Normal"],
            fontSize=14, textColor=colors.white)),
        Paragraph(f"ACTION: {enforcement.get('action','')}", ParagraphStyle("badge3", parent=styles["Normal"],
            fontSize=12, textColor=colors.white)),
    ]]
    badge_table = Table(badge_data, colWidths=[6*cm, 5*cm, 7*cm])
    badge_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), risk_color),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [5]),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 12))

    # ---- Executive Summary ----
    story.append(Paragraph("Executive Summary", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(cr.get("executive_summary", "-"), body))
    story.append(Spacer(1, 8))

    # ---- Override Log Banner ----
    override_log = ra.get("override_log", [])
    if override_log:
        ovr_rows = [[Paragraph(
            "RISK LEVEL OVERRIDE — System upgraded risk level due to inconsistency with findings:",
            ParagraphStyle("ovr_hdr", parent=styles["Normal"], fontSize=9,
                textColor=colors.HexColor("#7D3C00"), fontName="Helvetica-Bold")
        )]]
        for reason in override_log:
            ovr_rows.append([Paragraph(
                f"  • {reason}",
                ParagraphStyle("ovr_item", parent=styles["Normal"],
                    fontSize=9, textColor=colors.HexColor("#7D3C00"), leftIndent=8)
            )])
        ovr_table = Table(ovr_rows, colWidths=[18*cm])
        ovr_table.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#FEF3E2")),
            ("BOX",           (0,0), (-1,-1), 1, colors.HexColor("#E67E22")),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ]))
        story.append(ovr_table)
        story.append(Spacer(1, 8))

    # ---- Confidence Disclaimer Banner ----
    confidence  = ra.get("confidence", {})
    conf_level  = confidence.get("level", "HIGH")
    disclaimer  = confidence.get("disclaimer", "")
    conf_flags  = confidence.get("flags", [])
    conf_bg     = colors.HexColor("#FFF8E1") if conf_level == "LOW" else colors.HexColor("#E8F8F1")
    conf_border = colors.HexColor("#F39C12") if conf_level == "LOW" else colors.HexColor("#27AE60")
    conf_tc     = colors.HexColor("#7D5A00") if conf_level == "LOW" else colors.HexColor("#145A32")
    conf_rows   = [[Paragraph(disclaimer, ParagraphStyle(
        "conf_hdr", parent=styles["Normal"], fontSize=9, textColor=conf_tc, fontName="Helvetica-Bold"
    ))]]
    if conf_flags:
        conf_rows.append([Paragraph(
            "Flagged assumption-based statements (verify before relying on these findings):",
            ParagraphStyle("conf_sub", parent=styles["Normal"],
                fontSize=8, textColor=conf_tc, fontName="Helvetica-Bold")
        )])
        for flag in conf_flags[:5]:
            conf_rows.append([Paragraph(
                f'  [{flag["source"]}] "{flag["excerpt"]}" (trigger: \'{flag["trigger"]}\')',
                ParagraphStyle("conf_item", parent=styles["Normal"],
                    fontSize=8, textColor=conf_tc, leftIndent=8)
            )])
    conf_table = Table(conf_rows, colWidths=[18*cm])
    conf_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), conf_bg),
        ("BOX",           (0,0), (-1,-1), 1, conf_border),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    story.append(conf_table)
    story.append(Spacer(1, 8))

    # ---- Regulation Monitor ----
    story.append(Paragraph("1. Regulation Monitoring Results", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(f"Status: {mr.get('status', '-')}", h2))
    story.append(Paragraph(mr.get("monitor_notes", "-"), body))

    if mr.get("new_regulations_found"):
        story.append(Paragraph("New / Changed Regulations Found:", h2))
        for item in mr["new_regulations_found"]:
            story.append(Paragraph(f"  • {item}", body))
    story.append(Spacer(1, 8))

    # ---- Risk Analysis ----
    story.append(Paragraph("2. Risk Analysis", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(ra.get("risk_summary", "-"), body))

    if ra.get("risk_factors"):
        story.append(Paragraph("Risk Factors:", h2))
        for f in ra["risk_factors"]:
            story.append(Paragraph(f"  • {f}", body))

    if ra.get("violations_detected"):
        story.append(Paragraph("Potential Violations:", h2))
        for v in ra["violations_detected"]:
            story.append(Paragraph(f"  ⚠ {v}", body))
    story.append(Spacer(1, 8))

    # ---- Compliance Findings ----
    story.append(Paragraph("3. Compliance Findings", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))

    findings_list = cr.get("findings", [])
    if findings_list:
        th = [["No", "Finding", "Level", "Regulation / Source"]]
        for t in findings_list:
            reg_source = t.get("related_regulation", "")
            src_url    = t.get("source_url", "")
            reg_cell   = f"{reg_source}\n{src_url}" if src_url else reg_source
            th.append([
                str(t.get("number", "")),
                Paragraph(t.get("finding", ""), body),
                t.get("level", ""),
                Paragraph(reg_cell, body),
            ])
        t_table = Table(th, colWidths=[1*cm, 8.5*cm, 2.5*cm, 6*cm])
        t_table.setStyle(TableStyle([
            ("BACKGROUND",     (0,0), (-1,0), colors.HexColor("#2C3E50")),
            ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
            ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",       (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
            ("GRID",           (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
            ("TOPPADDING",     (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
            ("VALIGN",         (0,0), (-1,-1), "TOP"),
        ]))
        story.append(t_table)
    story.append(Spacer(1, 8))

    # ---- Recommended Actions ----
    story.append(Paragraph("4. Recommended Actions", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))

    rec_list = cr.get("recommendations", [])
    if rec_list:
        rh = [["#", "Action", "Deadline", "Responsible Party"]]
        for r in rec_list:
            rh.append([
                str(r.get("priority", "")),
                Paragraph(r.get("action", ""), body),
                r.get("deadline", ""),
                r.get("responsible_party", ""),
            ])
        r_table = Table(rh, colWidths=[1*cm, 9*cm, 2.5*cm, 5.5*cm])
        r_table.setStyle(TableStyle([
            ("BACKGROUND",     (0,0), (-1,0), colors.HexColor("#27AE60")),
            ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
            ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",       (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
            ("GRID",           (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
            ("TOPPADDING",     (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
            ("VALIGN",         (0,0), (-1,-1), "TOP"),
        ]))
        story.append(r_table)
    story.append(Spacer(1, 8))

    # ---- Policy Enforcement ----
    story.append(Paragraph("5. Policy Enforcement", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))

    enf_action = enforcement.get("action", "")
    enf_icon   = enforcement.get("icon", "")
    action_colors = {
        "BLOCK":           colors.HexColor("#C0392B"),
        "REVIEW_REQUIRED": colors.HexColor("#E67E22"),
        "WARNING":         colors.HexColor("#F39C12"),
        "PASS":            colors.HexColor("#27AE60"),
    }
    action_color = action_colors.get(enf_action, colors.grey)

    # Badge action
    badge_enf = [[
        Paragraph(
            f"{enf_icon}  {enf_action}",
            ParagraphStyle("enf_badge", parent=styles["Normal"],
                fontSize=13, textColor=colors.white, fontName="Helvetica-Bold")
        )
    ]]
    badge_enf_table = Table(badge_enf, colWidths=[18*cm])
    badge_enf_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), action_color),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(badge_enf_table)
    story.append(Spacer(1, 8))

    # Render message baris per baris supaya formatting terjaga
    message_text = enforcement.get("message", "-")
    for line in message_text.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
        elif line.startswith("[") or line.startswith("•") or line.startswith("  "):
            story.append(Paragraph(line, ParagraphStyle(
                "enf_item", parent=styles["Normal"],
                fontSize=9, leading=13, leftIndent=12, spaceAfter=2
            )))
        elif line.endswith(":"):
            story.append(Paragraph(line, ParagraphStyle(
                "enf_sub", parent=styles["Normal"],
                fontSize=10, fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=2
            )))
        else:
            story.append(Paragraph(line, body))
    story.append(Spacer(1, 12))

    # ---- Footer ----
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(
        f"This document was automatically generated by Compliance Regulator AI "
        f"on {datetime.datetime.now().strftime('%d %B %Y at %H:%M')}. "
        "This is not a substitute for professional legal consultation.",
        ParagraphStyle("footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey)
    ))

    doc.build(story)
    log_activity("SAVE_PDF", f"PDF saved: {path}", report_id)
    return path


def display_results(d: dict, analysis: dict, enforcement: dict, report_id: str,
                    json_path: str, pdf_path: str):
    ra = analysis.get("risk_analysis", {})
    mr = analysis.get("regulation_monitor", {})
    cr = analysis.get("compliance_report", {})
    rl = ra.get("risk_level", "LOW")

    icons = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🟢"}

    print("\n" + "="*62)
    print(f"  📊  COMPLIANCE REPORT  [{report_id}]")
    print("="*62)

    print(f"""
  Company     : {d['company_name']}
  Industry    : {d['industry']}
  Regulations : {', '.join(d['regulations'])}

  ┌──────────────────────────────────────────────┐
  │  RISK SCORE  :  {str(ra.get('risk_score','?')).ljust(6)} / 100                    
  │  RISK LEVEL  :  {icons.get(rl,'⚪')} {rl.ljust(10)}                 
  │  STATUS      :  {cr.get('compliance_status','-').ljust(20)}           
  └──────────────────────────────────────────────┘""")

    print(f"\n  📡 REGULATION MONITOR  [{mr.get('status','-')}]")
    print(f"  {mr.get('monitor_notes','-')}")
    if mr.get("new_regulations_found"):
        for t in mr["new_regulations_found"]:
            print(f"    • {t}")

    print(f"\n  ⚠️  RISK SUMMARY")
    print(f"  {ra.get('risk_summary','-')}")

    override_log = ra.get("override_log", [])
    if override_log:
        print(f"\n  🔺 RISK LEVEL OVERRIDE")
        for reason in override_log:
            print(f"    • {reason}")

    confidence = ra.get("confidence", {})
    print(f"\n  🔍 CONFIDENCE: {confidence.get('level', 'HIGH')}")
    print(f"  {confidence.get('disclaimer', '')}")
    if confidence.get("flags"):
        print("  Flagged statements:")
        for flag in confidence["flags"][:3]:
            print(f'    [{flag["source"]}] "{flag["excerpt"][:80]}..."')

    print(f"\n  📋 COMPLIANCE FINDINGS")
    for t in cr.get("findings", []):
        print(f"  [{t.get('level','?')}] {t.get('finding','-')} ({t.get('related_regulation','-')})")

    print(f"\n  💡 RECOMMENDATIONS")
    for r in cr.get("recommendations", []):
        print(f"  {r.get('priority','?')}. [{r.get('deadline','?')}] {r.get('action','-')} → {r.get('responsible_party','-')}")

    print(f"\n  ⚙️  POLICY ENFORCEMENT")
    print(f"  {enforcement.get('icon','')} {enforcement.get('action','')}")
    print("  " + "-"*58)
    for line in enforcement.get("message", "").split("\n"):
        print(f"  {line}")

    print(f"\n  💾 FILES SAVED")
    print(f"  JSON : {json_path}")
    print(f"  PDF  : {pdf_path}")
    print("="*62)


def show_monitor():
    print("\n" + "="*62)
    print("  📡  REGULATION MONITOR — SUMMARY")
    print("="*62)
    if not DB["compliance_reports"]:
        print("\n  No reports saved yet.\n")
        return

    risk_count = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for r in DB["compliance_reports"]:
        rl = r.get("risk_level", "LOW")
        risk_count[rl] = risk_count.get(rl, 0) + 1

    print(f"""
  Total Reports   : {len(DB['compliance_reports'])}
  Total Entities  : {len(DB['regulations'])}

  RISK DISTRIBUTION:
    🟢 LOW      : {risk_count['LOW']}
    🟠 MEDIUM   : {risk_count['MEDIUM']}
    🟡 HIGH     : {risk_count['HIGH']}
    🔴 CRITICAL : {risk_count['CRITICAL']}
    """)

    high = [r for r in DB["compliance_reports"] if r.get("risk_level") in ("HIGH", "CRITICAL")]
    if high:
        print("  ⚠️  REQUIRES ATTENTION:")
        for r in high:
            print(f"    • [{r['report_id']}] {r['company_name']} → {r['risk_level']}")
    else:
        print("  ✅  No high-risk entities at this time.")


def show_activity_log():
    print("\n" + "="*62)
    print("  🗂️   ACTIVITY LOG")
    print("="*62)
    if not DB["activity_log"]:
        print("\n  No activity yet.\n")
        return
    for entry in DB["activity_log"][-20:]:
        ts = entry["timestamp"][11:19]
        print(f"  {ts}  [{entry['action']:<14}]  {entry['detail']}")


def show_all_reports():
    print("\n" + "="*62)
    print("  📁  ALL REPORTS")
    print("="*62)
    if not DB["compliance_reports"]:
        print("\n  No reports yet.\n")
        return
    for r in DB["compliance_reports"]:
        icons = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🟢"}
        rl = r.get("risk_level", "LOW")
        print(f"  {icons.get(rl,'⚪')} [{r['report_id']}]  {r['company_name']:<25}  {rl:<10}  Score:{r.get('risk_score','?')}")


def run_full_flow():
    # 1. Input
    d = collect_input()
    save_regulation(d)

    # 2. TinyFish analysis
    analysis = run_tinyfish(d)
    print(f"\n  🔎  DEBUG — analysis top-level keys: {list(analysis.keys())}")
    print(f"  🔎  DEBUG — risk_analysis raw: {analysis.get('risk_analysis', 'KEY MISSING')}")

    # IDs
    report_id = f"RPT-{len(DB['compliance_reports'])+1:04d}"
    ra = analysis.get("risk_analysis", {})

    # 3. Save to DB
    DB["compliance_reports"].append({
        "report_id":    report_id,
        "company_name": d["company_name"],
        "risk_level":   ra.get("risk_level", "LOW"),
        "risk_score":   ra.get("risk_score", 0),
        "timestamp":    datetime.datetime.now().isoformat(),
    })
    DB["risk_analyses"].append({"report_id": report_id, **analysis})
    log_activity("REPORT", f"Compliance report created: {report_id}", report_id)

    # 4. Policy enforcement
    actual_risk_level = ra.get("risk_level", "LOW")
    print(f"\n  🔎  DEBUG — risk_analysis keys : {list(ra.keys())}")
    print(f"  🔎  DEBUG — risk_level detected : {actual_risk_level}")
    enforcement = enforce_policy(actual_risk_level, report_id, analysis)

    # 5. Save JSON + PDF
    json_path = save_json(report_id, d, analysis, enforcement)
    pdf_path  = save_pdf(report_id, d, analysis, enforcement)

    # 6. Display to terminal
    display_results(d, analysis, enforcement, report_id, json_path, pdf_path)


def main():
    print("\n" + "█"*62)
    print("█" + "  COMPLIANCE REGULATOR AI  —  Dreelio ".center(60) + "█")
    print("█"*62)

    while True:
        print("""
  MENU:
  [1]  Input Data & Run New Analysis
  [2]  Regulation Monitor (Summary)
  [3]  All Reports
  [4]  Activity Log
  [5]  Exit
""")
        choice = input("  Choose (1-5): ").strip()

        if choice == "1":
            run_full_flow()
            input("\n  Press Enter to return to menu...")
        elif choice == "2":
            show_monitor()
            input("\n  Press Enter to return to menu...")
        elif choice == "3":
            show_all_reports()
            input("\n  Press Enter to return to menu...")
        elif choice == "4":
            show_activity_log()
            input("\n  Press Enter to return to menu...")
        elif choice == "5":
            print("\n  👋  Goodbye!\n")
            break
        else:
            print("\n  ❌  Invalid choice. Please try again.")




# ─── FastAPI Endpoints ────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Compliance Regulator AI — FastAPI is running ✅"}


@app.post("/api/analyze")
async def api_analyze(data: RegulationInput):
    d = data.model_dump()
    d["id"]        = f"REG-{len(DB['regulations'])+1:04d}"
    d["timestamp"] = datetime.datetime.now().isoformat()

    DB["regulations"].append(d)
    log_activity("INPUT", f"Data received from frontend: {d['company_name']}", d["id"])

    analysis  = run_tinyfish(d)
    report_id = f"RPT-{len(DB['compliance_reports'])+1:04d}"
    ra        = analysis.get("risk_analysis", {})

    DB["compliance_reports"].append({
        "report_id":    report_id,
        "company_name": d["company_name"],
        "risk_level":   ra.get("risk_level", "LOW"),
        "risk_score":   ra.get("risk_score", 0),
        "timestamp":    datetime.datetime.now().isoformat(),
    })
    DB["risk_analyses"].append({"report_id": report_id, **analysis})
    log_activity("REPORT", f"Compliance report created: {report_id}", report_id)

    actual_risk_level = ra.get("risk_level", "LOW")
    enforcement = enforce_policy(actual_risk_level, report_id, analysis)

    json_path = save_json(report_id, d, analysis, enforcement)
    pdf_path  = save_pdf(report_id, d, analysis, enforcement)

    return {
        "report_id":   report_id,
        "analysis":    analysis,
        "enforcement": enforcement,
        "json_path":   json_path,
        "pdf_path":    pdf_path,
    }


@app.get("/api/reports")
def api_get_reports():
    return DB["compliance_reports"]


@app.get("/api/logs")
def api_get_logs():
    return DB["activity_log"]


@app.get("/api/monitor")
def api_get_monitor():
    risk_count = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for r in DB["compliance_reports"]:
        rl = r.get("risk_level", "LOW")
        risk_count[rl] = risk_count.get(rl, 0) + 1
    high_risk = [r for r in DB["compliance_reports"] if r.get("risk_level") in ("HIGH", "CRITICAL")]
    return {
        "total_reports":      len(DB["compliance_reports"]),
        "total_entities":     len(DB["regulations"]),
        "risk_distribution":  risk_count,
        "requires_attention": high_risk,
    }


if __name__ == "__main__":
    main()
