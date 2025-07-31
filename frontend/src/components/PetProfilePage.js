"use client";
import { useEffect, useState } from "react";

// Drop this inside your component file, or in a separate `PetAge.jsx` component
function PetAge({ birthDate }) {
  const [age, setAge] = useState(null);

  useEffect(() => {
    const years =
      new Date().getFullYear() - new Date(birthDate).getFullYear();
    setAge(years);
  }, [birthDate]);

  return <span>{age !== null ? `${age} years old` : "Loading..."}</span>;
}


export default function PetProfilePage({ /* props or data */ }) {
  const pet = mockPetProfiles[0]; // ← temp until real API

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">{pet.name}</h1>
      <p>Species: {pet.species}</p>
      <p>Breed: {pet.subspecies}</p>
      <p>Age: <PetAge birthDate={pet.birthday} /></p>
    </div>
  );
}
