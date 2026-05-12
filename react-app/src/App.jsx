import { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Activity } from 'lucide-react';
import KpiTiles from './components/KpiTiles';
import UsageChart from './components/UsageChart';
import RiskForm from './components/RiskForm';

const API_BASE = 'http://127.0.0.1:8000';

function App() {
  const [summary, setSummary] = useState(null);
  const [peakData, setPeakData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [prediction, setPrediction] = useState(null);
  const [formData, setFormData] = useState({ 
    region: 'Enter Region', 
    avg_usage: 0, 
    growth_rate: 0,
    variability: 0 // Added to match API requirements
  });

  useEffect(() => {
    const initData = async () => {
      try {
        const [sumRes, peakRes] = await Promise.all([
          axios.get(`${API_BASE}/usage/summary`),
          axios.get(`${API_BASE}/usage/peak`)
        ]);
        setSummary(sumRes.data);
        setPeakData(peakRes.data.top_hours.map(d => ({ 
          hour: `${d.hour}:00`, 
          usage: Math.round(d.total_usage) 
        })));
        setLoading(false);
      } catch (err) {
        console.error("Backend offline. Please start Uvicorn.", err);
      }
    };
    initData();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_BASE}/predict-usage-risk`, formData);
      setPrediction(res.data);
    } catch (err) {
      console.error("AI Prediction Failed:", err);
    }
  };

  if (loading) return <div className="vh-100 d-flex justify-content-center align-items-center"><h2>Booting Intelligence System...</h2></div>;

  return (
    <div className="dashboard-container container-fluid">
      <header className="dashboard-header d-flex justify-content-between align-items-center">
        <div className="d-flex align-items-center">
          <Activity size={32} className="text-primary me-3" />
          <h1 className="m-0">Telecom Intelligence <span style={{fontWeight: 300, color: '#6366f1'}}></span></h1>
        </div>
        <div className="badge bg-success-subtle text-success p-2 px-3 rounded-pill fw-bold border border-success">SYSTEM ONLINE</div>
      </header>

      <KpiTiles summary={summary} />

      <div className="row g-4">
        <div className="col-lg-8">
          <UsageChart data={peakData} />
        </div>
        <div className="col-lg-4">
          <RiskForm 
            formData={formData} 
            setFormData={setFormData} 
            onPredict={handlePredict} 
            prediction={prediction} 
          />
        </div>
      </div>
    </div>
  );
}

export default App;