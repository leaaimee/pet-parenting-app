"use client";

import { mockUserProfile } from "@/mock/mockData";

export default function UserProfilePage() {
  const profile = mockUserProfile;

  return (
    <section className="min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12">
      <div className="max-w-screen-md mx-auto space-y-8 bg-[#cbe7eb] hover:bg-[#d6eff3] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-lg transition-colors duration-300">

        <h1 className="text-3xl font-bold">Profile of {profile.name}</h1>
        <p className="text-base">{profile.pronouns}</p>
        <p className="text-base">{profile.location}</p>
        <p className="italic text-sm text-[#555]">{profile.profile_description}</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold mb-1">Languages</h4>
            <p>{profile.languages_spoken}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-1">Experience</h4>
            <p>{profile.experience_with}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-1">Birthdate</h4>
            <p>{profile.birth_date}</p>
          </div>
        </div>

        <div>
          <button className="bg-[#262229] text-[#F4F4F5] hover:bg-[#1a1a1a] px-4 py-2 rounded-md text-sm transition">
            Edit Profile
          </button>
        </div>
      </div>
    </section>
  );
}
