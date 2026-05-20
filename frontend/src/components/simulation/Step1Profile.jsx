import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Input, Label } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Slider } from '@/components/ui/Slider'
import { ToggleGroup } from '@/components/ui/ToggleGroup'

const genderOptions = [
  { value: 'Male', label: 'Homme' },
  { value: 'Female', label: 'Femme' },
]

const segmentOptions = [
  { value: 'SMB', label: 'PME' },
  { value: 'Enterprise', label: 'Grande entreprise' },
  { value: 'Startup', label: 'Startup' },
  { value: 'Consumer', label: 'Particulier' },
]

const contractOptions = [
  { value: 'Monthly', label: 'Mensuel' },
  { value: 'Annual', label: 'Annuel' },
  { value: 'Two-Year', label: 'Biannuel' },
]

export default function Step1Profile({ form, update }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Profil & contrat</CardTitle>
        <p className="text-xs text-slate-500 mt-1">
          Informations de base sur le client et son engagement contractuel.
        </p>
      </CardHeader>
      <CardContent className="grid grid-cols-2 gap-5">
        <div>
          <Label>Âge</Label>
          <Input
            type="number"
            min={18}
            max={100}
            value={form.age}
            onChange={(e) => update('age', Number(e.target.value))}
          />
        </div>
        <div>
          <Label>Genre</Label>
          <Select options={genderOptions} value={form.gender} onChange={(v) => update('gender', v)} />
        </div>
        <div>
          <Label>Segment client</Label>
          <Select options={segmentOptions} value={form.customer_segment} onChange={(v) => update('customer_segment', v)} />
        </div>
        <div>
          <Label>Type de contrat</Label>
          <ToggleGroup
            options={contractOptions}
            value={form.contract_type}
            onChange={(v) => update('contract_type', v)}
          />
        </div>
        <div className="col-span-2">
          <Label>Ancienneté (mois)</Label>
          <Slider
            min={0}
            max={120}
            value={form.tenure_months}
            onChange={(v) => update('tenure_months', v)}
            suffix="mois"
          />
        </div>
        <div>
          <Label>Frais mensuels (€)</Label>
          <Input
            type="number"
            min={0}
            step="0.01"
            value={form.monthly_fee}
            onChange={(e) => update('monthly_fee', Number(e.target.value))}
          />
        </div>
        <div>
          <Label>Revenu total généré (€)</Label>
          <Input
            type="number"
            min={0}
            step="0.01"
            value={form.total_revenue}
            onChange={(e) => update('total_revenue', Number(e.target.value))}
          />
        </div>
      </CardContent>
    </Card>
  )
}
