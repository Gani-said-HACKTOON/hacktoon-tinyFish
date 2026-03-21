interface AnimatedTextProps {
  text: string;
  delay?: number;
  className?: string;
}

export default function AnimatedText({ text, delay = 0, className = "" }: AnimatedTextProps) {
  const words = text.split(" ");

  return (
    <span className={className} style={{ display: "inline" }}>
      {words.map((word, i) => (
        <span
          key={i}
          style={{
            display: "inline-block",
            overflow: "hidden",
            padding: "100em 0.8em 0.8em 0.8em",
            margin: "-100em -0.8em -0.8em -0.8em",
          }}
        >
          <span
            style={{
              display: "inline-block",
              opacity: 0,
              transform: "translateY(20px)",
              filter: "blur(8px)",
              animation: `wordReveal 0.5s cubic-bezier(0.22, 1, 0.36, 1) forwards`,
              animationDelay: `${delay + i * 0.06}s`,
            }}
          >
            {word}{i < words.length - 1 ? "\u00A0" : ""}
          </span>
        </span>
      ))}
    </span>
  );
}