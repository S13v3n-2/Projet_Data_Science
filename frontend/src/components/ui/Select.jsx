import { cn } from '@/lib/utils'
import { ChevronDown } from 'lucide-react'

export function Select({ className, options = [], value, onChange, ...props }) {
  return (
    <div className="relative">
      <select
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        className={cn(
          'h-10 w-full pl-3 pr-9 rounded-lg border border-brand-border bg-white text-sm text-slate-800 appearance-none focus:outline-none focus:ring-2 focus:ring-brand-accent/30 focus:border-brand-accent transition',
          className,
        )}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
    </div>
  )
}
