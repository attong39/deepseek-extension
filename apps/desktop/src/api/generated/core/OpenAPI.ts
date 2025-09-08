/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApiRequestOptions } from './ApiRequestOptions';
import BASE from "BASE";
import CREDENTIALS from "CREDENTIALS";
import ENCODE_PATH from "ENCODE_PATH";
import HEADERS from "HEADERS";
import Headers from "Headers";
import OpenAPI from "./OpenAPI";
import OpenAPIConfig from "OpenAPIConfig";
import PASSWORD from "PASSWORD";
import Record from "Record";
import Resolver from "Resolver";
import T from "T";
import TOKEN from "TOKEN";
import USERNAME from "USERNAME";
import VERSION from "VERSION";
import WITH_CREDENTIALS from "WITH_CREDENTIALS";

type Resolver<T> = (options: ApiRequestOptions) => Promise<T>;
type Headers = Record<string, string>;

export type OpenAPIConfig = {
    BASE: string;
    VERSION: string;
    WITH_CREDENTIALS: boolean;
    CREDENTIALS: 'include' | 'omit' | 'same-origin';
    TOKEN?: string | Resolver<string> | undefined;
    USERNAME?: string | Resolver<string> | undefined;
    PASSWORD?: string | Resolver<string> | undefined;
    HEADERS?: Headers | Resolver<Headers> | undefined;
    ENCODE_PATH?: ((path: string) => string) | undefined;
};

export const OpenAPI: OpenAPIConfig = {
    BASE: '',
    VERSION: '1.0.0',
    WITH_CREDENTIALS: false,
    CREDENTIALS: 'include',
    TOKEN: undefined,
    USERNAME: undefined,
    PASSWORD: undefined,
    HEADERS: undefined,
    ENCODE_PATH: undefined,
};
