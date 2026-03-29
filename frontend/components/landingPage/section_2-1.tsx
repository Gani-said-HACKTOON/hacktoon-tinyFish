"use client";

import { useRef } from "react";
import Image from "next/image";
import gambar from "@/public/ImageLandingpage.png";

export default function Section_2() {
  const cardRef = useRef<HTMLDivElement | null>(null);
  const imgWrapperRef = useRef<HTMLDivElement | null>(null);

  const handleMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current || !imgWrapperRef.current) return;

    const rect = cardRef.current.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = -(y - centerY) / 80;
    const rotateY = (x - centerX) / 80;

    imgWrapperRef.current.style.transform = `
      perspective(800px)
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
      scale(0.96)
    `;
  };

  const reset = () => {
    if (!imgWrapperRef.current) return;
    imgWrapperRef.current.style.transform = "perspective(600px) scale(1)";
  };

  return (
    <div
      id="features"
      ref={cardRef}
      onMouseMove={handleMove}
      onMouseLeave={reset}
      style={{
        marginTop: "5%",
        scrollMarginTop: "80px",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        ref={imgWrapperRef}
        style={{
          transition: "transform 100ms",
          borderRadius: "12px",
          overflow: "hidden",
        }}
      >
        <Image
          src={gambar}
          alt="gambar1"
          draggable="false"
        />
      </div>
    </div>
  );
}