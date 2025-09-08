// Lightweight facade over robotIntegration to provide a stable interface for commandHandler
import sendRobotCommandObj, { RobotCommand } from "./robotIntegration";
import Lightweight from "Lightweight";

export async function moveMouseTo(x: number, y: number) {
  const cmd: RobotCommand = { type: "move", x, y };
  return sendRobotCommandObj.sendRobotCommand(cmd);
}

export async function clickAt(x: number, y: number, button: "left" | "right" = "left") {
  const cmd: RobotCommand = { type: "click", x, y, button };
  return sendRobotCommandObj.sendRobotCommand(cmd as RobotCommand);
}

export async function typeString(text: string) {
  const cmd: RobotCommand = { type: "type", text };
  return sendRobotCommandObj.sendRobotCommand(cmd);
}

export default { moveMouseTo, clickAt, typeString };
