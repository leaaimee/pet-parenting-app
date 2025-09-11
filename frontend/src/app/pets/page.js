import Link from "next/link";
import { mockPetProfiles } from "@/mock/mockData";
import PetCard from "@/components/PetCard";

export default function PetsPage() {
  return (
    <section className="min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12">
      <div className="max-w-screen-lg mx-auto space-y-8">
        <h1 className="text-4xl font-bold">All Pets</h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {mockPetProfiles.map((pet) => (
            <Link key={pet.id} href={`/pets/${pet.id}`} className="block bg-[#f3eeea] text-[#1B1A1F] p-6 rounded-[32px] shadow hover:shadow-lg transition">
              <PetCard {...pet} />
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
