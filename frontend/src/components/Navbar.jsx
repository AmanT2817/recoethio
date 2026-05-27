import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logoutUser } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logoutUser()
    navigate('/')
  }

  return (
    <nav className="bg-secondary px-6 py-3 flex items-center justify-between shadow-lg">
      <Link to="/" className="text-accent font-bold text-xl tracking-wide">
        🎬 RecoEthio
      </Link>

      <div className="flex items-center gap-4 text-sm">
        <Link to="/browse/movie" className="hover:text-accent transition">Movies</Link>
        <Link to="/browse/music" className="hover:text-accent transition">Music</Link>
        <Link to="/browse/book" className="hover:text-accent transition">Books</Link>
        <Link to="/search" className="hover:text-accent transition">Search</Link>

        {user ? (
          <>
            <Link to="/dashboard" className="hover:text-accent transition">Dashboard</Link>
            <Link to="/wishlist" className="hover:text-accent transition">Wishlist</Link>
            {user.role === 'admin' && (
              <Link to="/admin" className="hover:text-gold transition">Admin</Link>
            )}
            <button
              onClick={handleLogout}
              className="bg-accent px-3 py-1 rounded hover:opacity-80 transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-accent transition">Login</Link>
            <Link
              to="/register"
              className="bg-accent px-3 py-1 rounded hover:opacity-80 transition"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
