import { afterEach, beforeAll } from "vitest";

import { installWsMock, resetWsMock } from "./ws-mock";

beforeAll(() => { installWsMock(); });
afterEach(() => { resetWsMock(); });