# VoIP Tracer Frontend

A modern React frontend for the VoIP Meta Tracer project, built with Vite, TypeScript, and Tailwind CSS.

## Features

- 📁 **PCAP File Upload**: Drag-and-drop interface for uploading PCAP files
- 📊 **Dashboard**: Real-time analysis overview with key metrics
- 🔍 **Results View**: Detailed call analysis with filtering and search
- 🚨 **Anomaly Detection**: Visual highlighting of suspicious call patterns
- 📈 **Data Export**: Download analysis results in JSON format
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Axios** for API communication

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- VoIP Tracer backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Backend Integration

The frontend communicates with the VoIP Tracer FastAPI backend through:

- **Upload Endpoint**: `POST /upload-pcap` - Upload PCAP files for analysis
- **Health Check**: `GET /` - Verify backend connectivity
- **Proxy Configuration**: Vite dev server proxies `/api/*` to `http://localhost:8000`

## Usage

1. **Start the Backend**: Ensure your VoIP Tracer API is running on port 8000
2. **Start the Frontend**: Run `npm run dev` to start the development server
3. **Upload PCAP**: Navigate to the Upload tab and drag/drop a `.pcap` or `.pcapng` file
4. **View Results**: Analysis results will automatically display in the Dashboard
5. **Explore Details**: Switch to the Results tab for detailed call information

## Development

```bash
npm run dev    # Start development server
npm run build  # Build for production
npm run preview # Preview production build
```
