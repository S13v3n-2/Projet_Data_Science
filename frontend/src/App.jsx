import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from '@/components/layout/Layout'
import Overview from '@/pages/Overview'
import Simulation from '@/pages/Simulation'
import RiskClients from '@/pages/RiskClients'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/simulation" element={<Simulation />} />
        <Route path="/clients" element={<RiskClients />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}
