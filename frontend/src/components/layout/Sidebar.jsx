import { NavLink } from 'react-router-dom'
import { Shield, Sparkles, LayoutDashboard, UserSearch, Circle, AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useApiHealth } from '@/hooks/useApiHealth'

const navItems = [
  { to: '/', label: "Vue d'ensemble", icon: LayoutDashboard, end: true },
  { to: '/clients', label: 'Clients a risque', icon: AlertTriangle },
  { to: '/simulation', label: 'Simulation client', icon: UserSearch },
]

export default function Sidebar() {
  const health = useApiHealth()

  return (
    <aside className="fixed top-0 left-0 h-screen w-[240px] bg-brand-sidebar text-slate-200 flex flex-col">
      <div className="px-6 pt-6 pb-8">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Shield className="w-7 h-7 text-brand-accent" strokeWidth={2.2} />
            <Sparkles className="w-3.5 h-3.5 text-amber-300 absolute -right-1 -top-1" />
          </div>
          <span className="text-lg font-semibold tracking-tight text-white">
            RetainIQ
          </span>
        </div>
        <p className="mt-1 text-[11px] text-slate-400">Plateforme de rétention</p>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-white/10 text-white'
                  : 'text-slate-300 hover:bg-white/5 hover:text-white',
              )
            }
          >
            <Icon className="w-4.5 h-4.5" size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-4 pb-5 pt-4 border-t border-white/10">
        <div className="flex items-center gap-2">
          <Circle
            className={cn(
              'w-2.5 h-2.5 fill-current',
              health.online ? 'text-emerald-400' : 'text-red-400',
            )}
          />
          <span className="text-xs text-slate-300">
            {health.checking
              ? 'Vérification…'
              : health.online
                ? 'API connectée'
                : 'API hors ligne'}
          </span>
        </div>
        {health.modelName && (
          <p className="mt-1 text-[10px] text-slate-500 truncate">
            Modèle : {health.modelName}
          </p>
        )}
      </div>
    </aside>
  )
}
