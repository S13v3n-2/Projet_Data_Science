import { AlertCircle, Clock, ThumbsDown, CreditCard, Frown, MessageSquare, TrendingDown, Calendar, CheckCircle2, Star, Shield, Zap } from 'lucide-react'
import { Badge } from '@/components/ui/Badge'

export function computeRiskFactors(form) {
  const negative = []
  const positive = []

  // --- Facteurs negatifs ---
  if (form.last_login_days_ago >= 30) {
    negative.push({
      icon: Clock,
      label: `Derniere connexion il y a ${form.last_login_days_ago} jours`,
      tone: form.last_login_days_ago >= 60 ? 'danger' : 'warning',
    })
  }
  if (form.nps_score < 0) {
    negative.push({
      icon: ThumbsDown,
      label: `Score NPS negatif (${form.nps_score})`,
      tone: form.nps_score <= -30 ? 'danger' : 'warning',
    })
  }
  if (form.payment_failures >= 2) {
    negative.push({
      icon: CreditCard,
      label: `${form.payment_failures} echec${form.payment_failures > 1 ? 's' : ''} de paiement recent${form.payment_failures > 1 ? 's' : ''}`,
      tone: form.payment_failures >= 4 ? 'danger' : 'warning',
    })
  }
  if (form.csat_score < 5) {
    negative.push({
      icon: Frown,
      label: `Satisfaction client faible (CSAT ${form.csat_score}/10)`,
      tone: form.csat_score < 3 ? 'danger' : 'warning',
    })
  }
  if (form.support_tickets >= 5) {
    negative.push({
      icon: MessageSquare,
      label: `${form.support_tickets} tickets support ouverts`,
      tone: form.support_tickets >= 10 ? 'danger' : 'warning',
    })
  }
  if (form.escalations >= 1) {
    negative.push({
      icon: AlertCircle,
      label: `${form.escalations} escalade${form.escalations > 1 ? 's' : ''} client`,
      tone: form.escalations >= 3 ? 'danger' : 'warning',
    })
  }
  if (form.usage_growth_rate < 0) {
    negative.push({
      icon: TrendingDown,
      label: `Usage en baisse (${(form.usage_growth_rate * 100).toFixed(0)}%)`,
      tone: form.usage_growth_rate < -0.2 ? 'danger' : 'warning',
    })
  }
  if (form.tenure_months < 6) {
    negative.push({
      icon: Calendar,
      label: `Client recent (${form.tenure_months} mois d'anciennete)`,
      tone: 'warning',
    })
  }
  if (form.weekly_active_days <= 1) {
    negative.push({
      icon: Clock,
      label: `Engagement tres faible (${form.weekly_active_days} j/semaine)`,
      tone: 'warning',
    })
  }
  if (form.monthly_logins < 5) {
    negative.push({
      icon: TrendingDown,
      label: `Faible activite (${form.monthly_logins} connexions/mois)`,
      tone: 'warning',
    })
  }
  if (form.contract_type === 'Monthly') {
    negative.push({
      icon: Calendar,
      label: 'Contrat mensuel sans engagement',
      tone: 'warning',
    })
  }
  if (form.price_increase_last_3m === 'Yes') {
    negative.push({
      icon: TrendingDown,
      label: 'Hausse de prix appliquee recemment',
      tone: 'warning',
    })
  }

  // --- Facteurs positifs ---
  if (form.csat_score >= 8) {
    positive.push({ icon: Star, label: `Tres bonne satisfaction client (CSAT ${form.csat_score}/10)` })
  } else if (form.csat_score >= 6) {
    positive.push({ icon: Star, label: `Satisfaction client correcte (CSAT ${form.csat_score}/10)` })
  }
  if (form.tenure_months > 24) {
    positive.push({ icon: Shield, label: `Client fidele (${form.tenure_months} mois d'anciennete)` })
  }
  if (form.contract_type && form.contract_type !== 'Monthly') {
    positive.push({ icon: CheckCircle2, label: `Contrat engage (${form.contract_type})` })
  }
  if (form.nps_score >= 30) {
    positive.push({ icon: Star, label: `Score NPS tres positif (${form.nps_score})` })
  }
  if (form.usage_growth_rate > 0.1) {
    positive.push({ icon: Zap, label: `Usage en progression (+${(form.usage_growth_rate * 100).toFixed(0)}%)` })
  }

  // Prioritize danger > warning, max 5 negative
  const topNegative = negative
    .sort((a, b) => (a.tone === 'danger' ? -1 : 1) - (b.tone === 'danger' ? -1 : 1))
    .slice(0, 5)

  return { negative: topNegative, positive: positive.slice(0, 3) }
}

function getRecommendation(riskLevel, prob) {
  const level = riskLevel || (prob >= 0.6 ? 'High' : prob >= 0.3 ? 'Medium' : 'Low')
  if (level === 'High') {
    return {
      tone: 'danger',
      text: 'Action urgente - contacter ce client sous 48h et proposer une offre de fidelite personnalisee.',
    }
  }
  if (level === 'Medium') {
    return {
      tone: 'warning',
      text: 'Surveillance active - inclure dans la prochaine campagne de retention et suivre l\'evolution.',
    }
  }
  return {
    tone: 'success',
    text: 'Profil stable - communication standard suffisante, focus sur la valorisation des services.',
  }
}

export default function RiskFactors({ form, result }) {
  const { negative, positive } = computeRiskFactors(form)

  const recommendation = result
    ? getRecommendation(result.risk_level, result.churn_probability)
    : null

  const hasFactors = negative.length > 0 || positive.length > 0

  if (!hasFactors) {
    return (
      <div className="text-sm text-slate-500 italic">
        Aucun facteur de risque marquant identifie sur ce profil.
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {/* Facteurs negatifs */}
      {negative.length > 0 && (
        <ul className="space-y-2">
          {negative.map((f, i) => {
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
      )}

      {/* Facteurs positifs */}
      {positive.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1.5">Points forts</p>
          <ul className="space-y-1.5">
            {positive.map((f, i) => {
              const Icon = f.icon
              return (
                <li key={i} className="flex items-center gap-2.5 text-sm text-emerald-700 px-3 py-2 bg-emerald-50 rounded-lg border border-emerald-100">
                  <Icon className="w-4 h-4 text-emerald-500 shrink-0" />
                  {f.label}
                </li>
              )
            })}
          </ul>
        </div>
      )}

      {/* Recommandation d'action */}
      {recommendation && (
        <div className={`mt-1 px-3 py-2.5 rounded-lg border text-sm ${
          recommendation.tone === 'danger'
            ? 'bg-red-50 border-red-200 text-red-800'
            : recommendation.tone === 'warning'
              ? 'bg-amber-50 border-amber-200 text-amber-800'
              : 'bg-emerald-50 border-emerald-200 text-emerald-800'
        }`}>
          <span className="font-semibold">Recommandation : </span>
          {recommendation.text}
        </div>
      )}
    </div>
  )
}
