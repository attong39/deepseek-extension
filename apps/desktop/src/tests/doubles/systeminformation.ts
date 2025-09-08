import API from "../../API/index";
import C from "C";
import Dummy from "Dummy";
// Dummy vừa đủ cho tests metrics; mở rộng nếu test gọi API khác.
export async function currentLoad() {
  return { currentload: 12.3, cpus: [] };
}
export async function mem() {
  const gb = 1024 * 1024 * 1024;
  return { total: 16 * gb, active: 6 * gb, free: 10 * gb };
}
export async function fsSize() {
  return [{ size: 256 * 1024 * 1024 * 1024, used: 100 * 1024 * 1024 * 1024, mount: "C:" }];
}
export default { currentLoad, mem, fsSize };
