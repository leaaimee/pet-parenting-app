import FontStyle from "@/components/style/FontStyle";

export default function PetData({ data }) {
  if (!data) return <p className="text-red-500">No pet data found.</p>;

  return (
    <section className="bg-[#f3eeea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md space-y-4">
      <FontStyle variant="tileTitle">Additional Info</FontStyle>

      <ul className="space-y-2">
        <li>
          <FontStyle variant="label">Favorite Things</FontStyle>
          <FontStyle variant="value">{data.favorite_things || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Dislikes</FontStyle>
          <FontStyle variant="value">{data.dislikes || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Social Style</FontStyle>
          <FontStyle variant="value">{data.social_style || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Communication</FontStyle>
          <FontStyle variant="value">{data.communication || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Preferred Treats</FontStyle>
          <FontStyle variant="value">{data.preferred_treats || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Diet</FontStyle>
          <FontStyle variant="value">{data.diet || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Allergies</FontStyle>
          <FontStyle variant="value">{data.allergies || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Medical Alerts</FontStyle>
          <FontStyle variant="value">{data.medical_alerts || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Behavior Notes</FontStyle>
          <FontStyle variant="value">{data.behavior_notes || "—"}</FontStyle>
        </li>
        <li>
          <FontStyle variant="label">Other</FontStyle>
          <FontStyle variant="value">{data.additional_info || "—"}</FontStyle>
        </li>
      </ul>
    </section>
  );
}
