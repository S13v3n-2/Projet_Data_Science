import { cn } from '@/lib/utils'

const tones = {
  neutral: 'bg-slate-100 text-slate-700',
  success: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  warning: 'bg-amber-50 text-amber-700 border border-amber-200',
  danger: 'bg-red-50 text-red-700 border border-red-200',
  indigo: 'bg-indigo-50 text-indigo-700 border border-indigo-200',
}

export function Badge({ tone = 'neutral', className, children }) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 px-2 py-0.5 text-xs font-semibold rounded-md',
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  )
}
