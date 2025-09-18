"use client";
import { useLayoutEffect, useRef } from "react";
import { gsap } from "gsap";

export default function TitleAniSub() {
  const root = useRef(null);

  useLayoutEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = gsap.context(() => {
      gsap.set(".nest-glyph", {
        x: "100vw",
        rotate: 0,
        opacity: 0.9,
        scale: 0.96,
      });
      gsap.set(".nest-underline", {
        scaleX: 0,
        transformOrigin: "0% 50%",
      });

      const tl = gsap.timeline({ defaults: { ease: "power4.out" } });
      tl.to(".nest-glyph", {
        x: 0,
        rotate: 0,
        opacity: 1,
        scale: 1,
        duration: 1.4,
      }).to(".nest-underline", { scaleX: 1, duration: 0.45 }, "-=0.2");
    }, root);
    return () => ctx.revert();
  }, []);

  return (
    <div
      ref={root}
      className="inline-flex flex-col items-start text-left"
      style={{ fontSize: "clamp(48px, 8vw, 110px)", lineHeight: 1 }}
    >
      {/* row 1: logo + orb */}
<div className="flex items-baseline">
  <span className="tracking-tight uppercase leading-none">NEST</span>
  <span
  aria-hidden="true"
  className="nest-glyph ml-1 relative"   // <-- relative is key
  style={{
    display: "inline-block",
    position: "relative",                // <-- must have this
    top: "0.7em",                        // <-- now top works
    width: "0.23em",
    height: "0.23em",
    borderRadius: "9999px",
    background:
      "radial-gradient(120% 120% at 33% 28%, #F1E9FF 0%, #D8C8FF 32%, #B79BFF 68%, #8B6AE6 100%)",
    border: "1px solid rgba(255,255,255,0.22)",
    boxShadow: "0 4px 14px rgba(0,0,0,0.25)",
  }}
/>
</div>

{/* underline */}
<div
  className="nest-underline mt-1"
  style={{
    width: "2em",          // relative to outer font size
    height: "0.02em",        // relative
    background: "rgba(255,255,255,0.7)",
    marginLeft: "0.08em",
  }}
/>

{/* slogan */}
<span
  className="text-white/70 leading-none mt-2"
  style={{
    fontFamily: "var(--font-questrial)",
    fontSize: "0.14em",      // scales with outer fontSize
    display: "block",
    textIndent: "0.50em",
    marginLeft: "0.11em",
    textAlign: "left",
  }}
>
  pet parenting reimagined
</span>
    </div>
  );
}
