import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'

const data = [
  { contract: 'Mensuel', rate: 12.1 },
  { contract: 'Annuel', rate: 8.3 },
  { contract: 'Biannuel', rate: 5.9 },
]

const colors = ['#6366F1', '#818CF8', '#A5B4FC']

export default function ChurnByContractChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Taux de résiliation par type de contrat</CardTitle>
        <p className="text-xs text-slate-500 mt-1">En pourcentage de la base clients</p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
            <XAxis dataKey="contract" stroke="#94A3B8" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis
              stroke="#94A3B8"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `${v}%`}
            />
            <Tooltip
              cursor={{ fill: '#F1F5F9' }}
              contentStyle={{ borderRadius: 8, border: '1px solid #E2E8F0', fontSize: 12 }}
              formatter={(v) => [`${v}%`, 'Taux']}
            />
            <Bar dataKey="rate" radius={[6, 6, 0, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={colors[i]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
