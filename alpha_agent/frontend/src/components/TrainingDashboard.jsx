import React, { useState, useEffect } from 'react';

const TrainingDashboard = () => {
  const [trainingData, setTrainingData] = useState([]);

  // This is a placeholder for a WebSocket connection to receive training data
  useEffect(() => {
    const interval = setInterval(() => {
      const newReward = Math.random();
      setTrainingData(prevData => [...prevData, newReward]);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '16px', margin: '16px', height: '400px', overflowY: 'scroll' }}>
      <h3>Training Dashboard</h3>
      <div>
        <h4>Rewards Over Time</h4>
        <div style={{ border: '1px solid #eee', padding: '8px', height: '300px', overflowY: 'scroll' }}>
          {trainingData.map((reward, index) => (
            <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
              <div style={{ width: '50px' }}>Step {index + 1}:</div>
              <div style={{ flex: 1, backgroundColor: '#f0f0f0', borderRadius: '4px' }}>
                <div style={{ width: `${reward * 100}%`, backgroundColor: '#4caf50', height: '20px', borderRadius: '4px' }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TrainingDashboard;
