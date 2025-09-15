// app/lab/motion/MotionLabClient.js
"use client";

import { useEffect } from "react";
import { gsap } from "gsap";
import SplitType from "split-type";

export default function MotionLab() {
  useEffect(() => {
    if (typeof window !== "undefined" &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return;
    }

    // Split title into characters
    const split = new SplitType(".lab-title", { types: "chars" });

    // Find the first 'E' (case-insensitive)
    const eChar = split.chars.find(el => (el.textContent || "").toUpperCase() === "E");

    const tl = gsap.timeline({ defaults: { ease: "power2.out" } });

    // Start with a slightly loose tracking, then tighten during the stagger
    // (animation target: the H1 itself)
    tl.set(".lab-title", { letterSpacing: "0.06em" });

    // Stagger all letters in with a subtle forward tilt (X) so depth reads
    tl.fromTo(
      split.chars,
      { y: 32, opacity: 0, rotateX: -35, transformPerspective: 800 },
      { y: 0,  opacity: 1, rotateX: 0, duration: 0.55, stagger: 0.045 }
    );

    // Tighten tracking to final
    tl.to(".lab-title", { letterSpacing: "-0.01em", duration: 0.45 }, "-=0.38");

    // Give the E a distinct, visible “seat” move (brief, with depth cues)
    if (eChar) {
      tl.fromTo(
        eChar,
        { rotateX: -70, z: -12, filter: "brightness(0.9) blur(0.4px)" },
        { rotateX: 0,   z: 0,   filter: "brightness(1)   blur(0px)", duration: 0.38 },
        "-=0.30" // overlaps near the end so it feels like one gesture
      );
    }

    // Underline after title lands
    tl.fromTo(
      ".lab-underline",
      { scaleX: 0 },
      { scaleX: 1, duration: 0.4, transformOrigin: "0% 50%" },
      "-=0.10"
    );

    // Subtitle fade + rise
    tl.fromTo(
      ".lab-subtitle",
      { opacity: 0, y: 10 },
      { opacity: 1, y: 0, duration: 0.45 }
    );

    return () => split.revert();
  }, []);

  return (
    <section className="min-h-[80svh] bg-[var(--bg)] text-[var(--text)] flex items-center justify-center">
      <div className="space-y-4 text-center">
        <h1
          className="lab-title text-[48px] lg:text-7xl uppercase tracking-tight"
          style={{ perspective: "900px" }}  // 3D stage so rotateX has depth
        >
          HOMEBASE
        </h1>

        <div
          className="lab-underline mx-auto h-[2px] bg-white/70"
          style={{ transform: "scaleX(0)", width: "60%" }}
        />

        <p className="lab-subtitle text-sm text-white/70">
          SplitType + GSAP — visible but restrained
        </p>
      </div>
    </section>
  );
}
