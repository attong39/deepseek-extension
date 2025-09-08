import HealthStatus from "./HealthStatus";
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type HealthStatus = {
    status: string;
    timestamp: string;
    version: string;
    services: {
        api?: string;
        storage?: string;
        total_uploads?: number;
        total_jobs?: number;
        total_rules?: number;
        total_logs?: number;
    };
};

