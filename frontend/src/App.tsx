import { useState } from 'react';
import { Upload, Activity, BarChart3 } from 'lucide-react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import ResultsView from './components/ResultsView';
import ConnectionStatus from './components/ConnectionStatus';

interface AnalysisResults {
  calls: any[];
  anomalies: any[];
  stats: {
    total_calls: number;
    anomaly_count: number;
    total_packets: number;
    total_duration: number;
  };
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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">VoIP Meta Tracer</h1>
            </div>
            <ConnectionStatus onConnectionChange={setIsApiConnected} />
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  disabled={!isApiConnected && tab.id !== 'upload'}
                  className={`flex items-center px-3 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } ${!isApiConnected && tab.id !== 'upload' ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'upload' && (
          <FileUpload 
            onAnalysisComplete={handleAnalysisComplete}
            isAnalyzing={isAnalyzing}
            setIsAnalyzing={setIsAnalyzing}
          />
        )}
        
        {activeTab === 'dashboard' && (
          <Dashboard 
            results={analysisResults}
            onViewResults={() => setActiveTab('results')}
          />
        )}
        
        {activeTab === 'results' && (
          <ResultsView results={analysisResults} />
        )}
      </main>

      {/* Status Bar */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex justify-between items-center text-sm text-gray-500">
            <div>
              {analysisResults && (
                <span>
                  Last Analysis: {analysisResults.stats.total_calls} calls, {analysisResults.stats.anomaly_count} anomalies
                </span>
              )}
            </div>
            <div>VoIP Meta Tracer v1.0.0</div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
