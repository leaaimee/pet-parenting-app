import FontStyle from "@/components/style/FontStyle";

export default function PetCard({ name, species, subspecies, avatar_url }) {
  const initials = name ? name.charAt(0).toUpperCase() : "🐾";

  return (
  <div className="flex flex-col items-center">
    <div className="w-28 h-28 rounded-full overflow-hidden bg-[#262229] flex items-center justify-center mb-6">
      {avatar_url ? (
        <img
          src={avatar_url}
          alt={`${name}'s avatar`}
          className="w-full h-full object-cover"
        />
      ) : (
        <span className="text-2xl font-semibold text-[#DED3F3]">{initials}</span>
      )}
    </div>

    <div className="w-full text-left space-y-1">
      <FontStyle variant="tileTitle">{name}</FontStyle>
      {species && (
        <FontStyle variant="value">
          {species}
          {subspecies ? ` – ${subspecies}` : ""}
        </FontStyle>
      )}
    </div>
  </div>
    );
}
