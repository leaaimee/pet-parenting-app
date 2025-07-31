export default function PetCard({ name, age, species, subspecies, image }) {
  return (
    <div className="bg-white rounded-xl shadow p-6 space-y-4">
      <img
        src={image || "/default-pet.jpg"}
        alt={name}
        className="w-full h-48 object-cover rounded-lg"
      />

      <div>
        <h2 className="text-xl font-bold">{name}</h2>
        <p className="text-gray-600 text-sm">Species: {species || "?"}</p>
        {subspecies && (
          <p className="text-gray-600 text-sm">Breed: {subspecies}</p>
        )}
        <p className="text-gray-600 text-sm">Age: {age || "?"}</p>
      </div>
    </div>
  );
}
