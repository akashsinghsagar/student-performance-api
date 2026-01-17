/**
 * Navigation Component
 * 
 * Provides the top navigation bar for the application with:
 * - Brand logo and name
 * - Links to all major pages (Home, Predict, Analytics)
 * - Active page highlighting
 * - Responsive mobile menu (hamburger on small screens)
 */

import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import '../styles/navigation.css'

export default function Navigation() {
  // Track whether mobile menu is open/closed
  const [isOpen, setIsOpen] = useState(false)
  
  // Get current page location for active link highlighting
  const location = useLocation()

  /**
   * Check if a given path matches the current page
   * Returns 'active' class if path matches, empty string otherwise
   */
  const isActive = (path) => {
    return location.pathname === path ? 'active' : ''
  }

  return (
    <nav className="navbar">
      <div className="nav-container">
        {/* Brand logo - clicking takes user to home page */}
        <Link to="/" className="nav-brand">
          <span className="brand-icon">📚</span>
          <span className="brand-text">GradePredictor</span>
        </Link>

        {/* Hamburger menu button - only visible on mobile devices */}
        <button 
          className="hamburger"
          onClick={() => setIsOpen(!isOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        {/* Navigation links - becomes dropdown on mobile when hamburger is clicked */}
        <ul className={`nav-menu ${isOpen ? 'active' : ''}`}>
          <li className="nav-item">
            <Link to="/" className={`nav-link ${isActive('/')}`}>
              <span className="nav-icon">🏠</span>
              <span>Home</span>
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/predict" className={`nav-link ${isActive('/predict')}`}>
              <span className="nav-icon">⚡</span>
              <span>Predict</span>
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/analytics" className={`nav-link ${isActive('/analytics')}`}>
              <span className="nav-icon">📊</span>
              <span>Analytics</span>
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}
