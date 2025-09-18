import FontStyle from "@/components/style/FontStyle";

export default function UserCard({
  name,
  pronouns,
  location,
  profile_description,
  languages_spoken,
  experience_with,
}) {
  return (
    <div className="bg-transparent p-6">
      <div>
        <FontStyle variant="tileTitle">{name}</FontStyle>
        {pronouns && <FontStyle variant="value">{pronouns}</FontStyle>}
        {location && <FontStyle variant="value">{location}</FontStyle>}
      </div>

      {profile_description && (
        <p className="text-gray-700 italic">{profile_description}</p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {languages_spoken && (
          <div>
            <FontStyle variant="label">Languages</FontStyle>
            <FontStyle variant="value">{languages_spoken}</FontStyle>
          </div>
        )}
        {experience_with && (
          <div>
            <FontStyle variant="label">Experience</FontStyle>
            <FontStyle variant="value">{experience_with}</FontStyle>
          </div>
        )}
      </div>
    </div>
  );
}
