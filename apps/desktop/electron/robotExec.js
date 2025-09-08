// Lightweight robot execution module.
// Purpose: contain robot command implementations so ipcHandler remains small.
async function tryRobotjsMove(x, y) {
  try {
    const mod = await import("robotjs");
    const robot = mod.default || mod;
    robot.moveMouse(Math.round(x || 0), Math.round(y || 0));
    return { ok: true };
  } catch (e) {
    return { ok: false, error: "move not supported: " + String(e?.message || e) };
  }
}

async function tryRobotjsClick(button) {
  try {
    const mod = await import("robotjs");
    const robot = mod.default || mod;
    robot.mouseClick(button === "right" ? "right" : "left");
    return { ok: true };
  } catch (e) {
    return { ok: false, error: "click not supported: " + String(e?.message || e) };
  }
}

async function tryRobotjsType(text) {
  try {
    const mod = await import("robotjs");
    const robot = mod.default || mod;
    robot.typeString(String(text || ""));
    return { ok: true };
  } catch (e) {
    return { ok: false, error: "type not supported: " + String(e?.message || e) };
  }
}

async function tryHotkey(parsed) {
  try {
    const nut = await import("@nut-tree/nut-js");
    const keyboard = nut.keyboard;
    const Key = nut.Key;
    const mapMod = (m) =>
      ({
        control: Key.LeftControl,
        alt: Key.LeftAlt,
        shift: Key.LeftShift,
        command: Key.LeftSuper,
      })[m] ?? Key.LeftSuper;
    const modKeys = parsed.mods.map(mapMod);
    if (modKeys.length) await keyboard.pressKey(...modKeys);
    await keyboard.type(parsed.key);
    if (modKeys.length) await keyboard.releaseKey(...modKeys);
    return { ok: true };
  } catch {
    // fallback robotjs
    return tryRobotjsHotkey(parsed);
  }
}

async function tryRobotjsHotkey(parsed) {
  try {
    const mod = await import("robotjs");
    const robot = mod.default || mod;
    const mods = Array.isArray(parsed.mods) ? parsed.mods : [];
    if (typeof robot.keyTap === "function") {
      robot.keyTap(parsed.key, mods);
      return { ok: true };
    }
    return { ok: false, error: "no hotkey support" };
  } catch (e) {
    return { ok: false, error: String(e?.message || e) };
  }
}

export async function execRobotCommand(cmd) {
  if (!cmd || typeof cmd !== "object" || !cmd.type) {
    return { ok: false, error: "Invalid command" };
  }
  try {
    switch (cmd.type) {
      case "move":
        return await tryRobotjsMove(cmd.x, cmd.y);
      case "click":
        return await tryRobotjsClick(cmd.button);
      case "type":
        return await tryRobotjsType(cmd.text);
      case "hotkey": {
        const parsed = {
          key:
            Array.isArray(cmd.keys) && cmd.keys.length
              ? cmd.keys.slice(-1)[0]
              : String(cmd.keys || ""),
          mods: Array.isArray(cmd.keys) && cmd.keys.length ? cmd.keys.slice(0, -1) : [],
        };
        return await tryHotkey(parsed);
      }
      default:
        return { ok: false, error: "Unknown command type" };
    }
  } catch (e) {
    return { ok: false, error: e?.message || "robot exec failed" };
  }
}
