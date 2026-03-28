"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";
import gambar from "../public/ImageLandingpage.png";

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
          className="rounded-[14px] overflow-hidden will-change-transform"
          style={{
            transform: "rotateX(50deg) scale(0.88)",
            transformOrigin: "center bottom",
          }}
        >
          <Image
            src="/ImageLandingpage.png"
            alt="Ganisaid Dashboard"
            width={6000}
            height={6000}
            className="w-full h-auto block"
            priority
          />
        </div>
      </div>
    </section>
  );
}