import { useState } from 'react';
import { Upload, Activity, BarChart3 } from 'lucide-react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import ResultsView from './components/ResultsView';
import ConnectionStatus from './components/ConnectionStatus';
import ThemeToggle from './components/ThemeToggle';
import { ThemeProvider } from './contexts/ThemeContext';

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
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <Activity className="h-8 w-8 text-blue-600 dark:text-blue-400 mr-3" />
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">VoIP Meta Tracer</h1>
              </div>
              <div className="flex items-center space-x-4">
                <ThemeToggle />
                <ConnectionStatus onConnectionChange={setIsApiConnected} />
              </div>
            </div>
          </div>
        </header>

        {/* Navigation */}
        <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
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
                        ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                        : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
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
        <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div className="flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
              <div>
                {analysisResults && (
                  <span>
                    Last Analysis: {(analysisResults.stats?.total_calls || analysisResults.summary?.total_calls || 0)} calls, {(analysisResults.stats?.anomaly_count || analysisResults.summary?.anomalies || 0)} anomalies
                  </span>
                )}
              </div>
              <div>VoIP Meta Tracer v1.0.0</div>
            </div>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
}

export default App;
