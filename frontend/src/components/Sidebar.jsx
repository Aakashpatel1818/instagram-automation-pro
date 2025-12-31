import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, Settings, FileText, BarChart3, Menu } from 'lucide-react'

function Sidebar({ open }) {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/rules', label: 'Automation Rules', icon: Settings },
    { path: '/logs', label: 'Activity Logs', icon: FileText },
    { path: '/settings', label: 'Settings', icon: BarChart3 },
  ]

  return (
    <aside
      className={`bg-gradient-to-b from-primary-700 to-primary-900 text-white transition-all duration-300 ${
        open ? 'w-64' : 'w-20'
      }`}
    >
      <div className="p-6 flex items-center justify-center border-b border-primary-600">
        <div className="text-3xl font-bold">📱</div>
        {open && <span className="ml-3 font-bold text-lg">Insta Pro</span>}
      </div>

      <nav className="mt-6 space-y-2 px-3">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-primary-100 hover:bg-primary-600/50'
              }`}
              title={open ? '' : item.label}
            >
              <Icon size={20} />
              {open && <span className="font-medium">{item.label}</span>}
            </Link>
          )
        })}
      </nav>

      <div className="absolute bottom-6 left-0 right-0 px-3">
        <div className="bg-primary-600/30 rounded-lg p-4 text-center text-sm">
          {open ? (
            <>
              <p className="font-semibold">📊 Active Rules</p>
              <p className="text-2xl font-bold mt-1">5</p>
            </>
          ) : (
            <p className="text-lg">5</p>
          )}
        </div>
      </div>
    </aside>
  )
}

export default Sidebar