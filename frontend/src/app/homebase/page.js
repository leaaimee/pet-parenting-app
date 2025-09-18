// frontend/src/app/homebase/page.js

// ── imports ───────────────────────────────────────────────────────────────────
import Link from "next/link";
import { redirect } from "next/navigation";
import TitlePlain from "@/components/title/TitlePlain";
import { authedFetch } from "@/lib/authedFetch";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import HeaderBar from "@/components/ui/nav/HeaderBar";
import Tile from "@/components/ui/Tile";
import { sizes } from "@/design/tokens";
import AvatarMenu from "@/components/ui/nav/AvatarMenu";

// (optional) page metadata
export const metadata = { title: "HOMEBASE — NEST" };

// ── page ──────────────────────────────────────────────────────────────────────
export default async function HomebasePage() {
  // auth guard
  const meRes = await authedFetch("/api/v2/users/me");
  if (meRes.status === 401) redirect("/auth");
  const me = await meRes.json();

  // shared size token for header title + avatar
  const headerTitleSize = sizes.headerTitle || "clamp(28px,4vw,40px)";

  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <div className="max-w-screen-lg mx-auto px-6 py-10 space-y-6">
        {/* ── header: brand left, avatar right ─────────────────────────────── */}
<HeaderBar
  left={<TitlePlain />}
  rightSlot={
    <AvatarButton
      name={me.name || me.username || me.email}
      src={me.avatar_url || me.image || me.picture}
      status="online"
    />
  }
/>

<h1
  className="uppercase text-[var(--text)] mt-1"
  style={{ fontSize: "clamp(12px, 1.2vw, 30px)", letterSpacing: "0.22em" }}
>
  HOMEBASE
</h1>

        {/* ── row 1: hero tile ────────────────────────────────────────────── */}
        <div>
          <Tile
            href="/family"
            tone="lavender"
            variant="hero"
            className="w-full lg:w-2/3 p-6 text-[#1B1A1F]"
          >
            <h2 className="text-xl font-semibold">Your Family</h2>
          </Tile>
        </div>

        {/* ── row 2: three tiles ──────────────────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Tile href="/appointments" tone="aqua" className="min-h-[260px] p-6 flex flex-col text-[#1B1A1F]">
            <h3 className="text-lg font-medium">Appointments</h3>
          </Tile>
          <Tile href="/medical" tone="rose" className="min-h-[260px] p-6 flex flex-col text-[#1B1A1F]">
            <h3 className="text-lg font-medium">Medical</h3>
          </Tile>
          <Tile href="/marketplace" tone="sand" className="min-h-[260px] p-6 flex flex-col text-[#1B1A1F]">
            <h3 className="text-lg font-medium">Marketplace</h3>
          </Tile>
        </div>
      </div>
    </section>
  );
}
