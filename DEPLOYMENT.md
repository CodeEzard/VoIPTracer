# Deployment Guide: VoIP Tracer

## 🚀 Free Deployment Options

### Option 1: Vercel + Railway (Recommended)

#### Frontend Deployment (Vercel)
1. **Sign up for Vercel**: Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. **Connect Repository**: Import your GitHub repository
3. **Configure Build Settings**:
   - Framework Preset: `Vite`
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/dist`
   - Install Command: `cd frontend && npm install`
4. **Environment Variables**:
   - Add `VITE_API_URL` = `https://your-railway-app.railway.app`
5. **Deploy**: Click Deploy

#### Backend Deployment (Railway)
1. **Sign up for Railway**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **Deploy from GitHub**: Click "Deploy from GitHub repo"
3. **Select Repository**: Choose your VoIP Tracer repository
4. **Environment Variables**:
   - `PORT` = `8000`
   - `PYTHONPATH` = `/app`
5. **Deploy**: Railway will auto-deploy using your Dockerfile

### Option 2: Netlify + Render

#### Frontend (Netlify)
1. **Sign up**: [netlify.com](https://netlify.com)
2. **Site Settings**:
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/dist`
3. **Environment Variables**: Add `VITE_API_URL`

#### Backend (Render)
1. **Sign up**: [render.com](https://render.com)
2. **New Web Service**: Connect GitHub repository
3. **Settings**:
   - Environment: `Docker`
   - Branch: `main`

### Option 3: GitHub Pages + Fly.io

#### Frontend (GitHub Pages)
1. **Actions Setup**: Use provided workflow in `.github/workflows/`
2. **Enable Pages**: Repository → Settings → Pages → Actions

#### Backend (Fly.io)
1. **Install Fly CLI**: `npm install -g flyctl`
2. **Deploy**: `fly deploy`

## 🔧 Configuration Files Created

- `vercel.json` - Vercel deployment configuration
- `Procfile` - Process file for Railway/Heroku-style deployments
- `runtime.txt` - Python runtime specification
- `railway.sh` - Railway setup script
- `frontend/.env.production` - Production environment variables

## 🌍 Environment Variables

### Frontend (VITE_API_URL)
```bash
# For Railway backend
VITE_API_URL=https://your-app-name.railway.app

# For Render backend  
VITE_API_URL=https://your-app-name.onrender.com

# For Fly.io backend
VITE_API_URL=https://your-app-name.fly.dev
```

### Backend
```bash
PORT=8000
PYTHONPATH=/app
```

## 📋 Deployment Checklist

### Before Deployment:
- [ ] Push all changes to GitHub
- [ ] Update `VITE_API_URL` in frontend environment
- [ ] Test locally with production build
- [ ] Ensure CORS settings allow your frontend domain

### After Backend Deployment:
- [ ] Copy backend URL
- [ ] Update frontend environment variables
- [ ] Redeploy frontend
- [ ] Test end-to-end functionality

## 🔍 Common Issues

### CORS Errors
- Ensure backend CORS allows your frontend domain
- Check `src/api.py` CORS configuration

### Build Failures
- Verify Python version compatibility
- Check dependencies in `requirements.txt`
- Ensure tshark installation in Docker

### File Upload Issues
- Check file size limits on hosting platform
- Verify multipart/form-data support

## 💡 Cost Optimization

### Free Tier Limits:
- **Vercel**: 100GB bandwidth/month
- **Railway**: 500GB transfer/month, $5 credit
- **Netlify**: 100GB bandwidth/month
- **Render**: 750 hours/month, then sleeps

### Recommendations:
1. Use Railway for backend (best free tier)
2. Use Vercel for frontend (fastest deployments)
3. Consider Fly.io for better uptime (small cost)

## 🚀 Quick Deploy Commands

```bash
# 1. Commit your changes
git add .
git commit -m "Add deployment configuration"
git push origin main

# 2. Deploy backend to Railway
# - Go to railway.app
# - Connect GitHub repo
# - Auto-deploy

# 3. Deploy frontend to Vercel
# - Go to vercel.com  
# - Import GitHub repo
# - Set VITE_API_URL to Railway URL
# - Deploy
```
