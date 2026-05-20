import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'

function gaussian(x, mu, sigma, scale) {
  return scale * Math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
}
const data = []
for (let x = 0; x <= 60; x += 2) {
  data.push({
    tenure: x,
    nonChurn: Math.round(gaussian(x, 32, 14, 1100)),
    churn: Math.round(gaussian(x, 8, 6, 480)),
  })
}

export default function TenureDistributionChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Distribution de l'ancienneté par statut</CardTitle>
        <p className="text-xs text-slate-500 mt-1">Mois d'ancienneté des clients</p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="nonChurnGrad2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#6366F1" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#6366F1" stopOpacity={0.05} />
              </linearGradient>
              <linearGradient id="churnGrad2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#EF4444" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#EF4444" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
            <XAxis
              dataKey="tenure"
              stroke="#94A3B8"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `${v}m`}
            />
            <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{ borderRadius: 8, border: '1px solid #E2E8F0', fontSize: 12 }}
              labelFormatter={(v) => `${v} mois`}
            />
            <Legend
              iconType="circle"
              wrapperStyle={{ fontSize: 12, paddingTop: 4 }}
              formatter={(v) => (v === 'nonChurn' ? 'Clients actifs' : 'Clients résiliés')}
            />
            <Area type="monotone" dataKey="nonChurn" stroke="#6366F1" fill="url(#nonChurnGrad2)" strokeWidth={2} />
            <Area type="monotone" dataKey="churn" stroke="#EF4444" fill="url(#churnGrad2)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
