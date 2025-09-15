"use client";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { gsap } from "gsap";
import TitlePlain from "./TitlePlain";

export default function TitleAni({
  from = "right",         // "left" | "right"
  rollMode = "screen",    // "distance" | "screen"
  distanceMult = 7,
  ...props                // pass through all TitlePlain props (sizes, offsets, tone, etc.)
}) {
  const root = useRef(null);
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const dir = from === "right" ? 1 : -1;
  // when rollMode === "distance", scale travel by sizeEm so it feels consistent
  const sizeEm = props.sizeEm ?? 0.285;
  const startX =
    rollMode === "screen" ? `${dir * 100}vw` : dir * sizeEm * 100 * distanceMult;
  const rollAngle = useMemo(() => dir * 540, [dir]);

  useLayoutEffect(() => {
    if (!mounted || !root.current) return;
    if (
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      return;
    }

    const ctx = gsap.context(() => {
      // preset (no first-frame pop)
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
    }, root);

    return () => ctx.revert();
  }, [mounted, startX, rollAngle, rollMode]);

  if (!mounted) return null;

  return (
    <div ref={root}>
      {/* Force the glyph on for the animated version */}
      <TitlePlain {...props} showGlyph />
    </div>
  );
}
