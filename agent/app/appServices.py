
from pydantic import BaseModel

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
from app import appDatabase as db

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

class appService():
    token: str 

    def __init__(self, token):
        self.token = token

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

    RISK_COLORS = {
        "CRITICAL": colors.HexColor("#C0392B"),
        "HIGH":     colors.HexColor("#E67E22"),
        "MEDIUM":   colors.HexColor("#F1C40F"),
        "LOW":      colors.HexColor("#27AE60"),
    }

    _ASSUMPTION_PATTERNS = [
    "typically", "usually", "generally", "often", "may", "might", "could",
    "assumed", "assumption", "likely", "probably", "suggest", "appears",
    "seems", "too small", "too large", "too low", "too high",
    "insufficient", "excessive", "unusual", "uncommon",
    ]


    LEVEL_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
    RANK_LEVEL = {v: k for k, v in LEVEL_RANK.items()}



    async def add_log_activity(self, action: str, detail: str, ref_id: str = ""):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action":    action,
            "detail":    detail,
            "ref_id":    ref_id,
        }

        db.write_to_db("activity_log", entry, self.token)

    async def getDbByKey(self, key: str) -> any:
        jsonData: str = await db.read_from_db(key, self.token)
        dataObj = json.loads(jsonData)
        return dataObj




    def get_trusted_urls(self, country: str, regulations: list) -> list:
        """
        Kembalikan list URL sumber terpercaya berdasarkan negara.
        Selalu tambahkan sumber global (FATF, BIS, dll) sebagai pelengkap.
        """
        country_key = country.strip().lower()

        # Cari exact match dulu
        sources = list(self.TRUSTED_SOURCES.get(country_key, []))

        # Kalau tidak ada exact match, cari partial match
        if not sources:
            for key in self.TRUSTED_SOURCES:
                if key in country_key or country_key in key:
                    sources = list(self.TRUSTED_SOURCES[key])
                    break


        if not sources:
            # Coba Google Site Search ke domain .gov atau resmi negara tsb
            country_slug = country_key.replace(" ", "+")
            sources = [
                f"https://www.google.com/search?q={country_slug}+official+regulation+site:.gov+OR+site:.go+OR+site:.gov.{country_slug[:2]}",
            ]


        sources += self.TRUSTED_SOURCES["global"][:3] 
        return sources


    def run_tinyfish(self,d: dict) -> dict:
        print("\n" + "="*62)
        print("  🤖  Dreelio AI")
        print("="*62)

        # Determine target URL — prioritaskan URL manual, lalu sumber terpercaya
        if d.get("url"):
            urls = [d["url"]]
        else:
            urls = self.get_trusted_urls(d["country"], d["regulations"])

        url = urls[0]

        trusted_domains_str = "\n".join(f"  - {u}" for u in urls)

        goal = self.TINYFISH_GOAL.format(
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
            result = self.fallback_analysis(d)

        valid_levels = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

        if "risk_analysis" not in result:
            print("  ⚠️  'risk_analysis' key missing from AI response — using fallback.")
            result = self.fallback_analysis(d)

        ra_check = result.get("risk_analysis", {})
        detected_level = ra_check.get("risk_level", "").upper()
        if detected_level not in valid_levels:
            print(f"  ⚠️  Invalid risk_level '{detected_level}' — using fallback.")
            result = self.fallback_analysis(d)
        else:
            result["risk_analysis"]["risk_level"] = detected_level

        result = self.override_risk_level(result)
        result = self.inject_confidence_flags(result)

        final_level = result["risk_analysis"].get("risk_level")
        print(f"\n  ✅  Analysis complete. Risk Level: {final_level}\n")
        self.add_log_activity("AI_ANALYSIS", f"Dreelio analysis done: {d['company_name']}", d["id"])
        return result

    def override_risk_level(self,result: dict) -> dict:
        """
        Rule-based override: kalau temuan atau violations lebih parah
        dari risk_level yang diklaim AI, paksa naik ke level yang sesuai.
        """
        ra = result.get("risk_analysis", {})
        cr = result.get("compliance_report", {})

        current_level = ra.get("risk_level", "LOW")
        current_rank  = self.LEVEL_RANK.get(current_level, 1)
        findings      = cr.get("findings", [])
        violations    = ra.get("violations_detected", [])

        finding_levels   = [f.get("level", "LOW").upper() for f in findings]
        max_finding_rank = max((self.LEVEL_RANK.get(l, 1) for l in finding_levels), default=1)

        overridden_rank  = current_rank
        override_reasons = []

        if max_finding_rank > current_rank:
            overridden_rank = max_finding_rank
            top_level = self.RANK_LEVEL[max_finding_rank]
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
            new_level = self.RANK_LEVEL[overridden_rank]
            result["risk_analysis"]["risk_level"] = new_level
            result["risk_analysis"].setdefault("override_log", []).extend(override_reasons)
            for reason in override_reasons:
                print(f"  ⚠️  OVERRIDE: {reason}")
        else:
            result["risk_analysis"].setdefault("override_log", [])

        return result

    def inject_confidence_flags(self,result: dict) -> dict:
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
            for pat in self._ASSUMPTION_PATTERNS:
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


    def build_enforcement_message(self,risk_level: str, analysis: dict) -> str:
        """
        Bangun pesan policy enforcement yang detail dan kontekstual
        berdasarkan temuan nyata dari analisis AI.
        """
        p           = self.POLICY.get(risk_level, self.POLICY["LOW"])
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


    def enforce_policy(self, risk_level: str, report_id: str, analysis: dict = None) -> dict:
        p       = self.POLICY.get(risk_level, self.POLICY["LOW"])
        message = self.build_enforcement_message(risk_level, analysis or {})
        entry = {
            "timestamp":  datetime.datetime.now().isoformat(),
            "report_id":  report_id,
            "risk_level": risk_level,
            "action":     p["action"],
            "message":    message,
        }

        db.write_to_db("policy_enforcements",entry, self.token)
        self.add_log_activity("ENFORCEMENT", f"{p['action']} applied for {report_id}", report_id)
        return {**entry, "icon": p["icon"]}


    # step 4
    def save_json(self,report_id: str, d: dict, analysis: dict, enforcement: dict):
        payload = {
            "report_id":    report_id,
            "regulation":   d,
            "analysis":     analysis,
            "enforcement":  enforcement,
            "generated_at": datetime.datetime.now().isoformat(),
        }
        self.add_log_activity("SAVE_JSON", f"JSON saved on database", report_id)

        db.write_to_db("report_data",payload, self.token)


    def save_pdf(self,report_id: str, d: dict, analysis: dict, enforcement: dict):
        path = os.path.join("../compliance", f"{report_id}.pdf")
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
        risk_color = self.RISK_COLORS.get(rl, colors.grey)

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
        self.add_log_activity("SAVE_PDF", f"PDF saved: {path}", report_id)
        return path

    async def analyze_report(self, data: RegulationInput):
        d = data.model_dump()
        d["id"]        = f"REG-{len(await self.getDbByKey('regulations'))+1:04d}"
        d["timestamp"] = datetime.datetime.now().isoformat()

        db.write_to_db("regulations" , d, self.token)
        self.add_log_activity("INPUT", f"Data received from frontend: {d['company_name']}", d["id"])

        analysis  = self.run_tinyfish(d)
        report_id = f"RPT-{len(await self.getDbByKey('compliance_reports'))+1:04d}"
        ra        = analysis.get("risk_analysis", {})

        db.write_to_db("compliance_reports", {
            "report_id":    report_id,
            "company_name": d["company_name"],
            "risk_level":   ra.get("risk_level", "LOW"),
            "risk_score":   ra.get("risk_score", 0),
            "timestamp":    datetime.datetime.now().isoformat(),
        }, self.token)
        db.write_to_db("risk_analyses", {"report_id": report_id, **analysis}, self.token)
        self.add_log_activity("REPORT", f"Compliance report created: {report_id}", report_id)

        actual_risk_level = ra.get("risk_level", "LOW")
        enforcement = self.enforce_policy(actual_risk_level, report_id, analysis)

        json_path = self.save_json(report_id, d, analysis, enforcement)
        pdf_path  = self.save_pdf(report_id, d, analysis, enforcement)

        return {
            "report_id":   report_id,
            "analysis":    analysis,
            "enforcement": enforcement,
            "json_path":   json_path,
            "pdf_path":    pdf_path,
        }


    async def show_monitor(self):
        risk_count = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for r in await self.getDbByKey("compliance_reports"):
            rl = r.get("risk_level", "LOW")
            risk_count[rl] = risk_count.get(rl, 0) + 1
        high_risk = [r for r in await self.getDbByKey("compliance_reports") if r.get("risk_level") in ("HIGH", "CRITICAL")]
        return {
            "total_reports":      len(await self.getDbByKey("compliance_reports")),
            "total_entities":     len(await self.getDbByKey("regulations")),
            "risk_distribution":  risk_count,
            "requires_attention": high_risk,
        }