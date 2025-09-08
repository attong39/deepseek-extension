/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ActionResponse } from '../models/ActionResponse';
import type { HealthStatus } from '../models/HealthStatus';
import type { LogItem } from '../models/LogItem';
import type { RuleResponse } from '../models/RuleResponse';
import type { RuleUpsert } from '../models/RuleUpsert';
import type { TrainingJob } from '../models/TrainingJob';
import type { TrainingJobCreate } from '../models/TrainingJobCreate';
import type { UploadRequest } from '../models/UploadRequest';
import type { UploadResponse } from '../models/UploadResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
import ApiError from "ApiError";
import Cancel from "Cancel";
import Check from "Check";
import Create from "Create";
import DELETE from "DELETE";
import DefaultService from "./DefaultService";
import Delete from "Delete";
import File from "File";
import GET from "GET";
import Get from "Get";
import Health from "Health";
import Job from "Job";
import Jobs from "Jobs";
import List from "List";
import Logs from "../../../pages/Logs";
import POST from "POST";
import PUT from "PUT";
import Pause from "Pause";
import Response from "Response";
import Rule from "Rule";
import Rules from "Rules";
import Start from "Start";
import Successful from "Successful";
import Training from "../../../pages/Training";
import Update from "Update";
import Upload from "Upload";
import Uploads from "Uploads";
export class DefaultService {
    /**
     * Health Check
     * @returns HealthStatus Successful Response
     * @throws ApiError
     */
    public static healthCheck(): CancelablePromise<HealthStatus> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/health',
        });
    }
    /**
     * Upload File
     * @param formData
     * @returns UploadResponse Successful Response
     * @throws ApiError
     */
    public static uploadFile(
        formData: UploadRequest,
    ): CancelablePromise<UploadResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/uploads',
            formData: formData,
            mediaType: 'multipart/form-data',
        });
    }
    /**
     * List Uploads
     * @param limit
     * @param skip
     * @returns UploadResponse Successful Response
     * @throws ApiError
     */
    public static listUploads(
        limit: number = 50,
        skip?: number,
    ): CancelablePromise<Array<UploadResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/uploads',
            query: {
                'limit': limit,
                'skip': skip,
            },
        });
    }
    /**
     * Get Upload
     * @param fileId
     * @returns UploadResponse Successful Response
     * @throws ApiError
     */
    public static getUpload(
        fileId: string,
    ): CancelablePromise<UploadResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/uploads/{file_id}',
            path: {
                'file_id': fileId,
            },
        });
    }
    /**
     * Create Training Job
     * @param requestBody
     * @returns TrainingJob Successful Response
     * @throws ApiError
     */
    public static createTrainingJob(
        requestBody: TrainingJobCreate,
    ): CancelablePromise<TrainingJob> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/training/jobs',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * List Training Jobs
     * @param status
     * @param limit
     * @param skip
     * @returns TrainingJob Successful Response
     * @throws ApiError
     */
    public static listTrainingJobs(
        status?: string,
        limit: number = 50,
        skip?: number,
    ): CancelablePromise<Array<TrainingJob>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/training/jobs',
            query: {
                'status': status,
                'limit': limit,
                'skip': skip,
            },
        });
    }
    /**
     * Get Training Job
     * @param jobId
     * @returns TrainingJob Successful Response
     * @throws ApiError
     */
    public static getTrainingJob(
        jobId: string,
    ): CancelablePromise<TrainingJob> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/training/jobs/{job_id}',
            path: {
                'job_id': jobId,
            },
        });
    }
    /**
     * Start Training Job
     * @param jobId
     * @returns ActionResponse Successful Response
     * @throws ApiError
     */
    public static startTrainingJob(
        jobId: string,
    ): CancelablePromise<ActionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/training/jobs/{job_id}/start',
            path: {
                'job_id': jobId,
            },
        });
    }
    /**
     * Pause Training Job
     * @param jobId
     * @returns ActionResponse Successful Response
     * @throws ApiError
     */
    public static pauseTrainingJob(
        jobId: string,
    ): CancelablePromise<ActionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/training/jobs/{job_id}/pause',
            path: {
                'job_id': jobId,
            },
        });
    }
    /**
     * Cancel Training Job
     * @param jobId
     * @returns ActionResponse Successful Response
     * @throws ApiError
     */
    public static cancelTrainingJob(
        jobId: string,
    ): CancelablePromise<ActionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/training/jobs/{job_id}/cancel',
            path: {
                'job_id': jobId,
            },
        });
    }
    /**
     * Create Rule
     * @param requestBody
     * @returns RuleResponse Successful Response
     * @throws ApiError
     */
    public static createRule(
        requestBody: RuleUpsert,
    ): CancelablePromise<RuleResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/rules',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * List Rules
     * @param enabled
     * @param limit
     * @param skip
     * @returns RuleResponse Successful Response
     * @throws ApiError
     */
    public static listRules(
        enabled?: boolean,
        limit: number = 50,
        skip?: number,
    ): CancelablePromise<Array<RuleResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/rules',
            query: {
                'enabled': enabled,
                'limit': limit,
                'skip': skip,
            },
        });
    }
    /**
     * Get Rule
     * @param ruleId
     * @returns RuleResponse Successful Response
     * @throws ApiError
     */
    public static getRule(
        ruleId: string,
    ): CancelablePromise<RuleResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/rules/{rule_id}',
            path: {
                'rule_id': ruleId,
            },
        });
    }
    /**
     * Update Rule
     * @param ruleId
     * @param requestBody
     * @returns RuleResponse Successful Response
     * @throws ApiError
     */
    public static updateRule(
        ruleId: string,
        requestBody: RuleUpsert,
    ): CancelablePromise<RuleResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/rules/{rule_id}',
            path: {
                'rule_id': ruleId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Delete Rule
     * @param ruleId
     * @returns ActionResponse Successful Response
     * @throws ApiError
     */
    public static deleteRule(
        ruleId: string,
    ): CancelablePromise<ActionResponse> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/rules/{rule_id}',
            path: {
                'rule_id': ruleId,
            },
        });
    }
    /**
     * Get Logs
     * @param level
     * @param source
     * @param limit
     * @param skip
     * @returns LogItem Successful Response
     * @throws ApiError
     */
    public static getLogs(
        level?: string,
        source?: string,
        limit: number = 100,
        skip?: number,
    ): CancelablePromise<Array<LogItem>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/logs',
            query: {
                'level': level,
                'source': source,
                'limit': limit,
                'skip': skip,
            },
        });
    }
}
