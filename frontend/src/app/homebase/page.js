import { redirect } from "next/navigation";
import { authedFetch } from "@/lib/authedFetch";
import Tile from "@/components/ui/Tile";
import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";


export default async function HomebasePage() {
  const meRes = await authedFetch("/api/v2/users/me");
  if (meRes.status === 401) redirect("/auth");
  const me = await meRes.json();

  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <div className="max-w-screen-lg mx-auto px-6 py-10 space-y-6">
        <HeaderBar
          title="HOMEBASE"
          subtitle="Caring & Sharing | all in one place"
          rightSlot={
          <AvatarButton
            name={me.name || me.username || me.email}
            src={me.avatar_url || me.image || me.picture}
            sizeClamp="clamp(56px, 7vw, 88px)"
            shape="rounded"       // or "circle"
            tone="graphite"       // or "lavender" to echo the hero tile
            status="online"       // away | busy | offline
          />
          }
        />

        {/* ROW 1 — hero (2/3 width on lg) */}
        <div>
          <Tile
            href="/family"
            tone="lavender"
            variant="hero"
            className="w-full lg:w-2/3 p-6 text-[#1B1A1F]"
          >
            <h2 className="text-xl font-semibold">Your Family</h2>
            {/*<p className="text-sm opacity-70">All members in one glance</p>*/}
          </Tile>
        </div>

        {/* ROW 2 — three tiles */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Tile href="/appointments" tone="aqua" className="min-h-[260px] p-6 flex flex-col text-[#1B1A1F]">
            <h3 className="text-lg font-medium">Appointments</h3>
            {/*<p className="text-sm opacity-70 mt-2">Next vet: Mon, 14:30</p>*/}
          </Tile>
          <Tile href="/medical" tone="rose" className="min-h-[260px] p-6 flex flex-col text-[#1B1A1F]">
            <h3 className="text-lg font-medium">Medical</h3>
            {/*<p className="text-sm opacity-70 mt-2">Weight: 4.3 kg</p>*/}
          </Tile>
          <Tile href="/marketplace" tone="sand" className="min-h-[260px] p-6 flex flex-col text-[#1B1A1F]">
            <h3 className="text-lg font-medium">Marketplace</h3>
            {/*<p className="text-sm opacity-70 mt-2">Food stock low</p>*/}
          </Tile>
        </div>
      </div>
    </section>
  );
}