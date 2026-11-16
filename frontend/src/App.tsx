import { useEffect, useState } from 'react';
import './App.css';

interface Transaction {
  id: string;
  store: string;
  amount: number;
  status: string;
}

interface SalesData {
  total_revenue: number;
  total_orders: number;
  top_category: string;
  recent_transactions: Transaction[];
}

function App() {
  const [salesData, setSalesData] = useState<SalesData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch data from our FastAPI backend running on port 8000
    fetch('/api/sales-summary')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch data from backend');
        }
        return res.json();
      })
      .then((data) => {
        setSalesData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '40px', fontFamily: 'Inter, sans-serif', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ marginBottom: '30px', borderBottom: '1px solid #334155', paddingBottom: '20px' }}>
        <h1 style={{ margin: 0, fontSize: '28px', color: '#38bdf8' }}>Databricks Retail Analytics Dashboard</h1>
        <p style={{ margin: '5px 0 0', color: '#94a3b8' }}>Phase 1: Full-Stack Integration (React + FastAPI + Databricks Architecture)</p>
      </header>

      {loading && <p>Loading live retail metrics...</p>}
      {error && <p style={{ color: '#ef4444' }}>Error: {error}</p>}

      {salesData && (
        <div>
          {/* KPI Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', marginBottom: '40px' }}>
            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 10px', fontSize: '14px', color: '#94a3b8' }}>TOTAL REVENUE</h3>
              <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#4ade80' }}>
                ₹{salesData.total_revenue.toLocaleString('en-IN')}
              </p>
            </div>
            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 10px', fontSize: '14px', color: '#94a3b8' }}>TOTAL ORDERS</h3>
              <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#38bdf8' }}>
                {salesData.total_orders.toLocaleString()}
              </p>
            </div>
            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 10px', fontSize: '14px', color: '#94a3b8' }}>TOP CATEGORY</h3>
              <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#c084fc' }}>
                {salesData.top_category}
              </p>
            </div>
          </div>

          {/* Transactions Table */}
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
            <h3 style={{ marginTop: 0, marginBottom: '15px', fontSize: '18px' }}>Recent Transactions</h3>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
                  <th style={{ padding: '10px' }}>Transaction ID</th>
                  <th style={{ padding: '10px' }}>Store Location</th>
                  <th style={{ padding: '10px' }}>Amount (₹)</th>
                  <th style={{ padding: '10px' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {salesData.recent_transactions.map((tx) => (
                  <tr key={tx.id} style={{ borderBottom: '1px solid #334155' }}>
                    <td style={{ padding: '10px' }}>{tx.id}</td>
                    <td style={{ padding: '10px' }}>{tx.store}</td>
                    <td style={{ padding: '10px' }}>₹{tx.amount.toLocaleString('en-IN')}</td>
                    <td style={{ padding: '10px' }}>
                      <span style={{ 
                        padding: '4px 8px', 
                        borderRadius: '4px', 
                        fontSize: '12px',
                        backgroundColor: tx.status === 'Completed' ? 'rgba(74, 222, 128, 0.2)' : 'rgba(250, 204, 21, 0.2)',
                        color: tx.status === 'Completed' ? '#4ade80' : '#facc15'
                      }}>
                        {tx.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;