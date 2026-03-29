import Image from "next/image";
import Link from "next/link";

export default function SignInPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-5">
        <Image src="/gslogo.png" alt="Logo" width={36} height={36} />
        <Link
          href="/signUp"
          className="text-white text-sm font-medium hover:opacity-80 transition-opacity"
        >
          Sign Up
        </Link>
      </nav>

      {/* Card */}
      <div className="flex flex-1 items-center justify-center px-4">
        <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm px-10 py-10 flex flex-col gap-6">
          <h1 className="text-2xl font-bold text-gray-900 text-center">Sign In</h1>

          <div className="flex flex-col gap-4">
            <input
              type="email"
              placeholder="Work Email Address"
              className="w-full rounded-lg bg-gray-100 px-4 py-3 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full rounded-lg bg-gray-100 px-4 py-3 text-sm text-gray-700 placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-300 transition"
            />
          </div>

          <button className="w-full bg-gray-800 hover:bg-gray-700 active:bg-gray-900 text-white font-semibold py-3 rounded-lg transition-colors text-sm">
            Sign In
          </button>

          <p className="text-center text-xs text-gray-400">
            Don&apos;t have an account?{" "}
            <Link href="/signUp" className="text-gray-700 font-medium hover:underline">
              Sign Up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}