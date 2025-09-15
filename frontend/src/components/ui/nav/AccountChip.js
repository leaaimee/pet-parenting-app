"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Icon } from "@/components/icons/Icon";

function initialsFrom(nameOrEmail = "") {
  const s = nameOrEmail.trim();
  if (!s) return "?";
  const parts = s.includes("@") ? s.split("@")[0].split(/[._-]/) : s.split(" ");
  const letters = parts.filter(Boolean).slice(0, 2).map(p => p[0].toUpperCase());
  return letters.join("");
}

export default function AccountChip({
  name,
  email,
  avatarUrl,           // optional
  status = "online",   // "online" | "syncing" | "offline"
  className = "",
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const router = useRouter();

  // Close on outside click / Esc
  useEffect(() => {
    function onDoc(e) {
      if (e.key === "Escape") setOpen(false);
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("click", onDoc);
    document.addEventListener("keydown", onDoc);
    return () => {
      document.removeEventListener("click", onDoc);
      document.removeEventListener("keydown", onDoc);
    };
  }, []);

  async function logout() {
    await fetch("/api/logout", { method: "POST" });
    router.push("/auth");
  }

  const label = name || email || "Account";
  const initials = initialsFrom(name || email);

  // status colors
  const dot = {
    online: "#22c55e",
    syncing: "#f59e0b",
    offline: "#ef4444",
  }[status] || "#22c55e";

  return (
    <div ref={ref} className={`relative ${className}`}>
      <button
        aria-label="Account menu"
        onClick={(e) => { e.stopPropagation(); setOpen(v => !v); }}
        onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && setOpen(v => !v)}
        className="
          h-11 min-w-[56px] px-2 pr-1
          rounded-xl border border-white/20
          bg-transparent text-[#F4F4F5]/90
          inline-flex items-center justify-center gap-2
          hover:ring-2 hover:ring-[#A3E635] hover:ring-offset-2 hover:ring-offset-[#262229]
          focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#A3E635] focus-visible:ring-offset-2 focus-visible:ring-offset-[#262229]
          active:scale-[0.98] transition
        "
      >
        <span className="relative inline-flex items-center justify-center w-7 h-7 rounded-lg bg-white/5 border border-white/15">
          {avatarUrl ? (
            <img
              src={avatarUrl}
              alt=""
              className="w-full h-full rounded-lg object-cover"
            />
          ) : (
            <span className="text-[11px] tracking-wide">{initials}</span>
          )}
          {/* status dot */}
          <span
            aria-label={`Status: ${status}`}
            className="absolute -right-0.5 -top-0.5 w-2 h-2 rounded-full ring-2 ring-[#262229]"
            style={{ backgroundColor: dot }}
          />
        </span>
        <Icon name="chevron-down" size={16} className="opacity-80" />
      </button>

      {/* Popover / menu */}
      {open && (
        <div
          role="menu"
          className="
            absolute right-0 mt-2 w-56 rounded-2xl
            border border-white/15 bg-[#1f1b22] shadow-xl
            p-2 z-50
          "
        >
          <div className="px-3 py-2 text-sm opacity-80">
            <div className="font-medium">{name || email}</div>
            {name && <div className="opacity-70">{email}</div>}
          </div>
          <button
            role="menuitem"
            onClick={() => router.push("/profile")}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-white/10"
          >
            <Icon name="profile" />
            Profile
          </button>
          <button
            role="menuitem"
            onClick={() => router.push("/settings")}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-white/10"
          >
            <Icon name="settings" />
            Settings
          </button>
          <div className="h-px my-1 bg-white/10" />
          <button
            role="menuitem"
            onClick={logout}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-white/10 text-red-300"
          >
            <Icon name="logout" />
            Log out
          </button>
        </div>
      )}
    </div>
  );
}
