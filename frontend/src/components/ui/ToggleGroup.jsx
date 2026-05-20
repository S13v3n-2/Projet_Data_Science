import { cn } from '@/lib/utils'

export function ToggleGroup({ options = [], value, onChange, className }) {
  return (
    <div className={cn('inline-flex rounded-lg border border-brand-border bg-white p-1 gap-1', className)}>
      {options.map((opt) => {
        const active = opt.value === value
        return (
          <button
            type="button"
            key={opt.value}
            onClick={() => onChange?.(opt.value)}
            className={cn(
              'px-3 h-8 text-sm rounded-md font-medium transition-colors',
              active
                ? 'bg-brand-accent text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-50',
            )}
          >
            {opt.label}
          </button>
        )
      })}
    </div>
  )
}
