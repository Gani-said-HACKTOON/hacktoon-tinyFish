"use client";

import Image from "next/image";
import { useRef, useEffect } from "react";

export default function TiltImage() {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleScroll = () => {
        const el = ref.current;
        if (!el) return;

        const rect = el.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        // distance from center
        const elementCenter = rect.top + rect.height / 2;
        const screenCenter = windowHeight / 2;

        const distance = (elementCenter - screenCenter) / screenCenter;

        // clamp
        const clamped = Math.max(-1, Math.min(1, distance));

        // effects
        const rotateX = clamped * 12; // softer tilt
        const scale = 1 + (1 - Math.abs(clamped)) * 0.06; // subtle zoom

        // apply transform (clean, no line breaks)
        el.style.transform = `rotateX(${rotateX}deg) scale(${scale})`;
        };

        handleScroll();
        window.addEventListener("scroll", handleScroll);

        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <div className="mt-20 w-full flex justify-center">
        <div style={{ perspective: "1200px" }}>
            <div
            ref={ref}
            className="transition-transform duration-300 ease-out will-change-transform"
            >
            <Image
                src="/previewProjects.png"
                alt="preview"
                width={1200}
                height={700}
                className="w-full max-w-250 mx-auto rounded-xl shadow-2xl border border-gray-200"
            />
            </div>
        </div>
        </div>
    );
}