import { useState } from 'react'
import SimulationWizard, { DEFAULT_FORM } from '@/components/simulation/SimulationWizard'
import ResultPanel from '@/components/simulation/ResultPanel'
import { predict } from '@/api/client'

export default function Simulation() {
  const [form, setForm] = useState(DEFAULT_FORM)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit() {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const payload = { ...form }
      if (payload.complaint_type === '' || payload.complaint_type == null) {
        payload.complaint_type = null
      }
      const data = await predict(payload)
      setResult(data)
    } catch (err) {
      const status = err?.response?.status
      if (status === 503 || status === 500) {
        setError('Le service de prédiction est momentanément hors ligne. Réessayez dans quelques instants.')
      } else if (err?.response?.data?.detail) {
        const detail = err.response.data.detail
        setError(typeof detail === 'string' ? detail : 'Données invalides fournies au modèle.')
      } else {
        setError('Impossible de joindre le service de prédiction.')
      }
    } finally {
      setLoading(false)
    }
  }

  function handleReset() {
    setResult(null)
    setError(null)
  }

  return (
    <div className="max-w-[1400px]">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Analyser un profil client</h1>
        <p className="text-sm text-slate-500 mt-1">
          Renseignez les informations clés pour estimer le risque de résiliation et identifier les leviers d'action.
        </p>
      </header>

      <div className="grid grid-cols-5 gap-6">
        <div className="col-span-3">
          <SimulationWizard
            form={form}
            setForm={setForm}
            onSubmit={handleSubmit}
            loading={loading}
          />
        </div>
        <div className="col-span-2">
          <ResultPanel
            loading={loading}
            error={error}
            result={result}
            form={form}
            onReset={handleReset}
          />
        </div>
      </div>
    </div>
  )
}
