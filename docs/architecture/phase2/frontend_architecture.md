# Phase 2 - Step 02: Frontend Architecture Lock
Status: Architecture Lock - DONE

## Purpose
- Define the frontend architecture baseline for Phase 2 implementations without making product or UX decisions.
- Establish folder boundaries, state management expectations, and API access rules to avoid business logic creeping into the UI.
- Require any deviations to be documented in docs/decisions/.

## Stack Baseline
- Framework and tooling: React with Vite and TypeScript targeting Node 20+.
- Styling: TailwindCSS for utility-first styling; design tokens and shared classes must be centralized.
- Component library: shadcn/ui components may be used when consistent with Tailwind theming; custom components must follow the same accessibility and styling rules.
- Routing: React Router (or Vite-compatible router) for client-side navigation with route-level code splitting when possible.
- API client: centralized fetch layer (e.g., api/client.ts) handling base URL configuration, authentication headers, and error normalization.

## Folder and Module Boundaries
- **pages/**: Route-level components responsible for data loading orchestration and composition. Pages coordinate hooks and components but must not contain business rules.
- **components/**: Reusable presentational or container components. Presentational components accept props and render UI only; container components may wire hooks but must not embed business logic.
- **hooks/**: Shared logic for stateful concerns such as data fetching, form management, and feature toggles. Hooks encapsulate side effects and should consume the centralized API client for network calls.
- **api/**: Typed client definitions, request/response DTOs, and API-specific utilities. No UI logic or routing concerns belong here.
- Shared utilities (e.g., formatters) must live outside components to avoid duplication, and must remain free of business decisions.

## Rules and Dependency Direction
- UI components must not encode business rules; validation rules beyond basic formatting belong in domain or backend contracts and are consumed via hooks or API responses.
- Pages may depend on hooks, components, and api/ clients; components must not import from pages/.
- API client is the only layer issuing HTTP requests; direct fetch calls elsewhere are forbidden.
- Routing contract: pages register routes centrally with lazy loading where feasible; nested routing must keep params parsing inside route-level loaders or hooks.
- Cross-cutting concerns (theming, error boundaries, localization scaffolding) must be provided via top-level providers and consumed through context or hooks, not by ad hoc imports.

## State Management Rules
- Prefer React Query (or equivalent lightweight fetch caching) for server state; direct global stores for server data are forbidden.
- Local UI state should stay inside components using useState/useReducer; avoid prop drilling by composing components or using context only when shared state is required.
- Global client state (e.g., auth session, feature flags) must live in narrowly scoped providers with typed contexts; avoid uncontrolled global singletons.
- Do not store derived or transient server data in global state when it can be fetched or memoized through hooks.
- Any new state management library beyond React Query and React context requires a DECISION in docs/decisions/.

## Testing Strategy Boundaries
- Component tests verify rendering, accessibility cues, and interaction contracts without mocking business rules.
- Hook tests focus on side-effect coordination, API client usage, and error handling pathways.
- Integration tests exercise routing, API client wiring, and page composition against mock servers; UI assertions must track architecture contracts, not domain outcomes.
- Snapshot tests are acceptable for stable presentational components only; avoid snapshots for dynamic data flows.

## Enforcement and Deviations
- Architecture boundaries must be validated during review and CI linting; direct fetches, business logic in components, or unauthorized global state use must be rejected.
- Any deviation from these boundaries requires a documented DECISION under docs/decisions/ with justification and scope.
