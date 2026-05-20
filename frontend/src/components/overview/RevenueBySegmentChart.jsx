import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { formatEUR } from '@/lib/utils'

const data = [
  { segment: 'Particulier', revenue: 412300 },
  { segment: 'PME', revenue: 268440 },
  { segment: 'Grande entreprise', revenue: 121900 },
  { segment: 'Startup', revenue: 60000 },
]

const colors = ['#F59E0B', '#FB923C', '#FDBA74', '#FCD34D']

export default function RevenueBySegmentChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Revenu exposé par segment client</CardTitle>
        <p className="text-xs text-slate-500 mt-1">Volume potentiellement à risque</p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} layout="vertical" margin={{ top: 10, right: 30, left: 30, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" horizontal={false} />
            <XAxis
              type="number"
              stroke="#94A3B8"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `${(v / 1000).toFixed(0)}k €`}
            />
            <YAxis
              type="category"
              dataKey="segment"
              stroke="#94A3B8"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              width={110}
            />
            <Tooltip
              cursor={{ fill: '#F8FAFC' }}
              contentStyle={{ borderRadius: 8, border: '1px solid #E2E8F0', fontSize: 12 }}
              formatter={(v) => [formatEUR(v), 'Revenu exposé']}
            />
            <Bar dataKey="revenue" radius={[0, 6, 6, 0]}>
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
