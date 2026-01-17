/**
 * Main Application Component
 * 
 * This is the root component that sets up routing for the entire application.
 * It includes navigation, page routes, and a footer.
 */

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import Home from './pages/Home'
import Predict from './pages/Predict'
import Results from './pages/Results'
import Analytics from './pages/Analytics'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        {/* Top navigation bar - visible on all pages */}
        <Navigation />
        
        {/* Main content area where pages are rendered */}
        <main className="main-content">
          <Routes>
            {/* Home page - landing page with features and CTA */}
            <Route path="/" element={<Home />} />
            
            {/* Predict page - form to input student data */}
            <Route path="/predict" element={<Predict />} />
            
            {/* Results page - displays prediction results */}
            <Route path="/results" element={<Results />} />
            
            {/* Analytics page - charts and model insights */}
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
        
        {/* Footer - copyright and branding */}
        <footer className="app-footer">
          <p>&copy; 2026 Student Grade Prediction System. Powered by Machine Learning.</p>
        </footer>
      </div>
    </Router>
  )
}

export default App
