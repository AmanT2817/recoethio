import { useEffect, useState } from 'react'
import { adminStats, adminListUsers, adminDeleteUser, adminAddItem } from '../services/api'

const EMPTY_ITEM = {
  title: '', description: '', category: 'movie', genre: '',
  release_year: '', language: 'English', cover_image: '', is_ethiopian: false
}

export default function AdminPanel() {
  const [stats, setStats] = useState(null)
  const [users, setUsers] = useState([])
  const [tab, setTab] = useState('stats')
  const [form, setForm] = useState(EMPTY_ITEM)
  const [message, setMessage] = useState('')

  useEffect(() => {
    adminStats().then((r) => setStats(r.data.data))
    adminListUsers().then((r) => setUsers(r.data.data || []))
  }, [])

  const handleDeleteUser = async (id) => {
    if (!window.confirm('Delete this user?')) return
    await adminDeleteUser(id)
    setUsers((prev) => prev.filter((u) => u.id !== id))
  }

  const handleAddItem = async (e) => {
    e.preventDefault()
    setMessage('')
    try {
      await adminAddItem(form)
      setMessage('Item added successfully!')
      setForm(EMPTY_ITEM)
    } catch (err) {
      setMessage(err.response?.data?.message || 'Failed to add item.')
    }
  }

  const tabs = ['stats', 'users', 'add content']

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Admin Panel</h1>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded-full text-sm capitalize transition ${
              tab === t ? 'bg-accent' : 'bg-secondary border border-gray-700 hover:border-accent'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Stats */}
      {tab === 'stats' && stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-secondary rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-accent">{stats.users?.total_users || 0}</p>
            <p className="text-sm text-gray-400 mt-1">Total Users</p>
          </div>
          <div className="bg-secondary rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-accent">{stats.ratings?.total_ratings || 0}</p>
            <p className="text-sm text-gray-400 mt-1">Total Ratings</p>
          </div>
          {(stats.items || []).map((cat) => (
            <div key={cat.category} className="bg-secondary rounded-lg p-4 text-center">
              <p className="text-3xl font-bold text-gold">{cat.count}</p>
              <p className="text-sm text-gray-400 mt-1 capitalize">{cat.category}s</p>
            </div>
          ))}
        </div>
      )}

      {/* Users */}
      {tab === 'users' && (
        <div className="flex flex-col gap-2">
          {users.map((u) => (
            <div key={u.id} className="bg-secondary rounded-lg px-4 py-3 flex justify-between items-center">
              <div>
                <p className="font-medium text-sm">{u.username}</p>
                <p className="text-xs text-gray-400">{u.email} · {u.role}</p>
              </div>
              {u.role !== 'admin' && (
                <button
                  onClick={() => handleDeleteUser(u.id)}
                  className="text-red-400 hover:text-red-300 text-sm transition"
                >
                  Delete
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Add Content */}
      {tab === 'add content' && (
        <form onSubmit={handleAddItem} className="flex flex-col gap-4 max-w-lg">
          {message && (
            <div className={`px-4 py-2 rounded text-sm ${message.includes('success') ? 'bg-green-900/40 text-green-300' : 'bg-red-900/40 text-red-300'}`}>
              {message}
            </div>
          )}
          <input
            placeholder="Title *"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            required
            className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
          />
          <textarea
            placeholder="Description"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            rows={3}
            className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent resize-none"
          />
          <div className="grid grid-cols-2 gap-3">
            <select
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
              className="bg-primary border border-gray-700 rounded px-3 py-2 focus:outline-none focus:border-accent"
            >
              <option value="movie">Movie</option>
              <option value="music">Music</option>
              <option value="book">Book</option>
            </select>
            <input
              placeholder="Genre"
              value={form.genre}
              onChange={(e) => setForm({ ...form, genre: e.target.value })}
              className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
            />
            <input
              placeholder="Release Year"
              type="number"
              value={form.release_year}
              onChange={(e) => setForm({ ...form, release_year: e.target.value })}
              className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
            />
            <input
              placeholder="Language"
              value={form.language}
              onChange={(e) => setForm({ ...form, language: e.target.value })}
              className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
            />
          </div>
          <input
            placeholder="Cover Image URL"
            value={form.cover_image}
            onChange={(e) => setForm({ ...form, cover_image: e.target.value })}
            className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
          />
          <label className="flex items-center gap-2 text-sm cursor-pointer">
            <input
              type="checkbox"
              checked={form.is_ethiopian}
              onChange={(e) => setForm({ ...form, is_ethiopian: e.target.checked })}
              className="accent-gold"
            />
            🇪🇹 Mark as Ethiopian content
          </label>
          <button
            type="submit"
            className="bg-accent py-2 rounded font-semibold hover:opacity-80 transition"
          >
            Add Item
          </button>
        </form>
      )}
    </div>
  )
}
