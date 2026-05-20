import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'

// Bell-ish curves for non-churn (centered ~+30) and churn (centered ~-20)
function gaussian(x, mu, sigma, scale) {
  return scale * Math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
}
const data = []
for (let x = -100; x <= 100; x += 5) {
  data.push({
    nps: x,
    nonChurn: Math.round(gaussian(x, 30, 28, 900)),
    churn: Math.round(gaussian(x, -20, 32, 320)),
  })
}

export default function NPSDistributionChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Distribution du score NPS par statut</CardTitle>
        <p className="text-xs text-slate-500 mt-1">Clients résiliés vs clients actifs</p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="nonChurnGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#6366F1" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#6366F1" stopOpacity={0.05} />
              </linearGradient>
              <linearGradient id="churnGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#EF4444" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#EF4444" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
            <XAxis dataKey="nps" stroke="#94A3B8" fontSize={11} tickLine={false} axisLine={false} />
            <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{ borderRadius: 8, border: '1px solid #E2E8F0', fontSize: 12 }}
              labelFormatter={(v) => `NPS ${v}`}
            />
            <Legend
              iconType="circle"
              wrapperStyle={{ fontSize: 12, paddingTop: 4 }}
              formatter={(v) => (v === 'nonChurn' ? 'Clients actifs' : 'Clients résiliés')}
            />
            <Area type="monotone" dataKey="nonChurn" stroke="#6366F1" fill="url(#nonChurnGrad)" strokeWidth={2} />
            <Area type="monotone" dataKey="churn" stroke="#EF4444" fill="url(#churnGrad)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
