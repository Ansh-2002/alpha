import React, { useEffect, useState } from 'react';
import { companiesApi } from '../services/api';

const ResultsCard = ({ companyId }) => {
  const [snippets, setSnippets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSnippets = async () => {
      try {
        const response = await companiesApi.getSnippets(companyId);
        setSnippets(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to fetch results');
      } finally {
        setLoading(false);
      }
    };

    if (companyId) {
      fetchSnippets();
    }
  }, [companyId]);

  if (loading) {
    return <div className="loading">Loading results...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (snippets.length === 0) {
    return <div>No research results available yet.</div>;
  }

  return (
    <div className="results-card">
      <h3>Research Results</h3>
      {snippets.map((snippet) => (
        <div key={snippet.id} className="snippet">
          <div className="field-group">
            <label>Company Value Proposition:</label>
            <div className="value">
              {snippet.payload.company_value_prop || 'Not found'}
            </div>
          </div>
          
          <div className="field-group">
            <label>Product Names:</label>
            <div className="value">
              {Array.isArray(snippet.payload.product_names) 
                ? snippet.payload.product_names.join(', ') 
                : snippet.payload.product_names || 'Not found'}
            </div>
          </div>
          
          <div className="field-group">
            <label>Pricing Model:</label>
            <div className="value">
              {snippet.payload.pricing_model || 'Not found'}
            </div>
          </div>
          
          <div className="field-group">
            <label>Key Competitors:</label>
            <div className="value">
              {Array.isArray(snippet.payload.key_competitors) 
                ? snippet.payload.key_competitors.join(', ') 
                : snippet.payload.key_competitors || 'Not found'}
            </div>
          </div>
          
          <div className="field-group">
            <label>Company Domain:</label>
            <div className="value">
              {snippet.payload.company_domain || 'Not found'}
            </div>
          </div>
          
          <div className="field-group">
            <label>Source URLs:</label>
            <div className="value">
              {snippet.source_urls && snippet.source_urls.length > 0 
                ? snippet.source_urls.map((url, index) => (
                    <div key={index}>
                      <a href={url} target="_blank" rel="noopener noreferrer">
                        {url}
                      </a>
                    </div>
                  ))
                : 'No sources available'}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ResultsCard;