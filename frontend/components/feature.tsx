"use client";

import { useEffect, useState } from "react";
import TryButton from "@/components/tryButton";

export default function FeatureSection() {
    const [show, setShow] = useState(false);

    useEffect(() => {
        const t = setTimeout(() => setShow(true), 150);
        return () => clearTimeout(t);
    }, []);

    return (
        <section className="w-full flex justify-center py-28 bg-linear-to-b from-[#B1C3D4] to-[#E2E2E2]">
        
        <div className="max-w-6xl w-full px-6 grid md:grid-cols-2 items-center gap-6">

            {/* IMAGE */}
            <div
            className={`
                flex justify-center md:justify-end
                transition-all duration-700 ease-out
                ${show ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}
            `}
            >
            <div className="relative group">

                {/* glow */}
                <div className="absolute -z-10 w-65 h-65 bg-blue-300/30 blur-[100px] rounded-full" />

                {/* floating card */}
                <div className="
                w-65 md:w-75
                p-2 bg-white/70 backdrop-blur-xl
                rounded-2xl shadow-xl border border-white/40
                transition duration-500
                group-hover:-translate-y-2 group-hover:scale-[1.03]
                ">
                <img
                    src="/Tab-View.jpg"
                    alt="dashboard"
                    className="rounded-xl w-full"
                />
                </div>

            </div>
            </div>

            {/* TEXT */}
            <div
            className={`
                flex flex-col gap-4 max-w-125
                transition-all duration-700 delay-150
                ${show ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}
            `}
            >
            <p className="text-sm text-gray-700">
                AI Compliance Report
            </p>

            <h2 className="text-[34px] md:text-[42px] font-semibold leading-[1.1] text-white">
                Keep your business compliant automatically
            </h2>

            <p className="text-gray-100 text-[15px] leading-relaxed">
                Monitor regulations, detect policy violations, and ensure your
                operations follow industry rules in real time.
            </p>

            {/* CTA */}
            <div className="mt-3">
                <TryButton />
            </div>

            {/* TAGS */}
            <div className="flex flex-wrap gap-2 mt-3">
                {["Tasks", "Time Tracking", "Timesheets", "Reports"].map((tag) => (
                <span
                    key={tag}
                    className="
                    px-3 py-1 text-sm rounded-full
                    bg-white/70 text-gray-800 backdrop-blur
                    transition duration-300
                    hover:-translate-y-1 hover:scale-105
                    "
                >
                    {tag}
                </span>
                ))}
            </div>
            </div>
        </div>
        </section>
    );
    }