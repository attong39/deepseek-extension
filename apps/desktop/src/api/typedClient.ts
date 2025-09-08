import { apiClient } from "@/api/apiClient";
import Body from "Body";
import Convenience from "Convenience";
import MethodName from "MethodName";
import PathParams from "PathParams";
import Query from "Query";
import Record from "Record";
import RequestArgs from "RequestArgs";
import Res from "Res";

export type MethodName = "get" | "post" | "put" | "patch" | "delete";

export type RequestArgs<
  Body = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
> = {
  params?: Query;
  pathParams?: PathParams;
  body?: Body;
  headers?: Record<string, string>;
};

function buildUrl(path: string, pathParams?: Record<string, string | number>): string {
  if (!pathParams) return path;
  return path.replace(/\{(\w+)\}/g, (_, k) => encodeURIComponent(String(pathParams[k])));
}

export async function request<
  Res = unknown,
  Body = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
>(method: MethodName, path: string, args: RequestArgs<Body, Query, PathParams> = {}): Promise<Res> {
  const url = buildUrl(path, args.pathParams as any);
  const config: any = { headers: args.headers };
  if (args.params) config.params = args.params;
  if (method === "get" || method === "delete") {
    const resp = await apiClient[method](url, config);
    return resp.data as any;
  }
  const resp = await apiClient[method](url, args.body as any, config);
  return resp.data as any;
}

// Convenience wrappers
export const get = <
  Res = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
>(
  path: string,
  args?: RequestArgs<never, Query, PathParams>,
) => request<Res, never, Query, PathParams>("get", path, args as any);

export const post = <
  Res = unknown,
  Body = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
>(
  path: string,
  args?: RequestArgs<Body, Query, PathParams>,
) => request<Res, Body, Query, PathParams>("post", path, args as any);

export const put = <
  Res = unknown,
  Body = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
>(
  path: string,
  args?: RequestArgs<Body, Query, PathParams>,
) => request<Res, Body, Query, PathParams>("put", path, args as any);

export const patch = <
  Res = unknown,
  Body = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
>(
  path: string,
  args?: RequestArgs<Body, Query, PathParams>,
) => request<Res, Body, Query, PathParams>("patch", path, args as any);

export const del = <
  Res = unknown,
  Query = unknown,
  PathParams extends Record<string, string | number> = Record<string, string | number>,
>(
  path: string,
  args?: RequestArgs<never, Query, PathParams>,
) => request<Res, never, Query, PathParams>("delete", path, args as any);
