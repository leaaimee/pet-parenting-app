// components/PetProfile.js

function estimateAgeFromParts(year, month = 1) {
  const now = new Date();
  const birth = new Date(year, month - 1);
  const diffMs = now - birth;
  const ageYears = diffMs / (1000 * 60 * 60 * 24 * 365.25);
  return Math.round(ageYears * 10) / 10;
}

function getDisplayAge(pet) {
  if (pet.birthday) {
    const now = new Date();
    const birth = new Date(pet.birthday);
    let years = now.getFullYear() - birth.getFullYear();
    const m = now.getMonth() - birth.getMonth();
    const d = now.getDate() - birth.getDate();
    if (m < 0 || (m === 0 && d < 0)) years--;
    return `${years} years old`;
  }

  if (pet.birth_year) {
    const age = estimateAgeFromParts(pet.birth_year, pet.birth_month || 1);
    return `~${age} years old`;
  }

  return null;
}

export default function PetProfile({ pet }) {
  if (!pet) return <p className="text-red-500">No pet data provided.</p>;

  const ageText = getDisplayAge(pet);

  return (
    <section className="bg-[#e6dff1] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-lg space-y-4">
      <h2 className="text-2xl font-bold">{pet.name}</h2>

      <ul className="text-sm space-y-1">
        {pet.birthday ? (
          <li>
            <strong>Birthday:</strong> {pet.birthday}
            {ageText && ` (${ageText})`}
          </li>
        ) : pet.birth_year ? (
          <li>
            <strong>Estimated Birth:</strong>{" "}
            {pet.birth_month ? `${pet.birth_month}/` : ""}
            {pet.birth_year}
            {ageText && ` (${ageText})`}
          </li>
        ) : (
          <li><strong>Birth:</strong> Unknown</li>
        )}

        <li><strong>Species:</strong> {pet.species}</li>

        {pet.subspecies && (
          <li><strong>Breed:</strong> {pet.subspecies}</li>
        )}

        {pet.gender && (
          <li><strong>Gender:</strong> {pet.gender}</li>
        )}

        <li><strong>Created:</strong> {new Date(pet.created_at).toLocaleDateString()}</li>
      </ul>

      {pet.profile_description && (
        <p className="italic text-sm pt-2">{pet.profile_description}</p>
      )}
    </section>
  );
}
