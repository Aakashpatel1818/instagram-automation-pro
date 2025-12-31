import React from 'react'
import { Edit2, Trash2, MessageCircle, Send } from 'lucide-react'

function RuleCard({ rule, onEdit, onDelete }) {
  return (
    <div className="card p-6 border-l-4 border-primary-600">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900">{rule.rule_name}</h3>
          <p className="text-sm text-gray-500 mt-1">
            {rule.is_active ? '🟢 Active' : '🔴 Inactive'}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(rule)}
            className="p-2 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors"
            title="Edit rule"
          >
            <Edit2 size={18} />
          </button>
          <button
            onClick={() => onDelete(rule.id)}
            className="p-2 hover:bg-red-100 text-red-600 rounded-lg transition-colors"
            title="Delete rule"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>

      {/* Keywords */}
      <div className="mb-4">
        <p className="text-xs font-semibold text-gray-600 mb-2">🔑 Keywords:</p>
        <div className="flex flex-wrap gap-2">
          {rule.keywords.map((keyword) => (
            <span
              key={keyword}
              className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded"
            >
              {keyword}
            </span>
          ))}
        </div>
      </div>

      {/* Comment Reply */}
      <div className="mb-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-xs font-semibold text-gray-600 flex items-center gap-1 mb-1">
          <MessageCircle size={14} /> Comment Reply:
        </p>
        <p className="text-sm text-gray-700">{rule.comment_reply}</p>
      </div>

      {/* Toggle Status */}
      <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
        <div className={`p-3 rounded-lg ${
          rule.toggle.comment_only
            ? 'bg-orange-100 text-orange-700'
            : 'bg-blue-100 text-blue-700'
        }`}>
          <p className="font-semibold text-xs">Mode</p>
          <p className="text-sm mt-1">
            {rule.toggle.comment_only ? '📝 Comment Only' : '📝 + 📲 Comment + DM'}
          </p>
        </div>
        <div className={`p-3 rounded-lg ${
          rule.toggle.send_dm && !rule.toggle.comment_only
            ? 'bg-green-100 text-green-700'
            : 'bg-gray-100 text-gray-700'
        }`}>
          <p className="font-semibold text-xs">DM Status</p>
          <p className="text-sm mt-1">
            {rule.toggle.send_dm && !rule.toggle.comment_only ? '✅ Enabled' : '❌ Disabled'}
          </p>
        </div>
      </div>

      {/* DM Message Preview */}
      {rule.toggle.send_dm && !rule.toggle.comment_only && (
        <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-xs font-semibold text-green-700 flex items-center gap-1 mb-1">
            <Send size={14} /> DM Message:
          </p>
          <p className="text-sm text-green-800">{rule.toggle.dm_message}</p>
        </div>
      )}
    </div>
  )
}

export default RuleCard