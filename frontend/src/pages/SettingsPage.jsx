import React, { useState } from 'react'
import { Save } from 'lucide-react'

function SettingsPage() {
  const [settings, setSettings] = useState({
    instagramAccountId: '',
    accessToken: '',
    webhookVerifyToken: '',
    autoReplyDelay: 0,
    maxRulesPerDay: 1000,
    enableNotifications: true,
  })

  const [saved, setSaved] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSave = () => {
    // TODO: Save settings to backend
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900">⚙️ Settings</h1>
        <p className="text-gray-600 mt-2">Configure your Instagram Automation Pro account.</p>
      </div>

      {/* Success Message */}
      {saved && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          ✅ Settings saved successfully!
        </div>
      )}

      {/* Settings Sections */}
      <div className="space-y-6">
        {/* Instagram API Section */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🔑 Instagram API Configuration</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Business Account ID
              </label>
              <input
                type="text"
                name="instagramAccountId"
                value={settings.instagramAccountId}
                onChange={handleChange}
                placeholder="Your Instagram Business Account ID"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Access Token
              </label>
              <input
                type="password"
                name="accessToken"
                value={settings.accessToken}
                onChange={handleChange}
                placeholder="Your Meta Access Token"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Webhook Verify Token
              </label>
              <input
                type="password"
                name="webhookVerifyToken"
                value={settings.webhookVerifyToken}
                onChange={handleChange}
                placeholder="Your Webhook Verify Token"
                className="input-field"
              />
            </div>
          </div>
        </div>

        {/* Automation Settings */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🤖 Automation Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Auto-Reply Delay (seconds)
              </label>
              <input
                type="number"
                name="autoReplyDelay"
                value={settings.autoReplyDelay}
                onChange={handleChange}
                min="0"
                max="300"
                className="input-field"
              />
              <p className="text-xs text-gray-500 mt-1">
                Delay before responding to comments (0-300 seconds)
              </p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Max Rules Per Day
              </label>
              <input
                type="number"
                name="maxRulesPerDay"
                value={settings.maxRulesPerDay}
                onChange={handleChange}
                min="1"
                className="input-field"
              />
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🔔 Notifications</h2>
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              name="enableNotifications"
              checked={settings.enableNotifications}
              onChange={handleChange}
              className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500 cursor-pointer"
            />
            <span className="font-medium text-gray-700">Enable Email Notifications</span>
          </label>
          <p className="text-xs text-gray-500 mt-3">
            Get notifications when automation rules are triggered
          </p>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button onClick={handleSave} className="btn-primary flex items-center gap-2">
          <Save size={20} />
          Save Settings
        </button>
      </div>
    </div>
  )
}

export default SettingsPage