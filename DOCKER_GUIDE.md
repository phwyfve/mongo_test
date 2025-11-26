# 🐳 Docker Deployment Guide

## Quick Start for Linux

### 1. Clone and Build
```bash
# Clone the repository
git clone <your-repo-url>
cd mongo_test

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 2. Access the Application
- **Frontend**: http://localhost:3000 (React UI)
- **Backend**: http://localhost:8000 (FastAPI API) 
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## 🏗️ Services Overview

### MongoDB Database
- **Container**: mongo_db
- **Port**: 27017
- **Credentials**: root / example123
- **Volume**: mongo_data (persistent storage)

### FastAPI Backend
- **Container**: fastapi_backend  
- **Port**: 8000
- **Features**: JWT auth, GridFS files, user management
- **Health**: http://localhost:8000/health

### React Frontend
- **Container**: react_frontend
- **Port**: 3000 (production) / 3001 (development)
- **Features**: Login, file management, account deletion

## 🔧 Environment Configuration

### Backend Environment
```bash
MONGODB_URL=mongodb://root:example123@mongo:27017
DATABASE_NAME=fastapi_mongo_test
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
GRIDFS_BUCKET_NAME=images
```

### Frontend Environment
```bash
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Deployment Options

### Option 1: Full Production (Recommended)
```bash
# Builds everything including React production build
docker-compose up -d
```

### Option 2: Development Frontend
```bash
# Uncomment frontend-dev in docker-compose.yml, then:
docker-compose up -d
cd webapp
npm install && npm start
```

### Option 3: Individual Services
```bash
# Start only database and backend
docker-compose up -d mongo backend

# Run React separately
cd webapp && npm install && npm start
```

## 🧪 Testing the Deployment

### 1. Health Checks
```bash
# Check all services
curl http://localhost:8000/health
curl http://localhost:3000

# Check MongoDB
docker exec mongo_db mongo --eval "db.adminCommand('ping')" -u root -p example123
```

### 2. API Testing
```bash
# Register a user
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=TestPass123"
```

### 3. File Upload Test
1. Open http://localhost:3000
2. Register/Login with the test account
3. Upload an image file
4. Test rename, download, delete functions

## 📦 Docker Commands Reference

### Basic Operations
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Remove volumes (⚠️ deletes data)
docker-compose down -v
```

### Individual Service Management
```bash
# Restart specific service
docker-compose restart backend

# View service logs
docker-compose logs backend

# Scale services
docker-compose up -d --scale backend=2
```

### Troubleshooting
```bash
# Rebuild services
docker-compose up --build -d

# Clean rebuild (removes cached layers)
docker-compose build --no-cache

# Check container status
docker ps -a

# Access container shell
docker exec -it fastapi_backend sh
docker exec -it mongo_db bash
```

## 🔒 Production Security

### Before Production Deployment:

1. **Change Credentials**
```bash
# Update in docker-compose.yml:
MONGO_INITDB_ROOT_PASSWORD=your-secure-password
SECRET_KEY=your-super-secret-jwt-key-256-bits-long
```

2. **Configure CORS**
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

3. **Add SSL/TLS**
- Use reverse proxy (nginx/traefik)
- Configure HTTPS certificates
- Update REACT_APP_API_URL to https

4. **Resource Limits**
```yaml
# Add to docker-compose.yml services:
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

## 🗂️ Data Persistence

### MongoDB Data
- Volume: `mongo_data`
- Location: Docker managed volume
- Backup: `docker exec mongo_db mongodump -u root -p example123 --out /backup`

### File Uploads
- Volume: `uploads_data`
- GridFS storage in MongoDB
- No separate file system needed

### Backup Strategy
```bash
# Create backup
mkdir -p backups
docker exec mongo_db mongodump -u root -p example123 --out /backup
docker cp mongo_db:/backup ./backups/$(date +%Y%m%d_%H%M%S)

# Restore backup
docker cp ./backups/backup_folder mongo_db:/restore
docker exec mongo_db mongorestore -u root -p example123 /restore
```

## 🐛 Common Issues

### Port Conflicts
```bash
# Check what's using ports
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :27017

# Use different ports in docker-compose.yml
ports:
  - "3001:80"    # Frontend on 3001
  - "8001:8000"  # Backend on 8001
```

### MongoDB Connection
```bash
# Check MongoDB is accessible
docker exec mongo_db mongo --eval "db.runCommand({connectionStatus:1})" -u root -p example123

# Check from backend container
docker exec fastapi_backend curl -f http://mongo:27017 || echo "MongoDB not accessible"
```

### React Build Issues
```bash
# Manual React build
cd webapp
npm install
npm run build

# Copy to nginx
docker cp webapp/build/. react_frontend:/usr/share/nginx/html/
```

## 🎯 Default Test Account

For immediate testing:
- **Email**: test2@hotmail.com
- **Password**: password123

This account should work after the initial setup.
