"use client";

import Link from "next/link";

interface TryButtonProps {
  className?: string;
  href?: string;
}

export default function TryButton({
  className = "",
  href = "/chatbot",
}: TryButtonProps) {
  return (
    <div className="flex justify-center items-center w-full lg:w-auto">
      <Link href={href} className="w-full lg:w-auto">
        <button
          className={`group relative inline-flex items-center justify-center
          px-2 py-3 h-14 rounded-[45px]
          overflow-hidden cursor-pointer bg-white ${className} duration-250 ease-out w-full`}
        >
          <div className="relative w-full h-[1.4em] overflow-hidden flex items-center justify-center">
            <span
              className="absolute inset-x-0 flex items-center justify-center
              text-[16px] font-bold tracking-wide text-black bg-white
              transition-all duration-200 ease-[cubic-bezier(0.65,0,0.35,1)]
              translate-y-0 opacity-100
              group-hover:-translate-y-full group-hover:opacity-0"
            >
              Try Dreelio free
            </span>

            <span
              className="absolute inset-x-0 flex items-center justify-center
              text-[16px] font-bold tracking-wide text-black
              transition-all duration-200 ease-[cubic-bezier(0.65,0,0.35,1)]
              translate-y-full opacity-0
              group-hover:translate-y-0 group-hover:opacity-100"
            >
              Try Dreelio free
            </span>
          </div>
        </button>
      </Link>
    </div>
  );
}