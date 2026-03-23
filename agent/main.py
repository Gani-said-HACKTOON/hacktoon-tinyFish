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
You are a professional AI Compliance & Regulatory Risk Analyst for companies in Indonesia.

You have TWO tasks simultaneously:

=== TASK 1: REGULATORY MONITORING ===
Browse relevant regulatory sources and check:
- Are there any recent regulatory changes or updates that affect this company?
- Are the mentioned regulations still valid and up-to-date?
- Are there any new regulations that the company may not yet be aware of but are relevant to its industry?

=== TASK 2: RISK DETECTION & COMPLIANCE ANALYSIS ===
Based on company data and its activities, analyze:
- Do the activities being reviewed potentially violate applicable regulations?
- How significant is the compliance risk?
- What concrete actions should be taken?

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
    "new_regulations_found": ["<relevant new regulation/rule>"],
    "changed_regulations": ["<changed regulations>"],
    "monitor_notes": "<2-3 sentence monitoring summary>"
  }},
  "risk_analysis": {{
    "risk_score": <0-100>,
    "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
    "violations_detected": ["<specific articles/rules potentially violated>"],
    "risk_factors": ["<factors increasing risk>"],
    "risk_summary": "<2-3 sentence risk summary>"
  }},
  "compliance_report": {{
    "compliance_status": "<COMPLIANT|NEEDS_IMPROVEMENT|NON_COMPLIANT>",
    "findings": [
      {{"number": 1, "finding": "<description>", "level": "<LOW|MEDIUM|HIGH|CRITICAL>", "related_regulation": "<regulation name>"}}
    ],
    "recommendations": [
      {{"priority": 1, "action": "<concrete action>", "deadline": "<immediate|30 days|90 days>", "responsible_party": "<dept/role>"}}
    ],
    "executive_summary": "<executive summary for management, 3-4 sentences>"
  }}
}}
"""


def run_tinyfish(d: dict) -> dict:
    print("\n" + "="*62)
    print("  🤖  TINYFISH AI — REGULATION MONITOR & RISK ANALYSIS")
    print("="*62)

    # Determine target URL
    if d.get("url"):
        url = d["url"]
    else:
        regs = "+".join(d["regulations"][:2])
        url = f"https://www.google.com/search?q={regs}+regulation+latest+{d['country']}+{d['industry']}"

    goal = TINYFISH_GOAL.format(
        company_name    = d["company_name"],
        industry        = d["industry"],
        country         = d["country"],
        regulations     = ", ".join(d["regulations"]),
        activity        = d["activity"],
        value           = d["value"],
        parties_involved= d["parties_involved"],
        cross_border    = d["cross_border"],
        third_party     = d["third_party"],
        sensitive_data  = d["sensitive_data"],
    )

    print(f"\n  🔍  Browsing: {url[:70]}...")
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
        print(f"\n  ⚠️  TinyFish error: {e}")

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

    print(f"\n  ✅  Analysis complete.\n")
    log_activity("AI_ANALYSIS", f"TinyFish analysis done: {d['company_name']}", d["id"])
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
    "CRITICAL": {"action": "BLOCK",           "icon": "🔴", "msg": "Process BLOCKED. Immediate escalation to Compliance Officer required."},
    "HIGH":     {"action": "REVIEW_REQUIRED", "icon": "🟡", "msg": "Process ON HOLD. Manual review required before proceeding."},
    "MEDIUM":   {"action": "WARNING",         "icon": "🟠", "msg": "WARNING recorded. Process may continue under close monitoring."},
    "LOW":      {"action": "PASS",            "icon": "🟢", "msg": "Process APPROVED. No additional action required."},
}

def enforce_policy(risk_level: str, report_id: str) -> dict:
    p = POLICY.get(risk_level, POLICY["LOW"])
    entry = {
        "timestamp":  datetime.datetime.now().isoformat(),
        "report_id":  report_id,
        "risk_level": risk_level,
        "action":     p["action"],
        "message":    p["msg"],
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
    story.append(Paragraph("Powered by TinyFish AI", small))
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

    #Executive Summary
    story.append(Paragraph("Executive Summary", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(cr.get("executive_summary", "-"), body))
    story.append(Spacer(1, 8))

    #Regulation Monitor
    story.append(Paragraph("1. Regulation Monitoring Results", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(f"Status: {mr.get('status', '-')}", h2))
    story.append(Paragraph(mr.get("monitor_notes", "-"), body))

    if mr.get("new_regulations_found"):
        story.append(Paragraph("New / Changed Regulations Found:", h2))
        for item in mr["new_regulations_found"]:
            story.append(Paragraph(f"  • {item}", body))
    story.append(Spacer(1, 8))

    # Risk Analysis
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

    # Compliance Findings
    story.append(Paragraph("3. Compliance Findings", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))

    findings_list = cr.get("findings", [])
    if findings_list:
        th = [["No", "Finding", "Level", "Related Regulation"]]
        for t in findings_list:
            th.append([
                str(t.get("number", "")),
                Paragraph(t.get("finding", ""), body),
                t.get("level", ""),
                t.get("related_regulation", ""),
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

    # Recommended Actions
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

    # Policy Enforcement
    story.append(Paragraph("5. Policy Enforcement", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(enforcement.get("message", "-"), body))
    story.append(Spacer(1, 12))

    # Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(
        f"This document was automatically generated by Compliance Regulator AI (TinyFish) "
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

    print(f"\n  📋 COMPLIANCE FINDINGS")
    for t in cr.get("findings", []):
        print(f"  [{t.get('level','?')}] {t.get('finding','-')} ({t.get('related_regulation','-')})")

    print(f"\n  💡 RECOMMENDATIONS")
    for r in cr.get("recommendations", []):
        print(f"  {r.get('priority','?')}. [{r.get('deadline','?')}] {r.get('action','-')} → {r.get('responsible_party','-')}")

    print(f"\n  ⚙️  POLICY ENFORCEMENT")
    print(f"  {enforcement.get('icon','')} {enforcement.get('action','')} — {enforcement.get('message','')}")

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
    enforcement = enforce_policy(actual_risk_level, report_id)

    # 5. Save JSON + PDF
    json_path = save_json(report_id, d, analysis, enforcement)
    pdf_path  = save_pdf(report_id, d, analysis, enforcement)

    # 6. Display to terminal
    display_results(d, analysis, enforcement, report_id, json_path, pdf_path)


def main():
    print("\n" + "█"*62)
    print("█" + "  COMPLIANCE REGULATOR AI  —  Powered by TinyFish  ".center(60) + "█")
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


if __name__ == "__main__":
    main()