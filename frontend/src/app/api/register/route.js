import { NextResponse } from "next/server";
const BASE = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function POST(req) {
  const payload = await req.json(); // { email, password, ... }

  // Try canonical path first
  let r = await fetch(BASE + "/api/v2/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  // If that doesn't exist yet (404), fall back to your current root route
  if (r.status === 404) {
    r = await fetch(BASE + "/api/v2/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }

  // Bubble up backend response as-is
  const data = await r.json().catch(() => ({}));
  return NextResponse.json(data, { status: r.status });
}
