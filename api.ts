import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';
import {
  Contact,
  Project,
  Skill,
  AnalyticsEvent,
  ApiResponse,
  AuthResponse,
  DashboardStats,
  ContactFormData,
  ApiError
} from '@/types';

// Configure axios instance
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000, // 10 seconds
    });

    // Load token from localStorage
    this.token = localStorage.getItem('auth_token');

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        // Add auth token if available
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        return Promise.reject(this.handleError(error));
      }
    );
  }

  // Error handler
  private handleError(error: AxiosError): ApiError {
    if (error.response) {
      // Server responded with error status
      const data = error.response.data as any;
      return new ApiError(
        error.response.status,
        data.error || data.message || 'An error occurred',
        data.errors
      );
    } else if (error.request) {
      // Request made but no response
      return new ApiError(0, 'Network error - please check your connection');
    } else {
      // Something else happened
      return new ApiError(0, error.message || 'An unexpected error occurred');
    }
  }

  // Set authentication token
  setAuthToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  // Authentication
  async login(username: string, password: string): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/login', {
      username,
      password
    });

    if (response.data.token) {
      this.setAuthToken(response.data.token);
    }

    return response.data;
  }

  logout() {
    this.setAuthToken(null);
  }

  // Contact Form API
  async submitContactForm(data: ContactFormData): Promise<ApiResponse<Contact>> {
    const response = await this.api.post<ApiResponse<Contact>>('/contact', data);
    return response.data;
  }

  async getContacts(): Promise<Contact[]> {
    const response = await this.api.get<{ contacts: Contact[] }>('/contacts');
    return response.data.contacts;
  }

  async markContactAsRead(contactId: string): Promise<void> {
    await this.api.patch(`/contacts/${contactId}/read`);
  }

  // Projects API
  async getProjects(): Promise<Project[]> {
    const response = await this.api.get<{ projects: Project[] }>('/projects');
    return response.data.projects;
  }

  async getProject(projectId: string): Promise<Project> {
    const response = await this.api.get<Project>(`/projects/${projectId}`);
    return response.data;
  }

  async createProject(project: Omit<Project, 'id' | 'created_at'>): Promise<Project> {
    const response = await this.api.post<Project>('/projects', project);
    return response.data;
  }

  async updateProject(projectId: string, updates: Partial<Project>): Promise<Project> {
    const response = await this.api.put<Project>(`/projects/${projectId}`, updates);
    return response.data;
  }

  async deleteProject(projectId: string): Promise<void> {
    await this.api.delete(`/projects/${projectId}`);
  }

  // Skills API
  async getSkills(grouped: boolean = true): Promise<Record<string, Skill[]> | Skill[]> {
    const response = await this.api.get<{ skills: Record<string, Skill[]> | Skill[] }>(
      '/skills',
      { params: { grouped: grouped.toString() } }
    );
    return response.data.skills;
  }

  async getSkill(skillId: string): Promise<Skill> {
    const response = await this.api.get<Skill>(`/skills/${skillId}`);
    return response.data;
  }

  async createSkill(skill: Omit<Skill, 'id' | 'created_at'>): Promise<Skill> {
    const response = await this.api.post<Skill>('/skills', skill);
    return response.data;
  }

  async updateSkill(skillId: string, updates: Partial<Skill>): Promise<Skill> {
    const response = await this.api.put<Skill>(`/skills/${skillId}`, updates);
    return response.data;
  }

  async deleteSkill(skillId: string): Promise<void> {
    await this.api.delete(`/skills/${skillId}`);
  }

  async createSkillsBatch(skills: Array<Omit<Skill, 'id' | 'created_at'>>): Promise<void> {
    await this.api.post('/skills/batch', { skills });
  }

  // Analytics API
  async trackPageView(page: string): Promise<void> {
    try {
      await this.api.post('/analytics/track', {
        type: 'page_view',
        page
      });
    } catch (error) {
      // Don't throw errors for analytics
      console.error('Failed to track page view:', error);
    }
  }

  async trackProjectClick(projectId: string, projectTitle: string): Promise<void> {
    try {
      await this.api.post('/analytics/track', {
        type: 'project_click',
        project_id: projectId,
        project_title: projectTitle
      });
    } catch (error) {
      // Don't throw errors for analytics
      console.error('Failed to track project click:', error);
    }
  }

  async getAnalyticsDashboard(days: number = 30): Promise<DashboardStats> {
    const response = await this.api.get<DashboardStats>('/analytics/dashboard', {
      params: { days }
    });
    return response.data;
  }

  async getRecentEvents(limit: number = 50): Promise<AnalyticsEvent[]> {
    const response = await this.api.get<{ events: AnalyticsEvent[] }>('/analytics/events', {
      params: { limit }
    });
    return response.data.events;
  }

  // Utility method for custom requests
  async request<T>(config: AxiosRequestConfig): Promise<T> {
    const response = await this.api.request<T>(config);
    return response.data;
  }
}

// Export singleton instance
const apiService = new ApiService();
export default apiService;

// Export individual functions for backward compatibility
export const {
  submitContactForm,
  getProjects,
  getProject,
  getSkills,
  trackPageView,
  trackProjectClick,
} = {
  submitContactForm: (data: ContactFormData) => apiService.submitContactForm(data),
  getProjects: () => apiService.getProjects(),
  getProject: (id: string) => apiService.getProject(id),
  getSkills: (grouped?: boolean) => apiService.getSkills(grouped),
  trackPageView: (page: string) => apiService.trackPageView(page),
  trackProjectClick: (id: string, title: string) => apiService.trackProjectClick(id, title),
};