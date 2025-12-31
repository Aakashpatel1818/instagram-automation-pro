import React, { useState, useEffect } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/Tabs'
import LogTable from '../components/LogTable'
import { logs } from '../services/api'

function LogsPage() {
  const [commentLogs, setCommentLogs] = useState([])
  const [dmLogs, setDmLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState('timestamp')
  const [sortOrder, setSortOrder] = useState('desc')
  const [activeTab, setActiveTab] = useState('comments')

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      setLoading(true)
      const [commentsRes, dmsRes] = await Promise.all([
        logs.getComments(0, 50),
        logs.getDMs(0, 50)
      ])
      setCommentLogs(commentsRes.data.comments || [])
      setDmLogs(dmsRes.data.dms || [])
    } catch (error) {
      console.error('Failed to fetch logs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSort = (key) => {
    if (sortBy === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(key)
      setSortOrder('desc')
    }
  }

  const commentColumns = [
    {
      key: 'timestamp',
      label: '⏰ Timestamp',
      sortable: true,
      render: (value) => new Date(value).toLocaleDateString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    },
    {
      key: 'commenter_username',
      label: '👤 Username',
      sortable: true,
    },
    {
      key: 'comment_text',
      label: '💬 Comment',
      render: (value) => value.substring(0, 50) + (value.length > 50 ? '...' : '')
    },
    {
      key: 'reply_sent',
      label: '✅ Status',
      render: (value) => value ? '✓ Replied' : '✗ Pending'
    },
  ]

  const dmColumns = [
    {
      key: 'sent_at',
      label: '⏰ Sent At',
      sortable: true,
      render: (value) => new Date(value).toLocaleDateString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    },
    {
      key: 'recipient_username',
      label: '👤 Recipient',
      sortable: true,
    },
    {
      key: 'message',
      label: '📲 Message',
      render: (value) => value.substring(0, 40) + (value.length > 40 ? '...' : '')
    },
    {
      key: 'status',
      label: '📤 Status',
      render: (value) => (
        <span className={`badge ${
          value === 'delivered' ? 'badge-success' :
          value === 'failed' ? 'badge-danger' :
          'badge-warning'
        }`}>
          {value}
        </span>
      )
    },
  ]

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900">📋 Activity Logs</h1>
        <p className="text-gray-600 mt-2">Track all comments and DMs processed by your automation rules.</p>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="border-b border-gray-200">
          <div className="flex gap-8 px-6 pt-4">
            <button
              onClick={() => setActiveTab('comments')}
              className={`pb-4 font-medium transition-colors ${
                activeTab === 'comments'
                  ? 'text-primary-600 border-b-2 border-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              💬 Comments ({commentLogs.length})
            </button>
            <button
              onClick={() => setActiveTab('dms')}
              className={`pb-4 font-medium transition-colors ${
                activeTab === 'dms'
                  ? 'text-primary-600 border-b-2 border-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              📲 DMs ({dmLogs.length})
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'comments' && (
            <LogTable
              data={commentLogs}
              columns={commentColumns}
              onSort={handleSort}
              sortBy={sortBy}
              sortOrder={sortOrder}
            />
          )}
          {activeTab === 'dms' && (
            <LogTable
              data={dmLogs}
              columns={dmColumns}
              onSort={handleSort}
              sortBy={sortBy}
              sortOrder={sortOrder}
            />
          )}
        </div>
      </div>

      {/* Refresh Button */}
      <div className="text-center">
        <button
          onClick={fetchLogs}
          className="btn-secondary"
          disabled={loading}
        >
          {loading ? '🔄 Refreshing...' : '🔄 Refresh Logs'}
        </button>
      </div>
    </div>
  )
}

export default LogsPage