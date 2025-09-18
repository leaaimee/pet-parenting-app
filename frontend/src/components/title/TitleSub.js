"use client";

export default function TitlePlain() {
  return (
    <div
      className="inline-block"
      style={{
        fontSize: "clamp(120px, 14vw, 240px)",
        lineHeight: 1,
        whiteSpace: "nowrap",
        "--align": "0.09em",            // or "0.09em"
        "--align-sub": "calc(var(--align) + 0.02em)", // small, scalable extra nudge
      }}
    >

      {/* title */}
      <span
        className="tracking-tight uppercase leading-none"
        style={{ fontSize: "1em", lineHeight: 1 }}
      >
        NEST
      </span>


      <span
          aria-hidden="true"
          className="nest-glyph"
          style={{
          display: "inline-block",
          width: "0.230em",
          height: "0.230em",
          marginLeft: "0.02em",
          verticalAlign: "0.0em",
          borderRadius: "9999px",
          background:
            "radial-gradient(120% 120% at 33% 28%, \
             #F1E9FF 0%,  /* highlight */ \
             #D8C8FF 32%, /* mid */ \
             #B79BFF 68%, /* lavender */ \
             #8B6AE6 100%  /* rim */)",
          border: "1px solid rgba(255,255,255,0.22)",
          boxShadow: "0 4px 14px rgba(0,0,0,0.25)",
        }}
      />



      {/* underline */}
      <div
        className="nest-underline"
        style={{
          width: "70%",
          height: "2px",
          background: "rgba(255,255,255,0.7)",
          marginTop: 6,
          marginLeft: "var(--align)",
        }}
      />

    {/* subtitle */}
      <span
        className="text-white/70 leading-none"
        style={{
          fontFamily: "var(--font-questrial)",
          fontSize: "calc(1em * 0.14)",
          marginTop: 10,
          display: "block",
          // add a tiny extra nudge to counter the overhang
          textIndent: "0.50em",   // try 0.015–0.03em
          marginLeft: "var(--align-sub)",
        }}
      >
        pet parenting reimagined
      </span>

      </div>

  );
}


