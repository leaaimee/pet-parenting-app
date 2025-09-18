"use client";
import { useState } from "react";
import { getInitials } from "@/lib/getInitials";

export default function AvatarButton({
  name,
  src,
  sizeClamp = "88px",
  status = "online",
}) {
  const [open, setOpen] = useState(false);
  const initials = getInitials(name);

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
      className="cursor-pointer transition-all duration-500 ease-in-out flex flex-col items-center justify-start overflow-hidden rounded-[32px]"
      style={{
        width: sizeClamp,
        height: open ? "180px" : sizeClamp,   // 👈 shapeshift core
        background: "#1d1921",
        border: `3px solid ${sColor}`,
        boxShadow: `0 0 20px 4px ${sColor}66`,
      }}
    >
      {/* avatar face */}
      <div
        className="flex items-center justify-center"
        style={{ width: sizeClamp, height: sizeClamp }}
      >
        {src ? (
          <img
            src={src}
            alt=""
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <span
            style={{
              fontFamily: "var(--font-questrial)",
              fontSize: "1.6rem",
              fontWeight: 400,
              textTransform: "uppercase",
              color: "#DED3F3",
            }}
          >
            {initials}
          </span>
        )}
      </div>

      {/* shapeshift content */}
      {open && (
        <div className="text-xs text-[#DED3F3] mt-3 space-y-2">
          <button className="block w-full text-left">Settings</button>
          <button className="block w-full text-left">Logout</button>
        </div>
      )}
    </div>
  );
}
