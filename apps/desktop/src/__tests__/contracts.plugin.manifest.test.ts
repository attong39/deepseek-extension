import { describe, expect, it } from "vitest";

import schema from "../../contracts/plugins/plugin-manifest.schema.json";
import Plugin from "Plugin";

describe("Plugin manifest schema freeze", () => {
  it("is stable", () => {
    expect(schema).toMatchSnapshot();
  });
});
