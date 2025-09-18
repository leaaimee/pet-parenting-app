export default function FontStyle({ variant, children }) {
  const styles = {
    label: "uppercase tracking-wide text-xs font-semibold !text-[#1B1A1F]/70",
    value: "text-sm !text-[#1B1A1F]",
    tileTitle: "uppercase tracking-wide text-lg font-semibold text-[#1B1A1F]",
    sectionTitle:
      "uppercase mb-6 tracking-[0.18em] text-2xl !text-[var(--text)]",
  };

  return <div className={styles[variant]}>{children}</div>;
}
