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

# #ngetes fastapi di gabung sama tinyfish

"""
Tutorial alur dan cara jalannya
==============================================
Alur kerjaa:
  1. User input data regulasi (terminal)
  2. Simpan ke in-memory DB
  3. TinyFish: monitor regulasi terkini + deteksi risk
  4. Generate compliance report → JSON + PDF
  5. Policy enforcement otomatis (sistem)
  6. Monitor & riwayat aktivitas

run di terminal : python main.py atau py main.py //tergantung versi
Note : pastikan sudah terinstall semua libary dari requirements.txt dan di rekomendasikan menggunakan 
        virtual environtment
"""

from dotenv import load_dotenv
load_dotenv()

import json
import os
import datetime
from tinyfish import TinyFish

# Ubah jadi PDF agar menjadi lebih rapih
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

client = TinyFish()

#DB
DB = {
    "regulations":          [],   # data regulasi yang diinput user
    "risk_analyses":        [],   # hasil analisis AI
    "compliance_reports":   [],   # laporan compliance
    "policy_enforcements":  [],   # log enforcement
    "activity_log":         [],   # semua riwayat aktivitas
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


#step1
def collect_input() -> dict:
    print("\n" + "="*62)
    print("  📋  BUSINESS REGULATION INPUT DATA")
    print("="*62)

    d = {}

    print("\n[1] Company Identity")
    d["nama"]     = input("    Company Name         : ").strip()
    d["industri"] = input("    Industry             : ").strip()
    d["negara"]   = input("    Country of Operation : ").strip()

    print("\n[2] Applicable Regulations")
    print("    (comma-separated — e.g.: UU Cipta Kerja, OJK, PPATK, GDPR)")
    raw = input("    Regulations          : ").strip()
    d["regulasi"] = [r.strip() for r in raw.split(",") if r.strip()]

    print("\n[3] Activity / Transaction Under Review")
    d["aktivitas"]      = input("    Activity Description : ").strip()
    d["nilai"]          = input("    Value (Rp/USD)       : ").strip()
    d["pihak_terlibat"] = input("    Parties Involved     : ").strip()

    print("\n[4] Risk Factors")
    d["lintas_batas"]  = input("    Cross-border Transaction?  (yes/no): ").strip().lower()
    d["pihak_ketiga"]  = input("    Third Party Involved?      (yes/no): ").strip().lower()
    d["data_sensitif"] = input("    Sensitive Data Present?    (yes/no): ").strip().lower()

    print("\n[5] Regulation Reference URL  (leave blank = auto search)")
    d["url"] = input("    Reference URL        : ").strip()

    d["id"]        = f"REG-{len(DB['regulations'])+1:04d}"
    d["timestamp"] = datetime.datetime.now().isoformat()
    return d


def save_regulation(d: dict) -> str:
    DB["regulations"].append(d)
    log_activity("INPUT", f"Regulation data saved: {d['nama']}", d["id"])
    print(f"\n  ✅  Saved with ID: {d['id']}")
    return d["id"]


#step2
TINYFISH_GOAL = """
Kamu adalah AI Compliance & Regulatory Risk Analyst profesional untuk perusahaan di Indonesia.

Tugasmu ada DUA sekaligus:

=== TUGAS 1: MONITOR REGULASI ===
Browse sumber regulasi yang relevan dan periksa:
- Apakah ada perubahan / pembaruan regulasi terbaru yang mempengaruhi perusahaan ini?
- Apakah regulasi yang disebutkan masih berlaku dan up-to-date?
- Adakah regulasi baru yang mungkin belum diketahui perusahaan tapi relevan dengan industrinya?

=== TUGAS 2: DETEKSI RISK & COMPLIANCE ANALYSIS ===
Berdasarkan data perusahaan dan aktivitasnya, analisis:
- Apakah aktivitas yang diperiksa berpotensi melanggar regulasi yang berlaku?
- Seberapa besar risiko compliance-nya?
- Apa saja tindakan konkret yang harus dilakukan?

=== DATA PERUSAHAAN ===
- Nama        : {nama}
- Industri    : {industri}
- Negara      : {negara}
- Regulasi    : {regulasi}

=== AKTIVITAS YANG DIPERIKSA ===
- Deskripsi   : {aktivitas}
- Nilai       : {nilai}
- Pihak       : {pihak_terlibat}
- Lintas Batas: {lintas_batas}
- Pihak Ketiga: {pihak_ketiga}
- Data Sensitif: {data_sensitif}

=== FORMAT OUTPUT ===
Jawab HANYA dengan JSON valid berikut (tanpa markdown, tanpa teks lain):
{{
  "monitor_regulasi": {{
    "status": "UP_TO_DATE | PERUBAHAN_DITEMUKAN | PERLU_REVIEW",
    "temuan_regulasi_baru": ["<regulasi/aturan baru yang relevan>"],
    "regulasi_berubah": ["<regulasi yang berubah>"],
    "catatan_monitor": "<ringkasan hasil monitoring 2-3 kalimat>"
  }},
  "risk_analysis": {{
    "risk_score": <0-100>,
    "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
    "pelanggaran_terdeteksi": ["<pasal/aturan spesifik yang berpotensi dilanggar>"],
    "faktor_risiko": ["<faktor yang meningkatkan risiko>"],
    "ringkasan_risiko": "<ringkasan 2-3 kalimat>"
  }},
  "compliance_report": {{
    "status_kepatuhan": "<PATUH|PERLU_PERBAIKAN|TIDAK_PATUH>",
    "temuan": [
      {{"nomor": 1, "temuan": "<deskripsi>", "tingkat": "<LOW|MEDIUM|HIGH|CRITICAL>", "regulasi_terkait": "<nama regulasi>"}}
    ],
    "rekomendasi": [
      {{"prioritas": 1, "aksi": "<tindakan konkret>", "deadline": "<segera|30 hari|90 hari>", "penanggung_jawab": "<dept/role>"}}
    ],
    "ringkasan_eksekutif": "<ringkasan untuk manajemen, 3-4 kalimat>"
  }}
}}
"""


def run_tinyfish(d: dict) -> dict:
    print("\n" + "="*62)
    print("  🤖  TINYFISH AI — REGULATION MONITOR & RISK ANALYSIS")
    print("="*62)

    # Tentukan URL target
    if d.get("url"):
        url = d["url"]
    else:
        regs = "+".join(d["regulasi"][:2])
        url = f"https://www.google.com/search?q={regs}+regulasi+terbaru+Indonesia+{d['industri']}"

    goal = TINYFISH_GOAL.format(
        nama          = d["nama"],
        industri      = d["industri"],
        negara        = d["negara"],
        regulasi      = ", ".join(d["regulasi"]),
        aktivitas     = d["aktivitas"],
        nilai         = d["nilai"],
        pihak_terlibat= d["pihak_terlibat"],
        lintas_batas  = d["lintas_batas"],
        pihak_ketiga  = d["pihak_ketiga"],
        data_sensitif = d["data_sensitif"],
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

    # fetch hasil dari run_id karena result_json selalu None
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
    log_activity("AI_ANALYSIS", f"TinyFish analysis done: {d['nama']}", d["id"])
    return result


def fallback_analysis(d: dict) -> dict:
    score = 20
    faktor = []
    if d.get("lintas_batas") == "yes":
        score += 20; faktor.append("Cross-border transaction")
    if d.get("pihak_ketiga") == "yes":
        score += 15; faktor.append("Third party involved")
    if d.get("data_sensitif") == "yes":
        score += 25; faktor.append("Sensitive data present")
    score = min(score, 100)
    level = "LOW" if score < 40 else "MEDIUM" if score < 60 else "HIGH" if score < 80 else "CRITICAL"
    return {
        "monitor_regulasi": {
            "status": "PERLU_REVIEW",
            "temuan_regulasi_baru": [],
            "regulasi_berubah": [],
            "catatan_monitor": "Fallback analysis — unable to access online regulation sources."
        },
        "risk_analysis": {
            "risk_score": score,
            "risk_level": level,
            "pelanggaran_terdeteksi": [],
            "faktor_risiko": faktor,
            "ringkasan_risiko": f"Risk level {level} based on factors: {', '.join(faktor) or 'standard'}."
        },
        "compliance_report": {
            "status_kepatuhan": "PERLU_PERBAIKAN",
            "temuan": [{"nomor": 1, "temuan": "Manual review required", "tingkat": level, "regulasi_terkait": ", ".join(d["regulasi"])}],
            "rekomendasi": [{"prioritas": 1, "aksi": "Conduct manual review with compliance officer", "deadline": "30 days", "penanggung_jawab": "Compliance Dept"}],
            "ringkasan_eksekutif": "Automated analysis could not be completed. Manual review is recommended."
        }
    }


#step3
POLICY = {
    "CRITICAL": {"action": "BLOCK",           "icon": "🔴", "msg": "Process BLOCKED. Immediate escalation to Compliance Officer required."},
    "HIGH":     {"action": "REVIEW_REQUIRED", "icon": "🟡", "msg": "Process ON HOLD. Manual review required before proceeding."},
    "MEDIUM":   {"action": "WARNING",         "icon": "🟠", "msg": "WARNING recorded. Process may continue under close monitoring."},
    "LOW":      {"action": "PASS",            "icon": "🟢", "msg": "Process APPROVED. No additional action required."},
}

def enforce_policy(risk_level: str, report_id: str) -> dict:
    p = POLICY.get(risk_level, POLICY["LOW"])
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "report_id": report_id,
        "risk_level": risk_level,
        "action": p["action"],
        "message": p["msg"],
    }
    DB["policy_enforcements"].append(entry)
    log_activity("ENFORCEMENT", f"{p['action']} applied for {report_id}", report_id)
    return {**entry, "icon": p["icon"]}


#step4
def save_json(report_id: str, d: dict, analysis: dict, enforcement: dict) -> str:
    payload = {
        "report_id":   report_id,
        "regulation":  d,
        "analysis":    analysis,
        "enforcement": enforcement,
        "generated_at": datetime.datetime.now().isoformat(),
    }
    path = os.path.join(OUTPUT_DIR, f"{report_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    log_activity("SAVE_JSON", f"JSON saved: {path}", report_id)
    return path


#step5
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
    mr  = analysis.get("monitor_regulasi", {})
    cr  = analysis.get("compliance_report", {})
    rl  = ra.get("risk_level", "LOW")
    rs  = ra.get("risk_score", 0)
    risk_color = RISK_COLORS.get(rl, colors.grey)

    story.append(Paragraph("COMPLIANCE REPORT", title_style))
    story.append(Paragraph(f"Powered by TinyFish AI", small))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2C3E50")))
    story.append(Spacer(1, 6))
    info_data = [
        ["Report ID",   report_id,   "Date",        datetime.datetime.now().strftime("%d %b %Y %H:%M")],
        ["Company",     d["nama"],   "Industry",    d["industri"]],
        ["Country",     d["negara"], "Regulations", ", ".join(d["regulasi"])],
    ]
    info_table = Table(info_data, colWidths=[3.5*cm, 6*cm, 3*cm, 5.5*cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",    (2,0), (2,-1), "Helvetica-Bold"),
        ("BACKGROUND",  (0,0), (0,-1), colors.HexColor("#ECF0F1")),
        ("BACKGROUND",  (2,0), (2,-1), colors.HexColor("#ECF0F1")),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
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

    # ---- Ringkasan Eksekutif ----
    story.append(Paragraph("Executive Summary", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(cr.get("ringkasan_eksekutif", "-"), body))
    story.append(Spacer(1, 8))

    # ---- Monitor Regulasi ----
    story.append(Paragraph("1. Regulation Monitoring Results", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(f"Status: {mr.get('status', '-')}", h2))
    story.append(Paragraph(mr.get("catatan_monitor", "-"), body))

    if mr.get("temuan_regulasi_baru"):
        story.append(Paragraph("New / Changed Regulations Found:", h2))
        for item in mr["temuan_regulasi_baru"]:
            story.append(Paragraph(f"  • {item}", body))
    story.append(Spacer(1, 8))

    # ---- Risk Analysis ----
    story.append(Paragraph("2. Risk Analysis", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(ra.get("ringkasan_risiko", "-"), body))

    if ra.get("faktor_risiko"):
        story.append(Paragraph("Risk Factors:", h2))
        for f in ra["faktor_risiko"]:
            story.append(Paragraph(f"  • {f}", body))

    if ra.get("pelanggaran_terdeteksi"):
        story.append(Paragraph("Potential Violations:", h2))
        for v in ra["pelanggaran_terdeteksi"]:
            story.append(Paragraph(f"  ⚠ {v}", body))
    story.append(Spacer(1, 8))

    # ---- Compliance Report — Temuan ----
    story.append(Paragraph("3. Compliance Findings", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))

    temuan_list = cr.get("temuan", [])
    if temuan_list:
        th = [["No", "Finding", "Level", "Related Regulation"]]
        for t in temuan_list:
            th.append([
                str(t.get("nomor", "")),
                Paragraph(t.get("temuan", ""), body),
                t.get("tingkat", ""),
                t.get("regulasi_terkait", ""),
            ])
        t_table = Table(th, colWidths=[1*cm, 8.5*cm, 2.5*cm, 6*cm])
        t_table.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#2C3E50")),
            ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
            ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        story.append(t_table)
    story.append(Spacer(1, 8))

    # ---- Rekomendasi ----
    story.append(Paragraph("4. Recommended Actions", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))

    rek_list = cr.get("rekomendasi", [])
    if rek_list:
        rh = [["#", "Action", "Deadline", "Responsible Party"]]
        for r in rek_list:
            rh.append([
                str(r.get("prioritas", "")),
                Paragraph(r.get("aksi", ""), body),
                r.get("deadline", ""),
                r.get("penanggung_jawab", ""),
            ])
        r_table = Table(rh, colWidths=[1*cm, 9*cm, 2.5*cm, 5.5*cm])
        r_table.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#27AE60")),
            ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
            ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        story.append(r_table)
    story.append(Spacer(1, 8))

    # ---- Policy Enforcement ----
    story.append(Paragraph("5. Policy Enforcement", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7")))
    story.append(Paragraph(enforcement.get("message", "-"), body))
    story.append(Spacer(1, 12))

    # ---- Footer ----
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
    mr = analysis.get("monitor_regulasi", {})
    cr = analysis.get("compliance_report", {})
    rl = ra.get("risk_level", "LOW")

    icons = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🟢"}

    print("\n" + "="*62)
    print(f"  📊  COMPLIANCE REPORT  [{report_id}]")
    print("="*62)

    print(f"""
  Company     : {d['nama']}
  Industry    : {d['industri']}
  Regulations : {', '.join(d['regulasi'])}

  ┌──────────────────────────────────────────────┐
  │  RISK SCORE  :  {str(ra.get('risk_score','?')).ljust(6)} / 100                    
  │  RISK LEVEL  :  {icons.get(rl,'⚪')} {rl.ljust(10)}                 
  │  STATUS      :  {cr.get('status_kepatuhan','-').ljust(20)}           
  └──────────────────────────────────────────────┘""")

    print(f"\n  📡 REGULATION MONITOR  [{mr.get('status','-')}]")
    print(f"  {mr.get('catatan_monitor','-')}")
    if mr.get("temuan_regulasi_baru"):
        for t in mr["temuan_regulasi_baru"]:
            print(f"    • {t}")

    print(f"\n  ⚠️  RISK SUMMARY")
    print(f"  {ra.get('ringkasan_risiko','-')}")

    print(f"\n  📋 COMPLIANCE FINDINGS")
    for t in cr.get("temuan", []):
        print(f"  [{t.get('tingkat','?')}] {t.get('temuan','-')} ({t.get('regulasi_terkait','-')})")

    print(f"\n  💡 RECOMMENDATIONS")
    for r in cr.get("rekomendasi", []):
        print(f"  {r.get('prioritas','?')}. [{r.get('deadline','?')}] {r.get('aksi','-')} → {r.get('penanggung_jawab','-')}")

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

    high = [r for r in DB["compliance_reports"] if r.get("risk_level") in ("HIGH","CRITICAL")]
    if high:
        print("  ⚠️  REQUIRES ATTENTION:")
        for r in high:
            print(f"    • [{r['report_id']}] {r['nama']} → {r['risk_level']}")
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
        icons = {"CRITICAL":"🔴","HIGH":"🟡","MEDIUM":"🟠","LOW":"🟢"}
        rl = r.get("risk_level","LOW")
        print(f"  {icons.get(rl,'⚪')} [{r['report_id']}]  {r['nama']:<25}  {rl:<10}  Score:{r.get('risk_score','?')}")



def run_full_flow():
    # 1. Input
    d = collect_input()
    save_regulation(d)

    # 2. TinyFish analisis
    analysis = run_tinyfish(d)

    # IDs
    report_id = f"RPT-{len(DB['compliance_reports'])+1:04d}"
    ra = analysis.get("risk_analysis", {})

    # 3. Simpan ke DB
    DB["compliance_reports"].append({
        "report_id":  report_id,
        "nama":       d["nama"],
        "risk_level": ra.get("risk_level","LOW"),
        "risk_score": ra.get("risk_score", 0),
        "timestamp":  datetime.datetime.now().isoformat(),
    })
    DB["risk_analyses"].append({"report_id": report_id, **analysis})
    log_activity("REPORT", f"Compliance report created: {report_id}", report_id)

    # 4. Policy enforcement
    enforcement = enforce_policy(ra.get("risk_level","LOW"), report_id)

    # 5. Simpan JSON + PDF
    json_path = save_json(report_id, d, analysis, enforcement)
    pdf_path  = save_pdf(report_id, d, analysis, enforcement)

    # 6. Tampilkan ke terminal
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
        pilihan = input("  Choose (1-5): ").strip()

        if pilihan == "1":
            run_full_flow()
            input("\n  Press Enter to return to menu...")
        elif pilihan == "2":
            show_monitor()
            input("\n  Press Enter to return to menu...")
        elif pilihan == "3":
            show_all_reports()
            input("\n  Press Enter to return to menu...")
        elif pilihan == "4":
            show_activity_log()
            input("\n  Press Enter to return to menu...")
        elif pilihan == "5":
            print("\n  👋  Goodbye!\n")
            break
        else:
            print("\n  ❌  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()