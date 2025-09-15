// Defaults used by both TitlePlain and TitleAni
export const TitlePreset = {
  titleSize: "clamp(120px, 14vw, 240px)",
  subtitle: "pet parenting reimagined",
  subtitleScale: 0.18,

  // underline + subtitle layout
  underlineWidth: "64%",
  underlineTop: -8,
  subtitleTop: -6,
  alignOffsetPx: 22,        // your left-edge fix

  // dot (scales with title via em)
  sizeEm: 0.285,
  gapEm: 0.34,
  dotOffsetEm: 0.02,
  tone: "lavender",
};

// Page-specific variants (override the base as needed)
export const TitlePresets = {
  HomebaseHero: {
    ...TitlePreset,
    subtitle: "pet parenting reimagined",
    // bigger feel if you want:
    // titleSize: "clamp(140px, 16vw, 280px)",
  },
  LoginCompact: {
    ...TitlePreset,
    titleSize: "clamp(80px, 10vw, 160px)",
    sizeEm: 0.26,
    gapEm: 0.32,
    underlineTop: -6,
    subtitleTop: -5,
  },
  SubpageSlim: {
    ...TitlePreset,
    // if you hide the dot on subpages:
    showGlyph: false,       // TitlePlain supports this
    underlineTop: -4,
    subtitleTop: -2,
    subtitleScale: 0.16,
  },
};

// Animation-only knobs (used by TitleAni)
export const TitleAniPreset = {
  from: "right",
  rollMode: "screen",
  distanceMult: 7,
};
