import { useState, useEffect, useCallback } from 'react'
import { Download, AlertTriangle, ChevronLeft, ChevronRight } from 'lucide-react'
import { getClientsAtRisk, getClientsAtRiskExportUrl } from '@/api/client'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'

const SEGMENTS = ['', 'Premium', 'Standard', 'Basic']
const CONTRACTS = ['', 'Monthly', 'Annual', 'Biennial']

function probTone(p) {
  if (p >= 0.7) return 'danger'
  if (p >= 0.5) return 'warning'
  return 'indigo'
}

function formatEur(v) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(v)
}

export default function RiskClients() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [segment, setSegment] = useState('')
  const [contractType, setContractType] = useState('')
  const [minProb, setMinProb] = useState(0.3)
  const [page, setPage] = useState(1)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = { min_prob: minProb, page, page_size: 50 }
      if (segment) params.segment = segment
      if (contractType) params.contract_type = contractType
      const result = await getClientsAtRisk(params)
      setData(result)
    } catch {
      setError('Impossible de charger les clients. Verifiez que l\'API est disponible.')
    } finally {
      setLoading(false)
    }
  }, [segment, contractType, minProb, page])

  useEffect(() => {
    setPage(1)
  }, [segment, contractType, minProb])

  useEffect(() => {
    load()
  }, [load])

  function handleExport() {
    const params = { min_prob: minProb }
    if (segment) params.segment = segment
    if (contractType) params.contract_type = contractType
    window.open(getClientsAtRiskExportUrl(params), '_blank')
  }

  return (
    <div className="space-y-6">
      {/* En-tete */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-slate-800 flex items-center gap-2">
            <AlertTriangle className="w-6 h-6 text-amber-500" />
            Clients a risque
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Clients scores en batch par le modele, tries par probabilite de churn decroissante
          </p>
        </div>
        <Button variant="secondary" size="sm" onClick={handleExport}>
          <Download className="w-4 h-4" />
          Exporter CSV
        </Button>
      </div>

      {/* Filtres */}
      <div className="bg-white border border-brand-border rounded-xl p-4 flex flex-wrap gap-4 items-end">
        <div className="flex flex-col gap-1 min-w-[140px]">
          <label className="text-xs font-medium text-slate-500">Segment</label>
          <select
            value={segment}
            onChange={e => setSegment(e.target.value)}
            className="h-9 rounded-lg border border-slate-200 text-sm px-3 bg-white focus:outline-none focus:ring-2 focus:ring-brand-accent/30"
          >
            {SEGMENTS.map(s => (
              <option key={s} value={s}>{s || 'Tous'}</option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1 min-w-[160px]">
          <label className="text-xs font-medium text-slate-500">Type de contrat</label>
          <select
            value={contractType}
            onChange={e => setContractType(e.target.value)}
            className="h-9 rounded-lg border border-slate-200 text-sm px-3 bg-white focus:outline-none focus:ring-2 focus:ring-brand-accent/30"
          >
            {CONTRACTS.map(c => (
              <option key={c} value={c}>{c || 'Tous'}</option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1 flex-1 min-w-[200px]">
          <label className="text-xs font-medium text-slate-500">
            Seuil minimum de probabilite : <span className="text-slate-800 font-semibold">{Math.round(minProb * 100)}%</span>
          </label>
          <input
            type="range"
            min="0"
            max="0.9"
            step="0.05"
            value={minProb}
            onChange={e => setMinProb(parseFloat(e.target.value))}
            className="w-full accent-indigo-500"
          />
        </div>

        {data && (
          <div className="ml-auto text-sm text-slate-500 self-end pb-1">
            <span className="font-semibold text-slate-800">{data.total}</span> client{data.total !== 1 ? 's' : ''} trouve{data.total !== 1 ? 's' : ''}
          </div>
        )}
      </div>

      {/* Tableau */}
      <div className="bg-white border border-brand-border rounded-xl overflow-hidden">
        {loading && (
          <div className="py-16 text-center text-sm text-slate-400">Chargement...</div>
        )}
        {error && (
          <div className="py-16 text-center text-sm text-red-500">{error}</div>
        )}
        {!loading && !error && data && (
          <>
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-100">
                <tr>
                  <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">ID Client</th>
                  <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Segment</th>
                  <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Contrat</th>
                  <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Probabilite churn</th>
                  <th className="text-right px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Revenu a risque</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {data.results.length === 0 && (
                  <tr>
                    <td colSpan={5} className="py-12 text-center text-slate-400">Aucun client correspond aux criteres selectionnes.</td>
                  </tr>
                )}
                {data.results.map(row => (
                  <tr key={row.customer_id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-3 font-mono text-slate-600">{row.customer_id}</td>
                    <td className="px-4 py-3 text-slate-700">{row.segment}</td>
                    <td className="px-4 py-3 text-slate-700">{row.contract_type}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${row.churn_probability >= 0.7 ? 'bg-red-400' : row.churn_probability >= 0.5 ? 'bg-amber-400' : 'bg-indigo-400'}`}
                            style={{ width: `${row.churn_probability * 100}%` }}
                          />
                        </div>
                        <Badge tone={probTone(row.churn_probability)}>
                          {Math.round(row.churn_probability * 100)}%
                        </Badge>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-right font-medium text-slate-800">{formatEur(row.revenue_at_risk)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            {data.pages > 1 && (
              <div className="px-4 py-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  Page {data.page} sur {data.pages}
                </span>
                <div className="flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    disabled={page <= 1}
                    onClick={() => setPage(p => p - 1)}
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </Button>
                  {Array.from({ length: Math.min(data.pages, 5) }, (_, i) => {
                    const p = Math.max(1, Math.min(data.pages - 4, page - 2)) + i
                    return (
                      <Button
                        key={p}
                        variant={p === page ? 'primary' : 'ghost'}
                        size="sm"
                        onClick={() => setPage(p)}
                        className="w-8 px-0"
                      >
                        {p}
                      </Button>
                    )
                  })}
                  <Button
                    variant="ghost"
                    size="sm"
                    disabled={page >= data.pages}
                    onClick={() => setPage(p => p + 1)}
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
