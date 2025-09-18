import FontStyle from "@/components/style/FontStyle";

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
  const initials = pet.name ? pet.name.charAt(0).toUpperCase() : "🐾";

  return (
    <section className="bg-[#e6dff1] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-lg space-y-6">
      {/* avatar */}
      <div className="w-32 h-32 rounded-full overflow-hidden bg-[#262229] flex items-center justify-center mx-auto mb-6">
        {pet.avatar_url ? (
          <img
            src={pet.avatar_url}
            alt={`${pet.name}'s avatar`}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-2xl font-semibold text-[#DED3F3]">
            {initials}
          </span>
        )}
      </div>

      {/* name + details */}
      <div className="w-full text-left space-y-4">
        <FontStyle variant="tileTitle">{pet.name}</FontStyle>

        <ul className="space-y-2">
          {pet.birthday ? (
            <li>
              <FontStyle variant="label">Birthday</FontStyle>
              <FontStyle variant="value">
                {pet.birthday}
                {ageText && ` (${ageText})`}
              </FontStyle>
            </li>
          ) : pet.birth_year ? (
            <li>
              <FontStyle variant="label">Estimated Birth</FontStyle>
              <FontStyle variant="value">
                {pet.birth_month ? `${pet.birth_month}/` : ""}
                {pet.birth_year}
                {ageText && ` (${ageText})`}
              </FontStyle>
            </li>
          ) : (
            <li>
              <FontStyle variant="label">Birth</FontStyle>
              <FontStyle variant="value">Unknown</FontStyle>
            </li>
          )}

          <li>
            <FontStyle variant="label">Species</FontStyle>
            <FontStyle variant="value">{pet.species}</FontStyle>
          </li>

          {pet.subspecies && (
            <li>
              <FontStyle variant="label">Breed</FontStyle>
              <FontStyle variant="value">{pet.subspecies}</FontStyle>
            </li>
          )}

          {pet.gender && (
            <li>
              <FontStyle variant="label">Gender</FontStyle>
              <FontStyle variant="value">{pet.gender}</FontStyle>
            </li>
          )}

          <li>
            <FontStyle variant="label">Created</FontStyle>
            <FontStyle variant="value">
              {new Date(pet.created_at).toLocaleDateString()}
            </FontStyle>
          </li>
        </ul>

        {pet.profile_description && (
          <p className="italic text-sm pt-2">{pet.profile_description}</p>
        )}
      </div>
    </section>
  );
}