import { cn } from '@/lib/utils'

export function Slider({ min = 0, max = 100, step = 1, value, onChange, className, suffix }) {
  return (
    <div className={cn('flex items-center gap-3', className)}>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange?.(Number(e.target.value))}
        className="flex-1"
      />
      <span className="min-w-[3.5rem] text-right text-sm font-semibold text-slate-700 tabular-nums">
        {value}
        {suffix ? <span className="text-slate-400 font-normal ml-0.5">{suffix}</span> : null}
      </span>
    </div>
  )
}
