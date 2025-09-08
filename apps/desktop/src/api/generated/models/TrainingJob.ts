import CANCELLED from "CANCELLED";
import COMPLETED from "COMPLETED";
import CREATED from "CREATED";
import FAILED from "FAILED";
import PAUSED from "PAUSED";
import RUNNING from "RUNNING";
import Record from "Record";
import TrainingJob from "./TrainingJob";
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type TrainingJob = {
    id: string;
    name: string;
    status: TrainingJob.status;
    progress: number;
    created_at: string;
    updated_at: string;
    data_source?: string;
    config: Record<string, any>;
    logs: Array<string>;
};
export namespace TrainingJob {
    export enum status {
        CREATED = 'created',
        RUNNING = 'running',
        PAUSED = 'paused',
        COMPLETED = 'completed',
        CANCELLED = 'cancelled',
        FAILED = 'failed',
    }
}

