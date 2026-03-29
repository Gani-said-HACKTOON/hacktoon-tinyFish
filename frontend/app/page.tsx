"use client";

import TryButton from "@/components/tryButton";
import AnimatedText from "@/components/landingPage/animatedText";
import Link from "next/link";
import Section_2 from "@/components/landingPage/section_2-1";
import Section_3 from "@/components/landingPage/section_3";

export default function Home() {
  return (
    <>
      <section className="flex justify-center mt-10 py-20 md:py-28 lg:py-35">
        <div className="max-w-6xl w-full px-6 flex flex-col items-center justify-center md:px-10 lg:px-12">

          <h1 className="text-4xl md:text-5xl lg:text-8xl font-semibold text-center text-white">
            <AnimatedText text="Run your business like a pro." delay={0.05} />
          </h1>

          <p className="mt-4 text-base md:text-lg lg:text-xl font-semibold text-center max-w-2xl text-white">
            <AnimatedText text="All-in-one platform to help businesses automatically comply with regulations by using AI to monitor, detect, and prevent policy violations." delay={0.05} />
          </p>

          <div className="w-full flex flex-col items-center gap-2 mt-7 -mb-21 opacity-0 translate-y-2.5 animate-[fadeInBlur_0.6s_ease_0.7s_forwards]">
            <TryButton className="w-full lg:w-45" />
            <Link href="/chatBot" className="text-white underline font-bold">Sign In</Link>
          </div>

        </div>
      </section>

      <Section_2 />
      <Section_3 />

      {/* Footer */}
      <div className="flex flex-col items-center px-4 pb-6">
        <div
          className="w-full max-w-2xl rounded-2xl px-6 pt-6 pb-6 py-10"
          style={{ background: "rgba(255,255,255,0.20)", backdropFilter: "blur(12px)" }}
        >

          {/* Top: logo + nav */}
          <div className="flex items-start justify-between mb-6">

            {/* Logo */}
            <div>
              <img src="/gslogo.png" alt="GainSaid logo" className="w-9 h-9 object-contain" />
            </div>

            {/* Pages nav */}
            <div className="flex flex-col gap-1 text-right">
              <p className="text-xs font-medium mb-1" style={{ color: "rgba(255,255,255,0.60)" }}>
                Pages
              </p>
              <a href="#" className="text-sm hover:text-white transition-colors" style={{ color: "rgba(255,255,255,0.80)" }}>Features</a>
              <a href="#" className="text-sm hover:text-white transition-colors" style={{ color: "rgba(255,255,255,0.80)" }}>Benefits</a>
              <a href="#" className="text-sm hover:text-white transition-colors" style={{ color: "rgba(255,255,255,0.80)" }}>Pricing</a>
              <a href="#" className="text-sm hover:text-white transition-colors" style={{ color: "rgba(255,255,255,0.80)" }}>Contact Us</a>
            </div>
          </div>

          {/* Divider */}
          <div className="mb-4" style={{ borderTop: "1px solid rgba(255,255,255,0.30)" }} />

          {/* Copyright */}
          <div>
            <p className="text-sm font-medium" style={{ color: "rgba(255,255,255,0.80)" }}>
              © 2026  GainSaid
            </p>
            <p className="text-xs mt-0.5" style={{ color: "rgba(255,255,255,0.50)" }}>
              Inspired by Lean Hike Projects
            </p>
          </div>

        </div>
      </div>
    </>
  );
}