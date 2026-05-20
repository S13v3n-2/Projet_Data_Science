import { Users, TrendingDown, Wallet, AlertTriangle } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { formatEUR, formatNumber } from '@/lib/utils'

export default function KPIBar({ kpis }) {
  const items = [
    {
      label: 'Total clients',
      value: formatNumber(kpis.total_clients),
      icon: Users,
      iconBg: 'bg-indigo-50 text-indigo-600',
      badge: null,
    },
    {
      label: 'Taux de resiliation',
      value: `${kpis.churn_rate} %`,
      icon: TrendingDown,
      iconBg: 'bg-red-50 text-red-600',
      badge: { tone: 'danger', label: 'A surveiller' },
    },
    {
      label: 'Revenu total expose',
      value: formatEUR(kpis.total_revenue_exposed),
      icon: Wallet,
      iconBg: 'bg-amber-50 text-amber-600',
      badge: { tone: 'warning', label: 'Critique' },
    },
    {
      label: 'Perte mensuelle estimee',
      value: `${formatEUR(kpis.monthly_fee_at_risk)} / mois`,
      icon: AlertTriangle,
      iconBg: 'bg-red-50 text-red-600',
      badge: { tone: 'danger', label: 'Eleve' },
    },
  ]

  return (
    <div className="grid grid-cols-4 gap-4">
      {items.map(({ label, value, icon: Icon, iconBg, badge }) => (
        <Card key={label} className="p-5">
          <div className="flex items-start justify-between">
            <div className={`p-2 rounded-lg ${iconBg}`}>
              <Icon className="w-5 h-5" />
            </div>
            {badge && <Badge tone={badge.tone}>{badge.label}</Badge>}
          </div>
          <div className="mt-4">
            <p className="text-2xl font-semibold text-slate-900 tabular-nums">{value}</p>
            <p className="text-xs text-slate-500 mt-1">{label}</p>
          </div>
        </Card>
      ))}
    </div>
  )
}
