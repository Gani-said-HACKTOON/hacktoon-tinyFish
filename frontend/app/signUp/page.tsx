import Image from "next/image";
import Link from "next/link";

export default function SignUpPage() {
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
        <Link href="/signIn" style={{
          color: "white",
          fontSize: "14px",
          fontWeight: 500,
          textDecoration: "none",
        }}>
          Sign In
        </Link>
      </nav>

      {/* Card */}
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: "0 16px" }}>
        <div style={{
          background: "white",
          borderRadius: "24px",
          boxShadow: "0 8px 40px rgba(0,0,0,0.10)",
          width: "100%",
          maxWidth: "500px",
          padding: "48px 56px",
          display: "flex",
          flexDirection: "column",
        }}>

          {/* Logo */}

          <h1 style={{ fontSize: "26px", fontWeight: 700, color: "#111827", textAlign: "center", marginTop: 0, marginBottom: "32px" }}>
            Sign Up
          </h1>

          {/* Full Name */}
          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", fontSize: "13px", fontWeight: 600, color: "#111827", marginBottom: "10px" }}>
              Full Name
            </label>
            <div style={{ display: "flex", gap: "12px" }}>
              <input
                type="text"
                placeholder="First Name"
                style={{
                  width: "50%",
                  border: "1px solid #e5e7eb",
                  borderRadius: "8px",
                  padding: "10px 14px",
                  fontSize: "13px",
                  color: "#374151",
                  background: "transparent",
                  outline: "none",
                  boxSizing: "border-box",
                }}
              />
              <input
                type="text"
                placeholder="Last Name"
                style={{
                  width: "50%",
                  border: "1px solid #e5e7eb",
                  borderRadius: "8px",
                  padding: "10px 14px",
                  fontSize: "13px",
                  color: "#374151",
                  background: "transparent",
                  outline: "none",
                  boxSizing: "border-box",
                }}
              />
            </div>
          </div>

          {/* Work Email */}
          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", fontSize: "13px", fontWeight: 600, color: "#111827", marginBottom: "10px" }}>
              Work Email Address
            </label>
            <input
              type="email"
              placeholder="Work Email Address"
              style={{
                width: "100%",
                border: "none",
                borderBottom: "1px solid #d1d5db",
                paddingBottom: "10px",
                fontSize: "13px",
                color: "#374151",
                background: "transparent",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", fontSize: "13px", fontWeight: 600, color: "#111827", marginBottom: "10px" }}>
              Create Password
            </label>
            <input
              type="password"
              placeholder="Create Password"
              style={{
                width: "100%",
                border: "none",
                borderBottom: "1px solid #d1d5db",
                paddingBottom: "10px",
                fontSize: "13px",
                color: "#374151",
                background: "transparent",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Company */}
          <div style={{ marginBottom: "36px" }}>
            <label style={{ display: "block", fontSize: "13px", fontWeight: 600, color: "#111827", marginBottom: "10px" }}>
              Company Name
            </label>
            <input
              type="text"
              placeholder="Company Name"
              style={{
                width: "100%",
                border: "none",
                borderBottom: "1px solid #d1d5db",
                paddingBottom: "10px",
                fontSize: "13px",
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
            Create Account
          </button>

          {/* Footer */}
          <p style={{ textAlign: "center", fontSize: "13px", color: "#9ca3af", margin: 0 }}>
            Already have an account?{" "}
            <Link href="/signIn" style={{ color: "#111827", fontWeight: 700, textDecoration: "none" }}>
              Sign In
            </Link>
          </p>

        </div>
      </div>
    </div>
  );
}