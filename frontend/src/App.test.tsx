import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { AppRoutes } from "./App";

describe("AppRoutes", () => {
  it("renders the home route", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <AppRoutes />
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { level: 1, name: /welcome to the planning frontend/i })).toBeInTheDocument();
  });

  it("renders a not found page for unknown routes", () => {
    render(
      <MemoryRouter initialEntries={["/missing"]}>
        <AppRoutes />
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { level: 1, name: /page not found/i })).toBeInTheDocument();
  });
});

