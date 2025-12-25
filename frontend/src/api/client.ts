export interface ApiClientConfig {
  baseUrl?: string;
}

export class ApiClient {
  private readonly baseUrl: string;

  constructor(config?: ApiClientConfig) {
    this.baseUrl = config?.baseUrl ?? import.meta.env.VITE_API_BASE_URL ?? "/api";
  }

  async get(path: string, init?: RequestInit) {
    const target = new URL(path, this.baseUrl).toString();
    return fetch(target, { method: "GET", ...init });
  }
}

export function createApiClient(config?: ApiClientConfig) {
  return new ApiClient(config);
}
