"use client";

import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import Link from "next/link";
import { mockUserProfile } from "@/mock/mockData";
import { redirect } from "next/navigation";
import UserProfile from "@/components/features/UserProfile";

export default function UserProfilePage() {
  const profile = mockUserProfile;

  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)] pt-10">
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
            status="online"
          />
        }
        className="mb-4 max-w-screen-lg mx-auto px-6"
      />

      {/* MAIN CONTENT */}
      <UserProfile profile={profile} />
    </section>
  );
}
