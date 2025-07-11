import React from 'react';
import ReactDOM from 'react-dom/client';
import AgentCard from './components/AgentCard';
import TaskBoard from './components/TaskBoard';
import TrainingDashboard from './components/TrainingDashboard';

const App = () => {
  const sampleAgent = {
    id: 'a1b2c3d4',
    name: 'Analyzer-1',
    role: 'Data Analysis',
    is_running: true,
  };

  return (
    <div>
      <h1>Welcome to AgentAlpha</h1>
      <p>The future of AGI is here.</p>
      <div style={{ display: 'flex' }}>
        <AgentCard agent={sampleAgent} />
        <TaskBoard />
        <TrainingDashboard />
      </div>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
