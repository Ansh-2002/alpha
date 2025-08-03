import React, { useState } from 'react';
import { enrichmentApi } from '../services/api';
import ResearchProgress from './ResearchProgress';

const PersonCard = ({ person, onEnrichmentComplete }) => {
  const [isEnriching, setIsEnriching] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [error, setError] = useState(null);

  const handleEnrich = async () => {
    try {
      setIsEnriching(true);
      setError(null);
      const response = await enrichmentApi.enrich(person.id);
      setJobId(response.data.job_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start enrichment');
      setIsEnriching(false);
    }
  };

  const handleEnrichmentComplete = (result) => {
    setIsEnriching(false);
    setJobId(null);
    if (onEnrichmentComplete) {
      onEnrichmentComplete(result);
    }
  };

  return (
    <div className="person-card">
      <div className="person-info">
        <h3>{person.full_name}</h3>
        <p>{person.email}</p>
        <p>{person.title}</p>
      </div>
      <div>
        <button 
          className="research-btn"
          onClick={handleEnrich}
          disabled={isEnriching}
        >
          {isEnriching ? 'Researching...' : 'Run Research'}
        </button>
        {error && <div className="error">{error}</div>}
        {jobId && (
          <ResearchProgress 
            jobId={jobId} 
            personId={person.id}
            onComplete={handleEnrichmentComplete}
          />
        )}
      </div>
    </div>
  );
};

export default PersonCard;