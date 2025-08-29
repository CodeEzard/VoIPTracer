import React, { useCallback, useState } from 'react';
import { Upload, FileType, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

interface FileUploadProps {
  onAnalysisComplete: (results: any) => void;
  isAnalyzing: boolean;
  setIsAnalyzing: (analyzing: boolean) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ 
  onAnalysisComplete, 
  isAnalyzing, 
  setIsAnalyzing 
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = 'http://localhost:8000';

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.name.endsWith('.pcap') || file.name.endsWith('.pcapng')) {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please select a .pcap or .pcapng file');
      }
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.name.endsWith('.pcap') || file.name.endsWith('.pcapng')) {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please select a .pcap or .pcapng file');
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post(`${API_BASE_URL}/upload-pcap`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minute timeout
      });

      onAnalysisComplete(response.data);
    } catch (err: any) {
      console.error('Upload error:', err);
      if (err.code === 'ECONNREFUSED') {
        setError('Cannot connect to VoIP Tracer API. Please ensure the backend is running on http://localhost:8000');
      } else if (err.response?.status === 413) {
        setError('File too large. Please select a smaller PCAP file.');
      } else {
        setError(err.response?.data?.detail || 'Failed to analyze PCAP file. Please try again.');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="text-center mb-8">
          <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload PCAP File</h2>
          <p className="text-gray-600">
            Upload a PCAP file to analyze VoIP call metadata and detect anomalies
          </p>
        </div>

        {/* File Drop Zone */}
        <div
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-blue-400 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".pcap,.pcapng"
            onChange={handleFileSelect}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            disabled={isAnalyzing}
          />
          
          <div className="space-y-4">
            <FileType className="h-8 w-8 text-gray-400 mx-auto" />
            <div>
              <p className="text-lg font-medium text-gray-900">
                {selectedFile ? selectedFile.name : 'Drop your PCAP file here'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                or click to browse (.pcap, .pcapng files only)
              </p>
            </div>
            
            {selectedFile && (
              <div className="text-sm text-gray-600 bg-gray-50 rounded p-3">
                <p><strong>File:</strong> {selectedFile.name}</p>
                <p><strong>Size:</strong> {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
                <p><strong>Type:</strong> {selectedFile.type || 'application/octet-stream'}</p>
              </div>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
            <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-red-800">Upload Error</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Upload Button */}
        <div className="mt-6">
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isAnalyzing}
            className={`w-full flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md shadow-sm transition-colors ${
              selectedFile && !isAnalyzing
                ? 'text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                : 'text-gray-500 bg-gray-100 cursor-not-allowed'
            }`}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Analyzing PCAP...
              </>
            ) : (
              <>
                <Upload className="h-4 w-4 mr-2" />
                Analyze PCAP File
              </>
            )}
          </button>
        </div>

        {/* Analysis Progress */}
        {isAnalyzing && (
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center">
              <Loader2 className="h-5 w-5 text-blue-600 animate-spin mr-3" />
              <div>
                <h3 className="text-sm font-medium text-blue-800">Analyzing VoIP Traffic</h3>
                <p className="text-sm text-blue-700 mt-1">
                  Processing packets, detecting calls, and running anomaly analysis...
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="mt-6 text-xs text-gray-500 space-y-1">
          <p>• Supported formats: .pcap, .pcapng</p>
          <p>• Maximum file size: 100MB</p>
          <p>• Analysis includes: Call detection, anomaly detection, metadata extraction</p>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
