import React, { useState, useEffect } from 'react'
import { Plus, AlertCircle } from 'lucide-react'
import RuleForm from '../components/RuleForm'
import RuleCard from '../components/RuleCard'
import { rules } from '../services/api'

function RulesPage() {
  const [rulesList, setRulesList] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingRule, setEditingRule] = useState(null)
  const [filterActive, setFilterActive] = useState('all')

  useEffect(() => {
    fetchRules()
  }, [])

  const fetchRules = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await rules.getAll()
      setRulesList(response.data.rules || [])
    } catch (err) {
      setError('Failed to load rules')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRule = async (formData) => {
    try {
      if (editingRule) {
        await rules.update(editingRule.id, formData)
      } else {
        await rules.create(formData)
      }
      await fetchRules()
      setShowForm(false)
      setEditingRule(null)
    } catch (err) {
      setError('Failed to save rule')
      console.error(err)
    }
  }

  const handleDeleteRule = async (id) => {
    if (confirm('Are you sure you want to delete this rule?')) {
      try {
        await rules.delete(id)
        await fetchRules()
      } catch (err) {
        setError('Failed to delete rule')
        console.error(err)
      }
    }
  }

  const handleEditRule = (rule) => {
    setEditingRule(rule)
    setShowForm(true)
  }

  const filteredRules = rulesList.filter(rule => {
    if (filterActive === 'active') return rule.is_active
    if (filterActive === 'inactive') return !rule.is_active
    return true
  })

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-gray-900">⚙️ Automation Rules</h1>
          <p className="text-gray-600 mt-2">Create and manage your Instagram automation rules with toggle features.</p>
        </div>
        <button
          onClick={() => {
            setEditingRule(null)
            setShowForm(true)
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus size={20} />
          New Rule
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      {/* Filter Buttons */}
      <div className="flex gap-2">
        {['all', 'active', 'inactive'].map((status) => (
          <button
            key={status}
            onClick={() => setFilterActive(status)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filterActive === status
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {status === 'all' ? '📋 All' : status === 'active' ? '🟢 Active' : '🔴 Inactive'}
          </button>
        ))}
      </div>

      {/* Rules Grid */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin">
            <div className="w-12 h-12 border-4 border-gray-300 border-t-primary-600 rounded-full"></div>
          </div>
          <p className="text-gray-600 mt-4">Loading rules...</p>
        </div>
      ) : filteredRules.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredRules.map((rule) => (
            <RuleCard
              key={rule.id}
              rule={rule}
              onEdit={handleEditRule}
              onDelete={handleDeleteRule}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 card">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No rules yet</h3>
          <p className="text-gray-600 mb-6">
            {filterActive === 'all'
              ? 'Create your first automation rule to get started!'
              : `No ${filterActive} rules found`}
          </p>
          {filterActive === 'all' && (
            <button
              onClick={() => {
                setEditingRule(null)
                setShowForm(true)
              }}
              className="btn-primary"
            >
              Create First Rule
            </button>
          )}
        </div>
      )}

      {/* Rule Form Modal */}
      {showForm && (
        <RuleForm
          initialData={editingRule}
          onClose={() => {
            setShowForm(false)
            setEditingRule(null)
          }}
          onSubmit={handleCreateRule}
        />
      )}
    </div>
  )
}

export default RulesPage