import React, { useState, useEffect } from 'react';

const TaskBoard = () => {
  const [logs, setLogs] = useState([]);

  // This is a placeholder for a WebSocket connection
  useEffect(() => {
    const interval = setInterval(() => {
      const newLog = `[${new Date().toLocaleTimeString()}] New log entry.`;
      setLogs(prevLogs => [...prevLogs, newLog]);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleFeedback = (feedback) => {
    // In a real implementation, this would send the feedback to the backend
    console.log(`Feedback received: ${feedback}`);
  };

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '16px', margin: '16px', height: '400px', overflowY: 'scroll' }}>
      <h3>Task Board / Live Log</h3>
      <div>
        {logs.map((log, index) => (
          <div key={index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <p style={{ margin: 0 }}>{log}</p>
            <div>
              <button onClick={() => handleFeedback('good')} style={{ marginRight: '8px' }}>Good</button>
              <button onClick={() => handleFeedback('bad')}>Bad</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskBoard;
