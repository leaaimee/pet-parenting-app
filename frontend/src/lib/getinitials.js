// getInitials.js (keeps previous logic + stronger fallback)
export function getInitials(input = "") {
  const s = String(input).trim();
  if (!s) return "??";

  const base = s.includes("@") ? s.split("@")[0] : s;
  const cleaned = base
    .replace(/[._-]+/g, " ")
    .replace(/[^\p{L}\s]+/gu, " ");
  const parts = cleaned.split(/\s+/).filter(Boolean);

  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();

  const letters = parts[0]?.replace(/[^\p{L}]+/gu, "") ?? "";
  const two = (letters.slice(0, 2) || "??").toUpperCase();
  return two.length === 1 ? (two + letters.slice(1, 2).toUpperCase() || "??") : two;
}
