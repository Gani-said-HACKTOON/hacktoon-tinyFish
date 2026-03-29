import Image from "next/image";
import Link from "next/link";

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-5">
        <Image src="/gslogo.png" alt="Logo" width={36} height={36} />
        <Link
          href="/signIn"
          className="text-white text-sm font-medium hover:opacity-80 transition-opacity"
        >
          Sign In
        </Link>
      </nav>

      {/* Card */}
      <div className="flex flex-1 items-center justify-center px-4">
        <div className="bg-white rounded-2xl shadow-xl w-full max-w-md px-10 py-10 flex flex-col gap-5">
          {/* Logo inside card */}
          <div className="flex justify-center">
            <Image src="/gslogo.png" alt="Logo" width={40} height={40} className="opacity-30" />
          </div>

          <h1 className="text-2xl font-bold text-gray-900 text-center -mt-1">Sign Up</h1>

          <div className="flex flex-col gap-4">
            {/* Full Name */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-1">Full Name</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="First Name"
                  className="w-1/2 rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
                />
                <input
                  type="text"
                  placeholder="Last Name"
                  className="w-1/2 rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
                />
              </div>
            </div>

            {/* Work Email */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-1">Work Email Address</label>
              <input
                type="email"
                placeholder="Work Email Address"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-1">Create Password</label>
              <input
                type="password"
                placeholder="Create Password"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
              />
            </div>

            {/* Company */}
            <div>
              <label className="block text-sm font-medium text-gray-800 mb-1">Company Name</label>
              <input
                type="text"
                placeholder="Company Name"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
              />
            </div>
          </div>

          <button className="w-full bg-gray-800 hover:bg-gray-700 active:bg-gray-900 text-white font-semibold py-3 rounded-lg transition-colors text-sm mt-1">
            Create Account
          </button>

          <p className="text-center text-xs text-gray-400">
            Already have an account?{" "}
            <Link href="/signIn" className="text-gray-700 font-medium hover:underline">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}