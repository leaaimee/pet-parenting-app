import { cookies } from "next/headers";

export async function authedFetch(path, init = {}) {
  const token = cookies().get("access_token")?.value; // httpOnly cookie
  const headers = new Headers(init.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);

  return fetch(process.env.BACKEND_URL + path, {
    ...init,
    headers,
    cache: "no-store",
  });
}
