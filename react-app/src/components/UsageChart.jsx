import PropTypes from 'prop-types';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const UsageChart = ({ data }) => (
  <div className="content-section">
    <h4 className="mb-4" style={{fontWeight: 700}}>Network Usage Trends</h4>
    <div style={{ width: '100%', height: '450px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis dataKey="hour" axisLine={false} tickLine={false} />
          <YAxis tickFormatter={(val) => `${(val / 1000000).toFixed(0)}M`} axisLine={false} tickLine={false} />
          <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px rgba(0,0,0,0.1)'}} />
          <Bar dataKey="usage" fill="#6366f1" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
);

UsageChart.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape({
    hour: PropTypes.string.isRequired,
    usage: PropTypes.number.isRequired,
  })).isRequired
};

export default UsageChart;