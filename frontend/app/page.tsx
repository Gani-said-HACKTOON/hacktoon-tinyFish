"use client";

import { useRef } from "react";
import TryButton from "@/components/tryButton";
import AnimatedText from "@/components/landingPage/animatedText";
import Link from "next/link";
import Image from "next/image";
import gambar from '../public/ImageLandingpage.png';

export default function Home() {
  const cardRef = useRef(null);
  const imgWrapperRef = useRef(null);
const handleMove = (e) => {
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
    imgWrapperRef.current.style.transform = "perspective(600px) scale(1)";
  };

  return (
    <section className="flex justify-center mt-10 py-20 md:py-28 lg:py-35">
      <div className="max-w-6xl w-full px-6 flex flex-col items-center justify-center md:px-10 lg:px-12">

        <h1 className="text-4xl md:text-5xl lg:text-5xl font-bold text-center text-white">
          <AnimatedText text="Run your business like a pro." delay={0.05} />
        </h1>

        <p className="mt-4 text-base md:text-lg lg:text-xl font-semibold text-center max-w-2xl text-white">
          <AnimatedText text="All-in-one platform to help businesses automatically comply with regulations by using AI to monitor, detect, and prevent policy violations." delay={0.05} />
        </p>

        <div className="w-full flex flex-col items-center gap-2 mt-4 opacity-0 translate-y-2.5 animate-[fadeInBlur_0.6s_ease_0.7s_forwards]">
          <TryButton className="w-full lg:w-45" />
          <Link href="/" className="text-white underline font-bold">Sign In</Link>
        </div>

        <div
          ref={cardRef}
          onMouseMove={handleMove}
          onMouseLeave={reset}
          className="mt-[5%]"
        >
          <div
            ref={imgWrapperRef}
            className="transition-transform duration-100 rounded-xl overflow-hidden"
          >
            <Image
              src={gambar}
              alt="gambar1"
              draggable="false"
            />
          </div>
        </div>

      </div>
    </section>
  );
}