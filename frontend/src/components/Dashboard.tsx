import React from 'react';
import { Activity, AlertTriangle, Phone, Clock, Users, TrendingUp } from 'lucide-react';

interface DashboardProps {
  results: any;
  onViewResults: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ results, onViewResults }) => {
  if (!results) {
    return (
      <div className="text-center py-20">
        <div className="relative">
          <div className="absolute inset-0 bg-neutral-800/40 rounded-full blur-3xl"></div>
          <div className="relative w-24 h-24 terminal-window rounded-2xl flex items-center justify-center mx-auto mb-6 network-node">
            <Activity className="h-12 w-12 text-blue-400" />
          </div>
        </div>
        <h2 className="text-3xl font-bold cyber-text font-mono mb-4 tracking-wide">
          NO ANALYSIS DATA
        </h2>
  <p className="text-xl text-gray-400 max-w-md mx-auto leading-relaxed font-mono">
          DEPLOY PCAP FILES TO UNLOCK NETWORK SECURITY INTELLIGENCE
        </p>
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

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header Section */}
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold cyber-text font-mono mb-4 tracking-wide">
          NETWORK ANALYSIS DASHBOARD
        </h2>
  <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed font-mono">
          COMPREHENSIVE VOIP TRAFFIC MONITORING WITH REAL-TIME THREAT DETECTION AND ADVANCED PATTERN RECOGNITION
        </p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div
              key={index}
              className="cyber-glass rounded-2xl p-6 shadow-lg border border-neutral-700 relative overflow-hidden group"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Background circuit pattern */}
              <div className={`absolute inset-0 circuit-board opacity-5 ${
                stat.color === 'blue' ? 'from-blue-400 to-blue-600' :
                stat.color === 'red' ? 'from-red-400 to-red-600' :
                stat.color === 'purple' ? 'from-purple-400 to-purple-600' :
                'from-gray-400 to-gray-600'
              }`}></div>
              
              <div className="relative z-10">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className={`text-sm font-bold uppercase tracking-wider font-mono ${
                      stat.color === 'blue' ? 'text-blue-300' :
                      stat.color === 'red' ? 'text-red-300' :
                      stat.color === 'purple' ? 'text-purple-300' :
                      'text-gray-400'
                    }`}>{stat.title}</p>
                    <p className={`text-3xl font-bold mt-2 font-mono ${
                      stat.color === 'blue' ? 'text-blue-400' :
                      stat.color === 'red' ? 'text-red-400' :
                      stat.color === 'purple' ? 'text-purple-400' :
                      'text-gray-200'
                    }`}>{stat.value}</p>
                  </div>
                  <div className={`p-4 rounded-2xl terminal-window border ${
                    stat.color === 'blue' ? 'border-blue-400 bg-blue-400/20' :
                    stat.color === 'red' ? 'border-red-400 bg-red-400/20' :
                    stat.color === 'purple' ? 'border-purple-400 bg-purple-400/20' :
                    'border-gray-400 bg-gray-400/20'
                  } transition-transform duration-300 network-node`}>
                    <Icon className={`h-8 w-8 ${
                      stat.color === 'blue' ? 'text-blue-400' :
                      stat.color === 'red' ? 'text-red-400' :
                      stat.color === 'purple' ? 'text-purple-400' :
                      'text-gray-400'
                    }`} />
                  </div>
                </div>
                <div className="mt-6 flex items-center">
                  <span className={`text-sm font-bold px-3 py-1 rounded-full font-mono uppercase tracking-wide ${
                    stat.color === 'red' ? 'text-red-400 bg-red-400/20 border border-red-400/30' :
                    stat.color === 'blue' ? 'text-blue-400 bg-blue-400/20 border border-blue-400/30' :
                    stat.color === 'purple' ? 'text-purple-400 bg-purple-400/20 border border-purple-400/30' :
                    'text-gray-400 bg-gray-400/20 border border-gray-400/30'
                  }`}>
                    {stat.change}
                  </span>
                  <span className="text-sm text-gray-400 ml-2 font-mono">FROM BASELINE</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Anomaly Alert */}
      {anomalyCount > 0 && (
        <div className="cyber-glass rounded-2xl p-8 border border-red-400 bg-red-400/10 backdrop-blur-sm">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-14 h-14 bg-red-400/20 rounded-2xl flex items-center justify-center border border-red-400">
                <AlertTriangle className="h-8 w-8 text-red-400" />
              </div>
            </div>
            <div className="ml-6 flex-1">
              <h3 className="text-2xl font-bold text-red-400 mb-2 font-mono uppercase tracking-wide">
                {anomalyCount} THREAT{anomalyCount === 1 ? '' : 'S'} DETECTED
              </h3>
              <p className="text-red-300 text-lg leading-relaxed mb-4 font-mono">
                {anomalyRate.toFixed(1)}% OF TRAFFIC SHOWS SUSPICIOUS PATTERNS REQUIRING IMMEDIATE INVESTIGATION. 
                SECURITY AI HAS IDENTIFIED POTENTIAL NETWORK INTRUSIONS.
              </p>
              <button
                onClick={onViewResults}
                className="inline-flex items-center px-6 py-3 cyber-button font-mono uppercase tracking-wide transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-red-400/50"
              >
                <TrendingUp className="h-5 w-5 mr-2" />
                INVESTIGATE THREATS
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="cyber-glass rounded-2xl p-8 border border-blue-400/30 backdrop-blur-sm">
        <h3 className="text-2xl font-bold text-blue-400 mb-6 flex items-center font-mono uppercase tracking-wide">
          <div className="w-8 h-8 bg-blue-400/20 rounded-lg flex items-center justify-center mr-3 border border-blue-400">
            <TrendingUp className="h-5 w-5 text-blue-400" />
          </div>
          TACTICAL OPERATIONS
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
            onClick={onViewResults}
            className="flex items-center justify-center px-8 py-4 cyber-button font-mono uppercase tracking-wide transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-400/50"
          >
            <TrendingUp className="h-6 w-6 mr-3" />
            DETAILED ANALYSIS
          </button>
          <button
            onClick={() => {
              alert('Export functionality coming soon!');
            }}
            className="flex items-center justify-center px-8 py-4 border-2 border-dashed border-blue-400 text-blue-400 font-bold rounded-xl bg-blue-400/10 hover:bg-blue-400/20 hover:border-blue-300 transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-400/50 font-mono uppercase tracking-wide"
          >
            <Users className="h-6 w-6 mr-3" />
            EXPORT DATA
          </button>
        </div>
      </div>

      {/* Recent Activity Summary */}
      {results.calls && results.calls.length > 0 && (
        <div className="cyber-glass rounded-2xl p-8 border border-blue-400/30 backdrop-blur-sm">
          <h3 className="text-2xl font-bold text-blue-400 mb-6 flex items-center font-mono uppercase tracking-wide">
            <div className="w-8 h-8 bg-blue-400/20 rounded-lg flex items-center justify-center mr-3 border border-blue-400">
              <Phone className="h-5 w-5 text-blue-400" />
            </div>
            RECENT NETWORK ACTIVITY
          </h3>
          <div className="space-y-4">
            {results.calls.slice(0, 5).map((call: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-4 terminal-window rounded-xl border border-blue-400/30 transition-all duration-300">
                <div className="flex items-center">
                  <div className={`w-4 h-4 rounded-full mr-4 ${
                    call.is_anomaly ? 'status-danger' : 'bg-blue-400'
                  }`}></div>
                  <div>
                    <p className="font-bold text-blue-400 font-mono">{call.call_id || `CALL_${index + 1}`}</p>
                    <p className="text-sm text-gray-400 font-mono">
                      {call.total_pkts} PACKETS  {call.duration_s?.toFixed(1)}S DURATION
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  {!call.is_anomaly && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-bold bg-blue-400/20 text-blue-400 border border-blue-400 font-mono uppercase tracking-wide">
                       SECURE
                    </span>
                  )}
                  {!call.is_anomaly && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-bold bg-green-400/20 text-green-400 border border-green-400 font-mono uppercase tracking-wide">
                      ✅ SECURE
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
