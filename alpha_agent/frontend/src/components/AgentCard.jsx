import React from 'react';

const AgentCard = ({ agent }) => {
  if (!agent) {
    return null;
  }

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '16px', margin: '16px', maxWidth: '300px' }}>
      <h3>{agent.name}</h3>
      <p><strong>ID:</strong> {agent.id}</p>
      <p><strong>Role:</strong> {agent.role}</p>
      <p><strong>Status:</strong> {agent.is_running ? 'Running' : 'Stopped'}</p>
    </div>
  );
};

export default AgentCard;
