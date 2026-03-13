import Navbar from "@/components/navbar";

export default function Home() {
  return (
     <section className="flex justify-center mt-20 py-35">
      <div className="max-w-6xl w-full px-6 justify-center flex flex-col items-center">
        
        <div className="px-3 py-1.5 text-[12px] font-bold text-gray-600 bg-amber-50 rounded-[45px]">BLOG</div>
        <h1 className="text-6xl font-bold">
          Lorem ipsum dolor sit amet consectetur.
        </h1>

        <p className="mt-4 text-gray-700 font-semibold">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Nulla, voluptas dolor!
        </p>

      </div>
    </section>
  );
}
