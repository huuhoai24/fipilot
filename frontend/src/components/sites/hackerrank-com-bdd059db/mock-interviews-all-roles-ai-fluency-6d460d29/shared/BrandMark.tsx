import Link from "next/link";

interface BrandMarkProps {
  href?: string;
  compact?: boolean;
}

export function BrandMark({ href = "/", compact = false }: BrandMarkProps) {
  return (
    <Link
      className="ai-brand-mark"
      data-compact={compact || undefined}
      href={href}
      aria-label="Fipilot home"
    >
      <span>Fipilot</span>
    </Link>
  );
}
