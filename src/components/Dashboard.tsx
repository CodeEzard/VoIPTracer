import React from 'react';
import { Activity, AlertTriangle, Phone, Clock, Users, TrendingUp } from 'lucide-react';

interface DashboardProps {
  results: any;
  onViewResults: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ results, onViewResults }) => {
  if (!results) {
    return (
      <div className="text-center py-12">
        <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-medium text-gray-900 mb-2">No Analysis Data</h2>
        <p className="text-gray-600">Upload a PCAP file to see analysis results</p>
      </div>
    );
  }

  const stats = results.stats || {};
  const summary = results.summary || {};
  
  // Handle both API response formats
  const totalCalls = stats.total_calls || summary.total_calls || 0;
  const anomalyCount = stats.anomaly_count || summary.anomalies || 0;
  const totalPackets = stats.total_packets || results.packets_processed || 0;
  const totalDuration = stats.total_duration || 0;
  
  const anomalyRate = totalCalls > 0 ? (anomalyCount / totalCalls * 100) : 0;

  const statCards = [
    {
      title: 'Total Calls',
      value: totalCalls,
      icon: Phone,
      color: 'blue',
      change: '+12%'
    },
    {
      title: 'Anomalies Detected',
      value: anomalyCount,
      icon: AlertTriangle,
      color: 'red',
      change: `${anomalyRate.toFixed(1)}%`
    },
    {
      title: 'Total Packets',
      value: totalPackets.toLocaleString(),
      icon: Activity,
      color: 'green',
      change: '+5%'
    },
    {
      title: 'Total Duration',
      value: `${totalDuration.toFixed(1)}s`,
      icon: Clock,
      color: 'purple',
      change: '+8%'
    }
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700 text-blue-800 dark:text-blue-300',
      red: 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-700 text-red-800 dark:text-red-300',
      green: 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700 text-green-800 dark:text-green-300',
      purple: 'bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-700 text-purple-800 dark:text-purple-300'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  const getIconColor = (color: string) => {
    const colors = {
      blue: 'text-blue-600 dark:text-blue-400',
      red: 'text-red-600 dark:text-red-400',
      green: 'text-green-600 dark:text-green-400',
      purple: 'text-purple-600 dark:text-purple-400'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="space-y-8">
      {/* Overview Stats */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Analysis Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div
                key={index}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{stat.value}</p>
                  </div>
                  <div className={`p-3 rounded-lg ${getColorClasses(stat.color)}`}>
                    <Icon className={`h-6 w-6 ${getIconColor(stat.color)}`} />
                  </div>
                </div>
                <div className="mt-4">
                  <span className={`text-sm font-medium ${
                    stat.color === 'red' ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'
                  }`}>
                    {stat.change}
                  </span>
                  <span className="text-sm text-gray-600 dark:text-gray-400 ml-1">from baseline</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Anomaly Alert */}
      {anomalyCount > 0 && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-6">
          <div className="flex items-start">
            <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-400 mt-1 mr-4 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-medium text-red-800 dark:text-red-300">
                {anomalyCount} Anomal{anomalyCount === 1 ? 'y' : 'ies'} Detected
              </h3>
              <p className="text-red-700 dark:text-red-400 mt-1">
                {anomalyRate.toFixed(1)}% of calls show suspicious patterns. Review the detailed results for more information.
              </p>
              <button
                onClick={onViewResults}
                className="mt-3 inline-flex items-center px-3 py-2 border border-red-300 dark:border-red-600 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 dark:text-red-300 bg-white dark:bg-gray-800 hover:bg-red-50 dark:hover:bg-red-900/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 dark:focus:ring-offset-gray-800"
              >
                View Detailed Results
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={onViewResults}
            className="flex items-center justify-center px-4 py-3 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-800"
          >
            <TrendingUp className="h-4 w-4 mr-2" />
            View Detailed Analysis
          </button>
          <button
            onClick={() => {
              // Export functionality would go here
              alert('Export functionality coming soon!');
            }}
            className="flex items-center justify-center px-4 py-3 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-800"
          >
            <Users className="h-4 w-4 mr-2" />
            Export Results
          </button>
        </div>
      </div>

      {/* Recent Activity Summary */}
      {results.calls && results.calls.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent Call Summary</h3>
          <div className="space-y-3">
            {results.calls.slice(0, 5).map((call: any, index: number) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-b-0">
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-3 ${
                    call.is_anomaly ? 'bg-red-500' : 'bg-green-500'
                  }`}></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">{call.call_id || `Call ${index + 1}`}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {call.total_pkts} packets • {call.duration_s?.toFixed(1)}s duration
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  {call.is_anomaly && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300">
                      Anomaly
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
