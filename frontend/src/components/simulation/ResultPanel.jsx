import { Card, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import RiskGauge from './RiskGauge'
import RiskFactors from './RiskFactors'
import { formatEUR } from '@/lib/utils'
import { ShieldAlert, ShieldCheck, ShieldQuestion, CheckCircle2, XCircle, Wallet, AlertTriangle, Loader2 } from 'lucide-react'

function levelMeta(level, prob) {
  if (level === 'High' || prob >= 0.6) {
    return { label: 'RISQUE ÉLEVÉ', tone: 'danger', Icon: ShieldAlert }
  }
  if (level === 'Medium' || prob >= 0.3) {
    return { label: 'RISQUE MODÉRÉ', tone: 'warning', Icon: ShieldQuestion }
  }
  return { label: 'FAIBLE RISQUE', tone: 'success', Icon: ShieldCheck }
}

export default function ResultPanel({ loading, error, result, form, onReset }) {
  return (
    <div className="sticky top-8">
      <Card className="overflow-hidden">
        <div className="px-6 pt-5 pb-4 border-b border-brand-border bg-slate-50/50">
          <h3 className="text-sm font-semibold text-slate-700">Analyse du profil</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Évaluation en temps réel basée sur le modèle de rétention.
          </p>
        </div>

        <CardContent className="pt-6">
          {loading && (
            <div className="flex flex-col items-center justify-center py-16">
              <Loader2 className="w-8 h-8 text-brand-accent animate-spin" />
              <p className="mt-3 text-sm text-slate-500">Analyse en cours…</p>
            </div>
          )}

          {error && !loading && (
            <div className="py-10 flex flex-col items-center text-center">
              <AlertTriangle className="w-10 h-10 text-red-500" />
              <p className="mt-3 text-sm font-medium text-slate-800">
                Service temporairement indisponible
              </p>
              <p className="text-xs text-slate-500 mt-1 max-w-[260px]">
                {error}
              </p>
              <Button variant="secondary" size="sm" className="mt-4" onClick={onReset}>
                Réessayer
              </Button>
            </div>
          )}

          {!loading && !error && !result && (
            <div className="py-12 flex flex-col items-center text-center">
              <div className="w-20 h-20 rounded-full bg-indigo-50 flex items-center justify-center">
                <ShieldQuestion className="w-10 h-10 text-brand-accent" />
              </div>
              <p className="mt-4 text-sm font-medium text-slate-700">
                Complétez le profil pour obtenir une analyse
              </p>
              <p className="text-xs text-slate-500 mt-1 max-w-[260px]">
                Renseignez les trois étapes du formulaire puis lancez le calcul.
              </p>
            </div>
          )}

          {!loading && !error && result && (
            <ResultContent result={result} form={form} onReset={onReset} />
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function ResultContent({ result, form, onReset }) {
  const prob = result.churn_probability ?? 0
  const meta = levelMeta(result.risk_level, prob)
  const Icon = meta.Icon
  const willChurn = !!result.churn_prediction

  return (
    <div className="space-y-5">
      <RiskGauge probability={prob} />

      <div className="flex justify-center">
        <Badge tone={meta.tone} className="px-3 py-1 text-xs tracking-wide">
          <Icon className="w-3.5 h-3.5" />
          {meta.label}
        </Badge>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-brand-border p-3">
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Wallet className="w-3.5 h-3.5" /> Revenu exposé
          </div>
          <div className="mt-1.5 text-lg font-semibold text-slate-900 tabular-nums">
            {formatEUR(result.revenue_at_risk)}
          </div>
        </div>
        <div className="rounded-xl border border-brand-border p-3">
          <div className="flex items-center gap-2 text-xs text-slate-500">
            {willChurn ? (
              <XCircle className="w-3.5 h-3.5 text-red-500" />
            ) : (
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
            )}
            Décision
          </div>
          <div className={`mt-1.5 text-sm font-semibold ${willChurn ? 'text-red-600' : 'text-emerald-600'}`}>
            {willChurn ? 'Résiliera' : 'Ne résiliera pas'}
          </div>
        </div>
      </div>

      <div>
        <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">
          Facteurs déclenchants
        </h4>
        <RiskFactors form={form} result={result} />
      </div>

      <Button variant="secondary" className="w-full" onClick={onReset}>
        Réinitialiser
      </Button>
    </div>
  )
}
