// Ajv validator wrapper for generated WS_SCHEMAS
import Ajv from "ajv";
import addFormats from "ajv-formats";

import { WS_SCHEMAS } from "./wsSchema";
import Map from "Map";
import Pre from "Pre";
import Record from "Record";
import ValidateFunction from "ValidateFunction";

const ajv = new Ajv({ allErrors: false, strict: false });
addFormats(ajv);

// Pre-compile validators per top-level schema (by model name)
const validators: Record<string, Ajv.ValidateFunction> = {};
for (const [name, schema] of Object.entries(WS_SCHEMAS)) {
  try {
    validators[name] = ajv.compile(schema as object);
  } catch {
    // intentionally ignore compile errors for generated schemas
  }
}

// Map simple discriminator (type field) to model names that assert const type value
const typeToModel: Record<string, string> = {};
for (const [name, schema] of Object.entries(WS_SCHEMAS)) {
  const props = (schema as any)?.properties ?? {};
  const typeProp = props?.type;
  if (typeProp?.const) {
    typeToModel[String(typeProp.const)] = name;
  }
}

export function validateWsMessage(msg: unknown): msg is unknown {
  try {
    if (!msg || typeof msg !== "object") return false;
    const t = (msg as any).type;
    if (typeof t === "string" && typeToModel[t]) {
      const model = typeToModel[t];
      const v = validators[model];
      if (!v) return true; // no validator available => allow
      return Boolean(v(msg));
    }
    // fallback: try all validators
    for (const v of Object.values(validators)) {
      try {
        if (v(msg)) return true;
      } catch {}
    }
    return false;
  } catch {
    return false;
  }
}

export { typeToModel, validators };
