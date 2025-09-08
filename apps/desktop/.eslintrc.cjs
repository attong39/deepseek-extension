module.exports = {
  parser: "@typescript-eslint/parser",
  plugins: ["import", "@typescript-eslint"],
  extends: ["plugin:import/recommended", "plugin:@typescript-eslint/recommended"],
  settings: {
    "import/resolver": {
      typescript: { project: ["tsconfig.json"] },
    },
  },
  rules: {
    "import/no-relative-parent-imports": "error",
    "import/first": "error",
    "import/no-duplicates": "error",
    "import/order": [
      "warn",
      {
        "groups": [["builtin", "external"], ["internal"], ["parent", "sibling", "index"]],
        "newlines-between": "always",
        "alphabetize": { "order": "asc", "caseInsensitive": true }
      }
    ]
  },
};
