/**
 * Predict Page Component
 * 
 * This page allows users to input student information to predict their final grade (G3).
 * The form collects 32 different features about the student including:
 * - Basic information (school, age, sex, address)
 * - Family background (parents' education, jobs, family size)
 * - Academic data (study time, failures, previous grades G1 & G2)
 * - Lifestyle factors (going out, alcohol consumption, health)
 * - Support systems (school/family support, extra activities)
 * 
 * The form sends data to the Flask backend (/predict endpoint) which returns
 * a predicted final grade using a trained Random Forest model.
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/pages.css'

export default function Predict() {
  const navigate = useNavigate()
  
  // Form data holds all 32 student features with default values
  const [formData, setFormData] = useState({
    school: 'GP',
    sex: 'F',
    age: 15,
    address: 'U',
    famsize: 'GT3',
    Pstatus: 'T',
    Medu: 0,
    Fedu: 0,
    Mjob: 'at_home',
    Fjob: 'at_home',
    reason: 'course',
    guardian: 'mother',
    traveltime: 1,
    studytime: 1,
    failures: 0,
    schoolsup: 'no',
    famsup: 'no',
    paid: 'no',
    activities: 'no',
    nursery: 'no',
    higher: 'yes',
    internet: 'no',
    romantic: 'no',
    famrel: 3,
    freetime: 3,
    goout: 3,
    Dalc: 1,
    Walc: 1,
    health: 3,
    absences: 0,
    G1: 10,
    G2: 10
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Handle form input changes
   * Converts numeric strings to numbers for numeric fields
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: isNaN(value) ? value : parseFloat(value)
    }))
  }

  /**
   * Handle form submission
   * Sends student data to Flask API and navigates to results page
   */
  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      console.log('Sending prediction request to http://localhost:5000/predict')
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `Server error: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('Prediction successful:', data)
      setPrediction(data)
      
      // Navigate to results after 1 second
      setTimeout(() => {
        navigate('/results', { state: { prediction: data } })
      }, 1000)
    } catch (err) {
      console.error('Prediction error:', err)
      setError(`❌ Error: ${err.message}. Make sure the backend server is running on http://localhost:5000`)
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFormData({
      school: 'GP',
      sex: 'F',
      age: 15,
      address: 'U',
      famsize: 'GT3',
      Pstatus: 'T',
      Medu: 0,
      Fedu: 0,
      Mjob: 'at_home',
      Fjob: 'at_home',
      reason: 'course',
      guardian: 'mother',
      traveltime: 1,
      studytime: 1,
      failures: 0,
      schoolsup: 'no',
      famsup: 'no',
      paid: 'no',
      activities: 'no',
      nursery: 'no',
      higher: 'yes',
      internet: 'no',
      romantic: 'no',
      famrel: 3,
      freetime: 3,
      goout: 3,
      Dalc: 1,
      Walc: 1,
      health: 3,
      absences: 0,
      G1: 10,
      G2: 10
    })
  }

  return (
    <div className="predict-page">
      <div className="predict-header">
        <h1>Student Grade Prediction</h1>
        <p>Fill in the student information below to get a grade prediction</p>
      </div>

      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="form-sections">
          {/* Basic Information */}
          <div className="form-section">
            <h2 className="section-title">Basic Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>School</label>
                <select name="school" value={formData.school} onChange={handleInputChange}>
                  <option value="GP">Gabriel Pereira</option>
                  <option value="MS">Mousinho da Silveira</option>
                </select>
              </div>

              <div className="form-group">
                <label>Sex</label>
                <select name="sex" value={formData.sex} onChange={handleInputChange}>
                  <option value="F">Female</option>
                  <option value="M">Male</option>
                </select>
              </div>

              <div className="form-group">
                <label>Age</label>
                <input type="number" name="age" value={formData.age} onChange={handleInputChange} min="15" max="25" />
              </div>

              <div className="form-group">
                <label>Address Type</label>
                <select name="address" value={formData.address} onChange={handleInputChange}>
                  <option value="U">Urban</option>
                  <option value="R">Rural</option>
                </select>
              </div>
            </div>
          </div>

          {/* Family Information */}
          <div className="form-section">
            <h2 className="section-title">Family Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>Family Size</label>
                <select name="famsize" value={formData.famsize} onChange={handleInputChange}>
                  <option value="LT3">Less than 3</option>
                  <option value="GT3">Greater than 3</option>
                </select>
              </div>

              <div className="form-group">
                <label>Parent Cohabitation</label>
                <select name="Pstatus" value={formData.Pstatus} onChange={handleInputChange}>
                  <option value="T">Together</option>
                  <option value="A">Apart</option>
                </select>
              </div>

              <div className="form-group">
                <label>Mother's Education</label>
                <input type="number" name="Medu" value={formData.Medu} onChange={handleInputChange} min="0" max="4" />
              </div>

              <div className="form-group">
                <label>Father's Education</label>
                <input type="number" name="Fedu" value={formData.Fedu} onChange={handleInputChange} min="0" max="4" />
              </div>

              <div className="form-group">
                <label>Mother's Job</label>
                <select name="Mjob" value={formData.Mjob} onChange={handleInputChange}>
                  <option value="teacher">Teacher</option>
                  <option value="health">Health</option>
                  <option value="services">Services</option>
                  <option value="at_home">At Home</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label>Father's Job</label>
                <select name="Fjob" value={formData.Fjob} onChange={handleInputChange}>
                  <option value="teacher">Teacher</option>
                  <option value="health">Health</option>
                  <option value="services">Services</option>
                  <option value="at_home">At Home</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
          </div>

          {/* Academic Information */}
          <div className="form-section">
            <h2 className="section-title">Academic Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>Reason for Choosing School</label>
                <select name="reason" value={formData.reason} onChange={handleInputChange}>
                  <option value="course">Course Preference</option>
                  <option value="other">Other</option>
                  <option value="home">Close to Home</option>
                  <option value="reputation">Reputation</option>
                </select>
              </div>

              <div className="form-group">
                <label>Guardian</label>
                <select name="guardian" value={formData.guardian} onChange={handleInputChange}>
                  <option value="mother">Mother</option>
                  <option value="father">Father</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label>Travel Time (hours)</label>
                <input type="number" name="traveltime" value={formData.traveltime} onChange={handleInputChange} min="1" max="4" />
              </div>

              <div className="form-group">
                <label>Study Time (hours/week)</label>
                <input type="number" name="studytime" value={formData.studytime} onChange={handleInputChange} min="1" max="4" />
              </div>

              <div className="form-group">
                <label>Past Class Failures</label>
                <input type="number" name="failures" value={formData.failures} onChange={handleInputChange} min="0" max="4" />
              </div>

              <div className="form-group">
                <label>School Support</label>
                <select name="schoolsup" value={formData.schoolsup} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>
            </div>
          </div>

          {/* Additional Information */}
          <div className="form-section">
            <h2 className="section-title">Additional Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label>Family Support</label>
                <select name="famsup" value={formData.famsup} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>Extra Paid Classes</label>
                <select name="paid" value={formData.paid} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>Extracurricular Activities</label>
                <select name="activities" value={formData.activities} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>Attended Nursery School</label>
                <select name="nursery" value={formData.nursery} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>Wants to Pursue Higher Ed.</label>
                <select name="higher" value={formData.higher} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>Internet Access</label>
                <select name="internet" value={formData.internet} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>In a Romantic Relationship</label>
                <select name="romantic" value={formData.romantic} onChange={handleInputChange}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div className="form-group">
                <label>Family Relationship Quality (1-5)</label>
                <input type="number" name="famrel" value={formData.famrel} onChange={handleInputChange} min="1" max="5" />
              </div>

              <div className="form-group">
                <label>Free Time (1-5)</label>
                <input type="number" name="freetime" value={formData.freetime} onChange={handleInputChange} min="1" max="5" />
              </div>

              <div className="form-group">
                <label>Going Out (1-5)</label>
                <input type="number" name="goout" value={formData.goout} onChange={handleInputChange} min="1" max="5" />
              </div>

              <div className="form-group">
                <label>Weekday Alcohol Consumption (1-5)</label>
                <input type="number" name="Dalc" value={formData.Dalc} onChange={handleInputChange} min="1" max="5" />
              </div>

              <div className="form-group">
                <label>Weekend Alcohol Consumption (1-5)</label>
                <input type="number" name="Walc" value={formData.Walc} onChange={handleInputChange} min="1" max="5" />
              </div>

              <div className="form-group">
                <label>Current Health (1-5)</label>
                <input type="number" name="health" value={formData.health} onChange={handleInputChange} min="1" max="5" />
              </div>

              <div className="form-group">
                <label>School Absences</label>
                <input type="number" name="absences" value={formData.absences} onChange={handleInputChange} min="0" max="100" />
              </div>

              <div className="form-group">
                <label>Period 1 Grade (G1)</label>
                <input type="number" name="G1" value={formData.G1} onChange={handleInputChange} min="0" max="20" />
              </div>

              <div className="form-group">
                <label>Period 2 Grade (G2)</label>
                <input type="number" name="G2" value={formData.G2} onChange={handleInputChange} min="0" max="20" />
              </div>
            </div>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <button type="submit" className="submit-button" disabled={loading}>
            <span className="button-text">{loading ? 'Predicting...' : 'Predict Grade'}</span>
            <span className="button-icon">⚡</span>
          </button>
          <button type="button" className="reset-button" onClick={handleReset}>
            <span className="button-text">Reset Form</span>
            <span className="button-icon">↻</span>
          </button>
        </div>
      </form>
    </div>
  )
}
