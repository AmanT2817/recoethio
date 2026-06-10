import { useEffect, useState } from 'react'
import { getItems } from '../services/api'
import ItemCard from '../components/ItemCard'

const CATS = [
  { key: 'all', label: 'All Ethiopian' },
  { key: 'movie', label: '🎬 Movies' },
  { key: 'music', label: '🎵 Music' },
  { key: 'book', label: '📚 Books' },
]

export default function Ethiopian() {
  const [items, setItems] = useState([])
  const [cat, setCat] = useState('all')
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const [loading, setLoading] = useState(true)
  const LIMIT = 24

  useEffect(() => {
    setItems([]); setPage(1); setHasMore(true)
  }, [cat])

  useEffect(() => {
    setLoading(true)
    const params = { ethiopian: 1, limit: LIMIT, page }
    if (cat !== 'all') params.category = cat
    getItems(params).then((r) => {
      const data = r.data.data || []
      setItems((prev) => page === 1 ? data : [...prev, ...data])
      setHasMore(data.length === LIMIT)
    }).finally(() => setLoading(false))
  }, [cat, page])

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-1">🇪🇹 Ethiopian Content</h1>
        <p className="text-gray-400 text-sm">Discover movies, music, and books from Ethiopia</p>
      </div>
      <div className="flex gap-3 mb-8 flex-wrap">
        {CATS.map((c) => (
          <button key={c.key} onClick={() => setCat(c.key)}
            className={`px-5 py-2 rounded-full font-semibold text-sm transition ${cat === c.key ? 'bg-yellow-400 text-black' : 'bg-secondary border border-gray-700 hover:border-yellow-400'}`}>
            {c.label}
          </button>
        ))}
      </div>
      {items.length === 0 && !loading ? (
        <p className="text-gray-500">No Ethiopian content found.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {items.map((item) => <ItemCard key={item.id} item={item} />)}
        </div>
      )}
      {loading && <div className="text-center py-8 text-gray-400">Loading...</div>}
      {!loading && hasMore && (
        <div className="text-center mt-8">
          <button onClick={() => setPage((p) => p + 1)}
            className="bg-secondary border border-gray-600 px-8 py-2 rounded-full hover:border-yellow-400 transition">
            Load More
          </button>
        </div>
      )}
    </div>
  )
}
