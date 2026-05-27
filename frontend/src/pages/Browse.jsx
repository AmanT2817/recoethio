import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getItems } from '../services/api'
import ItemCard from '../components/ItemCard'

const CATEGORIES = [
  { key: 'movie', label: '🎬 Movies' },
  { key: 'music', label: '🎵 Music' },
  { key: 'book',  label: '📚 Books' },
]

export default function Browse() {
  const { category } = useParams()
  const navigate = useNavigate()
  const [items, setItems] = useState([])
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [hasMore, setHasMore] = useState(true)
  const LIMIT = 24

  const activeCategory = category || 'movie'

  useEffect(() => {
    setItems([])
    setPage(1)
    setHasMore(true)
  }, [activeCategory])

  useEffect(() => {
    setLoading(true)
    getItems({ category: activeCategory, page, limit: LIMIT })
      .then((r) => {
        const data = r.data.data || []
        setItems((prev) => page === 1 ? data : [...prev, ...data])
        setHasMore(data.length === LIMIT)
      })
      .finally(() => setLoading(false))
  }, [activeCategory, page])

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Category tabs */}
      <div className="flex gap-3 mb-8">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.key}
            onClick={() => navigate(`/browse/${cat.key}`)}
            className={`px-5 py-2 rounded-full font-semibold text-sm transition ${
              activeCategory === cat.key
                ? 'bg-accent text-white'
                : 'bg-secondary border border-gray-700 hover:border-accent'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      <h1 className="text-2xl font-bold mb-6 capitalize">
        {CATEGORIES.find(c => c.key === activeCategory)?.label}
      </h1>

      {/* Grid */}
      {items.length === 0 && !loading ? (
        <p className="text-gray-500">No items found.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {items.map((item) => <ItemCard key={item.id} item={item} />)}
        </div>
      )}

      {loading && (
        <div className="text-center py-8 text-gray-400">Loading...</div>
      )}

      {/* Load more */}
      {!loading && hasMore && (
        <div className="text-center mt-8">
          <button
            onClick={() => setPage((p) => p + 1)}
            className="bg-secondary border border-gray-600 px-8 py-2 rounded-full hover:border-accent transition"
          >
            Load More
          </button>
        </div>
      )}
    </div>
  )
}
