import AI from "AI";
import Agent from "Agent";
import Batch from "Batch";
import BatchProcessor from "./BatchProcessor";
import BatchProcessorOptions from "BatchProcessorOptions";
import BatchRequest from "BatchRequest";
import BatchResponse from "BatchResponse";
import Check from "Check";
import Clear from "Clear";
import Earlier from "Earlier";
import Efficiently from "Efficiently";
import Error from "Error";
import Extract from "Extract";
import For from "For";
import Global from "Global";
import Handle from "Handle";
import Higher from "Higher";
import Larger from "Larger";
import Math from "Math";
import NodeJS from "NodeJS";
import Ollama from "Ollama";
import Omit from "Omit";
import Partial from "Partial";
import PendingRequest from "PendingRequest";
import Process from "Process";
import Processor from "Processor";
import Queue from "Queue";
import Record from "Record";
import Reject from "Reject";
import Request from "Request";
import RequestRejecter from "RequestRejecter";
import RequestResolver from "RequestResolver";
import Schedule from "Schedule";
import Simulate from "Simulate";
import Smaller from "Smaller";
import Specialized from "Specialized";
import This from "This";
import Timeout from "Timeout";
import Zeta from "Zeta";
/**
 * Batch Processor for Zeta AI Agent
 * Efficiently handles batching of requests to optimize Ollama performance
 */

export interface BatchRequest {
  id: string;
  data: any;
  priority: 'low' | 'medium' | 'high';
  timeout: number;
  retries: number;
}

export interface BatchResponse {
  id: string;
  success: boolean;
  data?: any;
  error?: string;
  processingTime: number;
}

export interface BatchProcessorOptions {
  batchSize: number;
  maxWaitTime: number; // milliseconds
  maxConcurrentBatches: number;
  retryDelayMs: number;
  priorityLevels: {
    high: number;
    medium: number;
    low: number;
  };
}

type RequestResolver = (response: BatchResponse) => void;
type RequestRejecter = (error: Error) => void;

interface PendingRequest {
  request: BatchRequest;
  resolve: RequestResolver;
  reject: RequestRejecter;
  timestamp: number;
}

export class BatchProcessor {
  private batchQueue: PendingRequest[] = [];
  private processing = false;
  private activeBatches = 0;
  private readonly options: BatchProcessorOptions;
  private processingTimer: NodeJS.Timeout | null = null;

  constructor(options: Partial<BatchProcessorOptions> = {}) {
    this.options = {
      batchSize: options.batchSize || 5,
      maxWaitTime: options.maxWaitTime || 1000,
      maxConcurrentBatches: options.maxConcurrentBatches || 3,
      retryDelayMs: options.retryDelayMs || 1000,
      priorityLevels: options.priorityLevels || {
        high: 3,
        medium: 2,
        low: 1
      }
    };
  }

  async processRequest(request: Omit<BatchRequest, 'id'>): Promise<BatchResponse> {
    const fullRequest: BatchRequest = {
      id: this.generateRequestId(),
      ...request
    };

    return new Promise<BatchResponse>((resolve, reject) => {
      const pendingRequest: PendingRequest = {
        request: fullRequest,
        resolve,
        reject,
        timestamp: Date.now()
      };

      this.batchQueue.push(pendingRequest);
      this.sortQueueByPriority();
      this.scheduleProcessing();
    });
  }

  private generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  private sortQueueByPriority(): void {
    this.batchQueue.sort((a, b) => {
      const priorityA = this.options.priorityLevels[a.request.priority];
      const priorityB = this.options.priorityLevels[b.request.priority];
      
      if (priorityA !== priorityB) {
        return priorityB - priorityA; // Higher priority first
      }
      
      return a.timestamp - b.timestamp; // Earlier timestamp first for same priority
    });
  }

  private scheduleProcessing(): void {
    if (this.processing || this.activeBatches >= this.options.maxConcurrentBatches) {
      return;
    }

    // Process immediately if batch is full
    if (this.batchQueue.length >= this.options.batchSize) {
      this.processBatch();
      return;
    }

    // Schedule processing after max wait time
    if (!this.processingTimer && this.batchQueue.length > 0) {
      this.processingTimer = setTimeout(() => {
        this.processBatch();
      }, this.options.maxWaitTime);
    }
  }

