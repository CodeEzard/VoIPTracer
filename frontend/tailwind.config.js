/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-in-left': 'slideInLeft 0.6s ease-out',
        'slide-in-right': 'slideInRight 0.6s ease-out',
        'network-pulse': 'networkPulse 2s infinite',
        'data-flow': 'dataFlow 3s infinite',
        'scan-line': 'scanLine 4s infinite',
        'matrix-rain': 'matrixRain 8s infinite linear',
        'circuit-pulse': 'circuitPulse 2s infinite',
        'security-scan': 'securityScan 2s infinite',
        'hacking-glow': 'hackingGlow 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        networkPulse: {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '1' },
        },
        dataFlow: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        scanLine: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        matrixRain: {
          '0%': { transform: 'translateY(-100%)', opacity: '0' },
          '10%': { opacity: '1' },
          '90%': { opacity: '1' },
          '100%': { transform: 'translateY(100vh)', opacity: '0' },
        },
        circuitPulse: {
          '0%, 100%': { 
            boxShadow: '0 0 5px #00ff41, 0 0 10px #00ff41, 0 0 15px #00ff41'
          },
          '50%': { 
            boxShadow: '0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41'
          },
        },
        securityScan: {
          '0%': { width: '0%' },
          '100%': { width: '100%' },
        },
        hackingGlow: {
          '0%, 100%': { 
            textShadow: '0 0 5px #00ff41, 0 0 10px #00ff41, 0 0 15px #00ff41'
          },
          '50%': { 
            textShadow: '0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41'
          },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      borderWidth: {
        '3': '3px',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      fontFamily: {
        'display': ['Inter', 'ui-sans-serif', 'system-ui'],
        'mono': ['Courier New', 'monospace'],
      },
      colors: {
        gray: {
          950: '#0a0a0a',
        },
        cyber: {
          green: '#00ff41',
          cyan: '#00ffff',
          red: '#ff0040',
          yellow: '#ffff00',
          purple: '#8000ff',
          blue: '#0080ff',
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'grid-pattern': 'linear-gradient(to right, rgba(148, 163, 184, 0.1) 1px, transparent 1px), linear-gradient(to bottom, rgba(148, 163, 184, 0.1) 1px, transparent 1px)',
        'circuit-pattern': 'linear-gradient(90deg, #00ff4110 50%, transparent 50%), linear-gradient(#00ff4110 50%, transparent 50%)',
      },
      backgroundSize: {
        'grid': '20px 20px',
        'circuit': '40px 40px',
      },
    },
  },
  plugins: [],
}
