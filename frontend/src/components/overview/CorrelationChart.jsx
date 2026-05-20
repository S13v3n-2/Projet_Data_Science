import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'

function colorFor(v) {
  if (v >= 0.16) return '#3730A3'
  if (v >= 0.13) return '#4F46E5'
  if (v >= 0.10) return '#6366F1'
  if (v >= 0.07) return '#818CF8'
  return '#A5B4FC'
}

export default function CorrelationChart({ data }) {
  const maxCorr = Math.max(...data.map((d) => d.corr), 0.1)

  return (
    <Card>
      <CardHeader>
        <CardTitle>Facteurs correles a la resiliation</CardTitle>
        <p className="text-xs text-slate-500 mt-1">
          Intensite de correlation (valeur absolue) avec le depart d'un client
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
              domain={[0, Math.ceil(maxCorr * 10) / 10 + 0.02]}
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
              formatter={(v) => [v.toFixed(3), 'Correlation']}
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
