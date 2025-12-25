export interface ApiClientConfig {
  baseUrl?: string;
}

export class ApiClient {
  private readonly baseUrl: string;

  constructor(config?: ApiClientConfig) {
    this.baseUrl = resolveBaseUrl(config);
  }

  async get(path: string, init?: RequestInit) {
    const normalizedPath = path.startsWith("/") ? path.slice(1) : path;
    const target = new URL(normalizedPath, this.baseUrl).toString();
    return fetch(target, { method: "GET", ...init });
  }
}

export function createApiClient(config?: ApiClientConfig) {
  return new ApiClient(config);
}

function resolveBaseUrl(config?: ApiClientConfig) {
  if (config?.baseUrl) {
    return ensureTrailingSlash(config.baseUrl);
  }

  if (import.meta.env.VITE_API_BASE_URL) {
    return ensureTrailingSlash(import.meta.env.VITE_API_BASE_URL);
  }

  if (typeof window !== "undefined" && window.location?.origin) {
    return ensureTrailingSlash(`${window.location.origin}/api`);
  }

  return ensureTrailingSlash("/api");
}

function ensureTrailingSlash(url: string) {
  return url.endsWith("/") ? url : `${url}/`;
}
