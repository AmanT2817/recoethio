import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const PREFERENCES = {
  '🎬 Movies': ['Action','Thriller','Sci-Fi','Romance','Comedy','Drama','Horror','Documentary','Animation','Historical','Ethiopian Drama','Ethiopian Comedy','Ethiopian Romance'],
  '🎵 Music': ['Pop','Rock','Hip Hop','Jazz','Classical','R&B','Electronic','Folk','Tizita','Bati','Ambassel','Anchihoye','Ethio-Jazz','Oromo Music','Tigrinya Music','Amharic Contemporary'],
  '📚 Books': ['Fiction','Mystery','Fantasy','Biography','History','Self-Help','Science','Romance','Thriller','Amharic Literature','Ethiopian History','Ethiopian Fiction'],
}

const ETHIOPIAN_TAGS = ['Tizita','Bati','Ambassel','Anchihoye','Ethio-Jazz','Oromo Music','Tigrinya Music','Amharic Contemporary','Ethiopian Drama','Ethiopian Comedy','Ethiopian Romance','Amharic Literature','Ethiopian History','Ethiopian Fiction']

export default function Onboarding() {
  const [selected, setSelected] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const toggle = (pref) => setSelected((prev) => prev.includes(pref) ? prev.filter((p) => p !== pref) : [...prev, pref])

  const handleSubmit = async () => {
    if (selected.length < 3) { setError('Please select at least 3 preferences.'); return }
    setLoading(true); setError('')
    try {
      await api.post('/auth/onboarding', { preferences: selected })
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.message || 'Something went wrong.')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-primary px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold mb-2">What do you like?</h1>
          <p className="text-gray-400">Pick at least <span className="text-accent font-semibold">3 categories</span> to personalize your experience.</p>
          <div className="mt-3 text-sm text-gray-500">{selected.length} selected {selected.length >= 3 && <span className="text-green-400"> ✓ Ready!</span>}</div>
        </div>
        {Object.entries(PREFERENCES).map(([category, tags]) => (
          <div key={category} className="mb-8">
            <h2 className="text-lg font-semibold mb-4 text-accent">{category}</h2>
            <div className="flex flex-wrap gap-3">
              {tags.map((tag) => {
                const isSelected = selected.includes(tag)
                const isEt = ETHIOPIAN_TAGS.includes(tag)
                return (
                  <button key={tag} onClick={() => toggle(tag)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-150 border ${isSelected ? 'bg-accent border-accent text-white scale-105 shadow-lg' : isEt ? 'border-yellow-400 text-yellow-400 hover:bg-yellow-400 hover:text-black' : 'border-gray-600 text-gray-300 hover:border-gray-400 hover:text-white'}`}>
                    {isEt && !isSelected && '🇪🇹 '}{tag}
                  </button>
                )
              })}
            </div>
          </div>
        ))}
        {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}
        <div className="text-center mt-6">
          <button onClick={handleSubmit} disabled={loading || selected.length < 3}
            className="bg-accent px-10 py-3 rounded-full font-bold text-lg hover:opacity-90 transition disabled:opacity-40 disabled:cursor-not-allowed">
            {loading ? 'Saving...' : 'Start Discovering →'}
          </button>
        </div>
      </div>
    </div>
  )
}
