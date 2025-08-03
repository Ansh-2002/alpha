import React, { useState, useEffect } from 'react';
import { peopleApi } from './services/api';
import PersonCard from './components/PersonCard';
import ResultsCard from './components/ResultsCard';

function App() {
  const [people, setPeople] = useState([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPeople = async () => {
      try {
        const response = await peopleApi.getAll();
        setPeople(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to fetch people');
      } finally {
        setLoading(false);
      }
    };

    fetchPeople();
  }, []);

  const handleEnrichmentComplete = (result) => {
    if (result && result.company_id) {
      setSelectedCompanyId(result.company_id);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Alpha Platform - Deep Research Agent</h1>
        <p>Select a person to run deep research and extract company insights</p>
      </div>

      <div className="people-list">
        <h2 style={{ padding: '20px', margin: 0, borderBottom: '1px solid #eee' }}>
          People ({people.length})
        </h2>
        {people.map((person) => (
          <PersonCard 
            key={person.id} 
            person={person}
            onEnrichmentComplete={handleEnrichmentComplete}
          />
        ))}
      </div>

      {selectedCompanyId && (
        <ResultsCard companyId={selectedCompanyId} />
      )}
    </div>
  );
}

export default App;