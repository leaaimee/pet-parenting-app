// src/components/brand/NestWordmark.js
"use client";

import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { gsap } from "gsap";

export default function NestWordmark({
  // Typography
  titleSize = "clamp(120px, 14vw, 240px)",
  subtitle = "pet parenting reimagined",
  subtitleScale = 0.18,
  titleClass = "tracking-tight uppercase leading-none",

  // Underline / subtitle (these already behaved well for you)
  underlineWidth = "64%",
  underlineTop = -10,
  subtitleTop = -8,
  alignOffsetPx = 0, // keep 0 if left edge looks perfect

  // Ball (glyph) — responsive to title via EM units
  sizeEm = 0.28,      // ball diameter relative to title (try 0.26–0.32)
  gapEm = 0.35,       // space between NEST and ball (try 0.30–0.40)
  dotOffsetEm = 0,    // vertical fine-tune: positive = move UP, negative = down

  // Motion
  from = "right",
  rollMode = "screen",
  distanceMult = 7,
  tone = "lavender",
}) {
  const rootRef = useRef(null);
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const dir = from === "right" ? 1 : -1;
  const startX = rollMode === "screen" ? `${dir * 100}vw` : dir * (sizeEm * 100) * distanceMult; // rough; x anim is visual only
  const rollAngle = useMemo(() => dir * 540, [dir]);

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

  // GSAP entrance (glyph rolls, underline grows)
  useLayoutEffect(() => {
    if (!mounted || !rootRef.current) return;
    if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const ctx = gsap.context(() => {
      gsap.set(".nest-glyph", { x: startX, rotate: rollAngle, opacity: 0.9, scale: 0.96 });
      gsap.set(".nest-underline", { scaleX: 0, transformOrigin: "0% 50%" });

      const tl = gsap.timeline({ defaults: { ease: "power2.out" } });
      tl.to(".nest-glyph", {
        x: 0,
        rotate: 0,
        opacity: 1,
        scale: 1,
        duration: rollMode === "screen" ? 1.0 : 0.9,
        ease: "power3.out",
      });
      tl.to(".nest-underline", { scaleX: 1, duration: 0.45 }, "-=0.20");
    }, rootRef);

    return () => ctx.revert();
  }, [mounted, startX, rollAngle, rollMode]);

  if (!mounted) return null;

  return (
    <div ref={rootRef} className="inline-block">
      {/* ROW 1 — baseline context that scales with title */}
      <div
        style={{
          fontSize: titleSize,     // set the context to the title size
          whiteSpace: "nowrap",
          lineHeight: 1,           // tight line box for the row
          fontFamily: "inherit",
        }}
      >
        {/* Title at 1em inside this context */}
        <span
          className={`nest-word ${titleClass}`}
          style={{
            display: "inline-block",
            fontSize: "1em",
            lineHeight: 1,         // keeps letter bottoms as row baseline
            verticalAlign: "baseline",
          }}
        >
          NEST
        </span>

        {/* Ball sized in EMs, aligned to the same baseline */}
        <span
          aria-hidden="true"
          className="nest-glyph rounded-full"
          style={{
            display: "inline-block",
width: `${0.28}em`,
height: `${0.28}em`,
marginLeft: `${0.0}em`,
            borderRadius: "9999px",
            background: toneStyle.bg,
            border: toneStyle.border,
            boxShadow: "0 1px 0 rgba(255,255,255,0.25) inset, 0 8px 24px rgba(0,0,0,0.35)",
            // positive = lift (toward dot look), negative = lower
verticalAlign: `${0.00}em`,
            willChange: "transform, opacity",
          }}
        />
      </div>

      {/* ROW 2 — underline aligned to the left of the title */}
      <div
        className="nest-underline h-[2px] bg-white/70"
        style={{
          width: underlineWidth,
          marginTop: underlineTop,
          marginLeft: alignOffsetPx,
          justifySelf: "start",
        }}
      />

      {/* ROW 3 — subtitle */}
      <span
        className="text-white/70 leading-none"
        style={{
          fontFamily: "var(--font-questrial)",
          fontSize: subtitleSize,
          marginTop: subtitleTop,
          marginLeft: alignOffsetPx,
          justifySelf: "start",
        }}
      >
        {subtitle}
      </span>
    </div>
  );
}
