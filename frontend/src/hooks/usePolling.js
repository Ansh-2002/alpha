import { useState, useEffect, useCallback } from 'react';

export const usePolling = (pollFunction, interval = 3000, shouldPoll = true) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const poll = useCallback(async () => {
    if (!shouldPoll) return;
    
    try {
      setLoading(true);
      const result = await pollFunction();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [pollFunction, shouldPoll]);

  useEffect(() => {
    if (!shouldPoll) return;

    poll();
    const intervalId = setInterval(poll, interval);

    return () => clearInterval(intervalId);
  }, [poll, interval, shouldPoll]);

  return { data, error, loading, refetch: poll };
};