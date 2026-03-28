"use client";
import Image from "next/image";
import Link from "next/link";

const pages = [
  { label: "Features", href: "#features" },
  { label: "Benefits", href: "#benefits" },
  { label: "Pricing", href: "#pricing" },
  { label: "Contact Us", href: "/contact" },
];

export default function Footer() {
  return (
    <footer className="px-4 pb-6">
      <div className="
        max-w-6xl mx-auto
        bg-white/30
        backdrop-blur-[6px]
        rounded-[45px]
        px-8 py-8
        border border-white/40
        shadow-[0_10px_30px_rgba(0,0,0,0.1)]
      ">
        
        <div className="flex justify-between items-start">
          {/* Logo */}
          <Image
            src="/gslogo.png"
            alt="Logo"
            width={32}
            height={32}
          />

          {/* Pages */}
          <div className="flex flex-col gap-1.5">
            <span className="text-sm font-semibold text-white mb-1">
              Pages
            </span>

            {pages.map((page) => (
              <Link
                key={page.label}
                href={page.href}
                className="text-sm text-white/90 hover:text-white transition"
              >
                {page.label}
              </Link>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div className="mt-8 pt-4 border-t border-white/30">
          <p className="text-sm font-semibold text-white">
            © 2026 GainSaid
          </p>
          <p className="text-xs text-white/80">
            Inspired by Leon Hike Projects
          </p>
        </div>

      </div>
    </footer>
  );
}