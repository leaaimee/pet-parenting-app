import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import { authedFetch } from "@/lib/authedFetch";
import Link from "next/link";

import { mockPetProfiles } from "@/mock/mockData";
import PetProfile from "@/components/features/PetProfile";
import PetData from "@/components/features/PetData";
import EmptyStateTile from "@/components/EmptyStateTile";

export default async function PetDetailPage({ params }) {
  const meRes = await authedFetch("/api/v2/users/me");
  const me = await meRes.json();

  const petId = parseInt(params.id, 10);
  const pet = mockPetProfiles.find((p) => p.id === petId);

  if (!pet) {
    return (
      <section className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
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
        <div className="max-w-screen-lg mx-auto px-6 py-10">
          <EmptyStateTile message="Pet not found" emoji="🐾" />
        </div>
      </section>
    );
  }

  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
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

      <div className="max-w-screen-lg mx-auto px-6 py-10 space-y-8">
        <PetProfile pet={pet} />
        <PetData data={pet.data} />

        <Link href={`/pets/${pet.id}/medical`} className="block w-full">
          <div className="h-[220px] bg-[#f2e0e0] hover:bg-[#f9eaea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md hover:shadow-lg transition-colors duration-300 flex flex-col justify-between">
            <h4 className="text-xl font-semibold mb-2">🩺 Medical Records</h4>
            <p className="text-sm text-[#1B1A1F]/70">
              Weight logs, medications, vaccines & test results
            </p>
          </div>
        </Link>
      </div>
    </section>
  );
}
