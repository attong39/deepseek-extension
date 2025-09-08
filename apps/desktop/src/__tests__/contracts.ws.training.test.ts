import { describe, expect, it } from "vitest";

import schema from "../../contracts/ws/training-progress.schema.json";
import WS from "WS";

describe("WS schema freeze", () => {
  it("is stable", () => {
    // snapshot để phát hiện drift
    expect(schema).toMatchSnapshot();
  });
});
