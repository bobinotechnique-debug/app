import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiClient, createApiClient } from "./client";

describe("ApiClient", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllEnvs();
  });

  it("constructs with the default base URL", () => {
    const client = new ApiClient();

    expect(client).toBeInstanceOf(ApiClient);
  });

  it("performs a GET request via fetch", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(null, { status: 200 }));
    const client = createApiClient({ baseUrl: "https://example.test" });

    await client.get("/status");

    expect(fetchSpy).toHaveBeenCalledWith("https://example.test/status", { method: "GET" });
  });

  it("defaults to the window origin with the /api prefix when no config is provided", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(null, { status: 200 }));
    const client = new ApiClient();

    await client.get("/status");

    expect(fetchSpy).toHaveBeenCalledWith(`${window.location.origin}/api/status`, { method: "GET" });
  });

  it("prefers an environment base URL when present", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "https://env.example/api");
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(null, { status: 200 }));
    const client = new ApiClient();

    await client.get("/status");

    expect(fetchSpy).toHaveBeenCalledWith("https://env.example/api/status", { method: "GET" });
  });
});
