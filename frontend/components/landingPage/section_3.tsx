"use client";

import Image from "next/image";

export default function Section_3() {
  return (
    <section id="benefits" className="flex justify-center px-6 py-20 md:py-28">
      <div className="max-w-6xl w-full flex flex-col lg:flex-row items-center gap-12 lg:gap-16">

        {/* Left — Image */}
        <div className="w-full lg:w-1/2 flex justify-center">
          <Image
            src="/section3.png"
            alt="AI Agent Regulatory Dashboard"
            width={480}
            height={520}
            className="w-full h-auto rounded-2xl"
            priority
          />
        </div>

        {/* Right — Text */}
        <div className="w-full lg:w-1/2 flex flex-col gap-5">
          <span className="text-sm text-gray-500 font-medium tracking-wide">
            AI Compliance Report
          </span>

          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
            Keep your business compliant automatically
          </h2>

          <p className="text-base text-gray-500 leading-relaxed max-w-md">
            Monitor regulations, detect policy violations, and ensure your operations follow industry rules in real time. Our AI agent helps companies reduce legal risk, automate compliance checks, and stay ahead of changing regulations.
          </p>

          {/* Tags — 2 per baris */}
          <div className="flex flex-col gap-2 mt-1">
            <div className="flex gap-2">
              <span className="px-4 py-2 rounded-full border border-gray-300 text-sm text-gray-700">Tasks</span>
              <span className="px-4 py-2 rounded-full border border-gray-300 text-sm text-gray-700">Time Tracking</span>
            </div>
            <div className="flex gap-2">
              <span className="px-4 py-2 rounded-full border border-gray-300 text-sm text-gray-700">Timesheets</span>
              <span className="px-4 py-2 rounded-full border border-gray-300 text-sm text-gray-700">Reports</span>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}