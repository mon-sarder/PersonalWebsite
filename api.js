import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Contact Form API
export const submitContactForm = async (contactData) => {
  try {
    const response = await api.post('/contact', contactData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to submit contact form' };
  }
};

// Projects API
export const getProjects = async () => {
  try {
    const response = await api.get('/projects');
    return response.data.projects;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch projects' };
  }
};

export const getProject = async (projectId) => {
  try {
    const response = await api.get(`/projects/${projectId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch project' };
  }
};

// Skills API
export const getSkills = async (grouped = true) => {
  try {
    const response = await api.get('/skills', {
      params: { grouped: grouped.toString() }
    });
    return response.data.skills;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch skills' };
  }
};

// Analytics API
export const trackPageView = async (page) => {
  try {
    await api.post('/analytics/track', {
      type: 'page_view',
      page
    });
  } catch (error) {
    console.error('Failed to track page view:', error);
  }
};

export const trackProjectClick = async (projectId, projectTitle) => {
  try {
    await api.post('/analytics/track', {
      type: 'project_click',
      project_id: projectId,
      project_title: projectTitle
    });
  } catch (error) {
    console.error('Failed to track project click:', error);
  }
};

export default api;