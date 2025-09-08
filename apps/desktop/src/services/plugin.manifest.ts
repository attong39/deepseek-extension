import Ajv from "ajv";

import allow from "../../config/plugins.allowlist.json";
import manifestSchema from "../../contracts/plugins/plugin-manifest.schema.json";
import Manifest from "Manifest";
import Map from "Map";
import PluginInfo from "PluginInfo";
import Set from "Set";

/** Đọc manifest tĩnh đóng gói trong app (không tải từ ngoài). */
type Manifest = {
  key: string; 
  name: string; 
  version: string; 
  capabilities: string[];
  entry: string; 
  enabled?: boolean;
};

type PluginInfo = {
  key: string;
  name: string;
  version: string;
  capabilities: string[];
  enabled: boolean;
};

const plugins = new Map<string, { info: PluginInfo; loader: () => any }>();

// Dưới đây là ví dụ quét folder đóng gói sẵn (vite import glob)
const modules = import.meta.glob<{ default: any }>(
  "../plugins/**/manifest.json",
  { eager: true, import: "default" }
);

export function registerPlugin(info: PluginInfo, loader: () => any) {
  plugins.set(info.key, { info, loader });
}

export function setEnabled(key: string, enabled: boolean) {
  const plugin = plugins.get(key);
  if (plugin) {
    plugin.info.enabled = enabled;
  }
}

export function getPlugin(key: string) {
  return plugins.get(key);
}

export function loadPluginManifests(): PluginInfo[] {
  const ajv = new Ajv({ strict: true });
  const validate = ajv.compile<Manifest>(manifestSchema as any);
  const granted = new Set(allow.allow);
  const loaded: PluginInfo[] = [];

  Object.entries(modules).forEach(([path, json]) => {
    const man = json as unknown as Manifest;
    if (!validate(man)) return;                    // drop nếu sai schema
    if (!granted.has(man.key)) return;             // drop nếu không trong allowlist
    
    // entry phải là module đóng gói sẵn trong app (vite glob)
    const entryMod = import.meta.glob<any>("../plugins/**/index.js", { eager: true });
    const hit = Object.values(entryMod)[0];
    if (!hit) return;

    const pluginInfo: PluginInfo = {
      key: man.key, 
      name: man.name, 
      version: man.version,
      capabilities: man.capabilities, 
      enabled: man.enabled ?? true
    };

    registerPlugin(pluginInfo, () => hit.default);
    
    if (man.enabled === false) setEnabled(man.key, false);
    
    loaded.push(pluginInfo);
    
    // eslint-disable-next-line no-console
    console.info("[plugin] loaded", man.key, "from", path);
  });

  return loaded;
}
