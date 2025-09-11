

export default function PetData({ data }) {
  if (!data) return <p className="text-red-500">No pet data found.</p>;

  return (
    <section className="bg-[#f3eeea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md space-y-4">
      <h3 className="text-xl font-semibold mb-4">🐾 Additional Info</h3>

      <ul className="text-sm space-y-2">
        <li><strong>Favorite Things:</strong> {data.favorite_things || "—"}</li>
        <li><strong>Dislikes:</strong> {data.dislikes || "—"}</li>
        <li><strong>Social Style:</strong> {data.social_style || "—"}</li>
        <li><strong>Communication:</strong> {data.communication || "—"}</li>
        <li><strong>Preferred Treats:</strong> {data.preferred_treats || "—"}</li>
        <li><strong>Diet:</strong> {data.diet || "—"}</li>
        <li><strong>Allergies:</strong> {data.allergies || "—"}</li>
        <li><strong>Medical Alerts:</strong> {data.medical_alerts || "—"}</li>
        <li><strong>Behavior Notes:</strong> {data.behavior_notes || "—"}</li>
        <li><strong>Other:</strong> {data.additional_info || "—"}</li>
      </ul>
    </section>
  );
}
