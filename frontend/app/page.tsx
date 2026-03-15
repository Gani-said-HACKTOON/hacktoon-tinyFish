import Navbar from "@/components/navbar";
import TryButton from "@/components/tryButton";
import CustomButton from "@/components/customButton";
import { features } from "process";



export default function Home() {
  return (
     <section className="flex justify-center mt-10 py-20 md:py-28 lg:py-35">
      <div className="max-w-6xl w-full px-6 flex flex-col items-center justify-center md:px-10 lg:px-12">
        
        <h1 className="text-4xl md:text-5xl lg:text-5xl font-bold flex justify-center text-center ">
          Run your business like a pro.
        </h1>

        <p className="mt-4 text-base md:text-lg lg:text-xl text-gray-700 font-semibold flex justify-center text-center max-w-2xl">
          All-in-one platform to help businesses automatically comply with regulations by using AI to monitor, detect, and prevent policy violations.
        </p>

        <TryButton className="w-full lg:min-w-50 mt-4"/>

        <CustomButton label="see features" className="w-full lg:w-50 bg-white/20 backdrop-blur-4xl hover:bg-white/30 mt-40" />

        <div className="image mt-10 md:mt-14 lg:mt-16">
          
        </div>
        <p className= "text-gray-600 text-center">Trusted by 7,000+ top startups, freelancers and studios</p>
        <div className="marquee mt-6 w-full">
          <span>contact us for partnership  • contact us for partnership • contact us for partnership</span>
        </div>
      </div>
    </section>
  );
}
