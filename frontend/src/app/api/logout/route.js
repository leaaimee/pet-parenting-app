import { NextResponse } from "next/server";

export async function POST(req) {
  const res = NextResponse.redirect(new URL("/auth", req.url));
  res.cookies.set("access_token", "", { path: "/", maxAge: 0 });
  return res;
}
