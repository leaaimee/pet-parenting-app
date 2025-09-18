"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { getInitials } from "@/lib/getInitials";

export default function AvatarButton({
  name,
  src,
  sizeClamp = "88px",   // default size — can be overridden by pages
  status = "online",
}) {
  const [open, setOpen] = useState(false);          // expand/collapse state
  const [userStatus, setUserStatus] = useState(status); // online/offline toggle
  const router = useRouter();
  const initials = getInitials(name);

  // status → border + glow colors
  const statusColors = {
    online:  "#22c55e", // green
    away:    "#f59e0b", // amber (kept for future use)
    busy:    "#ef4444", // red (kept for future use)
    offline: "#ef4444", // red
  };
  const sColor = statusColors[userStatus] ?? statusColors.offline;

  return (
    <div
  onClick={() => setOpen(!open)}
  className="cursor-pointer flex flex-col items-center justify-start overflow-hidden rounded-[32px]"
      style={{
        width: sizeClamp,
        height: open ? "180px" : sizeClamp,  // 🔑 shapeshift height
        background: "#1d1921",               // plum background
        border: `3px solid ${sColor}`,       // border uses status color
        boxShadow: `0 0 20px 4px ${sColor}66`, // glow uses status color
        transition: "height 0.2s ease-in-out", // 🆕 smooth expand/collapse
      }}
    >
      {/* avatar face */}
      <div
        className="flex items-center justify-center"
        style={{
          width: sizeClamp,   // ✅ sync inner face with sizeClamp
          height: sizeClamp,  // ✅ no more hardcoded "88px"
        }}
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

      {/* dropdown content */}
      {open && (
        <div className="text-xs text-[#DED3F3] mt-3 space-y-2 w-full px-3">
          <button className="block w-full text-left">Settings</button>

          <button
            className="block w-full text-left"
            onClick={(e) => {
              e.stopPropagation(); // prevent parent toggle
              setUserStatus(userStatus === "online" ? "offline" : "online");
            }}
          >
            {userStatus === "online" ? "Go Offline" : "Go Online"}
          </button>

          <button
            className="block w-full text-left text-red-400 hover:text-red-300"
            onClick={(e) => {
              e.stopPropagation(); // don’t collapse
              router.push("/auth"); // fake logout → redirect to login
            }}
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
