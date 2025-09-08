import React, { useEffect, useMemo, useState } from "react";

import { PermissionDialog } from "../components/PermissionDialog";
import { Permission, subscribePermissionRequest } from "../services/permissionManager";
import Element from "Element";
import JSX from "JSX";
import PermissionProvider from "./PermissionProvider";
import ReactNode from "ReactNode";

export function PermissionProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const [open, setOpen] = useState(false);
  const [capability, setCapability] = useState<Permission>("screen");
  const [description, setDescription] = useState<string | undefined>(undefined);
  const resolverRef = useMemo(
    () => ({
      fn: ((_: boolean, __: boolean) => {}) as (ok: boolean, remember: boolean) => void,
    }),
    [],
  );

  useEffect(() => {
    const unsub = subscribePermissionRequest(({ permission, description, resolve }) => {
      setCapability(permission);
      setDescription(description);
      resolverRef.fn = resolve;
      setOpen(true);
    });
    return () => unsub();
  }, [resolverRef]);

  return (
    <>
      {children}
      {open && (
        <PermissionDialog
          open={open}
          capability={capability}
          {...(description !== undefined ? { description } : {})}
          onGrant={(remember) => {
            setOpen(false);
            resolverRef.fn(true, remember);
          }}
          onDeny={() => {
            setOpen(false);
            resolverRef.fn(false, false);
          }}
        />
      )}
    </>
  );
}
