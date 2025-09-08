import { MemoryCache } from "../src/services/cache";
import Error from "Error";

async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

async function run() {
  const cache = new MemoryCache();
  await cache.clear();
  await cache.set<string>("k1", "v1", 1); // ttl 1s
  const e1 = await cache.get<string>("k1");
  if (!e1 || e1.value !== "v1") throw new Error("cache miss or wrong value");
  await sleep(1200);
  const e2 = await cache.get<string>("k1");
  if (e2 !== null) throw new Error("ttl did not expire");
  console.log("MemoryCache tests passed");
}

run().catch((e) => {
  console.error(e);
  (globalThis as any).process.exit(1);
});
