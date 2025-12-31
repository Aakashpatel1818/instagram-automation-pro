# Setup Guide - Instagram Automation Pro

## Prerequisites

### System Requirements
- Node.js 16+ (for frontend)
- Python 3.9+ (for backend)
- MongoDB Atlas account (or local MongoDB)
- Meta Developer account
- Git

### Required Accounts
1. **MongoDB Atlas** - Cloud database
   - Create free cluster at https://www.mongodb.com/cloud/atlas
   - Get connection string

2. **Meta Developer Platform** - Instagram API access
   - Register at https://developers.facebook.com
   - Create app with Instagram Graph API
   - Get App ID, App Secret, Access Token

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Python Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Run Backend
```bash
python run.py
# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Setup Environment Variables
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

### 4. Run Frontend Development Server
```bash
npm run dev
# Frontend runs at http://localhost:5173
```

## Verification

### Backend Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", "environment": "development"}
```

### Frontend Access
- Open http://localhost:5173 in your browser
- You should see the Instagram Automation Pro dashboard

## Common Issues

### MongoDB Connection Error
- Check connection string in .env
- Verify IP whitelist in MongoDB Atlas
- Ensure firewall allows connection

### Port Already in Use
```bash
# Backend (change port in .env)
SERVER_PORT=8001
```

### CORS Errors
- Check ALLOWED_ORIGINS in backend .env
- Ensure frontend URL is added to CORS settings

## Next Steps

1. Configure Meta API credentials
2. Set up Instagram webhook
3. Create sample automation rules
4. Test comment automation
5. Deploy to production

See DEPLOYMENT.md for production deployment guide.