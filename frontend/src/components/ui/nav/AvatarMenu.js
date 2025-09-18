"use client";
import { useState } from "react";
import AvatarButton from "./AvatarButton";

export default function AvatarMenu({ name, src }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block">
      {/* Avatar button */}
      <AvatarButton
        name={name}
        src={src}
        onClick={() => setOpen(!open)}
      />

      {/* Expanding menu */}
      <div
        className={`absolute right-0 mt-2 w-40 rounded-2xl shadow-lg overflow-hidden transition-all duration-300 ${
          open ? "max-h-60 opacity-100" : "max-h-0 opacity-0"
        }`}
        style={{
          background: "rgba(255,255,255,0.08)",
          backdropFilter: "blur(8px)",
        }}
      >
        <button className="block w-full px-4 py-2 text-left text-sm hover:bg-white/10">
          Settings
        </button>
        <button className="block w-full px-4 py-2 text-left text-sm hover:bg-white/10">
          Logout
        </button>
      </div>
    </div>
  );
}
