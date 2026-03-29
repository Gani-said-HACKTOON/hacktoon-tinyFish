"use client";

const features = [
  "Unlimited projects",
  "Unlimited clients",
  "Time tracking",
  "CRM",
  "iOS & Android app",
];

export default function Section_4() {
  return (
    <section
      id="pricing"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "80px 24px",
        gap: "48px",
      }}
    >
      {/* Title */}
      <h2
        style={{
          fontSize: "40px",
          fontWeight: 700,
          color: "white",
          textAlign: "center",
          margin: 0,
          textShadow: "0 1px 12px rgba(0,0,0,0.15)",
        }}
      >
        Pricing
      </h2>

      {/* Card */}
      <div
        style={{
          background: "linear-gradient(160deg, #6b8fa8 0%, #7aa0b8 30%, #8fb5c8 55%, #a8c4d0 75%, #b8cfd8 100%)",
          borderRadius: "24px",
          padding: "36px 40px",
          width: "100%",
          maxWidth: "320px",
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          boxShadow: "0 12px 48px rgba(80,110,140,0.35), inset 0 1px 0 rgba(255,255,255,0.3)",
          border: "1px solid rgba(255,255,255,0.3)",
        }}
      >
        {/* Card Header */}
        <div>
          <p
            style={{
              fontSize: "14px",
              color: "rgba(255,255,255,0.85)",
              margin: "0 0 6px 0",
              fontWeight: 500,
            }}
          >
            GaniSaid Basic
          </p>
          <h3
            style={{
              fontSize: "52px",
              fontWeight: 700,
              color: "white",
              margin: 0,
              lineHeight: 1.1,
            }}
          >
            Free
          </h3>
        </div>

        {/* Subtitle */}
        <p
          style={{
            fontSize: "14px",
            color: "rgba(255,255,255,0.8)",
            margin: 0,
            fontWeight: 400,
          }}
        >
          For solo use with light needs.
        </p>

        {/* Divider */}
        <div style={{ height: "1px", background: "rgba(255,255,255,0.25)" }} />

        {/* Feature List */}
        <ul
          style={{
            listStyle: "none",
            padding: 0,
            margin: 0,
            display: "flex",
            flexDirection: "column",
            gap: "12px",
          }}
        >
          {features.map((feature) => (
            <li
              key={feature}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                fontSize: "14px",
                color: "white",
              }}
            >
              <span
                style={{
                  width: "18px",
                  height: "18px",
                  borderRadius: "50%",
                  border: "1.5px solid rgba(255,255,255,0.6)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                  fontSize: "10px",
                  color: "white",
                }}
              >
                ✓
              </span>
              {feature}
            </li>
          ))}
        </ul>

        {/* Button */}
        <button
          style={{
            marginTop: "8px",
            width: "100%",
            padding: "13px 0",
            borderRadius: "50px",
            border: "none",
            background: "#1f2937",
            fontSize: "14px",
            fontWeight: 600,
            color: "white",
            cursor: "pointer",
          }}
        >
          Try GaniSaid free
        </button>
      </div>
    </section>
  );
}