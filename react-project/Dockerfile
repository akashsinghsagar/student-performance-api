# Frontend build + preview server
FROM node:20-alpine
WORKDIR /app

# Install dependencies
COPY react-project/package.json react-project/package-lock.json ./
RUN npm ci

# Copy source
COPY react-project/ ./

# Configure API base URL (compile-time)
ARG VITE_API_URL=http://api:8000/api
ENV VITE_API_URL=$VITE_API_URL

# Build static files
RUN npm run build

# Serve built app with Vite preview
EXPOSE 4173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
