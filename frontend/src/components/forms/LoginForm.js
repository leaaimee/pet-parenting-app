"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const router = useRouter();

  async function handleLogin(e) {
    e.preventDefault();
    setErr("");

    // Call our Next BFF route → it sets an httpOnly cookie if creds are valid
    const r = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: email, password }),
    });

    if (r.ok) {
      router.push("/homebase"); // or "/family"
    } else {
      const d = await r.json().catch(() => ({}));
      setErr(d?.error || "Login failed. Check your credentials.");
    }
  }

  return (
    <form onSubmit={handleLogin} className="space-y-5 text-inherit">
      <div>
        <label htmlFor="email" className="block text-sm mb-1">Email</label>
      <input
        id="email"
        className="w-full px-4 py-3 rounded-[var(--radius-input)] bg-white text-[#1B1A1F]
                   placeholder:text-black/50 border border-black/10
                   focus:outline-none focus:ring-2 focus:ring-[var(--ring)] focus:border-transparent shadow-sm"
        type="email"
        placeholder="you@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm mb-1">Password</label>
        <input
          id="password"
          className="w-full px-4 py-3 rounded-[var(--radius-input)] bg-white text-[#1B1A1F]
                     placeholder:text-black/50 border border-black/10
                     focus:outline-none focus:ring-2 focus:ring-[var(--ring)] focus:border-transparent shadow-sm"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>

      {err && <p className="text-red-600 text-sm">{err}</p>}

      <button
        type="submit"
        className="w-full bg-[#A3E635] text-[#1f1b19] font-bold py-2 rounded-xl hover:bg-[#B2F554] transition duration-150"
      >
        Enter
      </button>
    </form>
  );
}
