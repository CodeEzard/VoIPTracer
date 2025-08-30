import axios from 'axios';

// Use environment variable for production deployment
const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api' : '/api');

// Disable mock mode for production deployment with working API
const MOCK_MODE = false;

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
  if (MOCK_MODE) {
    return { 
      success: true, 
      data: { 
        status: "healthy", 
        message: "VoIP Tracer API is running (mock mode)", 
        version: "1.0.0" 
      } 
    };
  }
  
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
  if (MOCK_MODE) {
    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      success: true,
      data: {
        calls: [
          {
            call_id: "uploaded-call-1",
            from_uri: "sip:user1@uploaded.com",
            to_uri: "sip:user2@uploaded.com",
            duration: 32.5,
            packets: 89,
            anomaly: false
          },
          {
            call_id: "uploaded-call-2",
            from_uri: "sip:user3@uploaded.com",
            to_uri: "sip:user4@uploaded.com",
            duration: 156.2,
            packets: 420,
            anomaly: true
          }
        ],
        summary: {
          total_calls: 2,
          anomalies: 1,
          anomaly_rate: 0.5
        },
        stats: {
          total_calls: 2,
          anomaly_count: 1,
          total_packets: 509,
          total_duration: 188.7
        },
        message: `Successfully analyzed ${file.name} (mock mode)`,
        packets_processed: 509
      }
    };
  }

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
  if (MOCK_MODE) {
    return {
      success: true,
      data: {
        calls: [
          {
            call_id: "demo-call-1",
            from_uri: "sip:alice@example.com",
            to_uri: "sip:bob@example.com",
            duration: 45.2,
            packets: 120,
            anomaly: false
          },
          {
            call_id: "demo-call-2",
            from_uri: "sip:charlie@example.com",
            to_uri: "sip:diana@example.com",
            duration: 12.8,
            packets: 35,
            anomaly: true
          },
          {
            call_id: "demo-call-3",
            from_uri: "sip:eve@example.com",
            to_uri: "sip:frank@example.com",
            duration: 89.1,
            packets: 245,
            anomaly: false
          }
        ],
        summary: {
          total_calls: 3,
          anomalies: 1,
          anomaly_rate: 0.33
        },
        stats: {
          total_calls: 3,
          anomaly_count: 1,
          total_packets: 400,
          total_duration: 147.1
        },
        message: "Demo analysis completed successfully (mock mode)",
        packets_processed: 400
      }
    };
  }

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
