import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  const cwd = process.cwd();
  const envPath = path.join(cwd, ".env.local");
  const envExists = fs.existsSync(envPath);

  // peek at package.json to confirm we're in the Next app root
  let hasNextDep = false;
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(cwd, "package.json"), "utf8"));
    hasNextDep = Boolean(pkg.dependencies?.next || pkg.devDependencies?.next);
  } catch {}

  return NextResponse.json({
    cwd,
    envExists,
    hasNextDep,
    BACKEND_URL: process.env.BACKEND_URL ?? null,
  });
}
