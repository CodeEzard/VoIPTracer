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
      return <RefreshCw className="h-4 w-4 animate-spin" />;
    }
    return isConnected ? (
      <Wifi className="h-4 w-4 text-green-500" />
    ) : (
      <WifiOff className="h-4 w-4 text-red-500" />
    );
  };

  const getStatusText = () => {
    if (isChecking) return 'Checking...';
    if (isConnected === null) return 'Unknown';
    return isConnected ? 'API Connected' : 'API Disconnected';
  };

  const getStatusColor = () => {
    if (isChecking) return 'text-yellow-600 dark:text-yellow-400';
    if (isConnected === null) return 'text-gray-600 dark:text-gray-400';
    return isConnected ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400';
  };

  return (
    <div className="flex items-center space-x-2">
      <div className={`flex items-center space-x-1 ${getStatusColor()}`}>
        {getStatusIcon()}
        <span className="text-sm font-medium">{getStatusText()}</span>
      </div>
      
      {!isConnected && !isChecking && (
        <button
          onClick={checkConnection}
          className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 underline"
        >
          Retry
        </button>
      )}
      
      {lastChecked && (
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {lastChecked.toLocaleTimeString()}
        </span>
      )}
    </div>
  );
};

export default ConnectionStatus;
