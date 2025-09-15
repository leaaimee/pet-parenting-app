import Tile from "@/components/ui/Tile";

export default function PetCard({
  name,
  age,
  species,
  subspecies,
  image,
  href,           // optional
  tone = "lavender",
}) {
  const title = name ?? "Pet";
  return (
    <Tile href={href} tone={tone} variant="tall" className="p-0 overflow-hidden text-[#1B1A1F]">
      <div className="aspect-[4/3] bg-white/40">
        {image ? (
          <img src={image} alt={title} className="w-full h-full object-cover" loading="lazy" />
        ) : (
          <div className="w-full h-full grid place-items-center text-5xl opacity-70">🐾</div>
        )}
      </div>
      <div className="p-4 space-y-1">
        <h3 className="text-lg font-medium">{title}</h3>
        <div className="text-sm opacity-80 space-y-0.5">
          {species && <p>Species: {species}</p>}
          {subspecies && <p>Breed: {subspecies}</p>}
          {age && <p>Age: {age}</p>}
        </div>
      </div>
    </Tile>
  );
}
