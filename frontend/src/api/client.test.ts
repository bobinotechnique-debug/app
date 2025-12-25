import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiClient, createApiClient } from "./client";

describe("ApiClient", () => {
  afterEach(() => {
    vi.restoreAllMocks();
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
});
