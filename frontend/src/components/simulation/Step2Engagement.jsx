import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Input, Label } from '@/components/ui/Input'
import { Slider } from '@/components/ui/Slider'
import { ToggleGroup } from '@/components/ui/ToggleGroup'

const daysOptions = [0, 1, 2, 3, 4, 5, 6, 7].map((n) => ({ value: n, label: String(n) }))

function npsBarColor(value) {
  if (value < 0) return 'from-red-400 to-red-500'
  if (value <= 50) return 'from-slate-300 to-slate-400'
  return 'from-emerald-400 to-emerald-500'
}

export default function Step2Engagement({ form, update }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Engagement & utilisation</CardTitle>
        <p className="text-xs text-slate-500 mt-1">
          Activité du client sur le produit et perception de la marque.
        </p>
      </CardHeader>
      <CardContent className="grid grid-cols-2 gap-5">
        <div className="col-span-2">
          <Label>Connexions par mois</Label>
          <Slider min={0} max={60} value={form.monthly_logins} onChange={(v) => update('monthly_logins', v)} />
        </div>

        <div className="col-span-2">
          <Label>Jours actifs par semaine</Label>
          <ToggleGroup
            options={daysOptions}
            value={form.weekly_active_days}
            onChange={(v) => update('weekly_active_days', v)}
          />
        </div>

        <div>
          <Label>Durée moyenne d'une session (min)</Label>
          <Input
            type="number"
            min={0}
            step="0.1"
            value={form.avg_session_time}
            onChange={(e) => update('avg_session_time', Number(e.target.value))}
          />
        </div>

        <div>
          <Label>Croissance d'usage récente</Label>
          <Input
            type="number"
            step="0.01"
            value={form.usage_growth_rate}
            onChange={(e) => update('usage_growth_rate', Number(e.target.value))}
          />
        </div>

        <div className="col-span-2">
          <Label>Fonctionnalités utilisées</Label>
          <Slider min={0} max={20} value={form.features_used} onChange={(v) => update('features_used', v)} />
        </div>

        <div className="col-span-2">
          <Label>Dernière connexion (jours)</Label>
          <Slider
            min={0}
            max={90}
            value={form.last_login_days_ago}
            onChange={(v) => update('last_login_days_ago', v)}
            suffix="j"
          />
        </div>

        <div className="col-span-2">
          <Label>Score NPS</Label>
          <div className="space-y-2">
            <Slider min={-100} max={100} value={form.nps_score} onChange={(v) => update('nps_score', v)} />
            <div className="h-2 w-full rounded-full overflow-hidden flex">
              <div className="w-1/2 bg-gradient-to-r from-red-400 to-red-200" />
              <div className="w-1/4 bg-slate-200" />
              <div className="w-1/4 bg-gradient-to-r from-emerald-200 to-emerald-500" />
            </div>
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>-100 (détracteurs)</span>
              <span>0</span>
              <span>+50</span>
              <span>+100 (promoteurs)</span>
            </div>
          </div>
        </div>

        <div className="col-span-2">
          <Label>Réponse à la dernière enquête</Label>
          <ToggleGroup
            options={[
              { value: 'Positive', label: 'Positive' },
              { value: 'Neutral', label: 'Neutre' },
              { value: 'Negative', label: 'Négative' },
            ]}
            value={form.survey_response}
            onChange={(v) => update('survey_response', v)}
          />
        </div>
      </CardContent>
    </Card>
  )
}
