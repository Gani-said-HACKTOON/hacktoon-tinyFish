import TryButton from "@/components/tryButton";
import CustomButton from "@/components/customButton";
import AnimatedText from "@/components/landingPage/animatedText";

export default function Home() {
  return (
    <section className="flex justify-center mt-10 py-20 md:py-28 lg:py-35">
      <div className="max-w-6xl w-full px-6 flex flex-col items-center justify-center md:px-10 lg:px-12">

        <h1 className="text-4xl md:text-5xl lg:text-5xl font-bold text-center flex flex-wrap justify-center">
          <AnimatedText text="Run your business like a pro." delay={0.05} />
        </h1>

        <p className="mt-4 text-base md:text-lg lg:text-xl text-gray-700 font-semibold text-center max-w-2xl flex flex-wrap justify-center">
          <AnimatedText text="All-in-one platform to help businesses automatically comply with regulations by using AI to monitor, detect, and prevent policy violations." delay={0.05} />
        </p>

        <div
          className="w-full flex flex-col lg:flex-row justify-center items-center gap-2 mt-4
            opacity-0 animate-[fadeInBlur_0.6s_ease_0.7s_forwards]"
        >
          <TryButton className="w-full lg:w-45" />
          <CustomButton label="see features" className="w-full lg:w-45 bg-white/20 backdrop-blur-4xl hover:bg-white/30" />
        </div>

      </div>
    </section>
  );
}