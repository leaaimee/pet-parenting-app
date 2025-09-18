// frontend/src/components/ui/nav/HeaderBar.js
"use client";

export default function HeaderBar({
  left = null,       // e.g. <TitlePlain />
  rightSlot = null,  // e.g. <AvatarButton />
  className = "",
}) {
  return (
    <header
      role="banner"
       className={`sticky top-0 z-40 flex items-start justify-between gap-4 ${className}`}


    >
      {/* left side */}
      <div className="flex items-center h-full">
        {left}
      </div>

      {/* right side */}
      <div className="shrink-0 flex items-start">{rightSlot}</div>
    </header>
  );
}

