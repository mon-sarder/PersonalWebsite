import { useEffect } from 'react';
import { trackPageView } from '../services/api';

/**
 * Custom hook to track page views
 * @param {string} pageName - Name of the page to track
 */
export const usePageTracking = (pageName) => {
  useEffect(() => {
    trackPageView(pageName);
  }, [pageName]);
};