import React from 'react'
import { Menu, LogOut, Settings, Bell } from 'lucide-react'

function Navbar({ onMenuClick }) {
  return (
    <nav className="bg-white shadow-md border-b border-gray-200">
      <div className="px-6 py-4 flex justify-between items-center">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label="Toggle sidebar"
        >
          <Menu size={24} className="text-gray-700" />
        </button>

        <div className="flex items-center gap-6">
          {/* Notifications */}
          <button className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <Bell size={20} className="text-gray-700" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User Menu */}
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">Aakash Patel</p>
              <p className="text-xs text-gray-500">Admin</p>
            </div>
            <img
              src="https://ui-avatars.com/api/?name=Aakash+Patel&background=0ea5e9&color=fff"
              alt="User avatar"
              className="w-10 h-10 rounded-full"
            />
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <LogOut size={20} className="text-gray-700" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar