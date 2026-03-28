"use client";
import Navbar from "@/components/navbar";
import { useState, useRef, useEffect } from "react";

type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
type ComplianceStatus = "COMPLIANT" | "NEEDS_IMPROVEMENT" | "NON_COMPLIANT";
type MonitorStatus = "UP_TO_DATE" | "CHANGES_FOUND" | "NEEDS_REVIEW";

type ChatStep =
  | "idle"
  | "company_name"
  | "industry"
  | "country"
  | "regulations"
  | "activity"
  | "value"
  | "parties"
  | "cross_border"
  | "third_party"
  | "sensitive_data"
  | "url"
  | "analyzing"
  | "done";

interface Finding {
  number: number;
  finding: string;
  level: RiskLevel;
  related_regulation: string;
  source_url?: string;
}

interface Recommendation {
  priority: number;
  action: string;
  deadline: string;
  responsible_party: string;
}

interface AnalysisResult {
  regulation_monitor: {
    status: MonitorStatus;
    new_regulations_found: string[];
    changed_regulations: string[];
    monitor_notes: string;
  };
  risk_analysis: {
    risk_score: number;
    risk_level: RiskLevel;
    violations_detected: string[];
    risk_factors: string[];
    risk_summary: string;
    confidence?: { level: string; disclaimer: string };
  };
  compliance_report: {
    compliance_status: ComplianceStatus;
    findings: Finding[];
    recommendations: Recommendation[];
    executive_summary: string;
  };
}

interface RegulationData {
  company_name: string;
  industry: string;
  country: string;
  regulations: string[];
  activity: string;
  value: string;
  parties_involved: string;
  cross_border: string;
  third_party: string;
  sensitive_data: string;
  url: string;
}

interface Message {
  role: "assistant" | "user" | "system";
  content: string;
  result?: AnalysisResult;
  data?: RegulationData;
  reportId?: string;
  enforcement?: EnforcementResult;
  timestamp?: Date;
}


interface EnforcementResult {
  report_id: string;
  risk_level: string;
  action: string;
  message: string;
  icon: string;
  timestamp: string;
}


const STEP_ORDER: ChatStep[] = [
  "company_name", "industry", "country", "regulations",
  "activity", "value", "parties", "cross_border",
  "third_party", "sensitive_data", "url",
];

const STEP_QUESTIONS: Partial<Record<ChatStep, string>> = {
  company_name:   "Masukkan **nama perusahaan** yang akan dianalisis:",
  industry:       "Masukkan **industri** perusahaan:\n_(contoh: Fintech, Perbankan, E-commerce, Asuransi)_",
  country:        "Masukkan **negara operasi** perusahaan:",
  regulations:    "Masukkan **regulasi yang berlaku**, pisahkan dengan koma:\n_(contoh: UU Cipta Kerja, OJK, PPATK, GDPR)_",
  activity:       "Jelaskan **aktivitas / transaksi** yang sedang ditinjau:",
  value:          "Masukkan **nilai transaksi** dalam USD:",
  parties:        "Siapa saja **pihak yang terlibat** dalam transaksi ini?",
  cross_border:   "Apakah ini **transaksi lintas negara**? Ketik `ya` atau `tidak`",
  third_party:    "Apakah ada **pihak ketiga** yang terlibat? Ketik `ya` atau `tidak`",
  sensitive_data: "Apakah ada **data sensitif** yang diproses? Ketik `ya` atau `tidak`",
  url:            "Masukkan **URL referensi regulasi** _(opsional — kosongkan untuk pencarian otomatis)_:",
};

// URL FastAPI backend — ganti ke production URL kalau sudah deploy di sini ya mass
const API_BASE = "http://localhost:8000";