  private async processBatch(): Promise<void> {
    if (this.processing || this.batchQueue.length === 0) {
      return;
    }

    this.processing = true;
    this.activeBatches++;

    // Clear timer if set
    if (this.processingTimer) {
      clearTimeout(this.processingTimer);
      this.processingTimer = null;
    }

    // Extract batch from queue
    const batchSize = Math.min(this.options.batchSize, this.batchQueue.length);
    const batch = this.batchQueue.splice(0, batchSize);

    try {
      await this.executeBatch(batch);
    } catch (error) {
      console.error('Batch processing error:', error);
      // Reject all requests in the failed batch
      batch.forEach(pending => {
        pending.reject(new Error(`Batch processing failed: ${error}`));
      });
    } finally {
      this.processing = false;
      this.activeBatches--;
      
      // Schedule next batch if queue is not empty
      if (this.batchQueue.length > 0) {
        this.scheduleProcessing();
      }
    }
  }

  private async executeBatch(batch: PendingRequest[]): Promise<void> {
    const startTime = Date.now();
    const promises = batch.map(pending => this.executeRequest(pending));
    
    await Promise.allSettled(promises);
    
    const processingTime = Date.now() - startTime;
    console.log(`Batch of ${batch.length} requests processed in ${processingTime}ms`);
  }

  private async executeRequest(pending: PendingRequest): Promise<void> {
    const { request, resolve, reject } = pending;
    const startTime = Date.now();

    try {
      // Check for timeout
      if (Date.now() - pending.timestamp > request.timeout) {
        throw new Error('Request timeout');
      }

      // Simulate processing (replace with actual Ollama call)
      const result = await this.processOllamaRequest(request.data);
      
      const response: BatchResponse = {
        id: request.id,
        success: true,
        data: result,
        processingTime: Date.now() - startTime
      };

      resolve(response);
    } catch (error) {
      const response: BatchResponse = {
        id: request.id,
        success: false,
        error: error instanceof Error ? error.message : String(error),
        processingTime: Date.now() - startTime
      };

      // Handle retries
      if (request.retries > 0) {
        const retryRequest: BatchRequest = {
          ...request,
          retries: request.retries - 1
        };

        setTimeout(() => {
          this.batchQueue.unshift({
            request: retryRequest,
            resolve,
            reject,
            timestamp: Date.now()
          });
          this.scheduleProcessing();
        }, this.options.retryDelayMs);
      } else {
        reject(new Error(response.error));
      }
    }
  }

  private async processOllamaRequest(data: any): Promise<any> {
    // This should be replaced with actual Ollama client call
    // For now, simulate processing
    await new Promise(resolve => setTimeout(resolve, Math.random() * 100 + 50));
    return { processed: true, originalData: data };
  }

  // Queue management
  getQueueStatus(): {
    queueLength: number;
    activeBatches: number;
    isProcessing: boolean;
    priorityBreakdown: Record<string, number>;
    } {
    const priorityBreakdown = this.batchQueue.reduce((acc, pending) => {
      acc[pending.request.priority] = (acc[pending.request.priority] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      queueLength: this.batchQueue.length,
      activeBatches: this.activeBatches,
      isProcessing: this.processing,
      priorityBreakdown
    };
  }

  async flush(): Promise<void> {
    while (this.batchQueue.length > 0 || this.activeBatches > 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  async clearQueue(): Promise<number> {
    const cleared = this.batchQueue.length;
    this.batchQueue.forEach(pending => {
      pending.reject(new Error('Request cancelled - queue cleared'));
    });
    this.batchQueue = [];
    return cleared;
  }
}

// Global batch processor instance
export const globalBatchProcessor = new BatchProcessor({
  batchSize: 3,
  maxWaitTime: 500,
  maxConcurrentBatches: 2,
  retryDelayMs: 1000
});

// Specialized batch processors
export const chatBatchProcessor = new BatchProcessor({
  batchSize: 2, // Smaller batches for interactive chat
  maxWaitTime: 200,
  maxConcurrentBatches: 3,
  retryDelayMs: 500
});

export const analysisBatchProcessor = new BatchProcessor({
  batchSize: 5, // Larger batches for analysis tasks
  maxWaitTime: 2000,
  maxConcurrentBatches: 2,
  retryDelayMs: 2000
});
