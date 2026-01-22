/**
 * Form Validation Utility
 */

export const validateStudentForm = (formData) => {
  const errors = {};

  // Age validation
  if (formData.age < 15 || formData.age > 22) {
    errors.age = 'Age must be between 15 and 22';
  }

  // Education level validation (0-4)
  if (formData.Medu < 0 || formData.Medu > 4) {
    errors.Medu = "Mother's education must be between 0 and 4";
  }
  if (formData.Fedu < 0 || formData.Fedu > 4) {
    errors.Fedu = "Father's education must be between 0 and 4";
  }

  // Time/rating validations (1-5)
  const ratingFields = ['famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health'];
  ratingFields.forEach(field => {
    if (formData[field] < 1 || formData[field] > 5) {
      errors[field] = `${field} must be between 1 and 5`;
    }
  });

  // Travel/study time validation (1-4)
  const timeFields = ['traveltime', 'studytime'];
  timeFields.forEach(field => {
    if (formData[field] < 1 || formData[field] > 4) {
      errors[field] = `${field} must be between 1 and 4`;
    }
  });

  // Failures validation (0-4)
  if (formData.failures < 0 || formData.failures > 4) {
    errors.failures = 'Failures must be between 0 and 4';
  }

  // Absences validation
  if (formData.absences < 0) {
    errors.absences = 'Absences cannot be negative';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};
