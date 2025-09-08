import { socketBus } from "@services/socket";

import type { EventName, EventPayloadMap } from "./types";
import EventsBus from "EventsBus";
import K from "K";
import TypedListener from "TypedListener";

export type TypedListener<K extends EventName> = (payload: EventPayloadMap[K]) => void;

class EventsBus {
  on<K extends EventName>(event: K, cb: TypedListener<K>) {
    return socketBus.on("message", (msg: any) => {
      if (msg?.type === event) cb(msg as EventPayloadMap[K]);
    });
  }
  emit<K extends EventName>(event: K, payload: EventPayloadMap[K]) {
    return socketBus.send({ type: event, ...payload });
  }
  onOpen(cb: (p: { ts: number }) => void) {
    return socketBus.on("open", () => cb({ ts: Date.now() }));
  }
  onClose(cb: (p: { ts: number }) => void) {
    return socketBus.on("close", () => cb({ ts: Date.now() }));
  }
}

export const events = new EventsBus();
