"use client"

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
        <h2 className="text-2xl font-bold">{name}</h2>
        {pronouns && <p className="text-gray-500">{pronouns}</p>}
        {location && <p className="text-gray-500">{location}</p>}
      </div>

      {profile_description && (
        <p className="text-gray-700 italic">{profile_description}</p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {languages_spoken && (
          <div>
            <h4 className="font-semibold text-gray-600">Languages</h4>
            <p>{languages_spoken}</p>
          </div>
        )}
        {experience_with && (
          <div>
            <h4 className="font-semibold text-gray-600">Experience</h4>
            <p>{experience_with}</p>
          </div>
        )}
      </div>

      <div className="pt-4">
        <button
          onClick={() => console.log("Edit Profile")}
          className="text-sm bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-md"
        >
          Edit Profile
        </button>
      </div>
    </div>
  );
}
