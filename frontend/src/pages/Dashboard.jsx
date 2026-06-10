import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getRecommendations, getMyRatings } from '../services/api'
import ItemCard from '../components/ItemCard'

const CATEGORIES = ['all', 'movie', 'music', 'book']

export default function Dashboard() {
  const { user } = useAuth()
  const [recs, setRecs] = useState([])
  const [recType, setRecType] = useState('personalized')
  const [ratings, setRatings] = useState([])
  const [activeCategory, setActiveCategory] = useState('all')
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)

  useEffect(() => {
    setRecs([])
    setPage(1)
  }, [activeCategory])

  useEffect(() => {
    const params = activeCategory !== 'all' ? { category: activeCategory, page } : { page }
    setLoading(true)
    getRecommendations(params)
      .then((r) => {
        const items = r.data.data.items || []
        setRecs((prev) => page === 1 ? items : [...prev, ...items])
        setRecType(r.data.data.type)
      })
      .finally(() => setLoading(false))
  }, [activeCategory, page])

  useEffect(() => {
    getMyRatings().then((r) => setRatings(r.data.data || []))
  }, [])

  const loadMore = () => setPage((p) => p + 1)

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-1">
        Welcome back, {user?.username} 👋
      </h1>
      <p className="text-gray-400 text-sm mb-6">
        {recType === 'popular'
          ? 'Rate more items to unlock personalized recommendations.'
          : 'Your personalized picks are ready.'}
      </p>

      {/* Category filter */}
      <div className="flex gap-2 mb-6">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-1.5 rounded-full text-sm capitalize transition ${
              activeCategory === cat
                ? 'bg-accent text-white'
                : 'bg-secondary border border-gray-700 hover:border-accent'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Recommendations */}
      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-4">
          {recType === 'popular' ? '🔥 Trending' : '✨ Recommended for You'}
        </h2>
        {loading && page === 1 ? (
          <p className="text-gray-500">Loading...</p>
        ) : recs.length === 0 ? (
          <p className="text-gray-500 text-sm">No recommendations yet. Start rating items!</p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
            {recs.map((item) => <ItemCard key={item.id} item={item} />)}
          </div>
        )}
        {!loading && recs.length > 0 && recs.length % 20 === 0 && (
          <div className="text-center mt-6">
            <button
              onClick={loadMore}
              className="bg-secondary border border-gray-600 px-8 py-2 rounded-full hover:border-accent transition text-sm"
            >
              → Load More
            </button>
          </div>
        )}
        {loading && page > 1 && (
          <p className="text-center text-gray-500 mt-4 text-sm">Loading more...</p>
        )}
      </section>

      {/* Explore More */}
      <section className="mb-10">
        <div className="bg-secondary rounded-xl px-6 py-5 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold mb-1">🔍 Explore More</h2>
            <p className="text-gray-400 text-sm">Browse all movies, music, and books — or discover Ethiopian content.</p>
          </div>
          <div className="flex gap-3">
            <Link to="/browse" className="bg-accent px-5 py-2 rounded-full text-sm font-semibold hover:opacity-80 transition">
              Browse All
            </Link>
            <Link to="/ethiopian" className="border border-yellow-400 text-yellow-400 px-5 py-2 rounded-full text-sm font-semibold hover:bg-yellow-400 hover:text-black transition">
              🇪🇹 Ethiopian
            </Link>
          </div>
        </div>
      </section>

      {/* Recent ratings */}
      <section>
        <h2 className="text-lg font-semibold mb-4">⭐ Your Recent Ratings</h2>
        {ratings.length === 0 ? (
          <p className="text-gray-500 text-sm">You haven't rated anything yet.</p>
        ) : (
          <div className="flex flex-col gap-2">
            {ratings.slice(0, 5).map((r) => (
              <div key={r.id} className="bg-secondary px-4 py-3 rounded-lg flex justify-between items-center">
                <span className="text-sm">{r.title}</span>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-gray-400 capitalize">{r.category}</span>
                  <span className="text-gold text-sm">{'★'.repeat(r.score)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
