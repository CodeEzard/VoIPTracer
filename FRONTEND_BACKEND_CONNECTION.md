# VoIP Tracer - Frontend-Backend Connection Guide

## 🚀 Quick Start

Your VoIP Tracer frontend and backend are now properly connected! Here's how to use the system:

### Starting the Development Environment

#### Option 1: Using the startup scripts
- **Windows**: Double-click `start_dev.bat` or run in terminal
- **Linux/Mac**: Run `python start_dev.py`

#### Option 2: Manual startup
1. **Start Backend**:
   ```bash
   cd "C:\Users\ASUS\Desktop\Web P\VoIPTracer"
   python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

### Access URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 How the Connection Works

### Backend (FastAPI)
- **Location**: `src/api.py`
- **Port**: 8000
- **CORS**: Configured to allow frontend connections
- **Endpoints**:
  - `GET /` - Health check
  - `GET /demo` - Run demo analysis with sample data
  - `POST /upload-pcap` - Upload and analyze PCAP files
  - `POST /analyze-file` - Analyze existing files on server

### Frontend (React + Vite)
- **Location**: `frontend/`
- **Port**: 5173 (development)
- **Proxy**: Configured to proxy `/api/*` requests to backend
- **API Service**: `frontend/src/services/api.ts`

### Communication Flow
1. Frontend makes requests to `/api/*` endpoints
2. Vite proxy forwards requests to `http://localhost:8000`
3. Backend processes requests and returns JSON responses
4. Frontend displays results in the UI

## 📡 API Integration Details

### Frontend API Configuration
```typescript
// Uses proxy in development, direct URL in production
const API_BASE_URL = import.meta.env.DEV ? '/api' : 'http://localhost:8000';
```

### Backend CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", ...],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Vite Proxy Configuration
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

## 🧪 Testing the Connection

### Health Check
The frontend automatically checks backend connectivity on load using:
```typescript
const healthResponse = await checkApiHealth();
```

### Demo Analysis
Test the full pipeline with sample data:
```typescript
const demoResponse = await runDemo();
```

### File Upload
Upload PCAP files for analysis:
```typescript
const uploadResponse = await uploadPcapFile(file);
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Make sure backend includes CORS middleware
   - Check allowed origins include frontend URL

2. **Connection Refused**
   - Ensure backend is running on port 8000
   - Check firewall/antivirus blocking connections

3. **Module Import Errors**
   - Install backend dependencies: `pip install -r requirements.txt`
   - Make sure Python path includes `src/` directory

4. **Frontend Build Issues**
   - Install dependencies: `npm install`
   - Check Node.js version compatibility

### Debug Commands

Check backend health:
```bash
curl http://localhost:8000/
```

Test demo endpoint:
```bash
curl http://localhost:8000/demo
```

Check frontend proxy:
```bash
curl http://localhost:5173/api/
```

## 📁 Project Structure

```
VoIPTracer/
├── src/                     # Backend source code
│   ├── api.py              # FastAPI application
│   ├── capture.py          # Packet capture logic
│   ├── parser.py           # VoIP parsing
│   ├── analyze.py          # ML analysis
│   └── ...
├── frontend/               # React frontend
│   ├── src/
│   │   ├── services/
│   │   │   └── api.ts      # API client
│   │   ├── components/     # React components
│   │   └── ...
│   ├── vite.config.ts      # Vite configuration
│   └── package.json
├── start_dev.py            # Development startup script
├── start_dev.bat           # Windows startup script
└── requirements.txt        # Python dependencies
```

## 🔄 Development Workflow

1. Make changes to backend code in `src/`
2. Backend auto-reloads with `--reload` flag
3. Make changes to frontend code in `frontend/src/`
4. Frontend auto-reloads via Vite HMR
5. Test API endpoints at http://localhost:8000/docs
6. Test UI at http://localhost:5173

## 🚀 Production Deployment

For production deployment:

1. **Build Frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve Static Files**:
   Configure FastAPI to serve built frontend files

3. **Environment Variables**:
   Set production API URLs and configurations

4. **Docker** (optional):
   Use provided `Dockerfile` and `docker-compose.yml`

## ✅ Verification Checklist

- [ ] Backend starts without errors on port 8000
- [ ] Frontend starts without errors on port 5173
- [ ] Health check endpoint returns 200 status
- [ ] Demo endpoint returns analysis results
- [ ] Frontend can connect to backend (no CORS errors)
- [ ] File upload functionality works
- [ ] Results display properly in UI

Your VoIP Tracer is now fully connected and ready for use! 🎉
