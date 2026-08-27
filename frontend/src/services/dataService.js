import { apiGet } from './api';

export function fetchApplications(limit) {
  const query = limit ? `?limit=${encodeURIComponent(limit)}` : '';
  return apiGet(`/api/v1/applications${query}`);
}

export function fetchApplicationById(id) {
  return apiGet(`/api/v1/applications/${encodeURIComponent(id)}`);
}

export function fetchDataSources() {
  return apiGet('/api/v1/data-sources');
}

export function fetchStats() {
  return apiGet('/api/v1/stats');
}

export function criticalityVariant(criticality) {
  if (criticality === 'Critique') return 'critical';
  if (criticality === 'Élevée' || criticality === 'Haute') return 'danger';
  return 'warning';
}
