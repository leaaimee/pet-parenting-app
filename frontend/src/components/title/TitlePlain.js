// frontend/src/components/title/TitlePlain.js
"use client";
import { sizes } from "@/design/tokens";

export default function TitlePlain({ titleSize = sizes.headerTitle, alignNudgeEm = 0 }) {
  return (
    <div
      style={{
        fontSize: titleSize,
        lineHeight: 1,
        whiteSpace: "nowrap",
        textIndent: `${alignNudgeEm}em`,
      }}
    >
      <span
        className="tracking-tight uppercase leading-none"
        style={{ fontSize: "1em" }}
      >
        NEST
      </span>
      <span
        aria-hidden="true"
        className="nest-glyph"
        style={{
          display: "inline-block",
          width: "0.28em",
          height: "0.28em",
          marginLeft: "0.10em",
          verticalAlign: "0em",
          borderRadius: "9999px",
          background:
            "radial-gradient(120% 120% at 33% 28%, #F1E9FF 0%, #D8C8FF 32%, #B79BFF 68%, #8B6AE6 100%)",
          border: "1px solid rgba(255,255,255,0.18)",
        }}
      />
    </div>
  );
}
