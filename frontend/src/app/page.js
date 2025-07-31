import { redirect } from "next/navigation";

export default function Home() {
  const userIsLoggedIn = true; // 🔒 Replace with real logic when ready

  if (userIsLoggedIn) {
    redirect("/homebase");
  }

  return null; // or your login page in the future
}