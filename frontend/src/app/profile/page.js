"use client";

import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import { sizes } from "@/design/tokens";
import Link from "next/link";
import { mockUserProfile } from "@/mock/mockData";
import { redirect } from "next/navigation";
import Tile from "@/components/ui/Tile";
import AvatarMenu from "@/components/ui/nav/AvatarMenu";




export default function UserProfilePage() {
  const profile = mockUserProfile;

  return (
    <section className="min-h-screen bg-[#262229] text-[#F4F4F5]">
      {/* GLOBAL HEADER */}
      <HeaderBar
        left={
          <Link href="/homebase" aria-label="Home">
            <TitlePlain alignNudgeEm={-0.04} />
          </Link>
        }
        rightSlot={
          <AvatarButton
            name={profile.name}
            src={profile.avatar_url}
            sizeClamp={sizes.avatarClamp}
            shape="rounded"
            tone="graphite"
            status="online"
          />
        }
        className="mb-4 max-w-screen-lg mx-auto px-6"
      />


              {/* PAGE TITLE */}
      <header className="mb-4 max-w-screen-lg mx-auto px-6">
        <h1
          className="uppercase text-[var(--text)] mt-1"
          style={{ fontSize: "clamp(12px, 1.2vw, 30px)", letterSpacing: "0.22em" }}
        >
          Your Profile
        </h1>
      </header>




      <div className="max-w-screen-lg mx-auto space-y-8">
        {/* ── row 1: profile + background ────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* profile header */}
          <div className="bg-[#cbe7eb] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
            <div className="flex flex-col sm:flex-row items-center gap-6">
              {/* image placeholder */}
              <div className="w-32 h-32 bg-[#262229] rounded-full" />

              {/* main info */}
              <div className="space-y-2 text-center sm:text-left">
                <h1 className="text-3xl font-bold">{profile.name}</h1>
                <p className="text-sm text-gray-700">{profile.pronouns}</p>
                <p className="text-sm">{profile.birth_date}</p>
                <p className="text-sm">{profile.location}</p>
                <p className="italic text-sm text-gray-600">
                  {profile.profile_description}
                </p>
              </div>
            </div>
          </div>

          {/* background */}
          <div className="bg-[#e6dff1] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
            <h2 className="text-xl font-semibold mb-4">Background</h2>
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
                <h4 className="font-semibold mb-1">Certifications</h4>
                <p>{profile.certifications || "—"}</p>
              </div>
            </div>
          </div>
        </div>

        {/* ── row 2: uploads + (future slot) ────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* uploads */}
          <div className="bg-[#f2eaff] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
            <h2 className="text-xl font-semibold mb-4">Uploads</h2>
            {profile.certification_files ? (
              <p>{profile.certification_files}</p>
            ) : (
              <p className="text-sm text-gray-600 italic">
                No files uploaded yet
              </p>
            )}
          </div>

          {/* future tile (settings, activity, etc.) */}
          <div className="hidden lg:block" />
        </div>
      </div>

    </section>
  );
}
