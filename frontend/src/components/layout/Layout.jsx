import Sidebar from './Sidebar'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-brand-bg">
      <Sidebar />
      <main className="ml-[240px] min-h-screen">
        <div className="px-10 py-8">{children}</div>
      </main>
    </div>
  )
}
