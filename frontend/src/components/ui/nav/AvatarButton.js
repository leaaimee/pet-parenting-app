// src/components/ui/nav/AvatarButton.js
"use client";
import { getInitials } from "@/lib/getInitials";

export default function AvatarButton({
  name,
  src,
  onClick,
  sizeClamp = "clamp(56px, 7vw, 88px)",
  shape = "rounded",                // "circle" | "rounded" | "square"
  tone = "graphite",                 // "graphite" | "lavender" | "aqua" | "rose" | "sand"
  status = "online",                 // "online" | "away" | "busy" | "offline"
}) {
  const initials = getInitials(name);

  // shape radius
  const radius =
    shape === "circle"  ? "50%" :
    shape === "rounded" ? "var(--radius)" : "0px";

  // tones (background/foreground)
  const tones = {
    graphite: { bg: "rgba(255,255,255,0.10)", fg: "var(--text)", ring: "rgba(255,255,255,0.06)" },
    lavender:{ bg: "#DED3F3", fg: "#17161B", ring: "rgba(0,0,0,0.06)" },
    aqua:    { bg: "#C7EAF0", fg: "#17161B", ring: "rgba(0,0,0,0.06)" },
    rose:    { bg: "#F4DADA", fg: "#17161B", ring: "rgba(0,0,0,0.06)" },
    sand:    { bg: "#F1EAE2", fg: "#17161B", ring: "rgba(0,0,0,0.06)" },
  };
  const { bg, fg, ring } = tones[tone] ?? tones.graphite;

  // status colors
  const statusColors = {
    online:  "#22c55e",  // green-500
    away:    "#f59e0b",  // amber-500
    busy:    "#ef4444",  // red-500
    offline: "rgba(255,255,255,0.22)",
  };
  const sColor = statusColors[status] ?? statusColors.offline;

  // scale initials with size
  const fontSize = `calc(${sizeClamp} * 0.40)`;

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`Open profile menu (${status})`}
      title={name || "Profile"}
      style={{
        position: "relative",
        width: sizeClamp,
        height: sizeClamp,
        padding: 0,
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: radius,
        overflow: "hidden",
        boxSizing: "border-box",
        background: "#1d1921", // darker-plum vivid
        color: "#DED3F3", // light lavender
        // status border + subtle glow
        border: `3px solid ${sColor}`,
        boxShadow: `0 0 0 2px ${ring} inset, 0 10px 28px rgba(0,0,0,0.38)`,
        transition: "transform .15s ease, box-shadow .15s ease, filter .15s ease",
      }}
      className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)] hover:scale-[1.03]"
    >
      {src ? (
        <img src={src} alt="" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <span
          style={{
            fontFamily: "var(--font-questrial)",
            fontSize,
            fontWeight: 400,
            lineHeight: 1,
            letterSpacing: "-0.01em",
            textTransform: "uppercase",
            whiteSpace: "nowrap",
          }}
        >
          {initials}
        </span>
      )}

    </button>
  );
}
