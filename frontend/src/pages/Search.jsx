import { useState } from 'react'
import { searchItems } from '../services/api'
import ItemCard from '../components/ItemCard'

export default function Search() {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('')
  const [ethiopianOnly, setEthiopianOnly] = useState(false)
  const [results, setResults] = useState([])
  const [searched, setSearched] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setSearched(true)
    try {
      const params = { q: query }
      if (category) params.category = category
      if (ethiopianOnly) params.ethiopian = 1
      const res = await searchItems(params)
      setResults(res.data.data || [])
    } catch {
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Search Content</h1>

      <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3 mb-6">
        <input
          type="text"
          placeholder="Search movies, music, books..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 bg-secondary border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-accent"
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="bg-secondary border border-gray-700 rounded px-3 py-2 focus:outline-none focus:border-accent"
        >
          <option value="">All Categories</option>
          <option value="movie">Movies</option>
          <option value="music">Music</option>
          <option value="book">Books</option>
        </select>
        <label className="flex items-center gap-2 text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={ethiopianOnly}
            onChange={(e) => setEthiopianOnly(e.target.checked)}
            className="accent-gold"
          />
          🇪🇹 Ethiopian only
        </label>
        <button
          type="submit"
          className="bg-accent px-6 py-2 rounded font-semibold hover:opacity-80 transition"
        >
          Search
        </button>
      </form>

      {loading && <p className="text-gray-400">Searching...</p>}

      {!loading && searched && results.length === 0 && (
        <p className="text-gray-500">No results found for "{query}".</p>
      )}

      {results.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {results.map((item) => <ItemCard key={item.id} item={item} />)}
        </div>
      )}
    </div>
  )
}
