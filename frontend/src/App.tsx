import { useState } from 'react';
import { Upload, Activity, BarChart3 } from 'lucide-react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import ResultsView from './components/ResultsView';
import ConnectionStatus from './components/ConnectionStatus';

interface AnalysisResults {
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
}

function App() {
  const [activeTab, setActiveTab] = useState<'upload' | 'dashboard' | 'results'>('upload');
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isApiConnected, setIsApiConnected] = useState<boolean>(false);

  const handleAnalysisComplete = (results: AnalysisResults) => {
    setAnalysisResults(results);
    setActiveTab('dashboard');
  };

  const tabs = [
    { id: 'upload', label: 'Upload PCAP', icon: Upload },
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'results', label: 'Results', icon: BarChart3 },
  ];

  return (
    <div className="min-h-screen network-bg relative overflow-hidden">
  {/* No grid, just minimal background */}
      
      {/* Header */}
  <header className="cyber-glass border-b border-neutral-800 relative z-10 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="relative mr-4">
                <div className="w-12 h-12 bg-neutral-800 rounded-lg flex items-center justify-center">
                  <Activity className="h-7 w-7 text-gray-300" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-bold cyber-text font-mono tracking-wide">
                  VoIP META TRACER
                </h1>
                <p className="text-sm text-gray-400 mt-1 font-mono">
                  ADVANCED NETWORK SECURITY ANALYSIS PLATFORM
                </p>
              </div>
            </div>
            <ConnectionStatus onConnectionChange={setIsApiConnected} />
          </div>
        </div>
      </header>

      {/* Navigation */}
  <nav className="cyber-glass border-b border-neutral-800 sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  disabled={!isApiConnected && tab.id !== 'upload'}
                  className={`flex items-center px-6 py-4 text-sm font-mono font-bold uppercase tracking-wider border-b-3 transition-all duration-300 relative overflow-hidden group ${
                    activeTab === tab.id
                      ? 'border-gray-400 text-gray-100 bg-neutral-800'
                      : 'border-transparent text-gray-400 hover:text-gray-200 hover:bg-neutral-700 hover:border-gray-600'
                  } ${!isApiConnected && tab.id !== 'upload' ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {/* No colored hover background */}
                  <Icon className="h-5 w-5 mr-3 relative z-10" />
                  <span className="relative z-10">{tab.label}</span>
                  {activeTab === tab.id && (
                    <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-400 rounded-t-full"></div>
                  )}
                  <div className="data-flow absolute top-0 left-0 right-0 h-px"></div>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
        <div className="animate-fadeIn">
          {activeTab === 'upload' && (
            <div className="transform transition-all duration-500 ease-out">
              <FileUpload 
                onAnalysisComplete={handleAnalysisComplete}
                isAnalyzing={isAnalyzing}
                setIsAnalyzing={setIsAnalyzing}
              />
            </div>
          )}
          
          {activeTab === 'dashboard' && (
            <div className="transform transition-all duration-500 ease-out">
              <Dashboard 
                results={analysisResults}
                onViewResults={() => setActiveTab('results')}
              />
            </div>
          )}
          
          {activeTab === 'results' && (
            <div className="transform transition-all duration-500 ease-out">
              <ResultsView results={analysisResults} />
            </div>
          )}
        </div>
      </main>

      {/* Status Bar */}
  <footer className="cyber-glass border-t border-neutral-800 mt-auto relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center text-sm font-mono">
            <div className="flex items-center space-x-4">
              {analysisResults && (
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 status-secure rounded-full"></div>
                  <span className="text-gray-200 font-bold uppercase tracking-wide">
                    LAST SCAN: {(analysisResults.stats?.total_calls || analysisResults.summary?.total_calls || 0)} CALLS | {(analysisResults.stats?.anomaly_count || analysisResults.summary?.anomalies || 0)} THREATS
                  </span>
                </div>
              )}
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
              <span className="text-gray-400 uppercase tracking-wide">VOIP META TRACER v1.0.0</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
