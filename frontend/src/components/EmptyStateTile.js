export default function EmptyStateTile({ message = "Not found", emoji = "🚫" }) {
  return (
    <section className="bg-[#f3eeea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md text-center space-y-2">
      <div className="text-3xl">{emoji}</div>
      <h4 className="text-lg font-semibold">{message}</h4>
    </section>
  );
}
