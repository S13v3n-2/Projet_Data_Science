import { useState, useEffect } from 'react'
import { getStats } from '@/api/client'
import KPIBar from '@/components/overview/KPIBar'
import ChurnByContractChart from '@/components/overview/ChurnByContractChart'
import RevenueBySegmentChart from '@/components/overview/RevenueBySegmentChart'
import NPSDistributionChart from '@/components/overview/NPSDistributionChart'
import TenureDistributionChart from '@/components/overview/TenureDistributionChart'
import CorrelationChart from '@/components/overview/CorrelationChart'

function SkeletonCard({ className = '' }) {
  return (
    <div className={`bg-white rounded-xl border border-slate-100 animate-pulse ${className}`}>
      <div className="p-5 space-y-3">
        <div className="h-4 bg-slate-100 rounded w-1/2" />
        <div className="h-8 bg-slate-100 rounded w-2/3" />
        <div className="h-3 bg-slate-100 rounded w-1/3" />
      </div>
    </div>
  )
}

function LoadingSkeleton() {
  return (
    <div className="space-y-6 max-w-[1400px]">
      <header>
        <div className="h-7 bg-slate-100 rounded w-56 animate-pulse" />
        <div className="h-4 bg-slate-100 rounded w-96 mt-2 animate-pulse" />
      </header>
      <div className="grid grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => <SkeletonCard key={i} />)}
      </div>
      <div className="grid grid-cols-2 gap-4">
        <SkeletonCard className="h-80" />
        <SkeletonCard className="h-80" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <SkeletonCard className="h-80" />
        <SkeletonCard className="h-80" />
      </div>
      <SkeletonCard className="h-96" />
    </div>
  )
}

export default function Overview() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getStats()
      .then(setStats)
      .catch(() => setError("Impossible de charger les statistiques. Verifiez que l'API est demarree."))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSkeleton />

  if (error) {
    return (
      <div className="max-w-[1400px]">
        <header>
          <h1 className="text-2xl font-semibold text-slate-900">Vue d'ensemble</h1>
        </header>
        <div className="mt-6 p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
          {error}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 max-w-[1400px]">
      <header>
        <h1 className="text-2xl font-semibold text-slate-900">Vue d'ensemble</h1>
        <p className="text-sm text-slate-500 mt-1">
          Lecture instantanee de l'exposition au risque de resiliation sur votre base clients.
        </p>
      </header>

      <KPIBar kpis={stats.kpis} />

      <div className="grid grid-cols-2 gap-4">
        <ChurnByContractChart data={stats.churn_by_contract} />
        <RevenueBySegmentChart data={stats.revenue_by_segment} />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <NPSDistributionChart data={stats.nps_distribution} />
        <TenureDistributionChart data={stats.tenure_distribution} />
      </div>

      <CorrelationChart data={stats.correlations} />
    </div>
  )
}