function RiskBadge({ level }: { level: RiskLevel }) {
  const styles: Record<RiskLevel, string> = {
    LOW:      "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    MEDIUM:   "bg-orange-500/10  text-orange-400  border-orange-500/30",
    HIGH:     "bg-yellow-500/10  text-yellow-400  border-yellow-500/30",
    CRITICAL: "bg-red-500/10     text-red-400     border-red-500/30",
  };
  const dots: Record<RiskLevel, string> = {
    LOW: "bg-emerald-400", MEDIUM: "bg-orange-400", HIGH: "bg-yellow-400", CRITICAL: "bg-red-400",
  };
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[10px] font-bold tracking-widest font-mono border ${styles[level]}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dots[level]}`} />
      {level}
    </span>
  );
}

function RiskGauge({ score, level }: { score: number; level: RiskLevel }) {
  const r = 46;
  const circ = 2 * Math.PI * r;
  const offset = circ - (Math.min(100, Math.max(0, score)) / 100) * circ;
  const strokeColor: Record<RiskLevel, string> = {
    LOW: "#34d399", MEDIUM: "#fb923c", HIGH: "#facc15", CRITICAL: "#f87171",
  };
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={r} fill="none" stroke="#1e293b" strokeWidth="9" />
        <circle
          cx="60" cy="60" r={r}
          fill="none"
          stroke={strokeColor[level]}
          strokeWidth="9"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 60 60)"
          style={{ transition: "stroke-dashoffset 1.2s ease" }}
        />
        <text x="60" y="55" textAnchor="middle" fill={strokeColor[level]} fontSize="24" fontWeight="700" fontFamily="monospace">{score}</text>
        <text x="60" y="72" textAnchor="middle" fill="#475569" fontSize="10" fontFamily="monospace">/ 100</text>
      </svg>
      <RiskBadge level={level} />
    </div>
  );
}

function TypingDots() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 1, 2].map(i => (
        <span
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-sky-400 opacity-60"
          style={{ animation: `bounce 1.2s ${i * 0.2}s infinite` }}
        />
      ))}
      <style>{`@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}`}</style>
    </div>
  );
}

function parseMarkdown(text: string) {
  const parts = text.split(/(\*\*[^*]+\*\*|_[^_]+_|\n|`[^`]+`)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**"))
      return <strong key={i} className="text-sky-300 font-semibold">{part.slice(2, -2)}</strong>;
    if (part.startsWith("`") && part.endsWith("`"))
      return <code key={i} className="text-amber-300 bg-slate-700/60 px-1 rounded text-[11px]">{part.slice(1, -1)}</code>;
    if (part.startsWith("_") && part.endsWith("_"))
      return <em key={i} className="text-slate-400 not-italic text-xs">{part.slice(1, -1)}</em>;
    if (part === "\n") return <br key={i} />;
    return part;
  });
}


function EnforcementBanner({ enforcement }: { enforcement: EnforcementResult }) {
  const actionStyle: Record<string, string> = {
    BLOCK:            "border-red-500/50 bg-red-500/5 text-red-300",
    REVIEW_REQUIRED:  "border-yellow-500/50 bg-yellow-500/5 text-yellow-300",
    WARNING:          "border-orange-500/50 bg-orange-500/5 text-orange-300",
    PASS:             "border-emerald-500/50 bg-emerald-500/5 text-emerald-300",
  };
  const style = actionStyle[enforcement.action] ?? "border-slate-600 bg-slate-800 text-slate-300";

  return (
    <div className={`w-full max-w-2xl mt-2 border rounded-xl p-4 font-mono ${style}`}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-base">{enforcement.icon}</span>
        <span className="text-[11px] font-bold tracking-widest uppercase">{enforcement.action}</span>
        <span className="text-[10px] text-slate-500 ml-auto">{enforcement.report_id}</span>
      </div>
      <p className="text-[11px] leading-relaxed opacity-90 whitespace-pre-wrap">{enforcement.message}</p>
    </div>
  );
}

