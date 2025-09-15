// src/components/ui/Tile.js
import Link from "next/link";
import React from "react";
import { cn } from "@/lib/cn";

const variants = {
  hero:  "h-[220px]",
  tall:  "aspect-[9/10]",
  wide:  "aspect-[16/9]",
  square:"aspect-square",
};

export default function Tile({
  href,
  tone = "lavender",      // lavender | aqua | rose | sand | cream
  variant = "tall",       // hero | tall | wide | square
  interactive = true,
  className = "",
  children,
  ...props
}) {
  const Wrapper = href ? Link : "div";
  const vClass = variants[variant] || variants.tall;
  const inter  = interactive
    ? "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
    : "";

  return (
    <Wrapper href={href} {...(href ? {} : props)}>
      <div className={`tile tone-${tone} ${vClass} ${inter} ${className}`} {...(!href ? {} : props)}>
        {children}
      </div>
    </Wrapper>
  );
}
