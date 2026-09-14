import React, { useState } from 'react';
import { Gem, ActivitySquare, AlertTriangle, TrendingUp, Cpu, ShieldCheck, Users } from 'lucide-react'; 
import ChartPanel from './components/ChartPanel'; 
import MapPanel from './components/MapPanel'; 

// --- Dynamic Scenario Data (Now includes Live Metrics!) ---
const SCENARIOS = {
  normal: {
    status: "Optimal", color: "emerald",
    message: "Weather and machinery are operating within expected parameters. No intervention required.",
    metrics: { output: "2,450", health: "98%", safety: "Secure", workers: "142" },
    chartData: [
      { day: 'Mon', target: 4000, predicted: 4100 }, { day: 'Tue', target: 4000, predicted: 3950 },
      { day: 'Wed', target: 4000, predicted: 4200 }, { day: 'Thu', target: 4000, predicted: 4050 },
      { day: 'Fri', target: 4000, predicted: 4150 }, { day: 'Sat', target: 4000, predicted: 3900 }, { day: 'Sun', target: 4000, predicted: 4000 }
    ]
  },
  rain: {
    status: "Warning: Heavy Rainfall", color: "amber",
    message: "SHAP Model detects 40% moisture impact. Evacuate Zone A immediately and shift to Zone B.",
    metrics: { output: "1,120", health: "95%", safety: "At Risk (Zone A)", workers: "110" },
    chartData: [
      { day: 'Mon', target: 4000, predicted: 4100 }, { day: 'Tue', target: 4000, predicted: 3950 },
      { day: 'Wed', target: 4000, predicted: 4200 }, { day: 'Thu', target: 4000, predicted: 3200 },
      { day: 'Fri', target: 4000, predicted: 2500 }, { day: 'Sat', target: 4000, predicted: 2800 }, { day: 'Sun', target: 4000, predicted: 3500 }
    ]
  },
  machine: {
    status: "Critical: Excavator Failure", color: "rose",
    message: "Excavator-3 offline in Zone B. Uptime probability dropped to 12%. Dispatch maintenance.",
    metrics: { output: "1,850", health: "64%", safety: "Caution", workers: "142" },
    chartData: [
      { day: 'Mon', target: 4000, predicted: 4100 }, { day: 'Tue', target: 4000, predicted: 3950 },
      { day: 'Wed', target: 4000, predicted: 4200 }, { day: 'Thu', target: 4000, predicted: 3800 },
      { day: 'Fri', target: 4000, predicted: 3900 }, { day: 'Sat', target: 4000, predicted: 1500 }, { day: 'Sun', target: 4000, predicted: 1800 }
    ]
  }
};

