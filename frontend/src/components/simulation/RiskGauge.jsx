function colorFor(prob) {
  if (prob < 0.3) return '#10B981'
  if (prob < 0.6) return '#F59E0B'
  return '#EF4444'
}

export default function RiskGauge({ probability = 0 }) {
  const size = 200
  const stroke = 18
  const radius = (size - stroke) / 2
  const circumference = Math.PI * radius // half circle
  const offset = circumference * (1 - probability)
  const color = colorFor(probability)
  const pct = Math.round(probability * 100)

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size / 2 + 10} viewBox={`0 0 ${size} ${size / 2 + 10}`}>
        <path
          d={`M ${stroke / 2} ${size / 2} A ${radius} ${radius} 0 0 1 ${size - stroke / 2} ${size / 2}`}
          fill="none"
          stroke="#E2E8F0"
          strokeWidth={stroke}
          strokeLinecap="round"
        />
        <path
          d={`M ${stroke / 2} ${size / 2} A ${radius} ${radius} 0 0 1 ${size - stroke / 2} ${size / 2}`}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 600ms ease-out, stroke 300ms' }}
        />
      </svg>
      <div className="-mt-12 text-center">
        <div className="text-4xl font-bold tabular-nums" style={{ color }}>
          {pct}%
        </div>
        <div className="text-xs text-slate-500 mt-0.5">Probabilité de résiliation</div>
      </div>
    </div>
  )
}
