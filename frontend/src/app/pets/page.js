import { mockPetProfiles } from "@/mock/mockData";
import PetCard from "@/components/features/PetCard";

const tones = ["lavender", "aqua", "rose", "sand"];

export default function PetsPage() {
  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)] px-6 py-12">
      <div className="max-w-screen-lg mx-auto space-y-8">
        <h1 className="text-4xl font-bold">All Pets</h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {mockPetProfiles.map((pet, i) => (
            <PetCard
              key={pet.id}
              {...pet}
              href={`/pets/${pet.id}`}          // PetCard handles the link
              tone={tones[i % tones.length]}    // centralized tile colors
            />
          ))}
        </div>
      </div>
    </section>
  );
}
