const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';

export async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { Accept: 'application/json' },
  });

  if (!response.ok) {
    let message = `Erreur API (${response.status})`;
    try {
      const body = await response.json();
      if (body?.error?.message) {
        message = body.error.message;
      }
    } catch {
      // Keep the generic status message when the body is not JSON.
    }
    throw new Error(message);
  }

  return response.json();
}
