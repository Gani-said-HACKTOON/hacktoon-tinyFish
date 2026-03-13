"use client";

import { useState, useEffect } from "react";

// list yg keluar pas hamburger di pencet
const navLinks = [
  { label: "Features", href: "#features" },
  { label: "Benefits", href: "#benefits" },
  { label: "Pricing", href: "#pricing" },
  { label: "Blog", href: "#blog" },
  { label: "Contact Us", href: "#contact" },
];

// animasi navbar saat di scroll
export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 60);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024) setMenuOpen(false);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);


  // mobile and tablet (navbarnya hidden di 1024px)
  return (
    <>
      <nav className="lg:hidden fixed top-0 left-0 right-0 z-50">
        <div className={`mx-3 mt-3 bg-white/30 backdrop-blur-[6px] rounded-[45px] shadow-sm transition-colors duration-80 py-1 ${menuOpen ? "bg-white/50" : "bg-white/30"
          }`}>
          <div className="flex items-center justify-between px-4 py-3">
            <a href="/" className="flex items-center gap-2 font-bold text-xl text-gray-900 select-none">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 2C8 2 5 5.5 5 9c0 2.5 1.2 4.7 3 6.1V20a1 1 0 001 1h6a1 1 0 001-1v-4.9c1.8-1.4 3-3.6 3-6.1 0-3.5-3-7-7-7z" fill="currentColor" />
              </svg>
              Dreelio
            </a>
            <button
              onClick={() => setMenuOpen((o) => !o)}
              aria-label={menuOpen ? "Close menu" : "Open menu"}
              className="p-1"
            >
              {/* transisi hamburger ke silang */}
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#000000" strokeWidth="2.5">
                <line
                  x1="0.5" y1="6" x2="18.5" y2="6"
                  style={{
                    transformOrigin: "3px 6px",
                    transform: menuOpen ? "rotate(45deg) scaleX(1)" : "rotate(0deg)",
                    transition: "transform 120ms ",
                  }}
                />
                <line
                  x1="0.5" y1="15" x2="18.5" y2="15"
                  style={{
                    transformOrigin: "3px 15px",
                    transform: menuOpen ? "rotate(-45deg) scaleX(1)" : "rotate(0deg)",
                    transition: "transform 120ms ",
                  }}
                />
              </svg>
            </button>
          </div>
        </div>

        <div
          className={`mx-3 mt-2 bg-white/50 backdrop-blur-[6px] rounded-[45px] shadow-md overflow-hidden transition-all duration-300 ease-in-out ${menuOpen ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
            }`}
        >
          <ul className="py-2">
            {navLinks.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  onClick={() => setMenuOpen(false)}
                  className="block text-center py-3.5 text-gray-800 text-base font-medium mx-2 my-1 rounded-[45px] border border-transparent bg-transparent backdrop-blur-0 transition-all duration-200 hover:border-gray-400/30 hover:backdrop-opacity-40">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          <div className="px-4 pb-4 pt-1">
            <a
              href="#try"
              onClick={() => setMenuOpen(false)}
              className="block w-full text-center bg-gray-900 text-white font-semibold rounded-full overflow-hidden relative group h-13">
              <span className="flex flex-col transition-transform duration-300 ease-in-out group-hover:-translate-y-1/2">
                <span className="flex items-center justify-center h-13">Try Dreelio free</span>
                <span className="flex items-center justify-center h-13">Try Dreelio free</span>
              </span>
            </a>
          </div>
        </div>
      </nav>
    </>
  );
}