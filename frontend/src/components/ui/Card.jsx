import { cn } from '@/lib/utils'

export function Card({ className, children, ...props }) {
  return (
    <div
      className={cn(
        'bg-white border border-brand-border rounded-xl shadow-card',
        className,
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export function CardHeader({ className, children }) {
  return <div className={cn('px-6 pt-5 pb-3', className)}>{children}</div>
}

export function CardTitle({ className, children }) {
  return <h3 className={cn('text-sm font-semibold text-slate-700', className)}>{children}</h3>
}

export function CardContent({ className, children }) {
  return <div className={cn('px-6 pb-5', className)}>{children}</div>
}
