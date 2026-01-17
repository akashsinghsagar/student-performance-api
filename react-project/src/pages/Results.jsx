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

  // Use 'prediction' from API response (it returns prediction.prediction)
  const grade = prediction.prediction || prediction.predicted_grade || 0

  /**
   * Determine color based on grade performance level
   * All grades now use light purple shades
   */
  const gradeColor = (gradeVal) => {
    return '#a78bfa' // Light purple for all grades
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
            <div className="grade-circle" style={{ borderColor: gradeColor(grade) }}>
              <span className="grade-number" style={{ color: gradeColor(grade) }}>
                {grade.toFixed(2)}
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
            {grade >= 18 && (
              <div className="interpretation-card success-card">
                <span className="interpretation-icon">🌟</span>
                <h3>Excellent Performance (18-20)</h3>
                <p>Outstanding achievement! The student demonstrates exceptional mastery of the subject matter.</p>
                <ul className="interpretation-list">
                  <li>✓ Strong academic foundation</li>
                  <li>✓ Excellent study habits and discipline</li>
                  <li>✓ High likelihood of continued success</li>
                </ul>
                <div className="recommendation">
                  <strong>Recommendation:</strong> Encourage advanced coursework and leadership opportunities.
                </div>
              </div>
            )}
            {grade >= 15 && grade < 18 && (
              <div className="interpretation-card warning-card">
                <span className="interpretation-icon">📚</span>
                <h3>Good Performance (15-17)</h3>
                <p>Solid academic performance with room for excellence. The student shows strong understanding.</p>
                <ul className="interpretation-list">
                  <li>✓ Good grasp of core concepts</li>
                  <li>✓ Consistent study patterns</li>
                  <li>→ Potential for improvement to excellent range</li>
                </ul>
                <div className="recommendation">
                  <strong>Recommendation:</strong> Focus on challenging topics and seek clarification on difficult concepts.
                </div>
              </div>
            )}
            {grade >= 10 && grade < 15 && (
              <div className="interpretation-card info-card">
                <span className="interpretation-icon">📖</span>
                <h3>Average Performance (10-14)</h3>
                <p>The student meets basic requirements but has significant potential for improvement.</p>
                <ul className="interpretation-list">
                  <li>→ Basic understanding present</li>
                  <li>⚠ Needs more consistent study time</li>
                  <li>→ Additional support recommended</li>
                </ul>
                <div className="recommendation">
                  <strong>Recommendation:</strong> Increase study hours, consider tutoring, and improve attendance.
                </div>
              </div>
            )}
            {grade < 10 && (
              <div className="interpretation-card error-card">
                <span className="interpretation-icon">⚠️</span>
                <h3>Needs Attention (Below 10)</h3>
                <p>Immediate intervention required. The student needs substantial support to improve performance.</p>
                <ul className="interpretation-list">
                  <li>⚠ Struggling with fundamentals</li>
                  <li>⚠ High risk of academic failure</li>
                  <li>⚠ Requires urgent support</li>
                </ul>
                <div className="recommendation">
                  <strong>Recommendation:</strong> Urgent - Arrange one-on-one tutoring, parental meeting, and create personalized study plan.
                </div>
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
