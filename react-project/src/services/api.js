/**
 * API Service for Student Grade Prediction
 * Centralized API calls with error handling
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class APIError extends Error {
  constructor(message, status, errors = []) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.errors = errors;
  }
}

/**
 * Make API request with standardized error handling
 */
async function makeRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new APIError(
        data.detail || 'An error occurred',
        response.status,
        data.errors || []
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    
    // Network or parsing error
    throw new APIError(
      'Unable to connect to the server. Please check your connection.',
      0
    );
  }
}

/**
 * API Service Methods
 */
export const api = {
  /**
   * Health check
   */
  async healthCheck() {
    return makeRequest('/health');
  },

  /**
   * Get model metadata
   */
  async getMetadata() {
    return makeRequest('/metadata');
  },

  /**
   * Predict single student grade
   * @param {Object} studentData - Student features
   */
  async predictGrade(studentData) {
    return makeRequest('/predict', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  },

  /**
   * Batch predict student grades
   * @param {Array} students - Array of student features
   */
  async predictBatch(students) {
    return makeRequest('/predict-batch', {
      method: 'POST',
      body: JSON.stringify({ students }),
    });
  },
};

export { APIError };
export default api;
