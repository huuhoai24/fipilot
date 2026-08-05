import { cn } from '@/lib/utils'

type BrandLogoProps = {
  className?: string
}

export function BrandLogo({ className }: BrandLogoProps) {
  return <img src="/fipilot-logo.svg" alt="" aria-hidden="true" className={cn('shrink-0', className)} />
}
