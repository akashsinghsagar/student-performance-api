/**
 * Results Page Component
 * 
 * Displays the predicted final grade (G3) after form submission.
 * Shows:
 * - Predicted grade in a visual circular display
 * - Model metrics (accuracy, confidence interval)
 * - Performance interpretation based on grade level
 * - Navigation buttons to view analytics or make new prediction
 * 
 * Receives prediction data via React Router's location state from Predict page.
 */

import { useLocation, useNavigate } from 'react-router-dom'
import '../styles/pages.css'

export default function Results() {
  const location = useLocation()
  const navigate = useNavigate()
  
  // Get prediction data passed from Predict page
  const prediction = location.state?.prediction

  // Show error message if user navigates here without making a prediction
  if (!prediction) {
    return (
      <div className="results-page">
        <div className="no-results">
          <h2>No Prediction Data</h2>
          <p>Please submit a prediction first</p>
          <button className="nav-button" onClick={() => navigate('/predict')}>
            Go to Predict
          </button>
        </div>
      </div>
    )
  }

  /**
   * Determine color based on grade performance level
   * Green: Excellent (≥18), Orange: Good (≥15), Red: Needs improvement (<15)
   */
  const gradeColor = (grade) => {
    if (grade >= 18) return '#27ae60'
    if (grade >= 15) return '#f39c12'
    return '#e74c3c'
  }

  return (
    <div className="results-page">
      <div className="results-header">
        <h1>Prediction Results</h1>
        <p>Machine Learning Model Prediction</p>
      </div>

      <div className="results-container">
        <div className="prediction-result">
          <div className="grade-display">
            <div className="grade-circle" style={{ borderColor: gradeColor(prediction.predicted_grade) }}>
              <span className="grade-number" style={{ color: gradeColor(prediction.predicted_grade) }}>
                {prediction.predicted_grade.toFixed(2)}
              </span>
              <span className="grade-label">Final Grade</span>
            </div>
          </div>

          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-label">Grade Range</span>
              <span className="metric-value">0 - 20</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Model Accuracy</span>
              <span className="metric-value">R² 0.8121</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Confidence</span>
              <span className="metric-value">±1.16</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Prediction Status</span>
              <span className="metric-value success">✓ Success</span>
            </div>
          </div>
        </div>

        <div className="interpretation-section">
          <h2>Grade Interpretation</h2>
          <div className="grade-interpretation">
            {prediction.predicted_grade >= 18 && (
              <div className="interpretation-card success-card">
                <span className="interpretation-icon">🌟</span>
                <h3>Excellent Performance</h3>
                <p>The student is predicted to achieve an excellent grade (18-20). This indicates outstanding academic performance and mastery of the subject matter.</p>
              </div>
            )}
            {prediction.predicted_grade >= 15 && prediction.predicted_grade < 18 && (
              <div className="interpretation-card warning-card">
                <span className="interpretation-icon">📚</span>
                <h3>Good Performance</h3>
                <p>The student is predicted to achieve a good grade (15-17). This shows solid academic understanding and strong performance.</p>
              </div>
            )}
            {prediction.predicted_grade < 15 && (
              <div className="interpretation-card error-card">
                <span className="interpretation-icon">⚠️</span>
                <h3>Needs Improvement</h3>
                <p>The student may need additional support to improve their grade. Consider extra study time or tutoring to enhance performance.</p>
              </div>
            )}
          </div>
        </div>

        <div className="actions-section">
          <button className="nav-button new-prediction" onClick={() => navigate('/predict')}>
            <span>New Prediction</span>
            <span>+</span>
          </button>
          <button className="nav-button analytics" onClick={() => navigate('/analytics')}>
            <span>View Analytics</span>
            <span>📊</span>
          </button>
        </div>
      </div>
    </div>
  )
}
