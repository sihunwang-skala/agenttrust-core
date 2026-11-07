import "@testing-library/jest-dom/vitest";
import { beforeEach } from "vitest";

// App state is deep-linked through location.hash; start every test from a clean URL.
beforeEach(() => { window.history.replaceState(null, "", "/"); });
