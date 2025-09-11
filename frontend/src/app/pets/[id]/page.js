import { mockPetProfiles } from "@/mock/mockData";
import Link from "next/link";

import PetProfile from "@/components/PetProfile";
import PetData from "@/components/PetData";
import EmptyStateTile from "@/components/EmptyStateTile";

export default function PetDetailPage({ params }) {
  const petId = parseInt(params.id, 10);
  const pet = mockPetProfiles.find((p) => p.id === petId);

  if (!pet) {
    return (
      <section className="min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12">
        <div className="max-w-screen-md mx-auto space-y-8">
          <EmptyStateTile message="Pet not found" emoji="🐾" />
        </div>
      </section>
    );
  }

  return (
    <section className="min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12">
      <div className="max-w-screen-md mx-auto space-y-8">
        <PetProfile pet={pet} />
        <PetData data={pet.data} />
        <div className="w-full">
          <Link href={`/pets/${pet.id}/medical`} className="block w-full">
            <div className="h-[220px] bg-[#f2e0e0] hover:bg-[#f9eaea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md hover:shadow-lg transition-colors duration-300 flex flex-col justify-between">
              <h4 className="text-xl font-semibold mb-2">🩺 Medical Records</h4>
              <p className="text-sm text-[#1B1A1F]/70">
                Weight logs, medications, vaccines & test results
              </p>
            </div>
          </Link>
        </div>
      </div>
    </section>
  );
}
