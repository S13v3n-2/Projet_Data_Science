import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'

const data = [
  { factor: 'Score satisfaction (CSAT)', corr: 0.18 },
  { factor: 'Ancienneté', corr: 0.17 },
  { factor: 'Échecs de paiement', corr: 0.15 },
  { factor: 'Escalades support', corr: 0.13 },
  { factor: 'Frais mensuels', corr: 0.11 },
  { factor: 'Score NPS', corr: 0.10 },
  { factor: 'Tickets support', corr: 0.08 },
].sort((a, b) => b.corr - a.corr)

function colorFor(v) {
  // gradient blue intensity
  if (v >= 0.16) return '#3730A3'
  if (v >= 0.13) return '#4F46E5'
  if (v >= 0.10) return '#6366F1'
  if (v >= 0.07) return '#818CF8'
  return '#A5B4FC'
}

export default function CorrelationChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Facteurs corrélés à la résiliation</CardTitle>
        <p className="text-xs text-slate-500 mt-1">
          Intensité de corrélation avec le départ d'un client
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={data} layout="vertical" margin={{ top: 10, right: 30, left: 60, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" horizontal={false} />
            <XAxis
              type="number"
              stroke="#94A3B8"
              fontSize={11}
              domain={[0, 0.22]}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => v.toFixed(2)}
            />
            <YAxis
              type="category"
              dataKey="factor"
              stroke="#475569"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              width={170}
            />
            <Tooltip
              cursor={{ fill: '#F8FAFC' }}
              contentStyle={{ borderRadius: 8, border: '1px solid #E2E8F0', fontSize: 12 }}
              formatter={(v) => [v.toFixed(2), 'Corrélation']}
            />
            <Bar dataKey="corr" radius={[0, 6, 6, 0]}>
              {data.map((d, i) => (
                <Cell key={i} fill={colorFor(d.corr)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
