import Link from "next/link";
import FontStyle from "@/components/style/FontStyle";

export default function MedicalTile({ petId }) {
  return (
    <Link href={`/pets/${petId}/medical`} className="block w-full">
      <div className="h-[220px] bg-[#f2e0e0] hover:bg-[#f9eaea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md hover:shadow-lg transition-colors duration-300 flex flex-col justify-between">
        <FontStyle variant="tileTitle">Medical Records</FontStyle>
        <FontStyle variant="value">
          Weight logs, medications, vaccines & test results
        </FontStyle>
      </div>
    </Link>
  );
}