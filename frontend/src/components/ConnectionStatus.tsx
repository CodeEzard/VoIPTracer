import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';
import { checkApiHealth } from '../services/api';

interface ConnectionStatusProps {
  onConnectionChange?: (connected: boolean) => void;
}

const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ onConnectionChange }) => {
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkConnection = async () => {
    setIsChecking(true);
    try {
      const result = await checkApiHealth();
      setIsConnected(result.success);
      setLastChecked(new Date());
      onConnectionChange?.(result.success);
    } catch (error) {
      setIsConnected(false);
      onConnectionChange?.(false);
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkConnection();
    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = () => {
    if (isChecking) {
      return <RefreshCw className="h-4 w-4 animate-spin text-yellow-400" />;
    }
    return isConnected ? (
      <Wifi className="h-4 w-4 text-green-400" />
    ) : (
      <WifiOff className="h-4 w-4 text-red-400" />
    );
  };

  const getStatusText = () => {
    if (isChecking) return 'SCANNING...';
    if (isConnected === null) return 'UNKNOWN';
    return isConnected ? 'API ONLINE' : 'API OFFLINE';
  };

  const getStatusColor = () => {
    if (isChecking) return 'text-yellow-400';
    if (isConnected === null) return 'text-gray-400';
    return isConnected ? 'text-green-400' : 'text-red-400';
  };

  return (
    <div className="flex items-center space-x-3">
      <div className={`flex items-center space-x-3 px-4 py-2 rounded-xl transition-all duration-300 cyber-glass border ${
        isConnected 
          ? 'border-green-400 bg-green-400/10' 
          : 'border-red-400 bg-red-400/10'
      }`}>
        <div className="relative">
          {getStatusIcon()}
          {isConnected && (
            <div className="absolute inset-0 w-4 h-4 bg-green-400 rounded-full animate-network-pulse opacity-30"></div>
          )}
        </div>
        <div>
          <span className={`text-sm font-bold font-mono uppercase tracking-wide ${getStatusColor()}`}>
            {getStatusText()}
          </span>
          {lastChecked && (
            <div className="text-xs text-green-300 font-mono">
              {lastChecked.toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>
      
      {!isConnected && !isChecking && (
        <button
          onClick={checkConnection}
          className="px-3 py-1 text-xs font-bold text-red-400 bg-red-400/10 border border-red-400 rounded-lg hover:bg-red-400/20 hover:border-red-300 transition-all duration-300 transform hover:scale-105 font-mono uppercase tracking-wide"
        >
          RETRY
        </button>
      )}
    </div>
  );
};

export default ConnectionStatus;
