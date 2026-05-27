import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getItems } from '../services/api'
import { useAuth } from '../context/AuthContext'
import ItemCard from '../components/ItemCard'

export default function Home() {
  const { user } = useAuth()
  const [movies, setMovies] = useState([])
  const [music, setMusic] = useState([])
  const [books, setBooks] = useState([])

  useEffect(() => {
    getItems({ category: 'movie', limit: 6 }).then((r) => setMovies(r.data.data || []))
    getItems({ category: 'music', limit: 6 }).then((r) => setMusic(r.data.data || []))
    getItems({ category: 'book', limit: 6 }).then((r) => setBooks(r.data.data || []))
  }, [])

  const Section = ({ title, items }) => (
    <section className="mb-10">
      <h2 className="text-xl font-bold mb-4 text-accent">{title}</h2>
      {items.length === 0 ? (
        <p className="text-gray-500 text-sm">No content yet.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
          {items.map((item) => <ItemCard key={item.id} item={item} />)}
        </div>
      )}
    </section>
  )

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Hero */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-3">
          Discover Movies, Music & Books
        </h1>
        <p className="text-gray-400 mb-6 max-w-xl mx-auto">
          AI-powered recommendations tailored to your taste — including Ethiopian content.
        </p>
        <div className="flex gap-3 justify-center">
          {user ? (
            <Link
              to="/dashboard"
              className="bg-accent px-6 py-2 rounded-lg font-semibold hover:opacity-80 transition"
            >
              Go to Dashboard
            </Link>
          ) : (
            <Link
              to="/register"
              className="bg-accent px-6 py-2 rounded-lg font-semibold hover:opacity-80 transition"
            >
              Get Started
            </Link>
          )}
          <Link
            to="/search"
            className="border border-gray-600 px-6 py-2 rounded-lg hover:border-accent transition"
          >
            Browse Content
          </Link>
        </div>
      </div>

      <Section title="🎬 Popular Movies" items={movies} />
      <Section title="🎵 Popular Music" items={music} />
      <Section title="📚 Popular Books" items={books} />
    </div>
  )
}
