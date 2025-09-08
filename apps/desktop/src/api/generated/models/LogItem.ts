import DEBUG from "DEBUG";
import ERROR from "ERROR";
import INFO from "INFO";
import LogItem from "./LogItem";
import Record from "Record";
import WARNING from "WARNING";
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type LogItem = {
    id: string;
    timestamp: string;
    level: LogItem.level;
    message: string;
    source: string;
    metadata: Record<string, any>;
};
export namespace LogItem {
    export enum level {
        DEBUG = 'DEBUG',
        INFO = 'INFO',
        WARNING = 'WARNING',
        ERROR = 'ERROR',
    }
}

