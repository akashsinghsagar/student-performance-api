# 🎓 Student Grade Prediction System

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://react-project-swart-delta-40.vercel.app)
[![API](https://img.shields.io/badge/API-FastAPI-009688)](https://student-performance-api-1-3emm.onrender.com/api/health)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A full-stack machine learning application that predicts student final grades (G3) based on demographic, social, and academic factors using Random Forest regression.

**🔗 Live Application:** [https://react-project-swart-delta-40.vercel.app](https://react-project-swart-delta-40.vercel.app)

**📊 API Health:** [https://student-performance-api-1-3emm.onrender.com/api/health](https://student-performance-api-1-3emm.onrender.com/api/health)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎯 Core Functionality
- **Grade Prediction**: Predict student final grades on a 0-20 scale based on 32 input features
- **Real-time Analytics**: Interactive charts showing model performance, feature importance, and grade distributions
- **Batch Processing**: Support for predicting multiple students simultaneously
- **Model Transparency**: R² Score: **0.812**, Mean Absolute Error: **1.16**

### 🖥️ User Interface
- Modern, responsive React frontend with intuitive navigation
- Interactive form with client-side validation
- Real-time prediction results with confidence metrics
- Dynamic analytics dashboard with Chart.js visualizations

### 🛠️ Technical Features
- RESTful API with comprehensive error handling
- CORS-enabled for secure cross-origin requests
- Docker containerization for consistent deployments
- Automated CI/CD pipeline (GitHub → Render/Vercel)
- Health check endpoints for monitoring

---

## 🛠 Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.128.0
- **ML Library**: [scikit-learn](https://scikit-learn.org/) 1.8.0
- **Data Processing**: Pandas 2.3.3, NumPy 2.4.1
- **Model**: Random Forest Regressor
- **Server**: Uvicorn (ASGI)
- **Deployment**: Docker + Render

### Frontend
- **Framework**: [React](https://react.dev/) 19.2.0
- **Build Tool**: [Vite](https://vitejs.dev/) 7.3.1
- **Routing**: React Router DOM 7.12.0
- **Charts**: Chart.js 4.5.1 + react-chartjs-2 5.3.1
- **Deployment**: Vercel

### DevOps
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git, GitHub
- **Cloud Hosting**: Render (Backend), Vercel (Frontend)

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                   (React + Vite Frontend)                    │
│            https://react-project-swart-delta-40...           │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Requests (CORS)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│         https://student-performance-api-1-3emm...            │
│                                                               │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Routers   │→│   Services    │→│   ML Model    │        │
│  │  (API)     │  │  (Business)   │  │ (Prediction)  │        │
│  └────────────┘  └──────────────┘  └──────────────┘        │
│                                                               │
│  Model Artifacts:                                            │
│  • model.pkl (RandomForest)                                  │
│  • scaler.pkl (StandardScaler)                               │
│  • label_encoders.pkl (Categorical encoding)                 │
│  • feature_columns.pkl (Feature ordering)                    │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow
1. User submits student data via React form
2. Frontend validates input and sends POST to `/api/predict`
3. Backend validates schema using Pydantic models
4. Service layer preprocesses data (encoding, scaling)
5. Model predicts grade
6. Response returned with prediction + confidence metrics

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional)
- Git

### Local Development

#### Backend Setup

```bash
# Clone repository
git clone https://github.com/akashsinghsagar/student-performance-api.git
cd student-performance-api

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r student/requirements.txt

# Run server
cd student
python main.py
```

Server runs at: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`  
Health check: `http://localhost:8000/api/health`

#### Frontend Setup

```bash
# Navigate to frontend
cd react-project

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Using Docker Compose

```bash
# Build and run both services
docker compose build
docker compose up

# Access services
# Backend: http://localhost:8000/api/health
# Frontend: http://localhost:5173
```

---

## 📚 API Documentation

### Base URL
- **Production**: `https://student-performance-api-1-3emm.onrender.com/api`
- **Local**: `http://localhost:8000/api`

### Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "r2_score": 0.812,
  "mae": 1.158
}
```

#### Predict Single Student
```http
POST /api/predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "school": "GP",
  "sex": "F",
  "age": 17,
  "address": "U",
  "famsize": "GT3",
  "Pstatus": "T",
  "Medu": 4,
  "Fedu": 4,
  "Mjob": "teacher",
  "Fjob": "services",
  "reason": "course",
  "guardian": "mother",
  "traveltime": 2,
  "studytime": 2,
  "failures": 0,
  "schoolsup": "yes",
  "famsup": "no",
  "paid": "no",
  "activities": "no",
  "nursery": "yes",
  "higher": "yes",
  "internet": "yes",
  "romantic": "no",
  "famrel": 4,
  "freetime": 3,
  "goout": 4,
  "Dalc": 1,
  "Walc": 1,
  "health": 3,
  "absences": 6,
  "G1": 5,
  "G2": 6
}
```

**Response:**
```json
{
  "prediction": 17.23,
  "confidence": {
    "r2_score": 0.812,
    "mae": 1.158
  },
  "input_features": { ... }
}
```

#### Get Model Metadata
```http
GET /api/metadata
```

**Response:**
```json
{
  "r2_score": 0.812,
  "mae": 1.158,
  "features": ["school", "sex", "age", ...],
  "categorical_features": ["school", "sex", ...],
  "numerical_features": ["age", "absences", ...]
}
```

#### Interactive API Docs
Visit: `https://student-performance-api-1-3emm.onrender.com/docs`

---

## 🚢 Deployment

### Backend (Render)

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - New Web Service → Connect GitHub repo
   - Runtime: **Docker**
   - Environment Variables:
     - `ALLOWED_ORIGINS=https://your-frontend-url.vercel.app`

3. **Verify**
   ```bash
   curl https://student-performance-api-1-3emm.onrender.com/api/health
   ```

### Frontend (Vercel)

1. **Update Backend URL**
   ```bash
   # Edit react-project/.env.production
   VITE_API_URL=https://student-performance-api-1-3emm.onrender.com/api
   ```

2. **Deploy**
   ```bash
   cd react-project
   vercel login
   vercel --prod
   ```

3. **Update CORS**
   - Return to Render dashboard
   - Update `ALLOWED_ORIGINS` with your Vercel URL

---

## 📊 Model Performance

### Metrics
- **R² Score**: 0.812 (81.2% variance explained)
- **Mean Absolute Error**: 1.16 points (on 0-20 scale)
- **Model Type**: Random Forest Regressor
- **Training Dataset**: Portuguese secondary school students

### Top Features (by importance)
1. **G2** (Second period grade) - 60%
2. **G1** (First period grade) - 25%
3. **failures** (Past class failures) - 5%
4. **age** - 3%
5. **absences** - 2%

### Dataset
- **Source**: UCI Machine Learning Repository
- **Students**: 649 records
- **Features**: 32 input variables
- **Target**: G3 (final grade, 0-20)

---

## 📁 Project Structure

```
student-performance-api/
├── student/                    # Backend application
│   ├── main.py                # FastAPI app entry point
│   ├── routers.py             # API route handlers
│   ├── schemas.py             # Pydantic models
│   ├── services.py            # Business logic
│   ├── requirements.txt       # Python dependencies
│   ├── model.pkl              # Trained ML model
│   ├── scaler.pkl             # Feature scaler
│   ├── label_encoders.pkl     # Categorical encoders
│   ├── feature_columns.pkl    # Feature ordering
│   └── model_metadata.json    # Model metrics
│
├── react-project/             # Frontend application
│   ├── src/
│   │   ├── App.jsx           # Root component
│   │   ├── main.jsx          # Entry point
│   │   ├── pages/            # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Predict.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── Results.jsx
│   │   ├── components/       # Reusable components
│   │   ├── services/         # API client
│   │   ├── utils/            # Utilities
│   │   └── styles/           # CSS files
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── Dockerfile                 # Backend container config
├── docker-compose.yml         # Multi-service orchestration
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Write descriptive commit messages
- Add tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Akash Singh Sagar**

- GitHub: [@akashsinghsagar](https://github.com/akashsinghsagar)
- LinkedIn: [Connect](https://linkedin.com/in/akashsinghsagar)

---

## 🙏 Acknowledgments

- Dataset: [UCI ML Repository - Student Performance](https://archive.ics.uci.edu/ml/datasets/student+performance)
- FastAPI documentation and community
- React and Vite teams
- scikit-learn contributors

---

## 📞 Support

For issues, questions, or suggestions:
- **Issues**: [GitHub Issues](https://github.com/akashsinghsagar/student-performance-api/issues)
- **Email**: your.email@example.com

---

**⭐ If you find this project useful, please consider giving it a star!**

