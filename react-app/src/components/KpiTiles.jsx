import PropTypes from 'prop-types';
import { PhoneCall, MessageSquare, Globe, Clock, MapPin } from 'lucide-react';

const KpiTiles = ({ summary }) => {
  if (!summary) return null;
  
  return (
    <div className="row g-4 mb-5">
      <div className="col">
        <div className="card kpi-card p-3 h-100">
          <div className="kpi-label"><PhoneCall size={16} className="me-2"/>Calls</div>
          <div className="kpi-value">{summary.total_calls.toLocaleString()}</div>
        </div>
      </div>
      <div className="col">
        <div className="card kpi-card p-3 h-100">
          <div className="kpi-label"><MessageSquare size={16} className="me-2"/>SMS</div>
          <div className="kpi-value">{summary.total_sms.toLocaleString()}</div>
        </div>
      </div>
      <div className="col">
        <div className="card kpi-card p-3 h-100">
          <div className="kpi-label"><Globe size={16} className="me-2"/>Data</div>
          <div className="kpi-value">{Math.round(summary.total_internet_mb).toLocaleString()} MB</div>
        </div>
      </div>
      <div className="col">
        <div className="card kpi-card p-3 h-100">
          <div className="kpi-label"><Clock size={16} className="me-2"/>Peak</div>
          <div className="kpi-value">{summary.peak_hour}:00</div>
        </div>
      </div>
      <div className="col">
        <div className="card kpi-card p-3 h-100">
          <div className="kpi-label"><MapPin size={16} className="me-2"/>Busiest</div>
          <div className="kpi-value text-truncate">{summary.busiest_region}</div>
        </div>
      </div>
    </div>
  );
};

KpiTiles.propTypes = {
  summary: PropTypes.shape({
    total_calls: PropTypes.number.isRequired,
    total_sms: PropTypes.number.isRequired,
    total_internet_mb: PropTypes.number.isRequired,
    peak_hour: PropTypes.number.isRequired,
    busiest_region: PropTypes.string.isRequired,
  })
};

export default KpiTiles;