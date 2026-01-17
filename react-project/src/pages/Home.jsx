/**
 * Home Page Component
 * 
 * Landing page that introduces the Student Grade Prediction System.
 * Features:
 * - Hero section with title, description, and key statistics
 * - Call-to-action button navigating to Predict page
 * - Feature cards explaining system capabilities
 * - Information sections about the model and methodology
 * - Decorative animated circles for visual appeal
 */

import { useNavigate } from 'react-router-dom'
import '../styles/pages.css'

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Student Grade Prediction</h1>
          <p className="hero-subtitle">Predict student final grades using Machine Learning</p>
          
          <div className="hero-stats">
            <div className="stat-card">
              <span className="stat-number">395</span>
              <span className="stat-label">Students Analyzed</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">32</span>
              <span className="stat-label">Features Used</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">81.2%</span>
              <span className="stat-label">Model Accuracy (R²)</span>
            </div>
          </div>

          <button 
            className="cta-button"
            onClick={() => navigate('/predict')}
          >
            <span className="button-text">Get Started</span>
            <span className="button-icon">→</span>
          </button>
        </div>

        <div className="hero-decoration">
          <div className="decoration-circle decoration-circle-1"></div>
          <div className="decoration-circle decoration-circle-2"></div>
          <div className="decoration-circle decoration-circle-3"></div>
        </div>
      </div>

      <div className="features-section">
        <h2 className="section-title">Features</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎓</div>
            <h3>Student Profile</h3>
            <p>Analyze 32 student attributes including demographics and academic performance</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Smart Predictions</h3>
            <p>Get accurate grade predictions powered by Random Forest ML model</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📈</div>
            <h3>Analytics</h3>
            <p>View detailed charts and insights about model performance and data distribution</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Instant Results</h3>
            <p>Get predictions in real-time with confidence metrics and explanations</p>
          </div>
        </div>
      </div>

      <div className="info-section">
        <div className="info-card">
          <h3>How It Works</h3>
          <ol className="info-list">
            <li>Fill in the student information form</li>
            <li>Our ML model analyzes the data</li>
            <li>Receive predicted final grade instantly</li>
            <li>View analytics and model insights</li>
          </ol>
        </div>

        <div className="info-card">
          <h3>Model Details</h3>
          <ul className="info-list">
            <li>Algorithm: Random Forest Regressor</li>
            <li>Trees: 100 estimators</li>
            <li>Test Accuracy (R²): 0.8121</li>
            <li>Mean Absolute Error: 1.1585 grades</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
