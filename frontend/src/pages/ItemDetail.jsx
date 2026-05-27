import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getItem, rateItem, addToWishlist } from '../services/api'
import { useAuth } from '../context/AuthContext'
import StarRating from '../components/StarRating'

export default function ItemDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [item, setItem] = useState(null)
  const [userRating, setUserRating] = useState(0)
  const [review, setReview] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getItem(id)
      .then((r) => setItem(r.data.data))
      .finally(() => setLoading(false))
  }, [id])

  const handleRate = async () => {
    if (!userRating) return
    try {
      await rateItem({ item_id: id, score: userRating, review })
      setMessage('Rating saved!')
    } catch {
      setMessage('Failed to save rating.')
    }
  }

  const handleWishlist = async () => {
    try {
      await addToWishlist(Number(id))
      setMessage('Added to wishlist!')
    } catch {
      setMessage('Already in wishlist or error occurred.')
    }
  }

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>
  if (!item) return <div className="text-center py-20 text-gray-400">Item not found.</div>

  const details = item.details || {}
  const ratingInfo = item.rating_info || {}

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-400 hover:text-accent transition mb-6 text-sm"
      >
        ← Back
      </button>
      <div className="flex flex-col md:flex-row gap-8">
        {/* Cover */}
        <div className="w-full md:w-56 flex-shrink-0">
          <div className="bg-gray-800 rounded-lg h-72 flex items-center justify-center overflow-hidden">
            {item.cover_image ? (
              <img src={item.cover_image} alt={item.title} className="w-full h-full object-cover rounded-lg" />
            ) : (
              <span className="text-6xl">{item.category === 'movie' ? '🎬' : item.category === 'music' ? '🎵' : '📚'}</span>
            )}
          </div>
        </div>

        {/* Info */}
        <div className="flex-1">
          <div className="flex items-start justify-between gap-2 flex-wrap">
            <h1 className="text-2xl font-bold">{item.title}</h1>
            {item.is_ethiopian === 1 && (
              <span className="bg-gold text-black text-xs px-2 py-1 rounded font-semibold">🇪🇹 Ethiopian</span>
            )}
          </div>

          <div className="flex gap-3 text-sm text-gray-400 mt-1 flex-wrap">
            <span className="capitalize">{item.category}</span>
            {item.genre && <span>{item.genre}</span>}
            {item.release_year && <span>{item.release_year}</span>}
            {item.language && <span>{item.language}</span>}
          </div>

          {ratingInfo.avg_rating && (
            <div className="flex items-center gap-2 mt-2">
              <span className="text-gold text-lg">★ {Number(ratingInfo.avg_rating).toFixed(1)}</span>
              <span className="text-gray-500 text-sm">({ratingInfo.total} ratings)</span>
            </div>
          )}

          <p className="text-gray-300 mt-4 text-sm leading-relaxed">{item.description}</p>

          {/* Category-specific details */}
          <div className="mt-4 text-sm text-gray-400 flex flex-col gap-1">
            {details.author && <span>Author: <span className="text-white">{details.author}</span></span>}
            {details.director && <span>Director: <span className="text-white">{details.director}</span></span>}
            {details.artist && <span>Artist: <span className="text-white">{details.artist}</span></span>}
            {details.album && <span>Album: <span className="text-white">{details.album}</span></span>}
            {details.ethiopian_genre && (
              <span>Ethiopian Genre: <span className="text-gold">{details.ethiopian_genre}</span></span>
            )}
          </div>

          {/* Actions */}
          {user && (
            <div className="mt-6 flex flex-col gap-3">
              <div>
                <p className="text-sm text-gray-400 mb-1">Your Rating:</p>
                <StarRating value={userRating} onChange={setUserRating} />
              </div>
              <textarea
                placeholder="Write a review (optional)"
                value={review}
                onChange={(e) => setReview(e.target.value)}
                rows={2}
                className="bg-primary border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-accent resize-none"
              />
              <div className="flex gap-3">
                <button
                  onClick={handleRate}
                  className="bg-accent px-4 py-2 rounded text-sm font-semibold hover:opacity-80 transition"
                >
                  Submit Rating
                </button>
                <button
                  onClick={handleWishlist}
                  className="border border-gray-600 px-4 py-2 rounded text-sm hover:border-accent transition"
                >
                  + Wishlist
                </button>
              </div>
              {message && <p className="text-green-400 text-sm">{message}</p>}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
