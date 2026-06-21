import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState({ anomalies: [], total_anomalies: 0, total_checked_windows: 0, threshold: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/anomalies")
      .then(res => res.json())
      .then(resData => {
        setData(resData);
        setLoading(false);
      })
      .catch(err => console.error("Error connecting to server:", err));
  }, []);

  if (loading) {
    return (
      <div style={{padding: '40px', color: '#fff', backgroundColor: '#1a1a1a', height: '100vh', fontFamily: 'sans-serif'}}>
        📡 Connecting to local pipeline telemetry...
      </div>
    );
  }

  return (
    <div style={{ padding: '30px', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto', backgroundColor: '#1a1a1a', color: '#eaeaea', minHeight: '100vh' }}>
      <header style={{ borderBottom: '2px solid #333', paddingBottom: '15px', marginBottom: '30px' }}>
        <h1 style={{ margin: 0, color: '#ff4a4a', fontSize: '28px' }}>🚨 AI Log Anomaly Detection Center</h1>
        <p style={{ color: '#888', margin: '5px 0 0 0' }}>System Engine Model Status: Active | Evaluated Threshold: <strong>{data.threshold}</strong></p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '30px' }}>
        <div style={{ padding: '20px', background: '#252529', borderRadius: '8px', borderLeft: '4px solid #ff4a4a' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#aaa', fontSize: '14px', textTransform: 'uppercase' }}>Total Flagged Anomalies</h3>
          <p style={{ fontSize: '36px', margin: 0, fontWeight: 'bold', color: '#ff4a4a' }}>{data.total_anomalies}</p>
        </div>
        <div style={{ padding: '20px', background: '#252529', borderRadius: '8px', borderLeft: '4px solid #00E676' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#aaa', fontSize: '14px', textTransform: 'uppercase' }}>Total Checked Log Windows</h3>
          <p style={{ fontSize: '36px', margin: 0, fontWeight: 'bold', color: '#00E676' }}>{data.total_checked_windows}</p>
        </div>
      </div>

      <div style={{ background: '#252529', borderRadius: '8px', padding: '20px', overflowX: 'auto' }}>
        <h2 style={{ marginTop: 0, fontSize: '20px', borderBottom: '1px solid #444', paddingBottom: '10px', color: '#fff' }}>Real-time Alert Pipeline</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px', textAlign: 'left' }}>
          <thead>
            <tr style={{ color: '#aaa', borderBottom: '2px solid #444', fontSize: '14px' }}>
              <th style={{ padding: '12px' }}>Window Sequence Block ID</th>
              <th style={{ padding: '12px' }}>Model Reconstruction Loss</th>
              <th style={{ padding: '12px' }}>Severity Status</th>
              <th style={{ padding: '12px' }}>System Diagnostics Message</th>
            </tr>
          </thead>
          <tbody>
            {data.anomalies.map((alert) => (
              <tr key={alert.window_id} style={{ borderBottom: '1px solid #333' }}>
                <td style={{ padding: '12px', fontWeight: 'bold' }}>#{alert.window_id}</td>
                <td style={{ padding: '12px', color: '#ffb74d', fontWeight: '500' }}>{alert.score}</td>
                <td style={{ padding: '12px' }}>
                  <span style={{ 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    fontSize: '11px', 
                    fontWeight: 'bold',
                    backgroundColor: alert.severity === 'CRITICAL' ? '#c62828' : '#e65100',
                    color: '#fff'
                  }}>
                    {alert.severity}
                  </span>
                </td>
                <td style={{ padding: '12px', color: '#ccc', fontSize: '14px' }}>{alert.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;