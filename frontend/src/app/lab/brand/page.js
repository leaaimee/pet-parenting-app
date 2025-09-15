// src/app/lab/brand/page.js
import NestWordmark from "@/components/brand/NestWordmark";

export const metadata = { title: "NEST — Brand Lab" };

export default function Page() {
  return (
    <section className="min-h-[80svh] bg-[var(--bg)] text-[var(--text)] flex items-center justify-center">
<NestWordmark
  subtitle="pet parenting reimagined"
  sizeEm={0.285}
  gapEm={0.34}
  dotOffsetEm={0.018}
  underlineTop={-8}
  subtitleTop={-6}
  alignOffsetPx={22}
/>

    </section>
  );
}
