import { mockPetProfiles } from "@/mock/mockData";

export default function PetProfilePage({ params }) {
  const petId = parseInt(params.id);
  const pet = mockPetProfiles.find((p) => p.id === petId);

  if (!pet) {
    return <p className="p-6">Pet not found</p>;
  }

  return (
    <section className="min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12">
      <div className="max-w-screen-md mx-auto space-y-6 bg-[#e6dff1] hover:bg-[#f2eaff] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-lg transition-colors duration-300">
        <h1 className="text-3xl font-bold">{pet.name}</h1>
        <p className="text-lg">Species: <span className="font-medium">{pet.species}</span></p>
        <p className="text-lg">Breed: <span className="font-medium">{pet.subspecies}</span></p>
        <p className="text-lg">Birthday: <span className="font-medium">{pet.birthday}</span></p>
        <p className="italic text-sm text-[#555]">{pet.profile_description}</p>
      </div>
    </section>
  );
}
