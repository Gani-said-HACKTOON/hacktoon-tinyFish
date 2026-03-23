import AnimatedText from "@/components/landingPage/animatedText";
import PreviewImage from "@/components/previewImage";
import FeatureSection from "@/components/feature";

export default function Home() {
  return (
    <main className="relative overflow-hidden">

      <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-175 h-175 
        bg-white/20 blur-[160px] rounded-full pointer-events-none" />

      <section
        className="
          relative flex justify-center
          pt-44 pb-0
          bg-linear-to-b from-[#8FAAC4] to-[#E2E2E2]
        "
      >
        <div className="max-w-5xl w-full px-6 flex flex-col items-center text-center">
          
          {/* TEXT */}
          <div className="flex flex-col items-center gap-3">
            <h1 className="text-[44px] md:text-[64px] font-semibold text-white leading-[1.05]">
              <AnimatedText text="Run your business like a pro." delay={0.035} />
            </h1>

            <p className="text-white/80 max-w-lg text-[15px]">
              <AnimatedText
                text="All-in-one platform to help businesses automatically comply with regulations using AI."
                delay={0.035}
              />
            </p>
          </div>

          {/* IMAGE (VERY CLOSE NOW) */}
          <div className="mt-6 relative z-20">
            <PreviewImage />
          </div>
        </div>
      </section>

      <div className="h-20 bg-linear-to-b from-[#E2E2E2] to-[#B1C3D4]" />

      <section
        className="
        relative flex justify-center py-24
        bg-linear-to-b from-[#B1C3D4] to-[#E2E2E2]
      "
      >
        <div className="max-w-6xl w-full px-6">
          <FeatureSection />
        </div>
      </section>

    </main>
  );
}