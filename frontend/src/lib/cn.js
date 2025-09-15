import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

// merges conditional classes safely
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
