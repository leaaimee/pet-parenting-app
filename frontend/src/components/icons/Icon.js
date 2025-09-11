// Minimal icon system with a consistent style.
// Usage: <Icon name="family" size={20} className="opacity-80" />

const base = {
  xmlns: "http://www.w3.org/2000/svg",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round",
  strokeLinejoin: "round",
};

const Icons = {
  family: (p) => (
    <svg {...base} {...p}>
      <path d="M6 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
      <path d="M18 11.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z" />
      <path d="M3.5 20v-1.5A4.5 4.5 0 0 1 8 14h0A4.5 4.5 0 0 1 12.5 18.5V20" />
      <path d="M13.5 20v-1a3.5 3.5 0 0 1 3.5-3.5h0A3.5 3.5 0 0 1 20.5 19v1" />
    </svg>
  ),
  appointments: (p) => (
    <svg {...base} {...p}>
      <path d="M7 3v3M17 3v3" />
      <rect x="3.5" y="5" width="17" height="15" rx="2.5" />
      <path d="M3.5 9.5h17" />
      <circle cx="9" cy="13" r="1" />
    </svg>
  ),
  medical: (p) => (
    <svg {...base} {...p}>
      <rect x="4" y="4" width="16" height="16" rx="3" />
      <path d="M12 8v8M8 12h8" />
    </svg>
  ),
  marketplace: (p) => (
    <svg {...base} {...p}>
      <path d="M4 7h16" />
      <path d="M6 7l2 11h8l2-11" />
      <path d="M9.5 7l.8-2.4A2 2 0 0 1 12.2 3h-.4a2 2 0 0 1 1.9 1.6L14.5 7" />
    </svg>
  ),
  add: (p) => (
    <svg {...base} {...p}>
      <path d="M12 5v14M5 12h14" />
    </svg>
  ),
  "chevron-right": (p) => (
    <svg {...base} {...p}>
      <path d="M9 6l6 6-6 6" />
    </svg>
  ),
  "chevron-down": (p) => (
    <svg {...base} {...p}>
      <path d="M6 9l6 6 6-6" />
    </svg>
  ),
  settings: (p) => (
    <svg {...base} {...p}>
      <path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z" />
      <path d="M3 12h2M19 12h2M12 3v2M12 19v2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4" />
    </svg>
  ),
  profile: (p) => (
    <svg {...base} {...p}>
      <path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" />
      <path d="M4 20v-1.5A6.5 6.5 0 0 1 10.5 12h3A6.5 6.5 0 0 1 20 18.5V20" />
    </svg>
  ),
  logout: (p) => (
    <svg {...base} {...p}>
      <path d="M15 12H7" />
      <path d="M12 9l3 3-3 3" />
      <path d="M7 4h4a3 3 0 0 1 3 3v2" />
      <path d="M7 20h4a3 3 0 0 0 3-3v-2" />
    </svg>
  ),
  sync: (p) => (
    <svg {...base} {...p}>
      <path d="M4 12a8 8 0 0 1 13.7-5.7L20 4v6h-6l2.2-2.2A6 6 0 1 0 6 12" />
    </svg>
  ),
};

export function Icon({ name, size = 20, className, ...rest }) {
  const Comp = Icons[name];
  if (!Comp) return null;
  return <Comp width={size} height={size} className={className} {...rest} />;
}
