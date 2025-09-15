import Link from "next/link";
import PetCard from "@/components/features/PetCard";
import UserCard from "@/components/features/UserCard";
import { mockUserProfile, mockPetProfiles } from "@/mock/mockData";
import { Questrial } from "next/font/google";

const questrial = Questrial({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-questrial",
});

export default function FamilyPage() {
  return (
    <section className={`min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12 ${questrial.variable}`}>
      <div className="max-w-screen-lg mx-auto space-y-12">

        {/* PAGE TITLE */}
        <header className="space-y-2">
          <h2 className="text-4xl font-[var(--font-questrial)] tracking-tight uppercase">
            🐾 Your Pet Family
          </h2>
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
