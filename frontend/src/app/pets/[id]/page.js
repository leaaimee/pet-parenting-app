import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import { authedFetch } from "@/lib/authedFetch";
import Link from "next/link";

import { mockPetProfiles } from "@/mock/mockData";
import PetProfile from "@/components/features/PetProfile";
import PetData from "@/components/features/PetData";
import EmptyStateTile from "@/components/EmptyStateTile";
import MedicalTile from "@/components/features/MedicalTile";

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

        {/* Medical Records tile */}
        <MedicalTile petId={pet.id} />
      </div>
    </section>
  );
}
