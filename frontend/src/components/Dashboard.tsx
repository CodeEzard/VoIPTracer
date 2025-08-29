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
  const anomalyRate = stats.total_calls > 0 ? (stats.anomaly_count / stats.total_calls * 100) : 0;

  const statCards = [
    {
      title: 'Total Calls',
      value: stats.total_calls || 0,
      icon: Phone,
      color: 'blue',
      change: '+12%'
    },
    {
      title: 'Anomalies Detected',
      value: stats.anomaly_count || 0,
      icon: AlertTriangle,
      color: 'red',
      change: `${anomalyRate.toFixed(1)}%`
    },
    {
      title: 'Total Packets',
      value: (stats.total_packets || 0).toLocaleString(),
      icon: Activity,
      color: 'green',
      change: '+5%'
    },
    {
      title: 'Total Duration',
      value: `${(stats.total_duration || 0).toFixed(1)}s`,
      icon: Clock,
      color: 'purple',
      change: '+8%'
    }
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-50 border-blue-200 text-blue-800',
      red: 'bg-red-50 border-red-200 text-red-800',
      green: 'bg-green-50 border-green-200 text-green-800',
      purple: 'bg-purple-50 border-purple-200 text-purple-800'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  const getIconColor = (color: string) => {
    const colors = {
      blue: 'text-blue-600',
      red: 'text-red-600',
      green: 'text-green-600',
      purple: 'text-purple-600'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="space-y-8">
      {/* Overview Stats */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div
                key={index}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                  </div>
                  <div className={`p-3 rounded-lg ${getColorClasses(stat.color)}`}>
                    <Icon className={`h-6 w-6 ${getIconColor(stat.color)}`} />
                  </div>
                </div>
                <div className="mt-4">
                  <span className={`text-sm font-medium ${
                    stat.color === 'red' ? 'text-red-600' : 'text-green-600'
                  }`}>
                    {stat.change}
                  </span>
                  <span className="text-sm text-gray-600 ml-1">from baseline</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Anomaly Alert */}
      {stats.anomaly_count > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-start">
            <AlertTriangle className="h-6 w-6 text-red-600 mt-1 mr-4 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-medium text-red-800">
                {stats.anomaly_count} Anomal{stats.anomaly_count === 1 ? 'y' : 'ies'} Detected
              </h3>
              <p className="text-red-700 mt-1">
                {anomalyRate.toFixed(1)}% of calls show suspicious patterns. Review the detailed results for more information.
              </p>
              <button
                onClick={onViewResults}
                className="mt-3 inline-flex items-center px-3 py-2 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                View Detailed Results
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={onViewResults}
            className="flex items-center justify-center px-4 py-3 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <TrendingUp className="h-4 w-4 mr-2" />
            View Detailed Analysis
          </button>
          <button
            onClick={() => {
              // Export functionality would go here
              alert('Export functionality coming soon!');
            }}
            className="flex items-center justify-center px-4 py-3 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <Users className="h-4 w-4 mr-2" />
            Export Results
          </button>
        </div>
      </div>

      {/* Recent Activity Summary */}
      {results.calls && results.calls.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Call Summary</h3>
          <div className="space-y-3">
            {results.calls.slice(0, 5).map((call: any, index: number) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-3 ${
                    call.is_anomaly ? 'bg-red-500' : 'bg-green-500'
                  }`}></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{call.call_id || `Call ${index + 1}`}</p>
                    <p className="text-xs text-gray-500">
                      {call.total_pkts} packets • {call.duration_s?.toFixed(1)}s duration
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  {call.is_anomaly && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
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
