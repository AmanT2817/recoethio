import { Link } from 'react-router-dom'

const categoryIcon = { movie: '🎬', music: '🎵', book: '📚' }

export default function ItemCard({ item }) {
  return (
    <Link
      to={`/items/${item.id}`}
      className="bg-secondary rounded-lg overflow-hidden hover:scale-105 transition-transform duration-200 shadow-md flex flex-col"
    >
      <div className="h-48 bg-gray-800 flex items-center justify-center overflow-hidden">
        {item.cover_image ? (
          <img
            src={item.cover_image}
            alt={item.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-5xl">{categoryIcon[item.category] || '🎭'}</span>
        )}
      </div>

      <div className="p-3 flex flex-col gap-1 flex-1">
        <h3 className="font-semibold text-sm line-clamp-2">{item.title}</h3>
        <div className="flex items-center justify-between mt-auto pt-2">
          <span className="text-xs text-gray-400 capitalize">{item.category}</span>
          {item.is_ethiopian === 1 && (
            <span className="text-xs bg-gold text-black px-1.5 py-0.5 rounded font-medium">
              🇪🇹 Ethiopian
            </span>
          )}
        </div>
        {item.genre && (
          <span className="text-xs text-gray-500">{item.genre}</span>
        )}
        {item.avg_score && (
          <span className="text-xs text-gold">★ {Number(item.avg_score).toFixed(1)}</span>
        )}
      </div>
    </Link>
  )
}
