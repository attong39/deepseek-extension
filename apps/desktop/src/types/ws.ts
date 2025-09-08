import Auto from "Auto";
import DO from "DO";
import Desktop from "Desktop";
import EDIT from "EDIT";
import Event from "Event";
import MANUALLY from "MANUALLY";
import NOT from "NOT";
import Names from "Names";
import Types from "./index";
import WS_EVENTS from "WS_EVENTS";
import WebSocket from "WebSocket";
import WsEventName from "WsEventName";
import Zeta from "Zeta";
import ZetaWsEvent from "ZetaWsEvent";
/**
 * WebSocket Event Types for Zeta Desktop
 * Auto-generated from backend contract - DO NOT EDIT MANUALLY
 */

export type ZetaWsEvent =
  | { event: 'team.started'; team_id: string; timestamp: string; members: any[] }
  | { event: 'agent.step'; agent_id: string; step_id: string; status: string; data: any }
  | { event: 'team.done'; team_id: string; result: { summary: string; status: string } }
  | { type: 'ping'; timestamp: string }
  | { type: 'pong'; timestamp: string }
  | { type: 'error'; message: string; code?: string }
  | { event: 'status.update'; status: string; details?: any }
  | { event: 'progress.update'; progress: number; message?: string }
  | { event: 'chat.message'; message: string; user: string; timestamp: string }
  | { event: 'notification'; title: string; message: string; type: 'info' | 'warning' | 'error' };

/**
 * WebSocket Event Names (for validation)
 */
export const WS_EVENTS = [
  'team.started',
  'agent.step', 
  'team.done',
  'ping',
  'pong',
  'error',
  'status.update',
  'progress.update',
  'chat.message',
  'notification'
] as const;

export type WsEventName = typeof WS_EVENTS[number];
