import React, { useState, useEffect } from 'react'
import StatsCard from '../components/StatsCard'
import { logs } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [chartData, setChartData] = useState([
    { date: 'Mon', comments: 12, dms: 5 },
    { date: 'Tue', comments: 19, dms: 8 },
    { date: 'Wed', comments: 15, dms: 7 },
    { date: 'Thu', comments: 25, dms: 12 },
    { date: 'Fri', comments: 22, dms: 10 },
    { date: 'Sat', comments: 18, dms: 9 },
    { date: 'Sun', comments: 20, dms: 11 },
  ])

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const response = await logs.getStats()
      setStats(response.data)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900">📊 Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back! Here's your Instagram automation overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          icon="💬"
          label="Total Comments"
          value={stats?.total_comments || 0}
          trend={12.5}
          color="blue"
        />
        <StatsCard
          icon="📲"
          label="DMs Sent"
          value={stats?.total_dms_sent || 0}
          trend={8.2}
          color="green"
        />
        <StatsCard
          icon="⚙️"
          label="Active Rules"
          value={stats?.active_rules || 0}
          color="orange"
        />
        <StatsCard
          icon="✅"
          label="Engagement Rate"
          value={`${stats?.engagement_rate || 0}%`}
          trend={5.1}
          color="red"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">📈 Weekly Activity</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="comments" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
              <Bar dataKey="dms" fill="#22c55e" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Trend Chart */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">📉 DM Conversion Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Line
                type="monotone"
                dataKey="dms"
                stroke="#0ea5e9"
                strokeWidth={3}
                dot={{ fill: '#0ea5e9', r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6 bg-gradient-to-br from-blue-50 to-blue-100">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Today's Comments</h3>
          <p className="text-3xl font-bold text-blue-600">{stats?.today_comments || 0}</p>
          <p className="text-xs text-gray-500 mt-2">Real-time updates</p>
        </div>
        <div className="card p-6 bg-gradient-to-br from-green-50 to-green-100">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Today's DMs Sent</h3>
          <p className="text-3xl font-bold text-green-600">{stats?.today_dms_sent || 0}</p>
          <p className="text-xs text-gray-500 mt-2">Automated responses</p>
        </div>
        <div className="card p-6 bg-gradient-to-br from-purple-50 to-purple-100">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Avg Response Time</h3>
          <p className="text-3xl font-bold text-purple-600">{stats?.response_time_avg || 0}s</p>
          <p className="text-xs text-gray-500 mt-2">Per automation</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard