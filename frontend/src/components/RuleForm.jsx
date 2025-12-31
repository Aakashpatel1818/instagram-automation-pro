import React, { useState } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { X, Save } from 'lucide-react'

function RuleForm({ onClose, onSubmit, initialData = null }) {
  const { register, control, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: initialData || {
      rule_name: '',
      keywords: [],
      comment_reply: '',
      toggle: {
        comment_only: false,
        send_dm: false,
        dm_message: ''
      },
      is_active: true
    }
  })

  const [keywordInput, setKeywordInput] = useState('')
  const [keywords, setKeywords] = useState(initialData?.keywords || [])
  const toggle = watch('toggle')
  const commentOnly = watch('toggle.comment_only')

  const handleAddKeyword = () => {
    if (keywordInput.trim() && !keywords.includes(keywordInput.trim())) {
      const newKeywords = [...keywords, keywordInput.trim()]
      setKeywords(newKeywords)
      setKeywordInput('')
    }
  }

  const handleRemoveKeyword = (keyword) => {
    setKeywords(keywords.filter(k => k !== keyword))
  }

  const handleFormSubmit = (data) => {
    onSubmit({ ...data, keywords })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">
            {initialData ? '✏️ Edit Rule' : '➕ Create New Rule'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X size={24} className="text-gray-600" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(handleFormSubmit)} className="p-6 space-y-6">
          {/* Rule Name */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📝 Rule Name
            </label>
            <input
              type="text"
              {...register('rule_name', { required: 'Rule name is required' })}
              placeholder="e.g., Lead Generation, Support Bot"
              className="input-field"
            />
            {errors.rule_name && (
              <p className="text-red-500 text-sm mt-1">{errors.rule_name.message}</p>
            )}
          </div>

          {/* Keywords */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🔑 Keywords (Trigger words)
            </label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddKeyword()}
                placeholder="Type keyword and press Enter"
                className="input-field flex-1"
              />
              <button
                type="button"
                onClick={handleAddKeyword}
                className="btn-primary"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {keywords.map((keyword) => (
                <div
                  key={keyword}
                  className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm flex items-center gap-2"
                >
                  {keyword}
                  <button
                    type="button"
                    onClick={() => handleRemoveKeyword(keyword)}
                    className="hover:text-primary-900"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Comment Reply */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              💬 Comment Reply Message
            </label>
            <textarea
              {...register('comment_reply', { required: 'Reply message is required' })}
              placeholder="What should we reply to the comment?"
              rows="3"
              className="input-field"
            />
            {errors.comment_reply && (
              <p className="text-red-500 text-sm mt-1">{errors.comment_reply.message}</p>
            )}
          </div>

          {/* Toggle Section */}
          <div className="border-2 border-primary-200 rounded-lg p-4 bg-primary-50">
            <h3 className="text-lg font-bold mb-4 text-gray-900">📨 DM Action</h3>

            {/* Comment Only Toggle */}
            <label className="flex items-center gap-3 mb-4 cursor-pointer hover:bg-white p-2 rounded transition-colors">
              <input
                type="checkbox"
                {...register('toggle.comment_only')}
                className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500 cursor-pointer"
              />
              <span className="font-semibold text-gray-900">
                ✅ Comment Only (Don't send DM)
              </span>
            </label>

            {/* Send DM Toggle - Only show if comment_only is false */}
            {!commentOnly && (
              <div className="ml-6 border-l-4 border-green-500 pl-4 space-y-4">
                <label className="flex items-center gap-3 cursor-pointer hover:bg-white p-2 rounded transition-colors">
                  <input
                    type="checkbox"
                    {...register('toggle.send_dm')}
                    className="w-5 h-5 text-green-600 rounded focus:ring-green-500 cursor-pointer"
                  />
                  <span className="font-semibold text-gray-900">
                    📲 Also Send Automatic DM
                  </span>
                </label>

                {/* DM Message - Only show if send_dm is true */}
                {toggle.send_dm && (
                  <div className="mt-3 p-3 bg-white rounded-lg border border-green-200">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      DM Message
                    </label>
                    <textarea
                      {...register('toggle.dm_message', {
                        validate: (value) => {
                          if (toggle.send_dm && !value.trim()) {
                            return 'DM message is required when Send DM is enabled'
                          }
                          return true
                        }
                      })}
                      placeholder="What DM message to send?"
                      rows="3"
                      className="input-field"
                    />
                    {errors.toggle?.dm_message && (
                      <p className="text-red-500 text-sm mt-1">{errors.toggle.dm_message.message}</p>
                    )}
                    <p className="text-xs text-gray-500 mt-2">
                      💡 This message will be sent via DM to the commenter
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Active Status */}
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              {...register('is_active')}
              className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500 cursor-pointer"
            />
            <span className="font-medium text-gray-700">🟢 Active</span>
          </label>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4 border-t border-gray-200">
            <button
              type="submit"
              className="btn-primary flex items-center gap-2 flex-1 justify-center"
            >
              <Save size={20} />
              {initialData ? 'Update Rule' : 'Create Rule'}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default RuleForm