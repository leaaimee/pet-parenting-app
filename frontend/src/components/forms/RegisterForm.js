"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleRegister(e) {
    e.preventDefault();
    setErr("");
    setLoading(true);

    try {
      // 1) Real register via BFF → FastAPI /api/v2/users
      const regRes = await axios.post("/api/register", { email, password });
      if (regRes.status !== 200 && regRes.status !== 201) {
        setErr("Registration failed.");
        setLoading(false);
        return;
      }

      // 2) Real login via BFF → /token (sets httpOnly cookie)
      const loginRes = await axios.post("/api/login", {
        username: email,
        password,
      });

      if (loginRes.status === 200) {
        router.push("/homebase"); // or "/family"
      } else {
        router.push("/auth"); // fallback
      }
    } catch (error) {
      const msg =
        error?.response?.data?.detail ||
        error?.response?.data?.error ||
        "Registration failed. Try again.";
      setErr(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleRegister} className="space-y-5 text-inherit">
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
        disabled={loading}
        className="w-full bg-[#A3E635] text-[#1f1b19] font-bold py-2 rounded-xl hover:bg-[#B2F554] transition duration-150"
      >
        {loading ? "Registering..." : "Register"}
      </button>
    </form>

  );
}




//"use client";
//
//import { useState } from "react";
//import axios from "axios";
//import { useRouter } from "next/navigation";
//
//export default function RegisterForm() {
//  const [email, setEmail] = useState("");
//  const [password, setPassword] = useState("");
//  const router = useRouter();
//
//  const handleRegister = async (e) => {
//    e.preventDefault();
//    try {
//      const response = await axios.post("http://localhost:8000/register", {
//        email,
//        password,
//      });
//
//      if (response.status === 201) {
//        alert("Registration successful. You can now log in.");
//        router.push("/auth");
//      }
//    } catch (error) {
//      console.error("Registration failed:", error);
//      alert("Registration failed. Try again.");
//    }
//  };
//
//  return (
//    <form onSubmit={handleRegister} className="space-y-5 text-inherit]">
//      <div>
//        <label htmlFor="email" className="block text-sm mb-1">
//          Email
//        </label>
//        <input
//          id="email"
//          className="w-full px-4 py-2 rounded-xl bg-white border border-[#3A3633] focus:outline-none focus:ring-2 focus:ring-[#A3E635]"
//          type="email"
//          placeholder="you@example.com"
//          value={email}
//          onChange={(e) => setEmail(e.target.value)}
//          required
//        />
//      </div>
//
//      <div>
//        <label htmlFor="password" className="block text-sm mb-1">
//          Password
//        </label>
//        <input
//          id="password"
//          className="w-full px-4 py-2 rounded-xl bg-white border border-[#3A3633] focus:outline-none focus:ring-2 focus:ring-[#A3E635]"
//          type="password"
//          placeholder="••••••••"
//          value={password}
//          onChange={(e) => setPassword(e.target.value)}
//          required
//        />
//      </div>
//
//      <button
//        type="submit"
//        className="w-full bg-[#A3E635] text-[#1f1b19] font-bold py-2 rounded-xl hover:bg-[#B2F554] transition duration-150"
//      >
//        Register
//      </button>
//    </form>
//  );
//}
