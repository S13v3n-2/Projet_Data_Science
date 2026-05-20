import { AlertCircle, Clock, ThumbsDown, CreditCard, Frown, MessageSquare, TrendingDown, Calendar } from 'lucide-react'
import { Badge } from '@/components/ui/Badge'

export function computeRiskFactors(form) {
  const f = []
  if (form.last_login_days_ago >= 30) {
    f.push({
      icon: Clock,
      label: `Dernière connexion il y a ${form.last_login_days_ago} jours`,
      tone: form.last_login_days_ago >= 60 ? 'danger' : 'warning',
    })
  }
  if (form.nps_score < 0) {
    f.push({
      icon: ThumbsDown,
      label: `Score NPS négatif (${form.nps_score})`,
      tone: form.nps_score <= -30 ? 'danger' : 'warning',
    })
  }
  if (form.payment_failures >= 2) {
    f.push({
      icon: CreditCard,
      label: `${form.payment_failures} échecs de paiement détectés`,
      tone: form.payment_failures >= 4 ? 'danger' : 'warning',
    })
  }
  if (form.csat_score < 5) {
    f.push({
      icon: Frown,
      label: `Score CSAT faible (${form.csat_score}/10)`,
      tone: form.csat_score < 3 ? 'danger' : 'warning',
    })
  }
  if (form.support_tickets >= 5) {
    f.push({
      icon: MessageSquare,
      label: `${form.support_tickets} tickets support ouverts`,
      tone: form.support_tickets >= 10 ? 'danger' : 'warning',
    })
  }
  if (form.escalations >= 1) {
    f.push({
      icon: AlertCircle,
      label: `${form.escalations} escalade${form.escalations > 1 ? 's' : ''} client`,
      tone: form.escalations >= 3 ? 'danger' : 'warning',
    })
  }
  if (form.usage_growth_rate < 0) {
    f.push({
      icon: TrendingDown,
      label: `Usage en baisse (${(form.usage_growth_rate * 100).toFixed(0)}%)`,
      tone: form.usage_growth_rate < -0.2 ? 'danger' : 'warning',
    })
  }
  if (form.tenure_months < 6) {
    f.push({
      icon: Calendar,
      label: `Client récent (${form.tenure_months} mois d'ancienneté)`,
      tone: 'warning',
    })
  }
  if (form.weekly_active_days <= 1) {
    f.push({
      icon: Clock,
      label: `Engagement très faible (${form.weekly_active_days} j/semaine)`,
      tone: 'warning',
    })
  }
  if (form.price_increase_last_3m === 'Yes') {
    f.push({
      icon: TrendingDown,
      label: 'Hausse de prix appliquée récemment',
      tone: 'warning',
    })
  }
  // Prioritize danger > warning, max 5
  return f
    .sort((a, b) => (a.tone === 'danger' ? -1 : 1) - (b.tone === 'danger' ? -1 : 1))
    .slice(0, 5)
}

export default function RiskFactors({ form }) {
  const factors = computeRiskFactors(form)

  if (factors.length === 0) {
    return (
      <div className="text-sm text-slate-500 italic">
        Aucun facteur de risque marquant identifié sur ce profil.
      </div>
    )
  }

  return (
    <ul className="space-y-2">
      {factors.map((f, i) => {
        const Icon = f.icon
        const iconColor = f.tone === 'danger' ? 'text-red-500' : 'text-amber-500'
        return (
          <li
            key={i}
            className="flex items-center justify-between gap-3 px-3 py-2.5 bg-slate-50 rounded-lg border border-slate-100"
          >
            <div className="flex items-center gap-2.5 text-sm text-slate-700">
              <Icon className={`w-4 h-4 ${iconColor} shrink-0`} />
              {f.label}
            </div>
            <Badge tone={f.tone}>{f.tone === 'danger' ? 'Critique' : 'Vigilance'}</Badge>
          </li>
        )
      })}
    </ul>
  )
}
