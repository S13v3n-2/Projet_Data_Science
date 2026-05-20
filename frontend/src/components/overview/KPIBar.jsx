import { Users, TrendingDown, Wallet, AlertTriangle } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { formatEUR, formatNumber } from '@/lib/utils'

const kpis = [
  {
    label: 'Total clients',
    value: formatNumber(10000),
    icon: Users,
    iconBg: 'bg-indigo-50 text-indigo-600',
    badge: null,
  },
  {
    label: 'Taux de résiliation',
    value: '10,2 %',
    icon: TrendingDown,
    iconBg: 'bg-red-50 text-red-600',
    badge: { tone: 'danger', label: 'À surveiller' },
  },
  {
    label: 'Revenu total exposé',
    value: formatEUR(862640),
    icon: Wallet,
    iconBg: 'bg-amber-50 text-amber-600',
    badge: { tone: 'warning', label: 'Critique' },
  },
  {
    label: 'Perte mensuelle estimée',
    value: `${formatEUR(35300)} / mois`,
    icon: AlertTriangle,
    iconBg: 'bg-red-50 text-red-600',
    badge: { tone: 'danger', label: 'Élevé' },
  },
]

export default function KPIBar() {
  return (
    <div className="grid grid-cols-4 gap-4">
      {kpis.map(({ label, value, icon: Icon, iconBg, badge }) => (
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
