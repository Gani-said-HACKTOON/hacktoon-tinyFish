interface CustomButtonProps {
  label?: string;
  className?: string;
}

export default function CustomButton({ label = "try dreelio free", className = "" }: CustomButtonProps) {
  return (
    <div className="flex justify-center items-center w-full">
      <button
        className={`group relative inline-flex items-center justify-center
          px-8 py-3 h-13 rounded-[45px]
          overflow-hidden cursor-pointer ${className}`}
      >
        <div className="relative w-full h-[1.4em] overflow-hidden flex items-center justify-center">
          <span
            className="absolute inset-x-0 flex items-center justify-center
              text-[15px] font-medium tracking-wide text-gray-900
              transition-all duration-250 ease-[cubic-bezier(0.65,0,0.35,1)]
              translate-y-0 opacity-100
              group-hover:-translate-y-full group-hover:opacity-0"
          >
            {label}
          </span>
          <span
            className="absolute inset-x-0 flex items-center justify-center
              text-[15px] font-medium tracking-wide text-gray-900
              transition-all duration-250 ease-[cubic-bezier(0.65,0,0.35,1)]
              translate-y-full opacity-0
              group-hover:translate-y-0 group-hover:opacity-100"
          >
            {label}
          </span>
        </div>
      </button>
    </div>
  );
}