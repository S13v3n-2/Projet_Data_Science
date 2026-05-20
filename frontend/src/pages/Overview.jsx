import KPIBar from '@/components/overview/KPIBar'
import ChurnByContractChart from '@/components/overview/ChurnByContractChart'
import RevenueBySegmentChart from '@/components/overview/RevenueBySegmentChart'
import NPSDistributionChart from '@/components/overview/NPSDistributionChart'
import TenureDistributionChart from '@/components/overview/TenureDistributionChart'
import CorrelationChart from '@/components/overview/CorrelationChart'

export default function Overview() {
  return (
    <div className="space-y-6 max-w-[1400px]">
      <header>
        <h1 className="text-2xl font-semibold text-slate-900">Vue d'ensemble</h1>
        <p className="text-sm text-slate-500 mt-1">
          Lecture instantanée de l'exposition au risque de résiliation sur votre base clients.
        </p>
      </header>

      <KPIBar />

      <div className="grid grid-cols-2 gap-4">
        <ChurnByContractChart />
        <RevenueBySegmentChart />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <NPSDistributionChart />
        <TenureDistributionChart />
      </div>

      <CorrelationChart />
    </div>
  )
}
