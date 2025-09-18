"use client";

import FontStyle from "@/components/style/FontStyle";

export default function UserProfile({ profile }) {
  if (!profile) return <p className="text-red-500">No profile data found.</p>;

  return (
    <>
      {/* PAGE TITLE */}
      <header className="mb-6 max-w-screen-lg mx-auto px-6">
        <FontStyle variant="sectionTitle">Your Profile</FontStyle>
      </header>

      <div className="max-w-screen-lg mx-auto space-y-8">
        {/* ── row 1: profile + background ────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* profile header */}
          <div className="bg-[#cbe7eb] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
            <div className="flex flex-col sm:flex-row items-center gap-6">
              {/* image */}
              <div className="w-32 h-32 rounded-full overflow-hidden bg-[#262229]">
                {profile.avatar_url ? (
                  <img
                    src={profile.avatar_url}
                    alt={`${profile.name}'s avatar`}
                    className="w-full h-full object-cover"
                  />
                ) : null}
              </div>

              {/* main info */}
              <div className="space-y-2 text-center sm:text-left">
                <FontStyle variant="tileTitle">{profile.name}</FontStyle>
                <FontStyle variant="value">{profile.pronouns}</FontStyle>
                <FontStyle variant="value">{profile.birth_date}</FontStyle>
                <FontStyle variant="value">{profile.location}</FontStyle>
                <p className="italic text-sm text-gray-600">
                  {profile.profile_description}
                </p>
              </div>
            </div>
          </div>

          {/* background */}
          <div className="bg-[#e6dff1] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
            <FontStyle variant="tileTitle">Background</FontStyle>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <FontStyle variant="label">Languages</FontStyle>
                <FontStyle variant="value">{profile.languages_spoken}</FontStyle>
              </div>
              <div>
                <FontStyle variant="label">Experience</FontStyle>
                <FontStyle variant="value">{profile.experience_with}</FontStyle>
              </div>
              <div>
                <FontStyle variant="label">Certifications</FontStyle>
                <FontStyle variant="value">
                  {profile.certifications || "—"}
                </FontStyle>
              </div>
            </div>
          </div>
        </div>

        {/* ── row 2: uploads + (future slot) ────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* uploads */}
          <div className="bg-[#f2eaff] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
            <FontStyle variant="tileTitle">Uploads</FontStyle>
            {profile.certification_files ? (
              <p>{profile.certification_files}</p>
            ) : (
              <p className="text-sm text-gray-600 italic">
                No files uploaded yet
              </p>
            )}
          </div>

          {/* edit profile */}
          <div className="bg-[#e6f0f3] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md hover:shadow-lg transition-colors duration-300 cursor-pointer">
            <FontStyle variant="tileTitle">Edit Profile</FontStyle>
            <p className="text-sm text-gray-700">
              Update your personal details, background, and uploads.
            </p>
          </div>

          {/* future tile (settings, activity, etc.) */}
          <div className="hidden lg:block" />
        </div>
      </div>
    </>
  );
}
