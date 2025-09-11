import { NextResponse } from "next/server";
const BASE = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

export async function POST(req) {
  const { username, password } = await req.json();
  const body = new URLSearchParams({ username, password });
  const r = await fetch(BASE + "/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!r.ok) return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });

  const { access_token } = await r.json();

  // decide secure based on current protocol
  const isHttps = new URL(req.url).protocol === "https:"
               || req.headers.get("x-forwarded-proto") === "https";

  const res = NextResponse.json({ ok: true });
  res.cookies.set("access_token", access_token, {
    httpOnly: true,
    sameSite: "lax",
    secure: isHttps,       // <-- key line
    path: "/",
    maxAge: 60 * 60,       // 1h
  });
  return res;
}
