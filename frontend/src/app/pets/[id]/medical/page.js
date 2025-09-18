import HeaderBar from "@/components/ui/nav/HeaderBar";
import AvatarButton from "@/components/ui/nav/AvatarButton";
import TitlePlain from "@/components/title/TitlePlain";
import FontStyle from "@/components/style/FontStyle";
import Link from "next/link";
import { authedFetch } from "@/lib/authedFetch";
import { mockPetProfiles } from "@/mock/mockData";

export default async function MedicalPage({ params }) {
  const meRes = await authedFetch("/api/v2/users/me");
  const me = await meRes.json();

  const petId = parseInt(params.id, 10);
  const pet = mockPetProfiles.find((p) => p.id === petId);

  if (!pet) {
    return (
      <section className="min-h-screen bg-[var(--bg)] text-[var(--text)] p-10">
        <FontStyle variant="sectionTitle">Pet not found</FontStyle>
      </section>
    );
  }

  return (
    <section className="min-h-screen bg-[var(--bg)] text-[var(--text)] pt-10">
      {/* Global header */}
      <HeaderBar
        left={
          <Link href="/homebase" aria-label="Home">
            <TitlePlain alignNudgeEm={-0.04} />
          </Link>
        }
        rightSlot={
          <AvatarButton
            name={me.name || me.username || me.email}
            src={me.avatar_url || me.image || me.picture}
            status="online"
          />
        }
        className="mb-4 max-w-screen-lg mx-auto px-6"
      />

      {/* Page content */}
      <div className="max-w-screen-lg mx-auto px-6 py-10 space-y-8">
        <header className="mb-6">
          <FontStyle variant="sectionTitle">Medical Profile</FontStyle>
          <p className="text-sm text-[var(--text)]/70 mt-2">
            Detailed health data and history for {pet.name}
          </p>
        </header>

        {/* Overview */}
        <div className="bg-[#f2eaff] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <FontStyle variant="tileTitle">Overview</FontStyle>
            <button className="text-sm px-3 py-1 rounded-md bg-[#1B1A1F]/10 hover:bg-[#1B1A1F]/20 transition">
              Edit
            </button>
          </div>
          <ul className="space-y-2">
            <li>
              <FontStyle variant="label">Blood Type</FontStyle>
              <FontStyle variant="value">{pet.medical?.blood_type || "—"}</FontStyle>
            </li>
            <li>
              <FontStyle variant="label">Weight</FontStyle>
              <FontStyle variant="value">{pet.medical?.weight || "—"}</FontStyle>
            </li>
            <li>
              <FontStyle variant="label">Chronic Conditions</FontStyle>
              <FontStyle variant="value">{pet.medical?.chronic_conditions || "—"}</FontStyle>
            </li>
            <li>
              <FontStyle variant="label">Notes</FontStyle>
              <FontStyle variant="value">{pet.medical?.notes || "—"}</FontStyle>
            </li>
          </ul>
        </div>

        {/* Vaccinations */}
        <div className="bg-[#fef6e4] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <FontStyle variant="tileTitle">Vaccination Records</FontStyle>
            <button className="text-sm px-3 py-1 rounded-md bg-[#1B1A1F]/10 hover:bg-[#1B1A1F]/20 transition">
              Edit
            </button>
          </div>
          <p className="text-sm text-gray-600 italic">No vaccinations recorded yet.</p>
        </div>

        {/* Medications */}
        <div className="bg-[#fffaf2] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <FontStyle variant="tileTitle">Medications</FontStyle>
            <button className="text-sm px-3 py-1 rounded-md bg-[#1B1A1F]/10 hover:bg-[#1B1A1F]/20 transition">
              Edit
            </button>
          </div>
          <p className="text-sm text-gray-600 italic">No medications recorded yet.</p>
        </div>

        {/* Test Results */}
        <div className="bg-[#f3eeea] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <FontStyle variant="tileTitle">Test Results</FontStyle>
            <button className="text-sm px-3 py-1 rounded-md bg-[#1B1A1F]/10 hover:bg-[#1B1A1F]/20 transition">
              Edit
            </button>
          </div>
          <p className="text-sm text-gray-600 italic">No test results recorded yet.</p>
        </div>

        {/* Vet Visits */}
        <div className="bg-[#e6f0f3] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <FontStyle variant="tileTitle">Vet Visits</FontStyle>
            <button className="text-sm px-3 py-1 rounded-md bg-[#1B1A1F]/10 hover:bg-[#1B1A1F]/20 transition">
              Edit
            </button>
          </div>
          <p className="text-sm text-gray-600 italic">No vet visits recorded yet.</p>
        </div>

        {/* Documents */}
        <div className="bg-[#ede7f6] text-[#1B1A1F] border border-white/10 rounded-[32px] p-8 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <FontStyle variant="tileTitle">Medical Documents</FontStyle>
            <button className="text-sm px-3 py-1 rounded-md bg-[#1B1A1F]/10 hover:bg-[#1B1A1F]/20 transition">
              Edit
            </button>
          </div>
          <p className="text-sm text-gray-600 italic">No documents uploaded yet.</p>
        </div>
      </div>
    </section>
  );
}
