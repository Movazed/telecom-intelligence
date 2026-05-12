import { useState } from 'react';
import PropTypes from 'prop-types';
import { AlertTriangle, Zap, Info } from 'lucide-react';

const RiskForm = ({ formData, setFormData, onPredict, prediction }) => {
  const [errors, setErrors] = useState({});

  // 1. Validation Logic
  const validate = () => {
    let newErrors = {};
    if (!formData.region || formData.region.trim() === "") newErrors.region = "Region name is required";
    if (formData.avg_usage < 0) newErrors.avg_usage = "Usage cannot be negative";
    if (formData.growth_rate < -1 || formData.growth_rate > 1) newErrors.growth_rate = "Rate must be between -1 and 1";
    if (formData.variability < 0 || formData.variability > 1) newErrors.variability = "Variability must be between 0 and 1";
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onPredict(e);
    }
  };

  const getRiskStyles = (risk) => {
    switch (risk) {
      case 'HIGH': return 'bg-danger-subtle border-danger text-danger';
      case 'MEDIUM': return 'bg-warning-subtle border-warning text-dark';
      default: return 'bg-success-subtle border-success text-success';
    }
  };

  return (
    <div className="content-section">
      <h4 className="mb-4 d-flex align-items-center" style={{ fontWeight: 700 }}>
        <AlertTriangle className="text-warning me-2" /> AI Risk Engine
      </h4>
      
      <form onSubmit={handleSubmit}>
        {/* Region */}
        <div className="mb-3">
          <label className="form-label small fw-bold text-muted">TARGET REGION</label>
          <input 
            className={`form-control form-control-lg ${errors.region ? 'is-invalid' : ''}`}
            value={formData.region} 
            onChange={e => setFormData({ ...formData, region: e.target.value })} 
          />
          {errors.region && <div className="invalid-feedback">{errors.region}</div>}
        </div>

        {/* Avg Usage */}
        <div className="mb-3">
          <label className="form-label small fw-bold text-muted">AVG USAGE (MB)</label>
          <input 
            type="number" 
            className={`form-control form-control-lg ${errors.avg_usage ? 'is-invalid' : ''}`}
            value={formData.avg_usage} 
            onChange={e => setFormData({ ...formData, avg_usage: parseFloat(e.target.value) || 0 })} 
          />
          {errors.avg_usage && <div className="invalid-feedback">{errors.avg_usage}</div>}
        </div>

        {/* Growth Rate */}
        <div className="mb-3">
          <label className="form-label small fw-bold text-muted">GROWTH RATE (-1.0 to 1.0)</label>
          <input 
            type="number" step="0.01"
            className={`form-control form-control-lg ${errors.growth_rate ? 'is-invalid' : ''}`}
            value={formData.growth_rate} 
            onChange={e => setFormData({ ...formData, growth_rate: parseFloat(e.target.value) || 0 })} 
          />
          {errors.growth_rate && <div className="invalid-feedback">{errors.growth_rate}</div>}
        </div>

        {/* Variability */}
        <div className="mb-4">
          <label className="form-label small fw-bold text-muted">VARIABILITY (0.0 to 1.0)</label>
          <input 
            type="number" step="0.01"
            className={`form-control form-control-lg ${errors.variability ? 'is-invalid' : ''}`}
            value={formData.variability} 
            onChange={e => setFormData({ ...formData, variability: parseFloat(e.target.value) || 0 })} 
          />
          {errors.variability && <div className="invalid-feedback">{errors.variability}</div>}
        </div>

        <button type="submit" className="btn btn-ai w-100 py-3 d-flex align-items-center justify-content-center">
          <Zap size={20} className="me-2" /> EXECUTE AI PREDICTION
        </button>
      </form>

      {/* Result Display */}
      {prediction && (
        <div className={`mt-4 p-3 rounded-4 border-start border-4 ${getRiskStyles(prediction.congestion_risk)}`}>
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="mb-0 fw-bold">RISK: {prediction.congestion_risk}</h5>
            <span className="badge bg-white text-dark border">Conf: {(prediction.score * 100).toFixed(0)}%</span>
          </div>
          {prediction.anomaly_flag && (
            <div className="mt-2 small fw-bold text-uppercase"><Info size={14}/> Anomaly Detected</div>
          )}
        </div>
      )}
    </div>
  );
};

RiskForm.propTypes = {
  formData: PropTypes.object.isRequired,
  setFormData: PropTypes.func.isRequired,
  onPredict: PropTypes.func.isRequired,
  prediction: PropTypes.object,
};

export default RiskForm;