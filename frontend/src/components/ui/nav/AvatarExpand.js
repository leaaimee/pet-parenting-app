"use client";
import { useState } from "react";
import AvatarButton from "./AvatarButton";

export default function AvatarExpand({ name, src, status = "online" }) {
  const [open, setOpen] = useState(false);

  // status colors
  const statusColors = {
    online:  "#22c55e",
    away:    "#f59e0b",
    busy:    "#ef4444",
    offline: "rgba(255,255,255,0.22)",
  };
  const sColor = statusColors[status] ?? statusColors.offline;

  return (
    <div
      onClick={() => setOpen(!open)}
      className="rounded-[32px] cursor-pointer transition-all duration-500 ease-in-out flex flex-col items-center justify-start overflow-hidden"
      style={{
        width: "88px",
        height: open ? "180px" : "88px", // shapeshift here
        background: "#1d1921",
        border: `3px solid ${sColor}`,
        boxShadow: `0 0 20px 4px ${sColor}66`,
      }}
    >
      {/* AvatarButton inside, border hidden when expanded */}
      <AvatarButton
        name={name}
        src={src}
        status={status}
        hideBorder={open}  // 👈 we added this prop earlier
      />

      {/* Placeholder space for future menu */}
      {open && (
        <div className="text-xs text-[#DED3F3] mt-3">
          (menu goes here)
        </div>
      )}
    </div>
  );
}
