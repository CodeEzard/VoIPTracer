import React, { useCallback, useState } from 'react';
import { Upload, FileType, AlertCircle, Loader2, Play, Activity, AlertTriangle } from 'lucide-react';
import { uploadPcapFile, runDemo } from '../services/api';

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
      const result = await uploadPcapFile(selectedFile);
      
      if (result.success) {
        if (result.data?.status === 'no_voip_packets') {
          setError(result.data.message || 'No VoIP packets found in the uploaded file. Please check that your PCAP contains SIP, RTP, or other VoIP traffic.');
        } else if (result.data?.status === 'no_calls') {
          setError(result.data.message || 'No complete VoIP calls found. The file may contain partial or fragmented VoIP data.');
        } else {
          onAnalysisComplete(result.data);
        }
      } else {
        setError(result.error || 'Upload failed');
      }
    } catch (err: any) {
      console.error('Upload error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDemo = async () => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const result = await runDemo();
      
      if (result.success) {
        if (result.data?.status === 'no_voip_packets') {
          setError('Demo data failed to generate VoIP packets. Please contact support.');
        } else {
          onAnalysisComplete(result.data);
        }
      } else {
        setError(result.error || 'Demo failed');
      }
    } catch (err: any) {
      console.error('Demo error:', err);
      setError('Demo analysis failed. Please ensure the backend is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 relative">
  <div className="absolute inset-0 bg-neutral-800/40 rounded-3xl blur-3xl"></div>
        <div className="relative">
          <div className="inline-flex items-center justify-center w-20 h-20 terminal-window rounded-xl mb-6 network-node">
            <Upload className="h-10 w-10 text-gray-400" />
          </div>
          <h2 className="text-4xl font-bold cyber-text font-mono mb-4 tracking-wide">
            NETWORK TRAFFIC ANALYSIS
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed font-mono">
            Deploy advanced packet inspection algorithms to detect anomalous VoIP communications and identify potential security threats in your network infrastructure.
          </p>
        </div>
      </div>

      {/* Main Upload Card */}
      <div className="cyber-glass rounded-3xl p-8 shadow-2xl border border-neutral-700 relative overflow-hidden">
        {/* Circuit Board Background */}
        <div className="absolute inset-0 circuit-board opacity-10"></div>
        <div className="absolute top-0 right-0 w-32 h-32 bg-neutral-700/30 rounded-full blur-2xl"></div>
        
        <div className="relative z-10">
          {/* File Drop Zone */}
          <div
            className={`relative border-3 border-dashed rounded-2xl p-12 text-center transition-all duration-500 group terminal-window ${
              dragActive
                ? 'border-blue-400 bg-blue-400/10 scale-105 shadow-lg shadow-blue-400/25'
                : 'border-neutral-700 hover:border-blue-400 hover:bg-blue-400/5'
            } ${selectedFile ? 'border-blue-400 bg-blue-400/10' : ''}`}
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
            
            <div className="space-y-6">
              <div className="relative">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-xl transition-all duration-500 terminal-window ${
                  selectedFile 
                    ? 'bg-blue-400/20 text-blue-400 border-blue-400' 
                    : 'bg-neutral-700 text-gray-400 border-neutral-600'
                }`}>
                  <FileType className="h-8 w-8" />
                </div>
                {dragActive && (
                  <div className="absolute inset-0 w-16 h-16 bg-blue-400 rounded-xl opacity-30"></div>
                )}
              </div>
              
              <div>
                <p className="text-2xl font-bold text-blue-400 mb-2 font-mono uppercase tracking-wide">
                  {selectedFile ? 'PCAP FILE LOADED' : 'DEPLOY PACKET CAPTURE'}
                </p>
                <p className="text-gray-400 text-lg font-mono">
                  {selectedFile ? selectedFile.name : 'INITIALIZE NETWORK TRAFFIC ANALYSIS'}
                </p>
              </div>
              
              {selectedFile && (
                <div className="text-left cyber-glass rounded-xl p-6 border border-blue-400/30">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <p className="text-sm font-bold text-blue-300 uppercase tracking-wider font-mono">TARGET FILE</p>
                      <p className="text-lg font-bold text-blue-400 mt-1 truncate font-mono">{selectedFile.name}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm font-bold text-blue-300 uppercase tracking-wider font-mono">FILE SIZE</p>
                      <p className="text-lg font-bold text-blue-400 mt-1 font-mono">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm font-bold text-blue-300 uppercase tracking-wider font-mono">PROTOCOL</p>
                      <p className="text-lg font-bold text-blue-400 mt-1 font-mono">PCAP</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-6 p-6 terminal-window border border-red-400 rounded-2xl flex items-start shadow-lg animate-data-flow">
          <div className="flex-shrink-0">
            <div className="w-10 h-10 bg-red-400/20 rounded-xl flex items-center justify-center">
              <AlertCircle className="h-5 w-5 text-red-400" />
            </div>
          </div>
          <div className="ml-4">
            <h3 className="text-lg font-bold text-red-400 font-mono uppercase tracking-wide">ANALYSIS ERROR</h3>
            <p className="text-red-300 mt-2 leading-relaxed font-mono">{error}</p>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="mt-8 space-y-4">
        <button
          onClick={handleUpload}
          disabled={!selectedFile || isAnalyzing}
          className={`w-full flex items-center justify-center px-8 py-4 text-lg font-bold rounded-2xl shadow-lg transition-all duration-300 transform font-mono uppercase tracking-wide ${
            selectedFile && !isAnalyzing
              ? 'cyber-button hover:scale-105 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-blue-400/50'
              : 'text-gray-500 bg-gray-800 border-2 border-gray-600 cursor-not-allowed'
          }`}
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="h-6 w-6 mr-3 animate-spin" />
              ANALYZING PACKETS...
            </>
          ) : (
            <>
              <Upload className="h-6 w-6 mr-3" />
              INITIATE ANALYSIS
            </>
          )}
        </button>

        {/* Demo Button */}
        <button
          onClick={handleDemo}
          disabled={isAnalyzing}
          className={`w-full flex items-center justify-center px-8 py-4 text-lg font-bold rounded-2xl border-2 border-dashed transition-all duration-300 transform font-mono uppercase tracking-wide ${
            !isAnalyzing
              ? 'text-blue-400 border-blue-400 bg-blue-400/10 hover:bg-blue-400/20 hover:border-blue-300 hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-400/50'
              : 'text-gray-500 border-gray-600 bg-gray-800 cursor-not-allowed'
          }`}
        >
          <Play className="h-6 w-6 mr-3" />
          DEMO MODE
        </button>
      </div>

      {/* Analysis Progress */}
      {isAnalyzing && (
        <div className="mt-6 p-6 terminal-window border border-blue-400 rounded-2xl">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-blue-400/20 rounded-xl flex items-center justify-center">
                <Loader2 className="h-6 w-6 text-blue-400 animate-spin" />
              </div>
            </div>
            <div className="ml-4 flex-1">
              <h3 className="text-lg font-bold text-blue-400 font-mono uppercase tracking-wide">SCANNING NETWORK TRAFFIC</h3>
              <p className="text-blue-300 mt-1 leading-relaxed font-mono">
                Executing deep packet inspection protocols... Detecting anomalous patterns...
              </p>
              <div className="mt-3 bg-gray-800 rounded-full h-3 overflow-hidden border border-blue-400/30">
                <div className="bg-blue-400 h-full rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Features Showcase - all stationary, minimal style */}
      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="text-center p-6 cyber-glass rounded-2xl border border-neutral-700">
          <div className="w-12 h-12 bg-neutral-800 rounded-xl flex items-center justify-center mx-auto mb-4">
            <Activity className="h-6 w-6 text-gray-400" />
          </div>
          <h3 className="font-bold text-gray-200 mb-2 font-mono uppercase tracking-wide">REAL-TIME SCAN</h3>
          <p className="text-sm text-gray-400 font-mono">Advanced packet processing with immediate threat detection</p>
        </div>
        <div className="text-center p-6 cyber-glass rounded-2xl border border-neutral-700">
          <div className="w-12 h-12 bg-neutral-800 rounded-xl flex items-center justify-center mx-auto mb-4">
            <AlertTriangle className="h-6 w-6 text-gray-400" />
          </div>
          <h3 className="font-bold text-gray-200 mb-2 font-mono uppercase tracking-wide">THREAT DETECTION</h3>
          <p className="text-sm text-gray-400 font-mono">AI-powered anomaly identification and pattern recognition</p>
        </div>
        <div className="text-center p-6 cyber-glass rounded-2xl border border-neutral-700">
          <div className="w-12 h-12 bg-neutral-800 rounded-xl flex items-center justify-center mx-auto mb-4">
            <FileType className="h-6 w-6 text-gray-400" />
          </div>
          <h3 className="font-bold text-gray-200 mb-2 font-mono uppercase tracking-wide">SECURE ANALYSIS</h3>
          <p className="text-sm text-gray-400 font-mono">Metadata-only inspection without protocol decryption</p>
        </div>
      </div>

      {/* File Support Info */}
      <div className="mt-8 p-6 cyber-glass rounded-2xl border border-neutral-700">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-sm font-bold text-gray-400 uppercase tracking-wider font-mono">SUPPORTED FORMATS</p>
            <p className="text-gray-200 font-bold mt-1 font-mono">.PCAP, .PCAPNG</p>
          </div>
          <div>
            <p className="text-sm font-bold text-gray-400 uppercase tracking-wider font-mono">MAXIMUM SIZE</p>
            <p className="text-gray-200 font-bold mt-1 font-mono">100MB</p>
          </div>
          <div>
            <p className="text-sm font-bold text-gray-400 uppercase tracking-wider font-mono">PROTOCOLS</p>
            <p className="text-gray-200 font-bold mt-1 font-mono">SIP, RTP, DTLS</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
