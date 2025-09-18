import TitleAni from "@/components/title/TitleAni";
export const metadata = { title: "Lab - preimplement"};

export default function Page() {
  return (
  <section className="min-h-[80svh] bg-[var(--bg)] text-[var(--text)] grid place-items-center">
    <TitleAni />
  </section>
  );
}

