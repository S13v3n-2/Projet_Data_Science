import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Input, Label } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Slider } from '@/components/ui/Slider'
import { ToggleGroup } from '@/components/ui/ToggleGroup'
import { Star } from 'lucide-react'

const paymentOptions = [
  { value: 'Credit Card', label: 'Carte bancaire' },
  { value: 'Bank Transfer', label: 'Virement bancaire' },
  { value: 'PayPal', label: 'PayPal' },
  { value: 'Direct Debit', label: 'Prélèvement automatique' },
]

const complaintOptions = [
  { value: '', label: 'Aucune' },
  { value: 'Billing', label: 'Facturation' },
  { value: 'Technical', label: 'Technique' },
  { value: 'Service', label: 'Service client' },
]

function CSATStars({ value, onChange }) {
  return (
    <div className="flex items-center gap-1">
      {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
        <button
          key={n}
          type="button"
          onClick={() => onChange(n)}
          className="p-0.5 hover:scale-110 transition-transform"
        >
          <Star
            className={n <= value ? 'text-amber-400 fill-amber-400' : 'text-slate-300'}
            size={20}
          />
        </button>
      ))}
      <span className="ml-2 text-sm font-semibold text-slate-700 tabular-nums">{value}/10</span>
    </div>
  )
}

export default function Step3Support({ form, update }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Support & finances</CardTitle>
        <p className="text-xs text-slate-500 mt-1">
          Satisfaction client, incidents et historique de paiement.
        </p>
      </CardHeader>
      <CardContent className="grid grid-cols-2 gap-5">
        <div className="col-span-2">
          <Label>Échecs de paiement</Label>
          <Slider min={0} max={10} value={form.payment_failures} onChange={(v) => update('payment_failures', v)} />
        </div>

        <div className="col-span-2">
          <Label>Tickets de support ouverts</Label>
          <Slider min={0} max={20} value={form.support_tickets} onChange={(v) => update('support_tickets', v)} />
        </div>

        <div className="col-span-2">
          <Label>Score de satisfaction (CSAT)</Label>
          <CSATStars value={form.csat_score} onChange={(v) => update('csat_score', v)} />
        </div>

        <div>
          <Label>Temps moyen de résolution (h)</Label>
          <Input
            type="number"
            min={0}
            step="0.1"
            value={form.avg_resolution_time}
            onChange={(e) => update('avg_resolution_time', Number(e.target.value))}
          />
        </div>

        <div>
          <Label>Escalades</Label>
          <Input
            type="number"
            min={0}
            max={5}
            value={form.escalations}
            onChange={(e) => update('escalations', Number(e.target.value))}
          />
        </div>

        <div>
          <Label>Méthode de paiement</Label>
          <Select options={paymentOptions} value={form.payment_method} onChange={(v) => update('payment_method', v)} />
        </div>

        <div>
          <Label>Type de réclamation</Label>
          <Select
            options={complaintOptions}
            value={form.complaint_type || ''}
            onChange={(v) => update('complaint_type', v || null)}
          />
        </div>

        <div>
          <Label>Remise appliquée</Label>
          <ToggleGroup
            options={[
              { value: 'Yes', label: 'Oui' },
              { value: 'No', label: 'Non' },
            ]}
            value={form.discount_applied}
            onChange={(v) => update('discount_applied', v)}
          />
        </div>

        <div>
          <Label>Hausse de prix récente (3 mois)</Label>
          <ToggleGroup
            options={[
              { value: 'Yes', label: 'Oui' },
              { value: 'No', label: 'Non' },
            ]}
            value={form.price_increase_last_3m}
            onChange={(v) => update('price_increase_last_3m', v)}
          />
        </div>

        <div>
          <Label>Taux d'ouverture e-mails</Label>
          <Slider
            min={0}
            max={1}
            step={0.05}
            value={form.email_open_rate}
            onChange={(v) => update('email_open_rate', v)}
          />
        </div>

        <div>
          <Label>Taux de clic marketing</Label>
          <Slider
            min={0}
            max={1}
            step={0.05}
            value={form.marketing_click_rate}
            onChange={(v) => update('marketing_click_rate', v)}
          />
        </div>

        <div>
          <Label>Nombre de parrainages</Label>
          <Input
            type="number"
            min={0}
            value={form.referral_count}
            onChange={(e) => update('referral_count', Number(e.target.value))}
          />
        </div>
      </CardContent>
    </Card>
  )
}
