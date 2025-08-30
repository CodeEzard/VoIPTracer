import axios from 'axios';

// Use environment variable for production deployment
const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api' : 'http://localhost:8002');

export interface ApiResponse {
  success: boolean;
  data?: any;
  error?: string;
}

export interface AnalysisResults {
  calls: any[];
  summary?: {
    total_calls: number;
    anomalies: number;
    anomaly_rate: number;
  };
  stats?: {
    total_calls: number;
    anomaly_count: number;
    total_packets: number;
    total_duration: number;
  };
  status?: string;
  message?: string;
  packets_processed?: number;
  graph_stats?: {
    nodes: number;
    edges: number;
    components: number;
  };
}

// Health check
export const checkApiHealth = async (): Promise<ApiResponse> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/`, { timeout: 5000 });
    return { success: true, data: response.data };
  } catch (error: any) {
    console.error('Health check failed:', error);
    return { 
      success: false, 
      error: error.code === 'ECONNREFUSED' 
        ? 'Cannot connect to VoIP Tracer API. Please ensure the backend is running on http://localhost:8000'
        : 'API health check failed'
    };
  }
};

// Upload PCAP file
export const uploadPcapFile = async (file: File): Promise<ApiResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/upload-pcap`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 300000, // 5 minute timeout
    });

    return { success: true, data: response.data };
  } catch (error: any) {
    console.error('Upload error:', error);
    let errorMessage = 'Failed to analyze PCAP file. Please try again.';
    
    if (error.code === 'ECONNREFUSED') {
      errorMessage = 'Cannot connect to VoIP Tracer API. Please ensure the backend is running on http://localhost:8000';
    } else if (error.response?.status === 413) {
      errorMessage = 'File too large. Please select a smaller PCAP file.';
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    }

    return { success: false, error: errorMessage };
  }
};

// Test with demo data
export const runDemo = async (): Promise<ApiResponse> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/demo`, { timeout: 30000 });
    return { success: true, data: response.data };
  } catch (error: any) {
    console.error('Demo failed:', error);
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Demo analysis failed'
    };
  }
};

export default {
  checkApiHealth,
  uploadPcapFile,
  runDemo,
};
