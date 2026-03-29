import Image from "next/image";
import Link from "next/link";

export default function SignInPage() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>

      {/* Navbar */}
      <nav style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "20px 32px",
      }}>
        <Image src="/gslogo.png" alt="Logo" width={36} height={36} />
        <Link href="/signUp" style={{
          color: "white",
          fontSize: "14px",
          fontWeight: 500,
          textDecoration: "none",
        }}>
          Sign Up
        </Link>
      </nav>

      {/* Card */}
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: "0 16px" }}>
        <div style={{
          background: "white",
          borderRadius: "24px",
          boxShadow: "0 8px 40px rgba(0,0,0,0.10)",
          width: "100%",
          maxWidth: "440px",
          padding: "56px 56px 48px 56px",
          display: "flex",
          flexDirection: "column",
        }}>

          <h1 style={{ fontSize: "26px", fontWeight: 700, color: "#111827", textAlign: "center", marginTop: 0, marginBottom: "36px" }}>
            Sign In
          </h1>

          {/* Email */}
          <div style={{ marginBottom: "28px" }}>
            <input
              type="email"
              placeholder="jane@ganisaid.com"
              style={{
                width: "100%",
                border: "none",
                borderBottom: "1px solid #d1d5db",
                paddingBottom: "10px",
                fontSize: "14px",
                color: "#374151",
                background: "transparent",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom: "36px" }}>
            <input
              type="password"
              placeholder="Password"
              style={{
                width: "100%",
                border: "none",
                borderBottom: "1px solid #d1d5db",
                paddingBottom: "10px",
                fontSize: "14px",
                color: "#374151",
                background: "transparent",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Button */}
          <button style={{
            width: "100%",
            background: "#1f2937",
            color: "white",
            fontWeight: 600,
            fontSize: "14px",
            padding: "14px 0",
            borderRadius: "12px",
            border: "none",
            cursor: "pointer",
            marginBottom: "24px",
          }}>
            Sign In
          </button>

          {/* Footer */}
          <p style={{ textAlign: "center", fontSize: "13px", color: "#9ca3af", margin: 0 }}>
            Don&apos;t have an account?{" "}
            <Link href="/signUp" style={{ color: "#111827", fontWeight: 700, textDecoration: "none" }}>
              Sign Up
            </Link>
          </p>

        </div>
      </div>
    </div>
  );
}