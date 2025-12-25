import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { AppRoutes } from "./App";

describe("AppRoutes", () => {
  const wrapper = (ui: React.ReactNode, initialEntries: string[]) => {
    const queryClient = new QueryClient();

    return render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={initialEntries}>{ui}</MemoryRouter>
      </QueryClientProvider>,
    );
  };

  it("renders the home route", () => {
    wrapper(<AppRoutes />, ["/"]);

    expect(screen.getByRole("heading", { level: 1, name: /welcome to the planning frontend/i })).toBeInTheDocument();
  });

  it("renders a not found page for unknown routes", () => {
    wrapper(<AppRoutes />, ["/missing"]);

    expect(screen.getByRole("heading", { level: 1, name: /page not found/i })).toBeInTheDocument();
  });

  it("renders the placeholder route", () => {
    wrapper(<AppRoutes />, ["/placeholder"]);

    expect(screen.getByRole("heading", { level: 1, name: /placeholder/i })).toBeInTheDocument();
  });
});

