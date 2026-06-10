import { useState } from 'react'
import { useNavigate, Link, useSearchParams } from 'react-router-dom'
import { login } from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { loginUser } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await login(form)
      const { token, user } = res.data.data
      loginUser(token, user)
      const isNew = searchParams.get('new') === '1'
      navigate(isNew ? '/onboarding' : (user.role === 'admin' ? '/admin' : '/dashboard'))
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="bg-secondary p-8 rounded-xl w-full max-w-md shadow-xl">
        <h1 className="text-2xl font-bold mb-6 text-center">Welcome Back</h1>

        {error && (
          <div className="bg-red-900/40 border border-red-500 text-red-300 px-4 py-2 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
            className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
          />
          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
            className="bg-primary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-accent py-2 rounded font-semibold hover:opacity-80 transition disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-400 mt-4">
          Don't have an account?{' '}
          <Link to="/register" className="text-accent hover:underline">Register</Link>
        </p>
      </div>
    </div>
  )
}
