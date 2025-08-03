import React, { useState, useEffect } from 'react';
import { enrichmentApi } from '../services/api';
import { usePolling } from '../hooks/usePolling';

const ResearchProgress = ({ jobId, personId, onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState([]);
  const [isComplete, setIsComplete] = useState(false);

  const pollJob = async () => {
    const response = await enrichmentApi.getJobStatus(jobId);
    return response.data;
  };

  const { data: jobStatus, error } = usePolling(
    pollJob, 
    3000, 
    !isComplete
  );

  useEffect(() => {
    if (jobStatus) {
      const status = jobStatus.status;
      
      if (status === 'started') {
        setProgress(33);
        setLogs(prev => [...prev, 'Research job started...']);
      } else if (status === 'finished') {
        setProgress(100);
        setLogs(prev => [...prev, 'Research completed successfully!']);
        setIsComplete(true);
        if (onComplete) {
          onComplete(jobStatus.result);
        }
      } else if (status === 'failed') {
        setProgress(0);
        setLogs(prev => [...prev, `Research failed: ${jobStatus.error}`]);
        setIsComplete(true);
      } else if (status === 'queued') {
        setProgress(10);
        setLogs(prev => [...prev, 'Research job queued...']);
      }
    }
  }, [jobStatus, onComplete]);

  useEffect(() => {
    if (error) {
      setLogs(prev => [...prev, `Error: ${error.message}`]);
    }
  }, [error]);

  if (isComplete && progress === 100) {
    return null;
  }

  return (
    <div className="progress-container">
      <h4>Research Progress</h4>
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <div>{progress}% complete</div>
      
      <div className="log-console">
        {logs.map((log, index) => (
          <div key={index}>{new Date().toLocaleTimeString()}: {log}</div>
        ))}
      </div>
    </div>
  );
};

export default ResearchProgress;