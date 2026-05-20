import { cn } from '@/lib/utils'

export function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        'h-10 w-full px-3 rounded-lg border border-brand-border bg-white text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-accent/30 focus:border-brand-accent transition',
        className,
      )}
      {...props}
    />
  )
}

export function Label({ className, children, ...props }) {
  return (
    <label
      className={cn('block text-xs font-medium text-slate-600 mb-1.5', className)}
      {...props}
    >
      {children}
    </label>
  )
}
