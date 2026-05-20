import { useMemo, useState } from 'react'
import { ChevronLeft, ChevronRight, Sparkles, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import Step1Profile from './Step1Profile'
import Step2Engagement from './Step2Engagement'
import Step3Support from './Step3Support'
import { cn } from '@/lib/utils'

const STEPS = [
  { id: 1, label: 'Profil & contrat' },
  { id: 2, label: 'Engagement' },
  { id: 3, label: 'Support & finances' },
]

export const DEFAULT_FORM = {
  age: 35,
  gender: 'Male',
  country: 'France',
  city: 'Paris',
  customer_segment: 'SMB',
  tenure_months: 12,
  signup_channel: 'Web',
  contract_type: 'Monthly',
  monthly_logins: 20,
  weekly_active_days: 4,
  avg_session_time: 12.5,
  features_used: 6,
  usage_growth_rate: 0.05,
  last_login_days_ago: 5,
  monthly_fee: 49,
  total_revenue: 588,
  payment_method: 'Credit Card',
  payment_failures: 0,
  discount_applied: 'No',
  price_increase_last_3m: 'No',
  support_tickets: 1,
  avg_resolution_time: 3.0,
  complaint_type: null,
  csat_score: 7,
  escalations: 0,
  email_open_rate: 0.4,
  marketing_click_rate: 0.1,
  nps_score: 30,
  survey_response: 'Neutral',
  referral_count: 0,
}

export default function SimulationWizard({ form, setForm, onSubmit, loading }) {
  const [step, setStep] = useState(1)

  const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }))

  const progress = useMemo(() => (step / STEPS.length) * 100, [step])

  return (
    <div className="space-y-5">
      <div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            {STEPS.map((s) => (
              <div key={s.id} className="flex items-center gap-2">
                <div
                  className={cn(
                    'w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold transition-colors',
                    step === s.id
                      ? 'bg-brand-accent text-white'
                      : step > s.id
                        ? 'bg-emerald-500 text-white'
                        : 'bg-slate-200 text-slate-500',
                  )}
                >
                  {s.id}
                </div>
                <span
                  className={cn(
                    'text-xs font-medium',
                    step === s.id ? 'text-slate-800' : 'text-slate-400',
                  )}
                >
                  {s.label}
                </span>
              </div>
            ))}
          </div>
          <span className="text-xs text-slate-400">
            Étape {step} / {STEPS.length}
          </span>
        </div>
        <div className="h-1.5 w-full rounded-full bg-slate-200 overflow-hidden">
          <div
            className="h-full bg-brand-accent transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div key={step} className="step-enter step-enter-active">
        {step === 1 && <Step1Profile form={form} update={update} />}
        {step === 2 && <Step2Engagement form={form} update={update} />}
        {step === 3 && <Step3Support form={form} update={update} />}
      </div>

      <div className="flex items-center justify-between pt-2">
        <Button
          variant="secondary"
          disabled={step === 1}
          onClick={() => setStep((s) => Math.max(1, s - 1))}
        >
          <ChevronLeft className="w-4 h-4" />
          Précédent
        </Button>

        {step < STEPS.length ? (
          <Button onClick={() => setStep((s) => Math.min(STEPS.length, s + 1))}>
            Continuer
            <ChevronRight className="w-4 h-4" />
          </Button>
        ) : (
          <Button onClick={onSubmit} disabled={loading} size="lg">
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyse en cours…
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Calculer le risque
              </>
            )}
          </Button>
        )}
      </div>
    </div>
  )
}