function App() {
  const [currentScenario, setCurrentScenario] = useState('normal');
  const scenarioData = SCENARIOS[currentScenario];

  const bgColorClass = `bg-${scenarioData.color}-500/10`;
  const borderColorClass = `border-${scenarioData.color}-500/30`;
  const textColorClass = `text-${scenarioData.color}-400`;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans p-4 md:p-6">
      
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-center bg-slate-800 p-5 rounded-2xl shadow-xl mb-4 border border-slate-700">
        <div className="flex items-center gap-3 mb-4 md:mb-0">
          <div className="p-2 bg-emerald-500/20 rounded-lg">
            <Gem className="text-emerald-400" size={32} />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight">GeoMine <span className="text-emerald-400">AI</span></h1>
        </div>
        
        <div className="flex flex-wrap gap-3">
          <button onClick={() => setCurrentScenario('normal')} className={`px-5 py-2.5 rounded-lg font-semibold transition-all shadow-md border ${currentScenario === 'normal' ? 'bg-emerald-600 border-emerald-500' : 'bg-slate-700 hover:bg-slate-600 border-slate-600'}`}>Normal Day</button>
          <button onClick={() => setCurrentScenario('rain')} className={`px-5 py-2.5 rounded-lg font-semibold transition-all shadow-md border ${currentScenario === 'rain' ? 'bg-amber-600 border-amber-500' : 'bg-slate-700 hover:bg-slate-600 border-slate-600'}`}>Heavy Rain</button>
          <button onClick={() => setCurrentScenario('machine')} className={`px-5 py-2.5 rounded-lg font-semibold transition-all shadow-md border ${currentScenario === 'machine' ? 'bg-rose-600 border-rose-500' : 'bg-slate-700 hover:bg-slate-600 border-slate-600 text-rose-400'}`}>Machine Fail</button>
        </div>
      </header>

      {/* NEW: Live Metrics Ticker Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex items-center gap-4 shadow-lg transition-all">
          <div className="p-3 bg-blue-500/20 rounded-lg text-blue-400"><TrendingUp size={24} /></div>
          <div><p className="text-slate-400 text-xs font-bold uppercase">Live Output</p><p className="text-2xl font-extrabold">{scenarioData.metrics.output} <span className="text-sm font-normal text-slate-500">Tons</span></p></div>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex items-center gap-4 shadow-lg transition-all">
          <div className="p-3 bg-purple-500/20 rounded-lg text-purple-400"><Cpu size={24} /></div>
          <div><p className="text-slate-400 text-xs font-bold uppercase">Fleet Health</p><p className="text-2xl font-extrabold">{scenarioData.metrics.health}</p></div>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex items-center gap-4 shadow-lg transition-all">
          <div className={`p-3 rounded-lg ${textColorClass} ${bgColorClass}`}><ShieldCheck size={24} /></div>
          <div><p className="text-slate-400 text-xs font-bold uppercase">Safety Status</p><p className={`text-lg font-extrabold ${textColorClass}`}>{scenarioData.metrics.safety}</p></div>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex items-center gap-4 shadow-lg transition-all">
          <div className="p-3 bg-slate-500/20 rounded-lg text-slate-300"><Users size={24} /></div>
          <div><p className="text-slate-400 text-xs font-bold uppercase">Active Crew</p><p className="text-2xl font-extrabold">{scenarioData.metrics.workers}</p></div>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        
        {/* Left Side: Map */}
        <div className="xl:col-span-2 bg-slate-800 rounded-2xl p-5 shadow-xl border border-slate-700 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-slate-200">Live Prospectivity Map</h2>
            <span className={`flex items-center gap-2 text-xs font-medium bg-${scenarioData.color}-400/10 px-3 py-1 rounded-full border border-${scenarioData.color}-400/20 ${textColorClass}`}>
              <span className={`w-2 h-2 rounded-full bg-${scenarioData.color}-400 animate-pulse`}></span>Live Sync
            </span>
          </div>
          <div className="flex-1">
             {/* We pass the currentScenario down to the map! */}
             <MapPanel scenario={currentScenario} />
          </div>
        </div>

        {/* Right Side: Analytics */}
        <div className="flex flex-col gap-6">
          
          {/* Action Panel */}
          <div className="bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700">
            <div className="flex items-center gap-2 mb-4">
               {currentScenario === 'normal' ? <ActivitySquare className="text-emerald-400" size={24} /> : <AlertTriangle className={textColorClass} size={24} />}
               <h2 className="text-xl font-bold text-slate-200">AI Recommendations</h2>
            </div>
            <div className={`p-5 rounded-xl shadow-inner border transition-colors duration-500 ${bgColorClass} ${borderColorClass}`}>
              <h3 className={`font-bold mb-1 flex items-center gap-2 ${textColorClass}`}>{currentScenario === 'normal' ? '✓' : '⚠️'} {scenarioData.status}</h3>
              <p className="text-slate-300 text-sm leading-relaxed mt-2">{scenarioData.message}</p>
            </div>
          </div>

          {/* Chart Panel */}
          <div className="bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700 flex-1">
            <h2 className="text-xl font-bold text-slate-200 mb-2">Production Forecast</h2>
            <p className="text-slate-400 text-sm mb-4">7-day predicted output vs targets</p>
            <ChartPanel data={scenarioData.chartData} /> 
          </div>

        </div>
      </div>
      
    </div>
  );
}

export default App;