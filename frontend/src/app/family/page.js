// frontend/src/app/family/page.js
import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import Link from "next/link";
import PetCard from "@/components/features/PetCard";
import { mockUserProfile, mockPetProfiles } from "@/mock/mockData";
import { authedFetch } from "@/lib/authedFetch";
import Tile from "@/components/ui/Tile";
import { redirect } from "next/navigation";
import FontStyle from "@/components/style/FontStyle";

export default async function FamilyPage() {
  const meRes = await authedFetch("/api/v2/users/me");
  if (meRes.status === 401) redirect("/auth");
  const me = await meRes.json();

  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)] pt-10">
      {/* GLOBAL HEADER */}
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
          <FontStyle variant="sectionTitle">Your Pet Family</FontStyle>
        </header>

        {/* USER CARD */}
        <section className="bg-[#cbe7eb] text-[#1B1A1F] border border-white/10 rounded-[32px] shadow-md p-6 cursor-pointer">
          <Link href="/profile">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              {/* avatar */}
              <div className="w-28 h-28 rounded-full overflow-hidden bg-[#262229] shrink-0">
                {mockUserProfile.avatar_url ? (
                  <img
                    src={mockUserProfile.avatar_url}
                    alt={`${mockUserProfile.name}'s avatar`}
                    className="w-full h-full object-cover"
                  />
                ) : null}
              </div>

              {/* user info */}

              <div className="flex-1">
                <FontStyle variant="tileTitle">{mockUserProfile.name}</FontStyle>
                {mockUserProfile.pronouns && (
                  <FontStyle variant="value">{mockUserProfile.pronouns}</FontStyle>
                )}
                {mockUserProfile.location && (
                  <FontStyle variant="value">{mockUserProfile.location}</FontStyle>
                )}
                {mockUserProfile.languages_spoken && (
                  <FontStyle variant="value">{mockUserProfile.languages_spoken}</FontStyle>
                )}
              </div>

            </div>
          </Link>
        </section>

        {/* PET CARDS */}
        <section className="mt-10">
          <FontStyle variant="sectionTitle">Pet Family</FontStyle>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockPetProfiles.map((pet) => (
              <Link key={pet.id} href={`/pets/${pet.id}`}>
                <Tile className="p-6 text-[#1B1A1F] cursor-pointer">
                  <PetCard {...pet} />
                </Tile>
              </Link>
            ))}
          </div>
        </section>

        {/* ACTIONS */}
        <section className="mt-10">
          <FontStyle variant="sectionTitle">Actions</FontStyle>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            <div className="bg-[#cbe7eb] text-[#1B1A1F] border border-white/10 rounded-[32px] p-6 shadow-md cursor-pointer">
              <FontStyle variant="tileTitle">➕ Add New Pet</FontStyle>
              <p className="text-sm">Start a profile for a new companion.</p>
            </div>
          </div>
        </section>
      </div>
    </section>
  );
}
