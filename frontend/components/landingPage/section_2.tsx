"use client";

import { useEffect, useRef } from "react";

export default function Section_2() {
  const mockupRef = useRef<HTMLDivElement | null>(null);
  const wrapRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const mockup = mockupRef.current;
    const wrap = wrapRef.current;
    if (!mockup || !wrap) return;

    const updateTilt = () => {
      const rect = wrap.getBoundingClientRect();
      const vh = window.innerHeight;

      const progress = 1 - rect.top / vh;
      const clamped = Math.max(0, Math.min(1, progress));

      const rotateX = 50 - clamped * 50;
      const scale = 0.88 + clamped * 0.12;

      mockup.style.transformOrigin = "center bottom";
      mockup.style.transform = `rotateX(${rotateX.toFixed(2)}deg) scale(${scale.toFixed(3)})`;
      mockup.style.boxShadow = `0 ${Math.round(16 + clamped * 64)}px 100px rgba(0,0,0,${(0.28 - clamped * 0.1).toFixed(2)})`;
    };

    window.addEventListener("scroll", updateTilt, { passive: true });
    updateTilt();

    return () => window.removeEventListener("scroll", updateTilt);
  }, []);

  return (
    <section className="px-8 pb-32 flex justify-center">
      <div ref={wrapRef} className="w-full max-w-225 perspective-distant">
        <div
          ref={mockupRef}
          className="bg-white rounded-[14px] shadow-[0_32px_100px_rgba(0,0,0,0.2)] overflow-hidden will-change-transform"
          style={{
            transform: "rotateX(50deg) scale(0.88)",
            transformOrigin: "center bottom",
          }}
        >
          {/* bar */}
          <div className="bg-[#f5f5f5] px-4 py-2 flex items-center gap-1.5 border-b border-[#eee]">
            <div className="w-2.5 h-2.5 rounded-full bg-[#ff5f57]" />
            <div className="w-2.5 h-2.5 rounded-full bg-[#febc2e]" />
            <div className="w-2.5 h-2.5 rounded-full bg-[#28c840]" />
            <span className="text-[11px] text-[#999] ml-2">
              Dreelio — Dashboard
            </span>
          </div>

          {/* body */}
          <div className="grid grid-cols-[160px_1fr] min-h-70">
            {/* sidebar */}
            <div className="bg-[#fafafa] border-r border-[#eee] p-4 flex flex-col gap-1.5">
              <div className="text-[13px] font-bold text-[#111] mb-2">
                🌙 Dreelio
              </div>
              <div className="text-[12px] px-2 py-1.5 rounded bg-[#f0f0f0] font-semibold text-[#111]">
                Home
              </div>
              <div className="text-[12px] px-2 py-1.5 text-[#555]">
                Clients
              </div>
              <div className="text-[12px] px-2 py-1.5 text-[#555]">
                Projects
              </div>
              <div className="text-[12px] px-2 py-1.5 text-[#555]">
                Invoices
              </div>
              <div className="text-[12px] px-2 py-1.5 text-[#555]">
                Balance
              </div>
              <div className="text-[12px] px-2 py-1.5 text-[#555]">
                Accounting
              </div>
            </div>

            {/* content */}
            <div className="p-5 flex flex-col gap-3.5">
              <div className="text-[14px] font-bold text-[#111]">
                Hello, Leonardo 👋
                <span className="block text-[12px] text-[#888] font-normal mt-0.5">
                  What are you working on?
                </span>
              </div>

              {/* stats */}
              <div className="grid grid-cols-4 gap-2">
                {[
                  { label: "Total projects", num: 455, tag: "+16.4%", color: "text-green-500" },
                  { label: "Active", num: 55, tag: "-4.8%", color: "text-red-500" },
                  { label: "Completed", num: 400, tag: "+12.8%", color: "text-green-500" },
                  { label: "Hours", num: 600, tag: "-1.2%", color: "text-red-500" },
                ].map((item, i) => (
                  <div key={i} className="bg-[#f9f9f9] rounded-[10px] p-3 text-[11px] text-[#888]">
                    {item.label}
                    <div className="text-[20px] font-bold text-[#111] mt-1">
                      {item.num}
                    </div>
                    <div className={`text-[10px] mt-0.5 ${item.color}`}>
                      {item.tag}
                    </div>
                  </div>
                ))}
              </div>

              {/* chart */}
              <div className="text-[11px] text-[#888] font-medium">
                Earnings over time
              </div>
              <div className="flex items-end gap-1 h-17.5">
                {[75, 50, 85, 40, 90, 55, 70, 60, 45, 80].map((h, i) => (
                  <div
                    key={i}
                    className="flex-1 bg-[#dce8f5] border-b-2 border-[#7aaee8] rounded-t"
                    style={{ height: `${h}%` }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}