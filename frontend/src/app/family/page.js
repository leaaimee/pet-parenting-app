import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import Link from "next/link";
import PetCard from "@/components/features/PetCard";
import UserCard from "@/components/features/UserCard";
import { mockUserProfile, mockPetProfiles } from "@/mock/mockData";
import { sizes } from "@/design/tokens";
import { Questrial } from "next/font/google";
import { authedFetch } from "@/lib/authedFetch";

const questrial = Questrial({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-questrial",
});


export default async function FamilyPage() {
  const meRes = await authedFetch("/api/v2/users/me");
  if (meRes.status === 401) redirect("/auth");   // same guard as Homebase
  const me = await meRes.json();

return (
  <section className="...">
    <HeaderBar
      left={
        <Link href="/homebase" aria-label="Home">
          <TitlePlain alignNudgeEm={-0.04} />
        </Link>
      }
      rightSlot={
        <AvatarButton
          name={me.name || me.username || me.email}
          src={me.avatar_url || me.image || me.picture}
          status="online"
        />
      }
      className="mb-4 max-w-screen-lg mx-auto px-6"
    />


      {/* MAIN CONTENT */}
        <div className="max-w-screen-lg mx-auto px-6 pt-4 pb-10">

        {/* PAGE TITLE */}
      <header className="mb-6 space-y-1">
        <h1
          className="uppercase text-[var(--text)] mt-1"
          style={{ fontSize: "clamp(12px, 1.2vw, 30px)", letterSpacing: "0.22em" }}
        >
          Your pet family
        </h1>
        <p className="text-[#F4F4F5] text-lg">
          All members. One screen. Click to view details.
        </p>
      </header>
        {/* USER CARD */}
        <section className="bg-[#cbe7eb] hover:bg-[#d6eff3] text-[#1B1A1F] border border-white/10 rounded-[32px] shadow-md hover:shadow-lg p-6 transition-colors duration-300 cursor-pointer">
          <Link href="/profile">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div className="w-28 h-28 bg-[#262229] rounded-full shrink-0" />
              <UserCard {...mockUserProfile} />
            </div>
          </Link>
        </section>

        {/* PET CARDS */}
        <section>
          <h3 className="text-2xl font-semibold text-[#F4F4F5] mb-4">Pet Family</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockPetProfiles.map((pet) => (
              <Link key={pet.id} href={`/pets/${pet.id}`}>
                <div className="bg-[#e6dff1] hover:bg-[#f2eaff] text-[#1B1A1F] border border-white/10 p-5 rounded-[32px] shadow-sm hover:shadow-md transition-colors duration-300">
                  <PetCard {...pet} />
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* ACTIONS */}
        <section>
          <h3 className="text-2xl font-semibold text-[#F4F4F5] mb-4">Actions</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            <div className="bg-[#cbe7eb] hover:bg-[#d6eff3] text-[#1B1A1F] border border-white/10 rounded-[32px] p-6 shadow-md hover:shadow-lg transition-colors duration-300 cursor-pointer">
              <h4 className="text-lg font-semibold mb-2">➕ Add New Pet</h4>
              <p className="text-sm">Start a profile for a new companion.</p>
            </div>
          </div>
        </section>
      </div>
    </section>
  );
}
