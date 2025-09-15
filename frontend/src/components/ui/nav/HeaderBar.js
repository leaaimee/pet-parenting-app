export default function HeaderBar({
  title,
  subtitle,
  rightSlot = null,  // e.g., <AvatarButton/>
  className = "",
}) {
  return (
    <header className={`flex items-center justify-between gap-4 ${className}`}>
      <div>
        <h1 className="text-[28px] lg:text-5xl tracking-tight uppercase">{title}</h1>
        {subtitle && <p className="text-sm text-white/70">{subtitle}</p>}
      </div>
      {rightSlot}
    </header>
  );
}
