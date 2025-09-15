"use client";
import React from "react";

export default function TitlePlain({
  // Typography
  titleSize = "clamp(120px, 14vw, 240px)",
  subtitle = "pet parenting reimagined",
  subtitleScale = 0.18,
  titleClass = "tracking-tight uppercase leading-none",

  // Underline / subtitle
  underlineWidth = "64%",
  underlineTop = -8,
  subtitleTop = -6,
  alignOffsetPx = 22, // your left-edge fix

  // Dot (glyph) — responsive (scales with title via EM)
  showGlyph = true,
  sizeEm = 0.285,     // 0.26–0.32 looks good
  gapEm = 0.34,       // space between NEST and dot
  dotOffsetEm = 0.02, // positive lifts a hair (dot vibe)

  // Theme
  tone = "lavender",
}) {
  const subtitleSize = `calc(${titleSize} * ${subtitleScale})`;

  const stylesByTone = {
    lavender: {
      bg: "radial-gradient(120% 120% at 30% 30%, rgba(255,255,255,0.28) 0%, rgba(222,211,243,0.85) 45%, rgba(112,92,148,0.75) 100%)",
      border: "1px solid rgba(255,255,255,0.14)",
    },
    graphite: {
      bg: "linear-gradient(145deg, rgba(255,255,255,0.10), rgba(0,0,0,0.25))",
      border: "1px solid rgba(255,255,255,0.10)",
    },
  };
  const toneStyle = stylesByTone[tone] ?? stylesByTone.lavender;

  return (
    <div className="inline-block">
      {/* Row 1 — baseline context that scales with title */}
      <div
        style={{
          fontSize: titleSize, // 1em == title size for children
          lineHeight: 1,
          whiteSpace: "nowrap",
        }}
      >
        {/* Title at 1em inside this context */}
        <span
          className={`nest-word ${titleClass}`}
          style={{
            display: "inline-block",
            fontSize: "1em",
            lineHeight: 1,
            verticalAlign: "baseline",
          }}
        >
          NEST
        </span>

        {/* Dot (optional), sized & spaced in em (scales with title) */}
        {showGlyph && (
          <span
            aria-hidden="true"
            className="nest-glyph rounded-full"
            style={{
              display: "inline-block",
              width: `${sizeEm}em`,
              height: `${sizeEm}em`,
              marginLeft: `${gapEm}em`,
              borderRadius: "9999px",
              background: toneStyle.bg,
              border: toneStyle.border,
              boxShadow:
                "0 1px 0 rgba(255,255,255,0.25) inset, 0 8px 24px rgba(0,0,0,0.35)",
              // positive = lift a touch relative to the baseline
              verticalAlign: `${dotOffsetEm}em`,
              willChange: "transform, opacity",
            }}
          />
        )}
      </div>

      {/* Row 2 — underline aligned to the title's left */}
      <div
        className="nest-underline h-[2px] bg-white/70"
        style={{
          width: underlineWidth,     // % of title width
          marginTop: underlineTop,   // allow negatives for tight stack
          marginLeft: alignOffsetPx, // side-bearing nudge
          justifySelf: "start",
        }}
      />

      {/* Row 3 — subtitle */}
      <span
        className="text-white/70 leading-none"
        style={{
          fontFamily: "var(--font-questrial)",
          fontSize: subtitleSize,
          marginTop: subtitleTop,
          marginLeft: alignOffsetPx, // match the underline's nudge
          justifySelf: "start",
        }}
      >
        {subtitle}
      </span>
    </div>
  );
}