function AnalysisCard({ result, data }: { result: AnalysisResult; data?: RegulationData }) {
  const ra = result.risk_analysis;
  const mr = result.regulation_monitor;
  const cr = result.compliance_report;
  const [tab, setTab] = useState<"overview" | "findings" | "actions">("overview");

  const csStyle: Record<ComplianceStatus, string> = {
    COMPLIANT:         "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
    NEEDS_IMPROVEMENT: "text-orange-400  bg-orange-500/10  border-orange-500/30",
    NON_COMPLIANT:     "text-red-400     bg-red-500/10     border-red-500/30",
  };
  const msStyle: Record<MonitorStatus, { text: string; dot: string }> = {
    UP_TO_DATE:    { text: "text-emerald-400", dot: "bg-emerald-400 shadow-[0_0_6px_#34d399]" },
    CHANGES_FOUND: { text: "text-orange-400",  dot: "bg-orange-400  shadow-[0_0_6px_#fb923c]" },
    NEEDS_REVIEW:  { text: "text-yellow-400",  dot: "bg-yellow-400  shadow-[0_0_6px_#facc15]" },
  };
  const findingBorder: Record<RiskLevel, string> = {
    LOW: "border-l-emerald-500", MEDIUM: "border-l-orange-500", HIGH: "border-l-yellow-500", CRITICAL: "border-l-red-500",
  };
  const findingBg: Record<RiskLevel, string> = {
    LOW: "bg-emerald-500/5", MEDIUM: "bg-orange-500/5", HIGH: "bg-yellow-500/5", CRITICAL: "bg-red-500/5",
  };

  return (
    <div className="w-full max-w-2xl bg-slate-900 border border-slate-700/60 rounded-2xl overflow-hidden font-mono mt-2 shadow-2xl">

      <div className="bg-gradient-to-r from-slate-800 to-slate-900 border-b border-slate-700/60 px-5 py-4 flex justify-between items-start">
        <div>
          <p className="text-[10px] text-sky-500 tracking-[0.15em] mb-1 uppercase">Compliance Analysis Report</p>
          <p className="text-base font-bold text-white">{data?.company_name}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">{data?.industry} · {data?.country}</p>
          {data?.regulations && (
            <div className="flex flex-wrap gap-1 mt-2">
              {data.regulations.slice(0, 4).map((reg, i) => (
                <span key={i} className="text-[9px] px-1.5 py-0.5 bg-slate-700/60 text-slate-400 rounded border border-slate-600/50">{reg}</span>
              ))}
            </div>
          )}
        </div>
        <span className={`text-[10px] font-bold tracking-widest px-2.5 py-1 rounded border flex-shrink-0 ml-3 ${csStyle[cr.compliance_status]}`}>
          {cr.compliance_status.replace(/_/g, " ")}
        </span>
      </div>


      <div className="grid grid-cols-[148px_1fr] border-b border-slate-700/60">
        <div className="flex items-center justify-center p-4 border-r border-slate-700/60">
          <RiskGauge score={ra.risk_score} level={ra.risk_level} />
        </div>
        <div className="p-4">
          <p className="text-[10px] text-sky-500 tracking-[0.12em] uppercase mb-2">Risk Summary</p>
          <p className="text-xs text-slate-300 leading-relaxed">{ra.risk_summary}</p>
          {ra.risk_factors.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-3">
              {ra.risk_factors.slice(0, 4).map((f, i) => (
                <span key={i} className="text-[10px] px-2 py-0.5 bg-slate-800 text-slate-400 rounded border border-slate-700">
                  {f.length > 30 ? f.slice(0, 30) + "…" : f}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>


      <div className="flex items-start gap-3 px-5 py-3 border-b border-slate-700/60 bg-slate-800/30">
        <span className={`w-2 h-2 rounded-full mt-1 flex-shrink-0 ${msStyle[mr.status].dot}`} />
        <div>
          <span className={`text-[10px] font-bold tracking-widest uppercase ${msStyle[mr.status].text}`}>
            Regulation Monitor — {mr.status.replace(/_/g, " ")}
          </span>
          <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{mr.monitor_notes}</p>
          {mr.new_regulations_found?.slice(0, 2).map((r, i) => (
            <p key={i} className="text-[11px] text-orange-400 mt-1">↗ {r}</p>
          ))}
        </div>
      </div>


      <div className="flex border-b border-slate-700/60">
        {(["overview", "findings", "actions"] as const).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`flex-1 px-3 py-2.5 text-[10px] font-bold tracking-widest uppercase transition-all
              ${tab === t ? "text-sky-400 border-b-2 border-sky-400 bg-sky-500/5" : "text-slate-500 hover:text-slate-300"}`}
          >
            {t === "findings" ? `Findings (${cr.findings.length})` : t === "actions" ? `Actions (${cr.recommendations.length})` : "Overview"}
          </button>
        ))}
      </div>


      <div className="p-4">
        {tab === "overview" && (
          <div className="space-y-4">
            <div>
              <p className="text-[10px] text-sky-500 tracking-widest uppercase mb-2">Executive Summary</p>
              <p className="text-xs text-slate-300 leading-relaxed">{cr.executive_summary}</p>
            </div>
            {ra.violations_detected.length > 0 && (
              <div>
                <p className="text-[10px] text-red-400 tracking-widest uppercase mb-2">Violations Detected</p>
                {ra.violations_detected.map((v, i) => (
                  <div key={i} className="flex gap-2 mb-1.5">
                    <span className="text-red-500 text-xs mt-0.5 flex-shrink-0">⚠</span>
                    <span className="text-[11px] text-red-300/80 leading-relaxed">{v}</span>
                  </div>
                ))}
              </div>
            )}
            {ra.confidence && (
              <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg px-3 py-2.5">
                <p className="text-[10px] text-slate-400">
                  <span className="text-sky-400 font-bold">Confidence: {ra.confidence.level}</span> — {ra.confidence.disclaimer}
                </p>
              </div>
            )}
          </div>
        )}

        {tab === "findings" && (
          <div className="space-y-2.5">
            {cr.findings.length === 0
              ? <p className="text-xs text-slate-500 text-center py-6">Tidak ada findings ditemukan.</p>
              : cr.findings.map((f, i) => (
                  <div key={i} className={`p-3 rounded-lg border-l-[3px] ${findingBg[f.level]} ${findingBorder[f.level]}`}>
                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                      <RiskBadge level={f.level} />
                      <span className="text-[10px] text-slate-400">{f.related_regulation}</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{f.finding}</p>
                  </div>
                ))
            }
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-2.5">
            {cr.recommendations.length === 0
              ? <p className="text-xs text-slate-500 text-center py-6">Tidak ada rekomendasi.</p>
              : cr.recommendations.map((r, i) => (
                  <div key={i} className="p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
                    <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
                      <span className="text-[11px] font-bold text-sky-400">Priority #{r.priority}</span>
                      <div className="flex gap-1.5">
                        <span className="text-[10px] px-2 py-0.5 bg-slate-700 text-slate-300 rounded">{r.deadline}</span>
                        <span className="text-[10px] px-2 py-0.5 bg-slate-700 text-slate-300 rounded">{r.responsible_party}</span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{r.action}</p>
                  </div>
                ))
            }
          </div>
        )}
      </div>
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isUser   = msg.role === "user";
  const isSystem = msg.role === "system";

  if (isSystem) {
    return (
      <div className="flex justify-center my-2">
        <span className="text-[10px] text-slate-500 font-mono tracking-widest uppercase border border-slate-700/50 px-3 py-1 rounded-full">
          {msg.content}
        </span>
      </div>
    );
  }

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} items-end`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-sky-500/20 border border-sky-500/30 flex items-center justify-center flex-shrink-0 mb-0.5">
          <svg className="w-4 h-4 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
              d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.955 11.955 0 01.75 12c0 6.627 5.373 12 12 12s12-5.373 12-12A11.955 11.955 0 0120.402 6a11.959 11.959 0 01-2.648-3.286" />
          </svg>
        </div>
      )}

      <div className={`max-w-[82%] flex flex-col gap-1 ${isUser ? "items-end" : "items-start"}`}>
        {msg.content && (
          <div className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed font-mono
            ${isUser
              ? "bg-sky-600 text-white rounded-br-sm"
              : "bg-slate-800/80 text-slate-200 border border-slate-700/50 rounded-bl-sm"
            }`}
          >
            {parseMarkdown(msg.content)}
          </div>
        )}
        {msg.result && <AnalysisCard result={msg.result} data={msg.data} />}
        {msg.enforcement && <EnforcementBanner enforcement={msg.enforcement} />}
      </div>
    </div>
  );
}

