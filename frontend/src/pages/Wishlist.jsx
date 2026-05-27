import { useEffect, useState } from 'react'
import { getWishlist, removeFromWishlist } from '../services/api'
import { Link } from 'react-router-dom'

export default function Wishlist() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getWishlist()
      .then((r) => setItems(r.data.data || []))
      .finally(() => setLoading(false))
  }, [])

  const handleRemove = async (item_id) => {
    await removeFromWishlist(item_id)
    setItems((prev) => prev.filter((i) => i.item_id !== item_id))
  }

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">My Wishlist</h1>

      {items.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          <p className="text-4xl mb-3">📋</p>
          <p>Your wishlist is empty.</p>
          <Link to="/search" className="text-accent hover:underline text-sm mt-2 inline-block">
            Browse content to add items
          </Link>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {items.map((item) => (
            <div
              key={item.id}
              className="bg-secondary rounded-lg px-4 py-3 flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gray-800 rounded flex items-center justify-center text-lg flex-shrink-0">
                  {item.cover_image
                    ? <img src={item.cover_image} alt="" className="w-full h-full object-cover rounded" />
                    : item.category === 'movie' ? '🎬' : item.category === 'music' ? '🎵' : '📚'}
                </div>
                <div>
                  <Link to={`/items/${item.item_id}`} className="font-medium hover:text-accent transition text-sm">
                    {item.title}
                  </Link>
                  <p className="text-xs text-gray-500 capitalize">{item.category}</p>
                </div>
              </div>
              <button
                onClick={() => handleRemove(item.item_id)}
                className="text-gray-500 hover:text-red-400 transition text-sm"
                aria-label="Remove from wishlist"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