//  Main ChatBot 
export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Selamat datang di **Compliance Regulator AI** — sistem analisis kepatuhan regulasi bisnis.\n\nSaya akan memandu Anda menganalisis risiko kepatuhan perusahaan berdasarkan regulasi yang berlaku.\n\nKetik `mulai` untuk memulai analisis baru.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput]         = useState("");
  const [step, setStep]           = useState<ChatStep>("idle");
  const [formData, setFormData]   = useState<Partial<RegulationData>>({});
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const addMsg = (msg: Omit<Message, "timestamp">) =>
    setMessages(prev => [...prev, { ...msg, timestamp: new Date() }]);

const handleSend = async () => {
    const val = input.trim();
    
    // URL boleh kosong (opsional)
    if (step === "url" && !val) {
      setInput("");
      const nd = { ...formData, url: "" };
      setFormData(nd);
      addMsg({ role: "user", content: "_(skip — pencarian otomatis)_" });
      setStep("analyzing");
      addMsg({ role: "system", content: "Dreelio sedang menganalisis" });
      setIsLoading(true);
      await runAnalysis(nd as RegulationData);
      return;
    }

    if (!val || isLoading) return;


    if (step === "idle") {
      addMsg({ role: "user", content: val });
      if (val.toLowerCase().includes("mulai") || val.toLowerCase().includes("start")) {
        setStep("company_name");
        addMsg({ role: "assistant", content: STEP_QUESTIONS["company_name"]! });
      } else {
        addMsg({ role: "assistant", content: "Ketik **mulai** untuk memulai analisis kepatuhan baru." });
      }
      return;
    }


    if (STEP_ORDER.includes(step)) {
      addMsg({ role: "user", content: val });

      const nd = { ...formData };
      if      (step === "regulations")    nd.regulations      = val.split(",").map(s => s.trim()).filter(Boolean);
      else if (step === "company_name")   nd.company_name     = val;
      else if (step === "industry")       nd.industry         = val;
      else if (step === "country")        nd.country          = val;
      else if (step === "activity")       nd.activity         = val;
      else if (step === "value")          nd.value            = val;
      else if (step === "parties")        nd.parties_involved = val;
      else if (step === "cross_border")   nd.cross_border     = val.toLowerCase().startsWith("y") ? "yes" : "no";
      else if (step === "third_party")    nd.third_party      = val.toLowerCase().startsWith("y") ? "yes" : "no";
      else if (step === "sensitive_data") nd.sensitive_data   = val.toLowerCase().startsWith("y") ? "yes" : "no";
      else if (step === "url")            nd.url              = val;
      setFormData(nd);

      if (step === "url") {
        setStep("analyzing");
        addMsg({ role: "system", content: "Dreelio sedang menganalisis…" });
        setIsLoading(true);
        await runAnalysis(nd as RegulationData);
      } else {
        const idx = STEP_ORDER.indexOf(step);
        const ns  = STEP_ORDER[idx + 1];
        setStep(ns);
        addMsg({ role: "assistant", content: STEP_QUESTIONS[ns]! });
      }
      return;
    }

    // ── Done ──────────────────────────────────────────────────────
    if (step === "done") {
      addMsg({ role: "user", content: val });
      if (val.toLowerCase().includes("mulai") || val.toLowerCase().includes("baru")) {
        setStep("company_name");
        setFormData({});
        addMsg({ role: "assistant", content: STEP_QUESTIONS["company_name"]! });
      } else {
        addMsg({ role: "assistant", content: "Ketik **mulai** atau **analisis baru** untuk memulai analisis berikutnya." });
      }
    }
  };


  const runAnalysis = async (data: RegulationData) => {
    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company_name:     data.company_name,
          industry:         data.industry,
          country:          data.country,
          regulations:      data.regulations,
          activity:         data.activity,
          value:            data.value,
          parties_involved: data.parties_involved,
          cross_border:     data.cross_border,
          third_party:      data.third_party,
          sensitive_data:   data.sensitive_data,
          url:              data.url ?? "",
        }),
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Backend error ${response.status}: ${errText}`);
      }

      const res = await response.json();

      const result: AnalysisResult      = res.analysis;
      const enforcement: EnforcementResult = res.enforcement;
      const reportId: string             = res.report_id;

      setIsLoading(false);

      addMsg({
        role: "assistant",
        content: `Analisis selesai untuk **${data.company_name}** — Report ID: \`${reportId}\`\n\nBerikut laporan kepatuhan lengkap:`,
        result,
        data,
      });

      addMsg({
        role: "assistant",
        content: "",
        enforcement,
      });

      addMsg({
        role: "assistant",
        content: `📄 Laporan juga disimpan sebagai PDF & JSON di server.\n\nKetik **mulai** atau **analisis baru** untuk menganalisis perusahaan lain.`,
      });

      setStep("done");
    } catch (err) {
      setIsLoading(false);

      const errorMessage = err instanceof Error ? err.message : "Unknown error";
      const isNetworkError = errorMessage.includes("fetch") || errorMessage.includes("Failed to fetch");

      addMsg({
        role: "assistant",
        content: isNetworkError
          ? "❌ **Tidak dapat terhubung ke backend.**\n\nPastikan FastAPI sudah berjalan:\n```\nuvicorn main:app --reload --port 8000\n```\n\nLalu ketik **mulai** untuk mencoba ulang."
          : `❌ Terjadi kesalahan: ${errorMessage}\n\nKetik **mulai** untuk mencoba ulang.`,
      });

      setStep("idle");
      setFormData({});
    }
  };

  const currentIdx = STEP_ORDER.indexOf(step);
  const progress =
    step === "analyzing" || step === "done"
      ? 100
      : currentIdx === -1
      ? 0
      : Math.round((currentIdx / STEP_ORDER.length) * 100);

  const showProgress = step !== "idle" && step !== "done";

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-white overflow-hidden">
      <Navbar/>

      <header className="flex-shrink-0 flex items-center justify-between px-5 py-3 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-sky-500/20 border border-sky-500/40 flex items-center justify-center">
            <svg className="w-5 h-5 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.955 11.955 0 01.75 12c0 6.627 5.373 12 12 12s12-5.373 12-12A11.955 11.955 0 0120.402 6a11.959 11.959 0 01-2.648-3.286" />
            </svg>
          </div>
          <div>
            <h1 className="text-sm font-bold text-white font-mono tracking-tight">Compliance Regulator AI</h1>
            <p className="text-[10px] text-slate-500 font-mono">Powered by TinyFish · Risk & Regulatory Analysis</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
          <span className="text-[10px] text-emerald-400 font-mono tracking-widest">ONLINE</span>
        </div>
      </header>

      {showProgress && (
        <div className="flex-shrink-0 px-5 py-2.5 bg-slate-900/50 border-b border-slate-800/50">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[10px] text-slate-500 font-mono uppercase tracking-widest">Input Data Perusahaan</span>
            <span className="text-[10px] text-sky-400 font-mono">
              {step === "analyzing" ? "Menganalisis via TinyFish…" : `${progress}%`}
            </span>
          </div>
          <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-sky-500 to-blue-500 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      <main className="flex-1 overflow-y-auto px-4 py-5 space-y-4">
        {messages.map((msg, i) => <MessageBubble key={i} msg={msg} />)}

        {isLoading && (
          <div className="flex gap-3 items-end">
            <div className="w-8 h-8 rounded-lg bg-sky-500/20 border border-sky-500/30 flex items-center justify-center flex-shrink-0">
              <svg className="w-4 h-4 text-sky-400 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            </div>
            <div className="bg-slate-800/80 border border-slate-700/50 rounded-2xl rounded-bl-sm">
              <TypingDots />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      {step === "idle" && (
        <div className="flex-shrink-0 flex gap-2 px-4 pb-2">
          {[
            { label: "🚀 Mulai Analisis", val: "mulai" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => { setInput(val); setTimeout(handleSend, 30); }}
              className="text-[11px] font-mono px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 hover:border-sky-500/50 hover:text-sky-300 transition-all"
            >
              {label}
            </button>
          ))}
        </div>
      )}

      <div className="flex-shrink-0 px-4 pb-4">
        <div className="flex gap-2 bg-slate-800/80 border border-slate-700/60 rounded-xl p-2 focus-within:border-sky-500/50 transition-colors">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleSend()}
            placeholder={
              step === "idle"        ? "Ketik 'mulai' untuk memulai analisis…"
              : step === "analyzing" ? "Sedang menganalisis via TinyFish…"
              : step === "done"      ? "Ketik 'mulai' untuk analisis baru…"
              : "Ketik jawaban Anda…"
            }
            disabled={step === "analyzing" || isLoading}
            className="flex-1 bg-transparent text-sm text-white placeholder-slate-500 font-mono outline-none px-2 disabled:opacity-40"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || step === "analyzing" || isLoading}
            className="w-9 h-9 rounded-lg bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:opacity-40 flex items-center justify-center transition-all flex-shrink-0"
          >
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}