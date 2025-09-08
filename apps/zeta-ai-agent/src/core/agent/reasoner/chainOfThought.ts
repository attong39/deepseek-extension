/**
 * Chain-of-Thought Reasoner với Self-Consistency
 * Triển khai CoT + Self-Consistency: chạy đa lần, vote kết quả tốt nhất
 */

import { OllamaClient } from '../../ollama/client';
import { ChatMessage, ChatOptions } from '../../ollama/types';
import All from "All";
import Also from "Also";
import Always from "Always";
import Answer from "Answer";
import Are from "Are";
import Base from "Base";
import Cannot from "Cannot";
import Chain from "Chain";
import Check from "Check";
import CoT from "CoT";
import CoTExample from "CoTExample";
import CoTOptions from "CoTOptions";
import CoTReasoner from "CoTReasoner";
import CoTResult from "CoTResult";
import Confidence from "Confidence";
import Consistency from "Consistency";
import DEFAULT_COT_EXAMPLES from "DEFAULT_COT_EXAMPLES";
import Error from "Error";
import Example from "Example";
import Export from "Export";
import First from "First";
import For from "For";
import Format from "Format";
import How from "How";
import I from "I";
import Is from "Is";
import It from "It";
import LLM from "LLM";
import Looking from "Looking";
import Map from "Map";
import Math from "Math";
import Multiple from "Multiple";
import Normalize from "Normalize";
import O from "O";
import Parse from "Parse";
import PromiseFulfilledResult from "PromiseFulfilledResult";
import Question from "Question";
import Reasoner from "Reasoner";
import Reasoning from "Reasoning";
import ReasoningOutput from "ReasoningOutput";
import Remove from "Remove";
import Required from "Required";
import S from "S";
import Self from "Self";
import Think from "Think";
import This from "This";
import Thought from "Thought";
import Use from "Use";
import VotingResult from "VotingResult";
import What from "What";
import Why from "Why";
import You from "You";
import Your from "Your";

export interface CoTExample {
  question: string;
  reasoning: string;
  answer: string;
}

export interface CoTResult {
  finalAnswer: string;
  reasoning: string[];
  confidence: number;
  votingDetails: VotingResult;
}

export interface VotingResult {
  candidates: Array<{
    answer: string;
    votes: number;
    reasoning: string;
  }>;
  totalSamples: number;
  agreement: number; // % agreement on winning answer
  winner: {
    answer: string;
    votes: number;
    reasoning: string;
  };
}

export interface CoTOptions {
  numSamples?: number;
  temperature?: number;
  maxTokens?: number;
  requireExplanation?: boolean;
  votingStrategy?: 'majority' | 'weighted' | 'confidence';
}

export class CoTReasoner {
  private readonly ollama: OllamaClient;
  private readonly defaultOptions: Required<CoTOptions>;

  constructor(ollama: OllamaClient, options: CoTOptions = {}) {
    this.ollama = ollama;
    this.defaultOptions = {
      numSamples: options.numSamples || 4,
      temperature: options.temperature || 0.7,
      maxTokens: options.maxTokens || 2048,
      requireExplanation: options.requireExplanation ?? true,
      votingStrategy: options.votingStrategy || 'majority'
    };
  }

  /**
   * Chạy Chain-of-Thought reasoning với self-consistency
   */
  async reason(
    question: string, 
    examples: CoTExample[] = [], 
    options: CoTOptions = {}
  ): Promise<CoTResult> {
    const config = { ...this.defaultOptions, ...options };
    
    // Tạo nhiều reasoning samples
    const reasoningPromises = Array.from({ length: config.numSamples }, (_, i) =>
      this.generateReasoning(question, examples, config, i)
    );

    const reasoningResults = await Promise.allSettled(reasoningPromises);
    
    // Lọc kết quả thành công
    const validResults = reasoningResults
      .filter((result): result is PromiseFulfilledResult<ReasoningOutput> => 
        result.status === 'fulfilled' && result.value.answer !== null
      )
      .map(result => result.value);

    if (validResults.length === 0) {
      throw new Error('All reasoning attempts failed');
    }

    // Thực hiện voting để chọn kết quả tốt nhất
    const votingResult = this.performVoting(validResults, config.votingStrategy);
    
    return {
      finalAnswer: votingResult.winner.answer,
      reasoning: validResults.map(r => r.reasoning),
      confidence: this.calculateConfidence(votingResult),
      votingDetails: votingResult
    };
  }

  /**
   * Tạo một reasoning sample
   */
  private async generateReasoning(
    question: string,
    examples: CoTExample[],
    options: Required<CoTOptions>,
    sampleIndex: number
  ): Promise<ReasoningOutput> {
    const prompt = this.buildCoTPrompt(question, examples, options.requireExplanation);
    
    // Thêm variation trong temperature để tăng diversity
    const temperatureVariation = options.temperature + (Math.random() - 0.5) * 0.2;
    const clampedTemperature = Math.max(0.1, Math.min(1.0, temperatureVariation));

    const chatOptions: ChatOptions = {
      temperature: clampedTemperature,
      maxTokens: options.maxTokens,
      topP: 0.9,
      stop: ['Question:', 'Example:']
    };

    try {
      const response = await this.ollama.chat(prompt, chatOptions);
      const content = response.message.content;
      
      return this.parseReasoningOutput(content, sampleIndex);
    } catch (error) {
      console.warn(`Reasoning sample ${sampleIndex} failed:`, error);
      return {
        answer: null,
        reasoning: '',
        confidence: 0,
        sampleIndex
      };
    }
  }

  /**
   * Xây dựng prompt cho Chain-of-Thought
   */
  private buildCoTPrompt(
    question: string, 
    examples: CoTExample[], 
    requireExplanation: boolean
  ): ChatMessage[] {
    const systemMessage: ChatMessage = {
      role: 'system',
      content: `You are an expert logical reasoner. Think step-by-step and show your reasoning process clearly.

${requireExplanation ? 'Always explain your thinking process before giving the final answer.' : ''}

Format your response as:
Reasoning: [Your step-by-step thought process]
Answer: [Your final answer]`
    };

    const messages: ChatMessage[] = [systemMessage];

    // Thêm few-shot examples nếu có
    examples.forEach(example => {
      messages.push({
        role: 'user',
        content: `Question: ${example.question}`
      });
      messages.push({
        role: 'assistant',
        content: `Reasoning: ${example.reasoning}\nAnswer: ${example.answer}`
      });
    });

    // Thêm câu hỏi chính
    messages.push({
      role: 'user',
      content: `Question: ${question}`
    });

    return messages;
  }

  /**
   * Parse kết quả reasoning từ LLM response
   */
  private parseReasoningOutput(content: string, sampleIndex: number): ReasoningOutput {
    const reasoningRegex = /Reasoning:\s*([\s\S]*?)(?=Answer:|$)/i;
    const answerRegex = /Answer:\s*([\s\S]*?)$/i;
    
    const reasoningMatch = reasoningRegex.exec(content);
    const answerMatch = answerRegex.exec(content);

    const reasoning = reasoningMatch ? reasoningMatch[1].trim() : content;
    const answer = answerMatch ? answerMatch[1].trim() : this.extractImplicitAnswer(content);

    // Tính confidence dựa trên chất lượng của reasoning
    const confidence = this.assessReasoningQuality(reasoning, answer);

    return {
      answer,
      reasoning,
      confidence,
      sampleIndex
    };
  }

  /**
   * Trích xuất answer từ content khi không có format rõ ràng
   */
  private extractImplicitAnswer(content: string): string {
    // Tìm câu cuối cùng hoặc đoạn cuối
    const lines = content.split('\n').filter(line => line.trim());
    return lines.length > 0 ? lines[lines.length - 1].trim() : content.trim();
  }

  /**
   * Đánh giá chất lượng của reasoning
   */
  private assessReasoningQuality(reasoning: string, answer: string): number {
    let score = 0.5; // Base score

    // Kiểm tra độ dài và chi tiết của reasoning
    if (reasoning.length > 100) score += 0.1;
    if (reasoning.includes('because') || reasoning.includes('therefore')) score += 0.1;
    if (reasoning.includes('step') || reasoning.includes('first') || reasoning.includes('then')) score += 0.1;

    // Kiểm tra tính nhất quán
    if (answer && answer.length > 0 && answer !== 'unknown') score += 0.2;

    // Kiểm tra cấu trúc logic
    if (reasoning.split('.').length > 2) score += 0.1; // Multiple sentences

    return Math.min(1.0, score);
  }

  /**
   * Thực hiện voting để chọn kết quả tốt nhất
   */
  private performVoting(
    results: ReasoningOutput[], 
    strategy: 'majority' | 'weighted' | 'confidence'
  ): VotingResult {
    // Nhóm answers giống nhau
    const answerGroups = new Map<string, ReasoningOutput[]>();
    
    results.forEach(result => {
      if (result.answer) {
        const normalizedAnswer = this.normalizeAnswer(result.answer);
        if (!answerGroups.has(normalizedAnswer)) {
          answerGroups.set(normalizedAnswer, []);
        }
        answerGroups.get(normalizedAnswer)!.push(result);
      }
    });

    // Tính điểm cho mỗi nhóm
    const candidates = Array.from(answerGroups.entries()).map(([answer, group]) => {
      let votes: number;
      
      switch (strategy) {
      case 'majority':
        votes = group.length;
        break;
      case 'weighted':
        votes = group.reduce((sum, r) => sum + r.confidence, 0);
        break;
      case 'confidence':
        votes = Math.max(...group.map(r => r.confidence)) * group.length;
        break;
      default:
        votes = group.length;
      }

      return {
        answer,
        votes,
        reasoning: group[0].reasoning, // Lấy reasoning đầu tiên của nhóm
        group
      };
    });

    // Sắp xếp theo điểm số
    candidates.sort((a, b) => b.votes - a.votes);

    const winner = candidates[0];
    const totalVotes = candidates.reduce((sum, c) => sum + c.votes, 0);
    const agreement = totalVotes > 0 ? winner.votes / totalVotes : 0;

    return {
      candidates: candidates.map(c => ({
        answer: c.answer,
        votes: c.votes,
        reasoning: c.reasoning
      })),
      totalSamples: results.length,
      agreement,
      winner
    };
  }

  /**
   * Normalize answer để so sánh
   */
  private normalizeAnswer(answer: string): string {
    return answer
      .toLowerCase()
      .replace(/[^\w\s]/g, '') // Remove punctuation
      .replace(/\s+/g, ' ') // Normalize spaces
      .trim();
  }

  /**
   * Tính confidence tổng thể
   */
  private calculateConfidence(votingResult: VotingResult): number {
    // Confidence dựa trên agreement và chất lượng reasoning
    const agreementScore = votingResult.agreement;
    const qualityScore = votingResult.candidates[0]?.votes / votingResult.totalSamples || 0;
    
    return (agreementScore + qualityScore) / 2;
  }

  /**
   * Tạo CoT examples từ historical data
   */
  async generateExamples(domain: string, count = 3): Promise<CoTExample[]> {
    // Tích hợp với vector store để tìm examples tương tự
    // Hiện tại return empty array, sẽ implement sau khi có vector store
    return [];
  }
}

interface ReasoningOutput {
  answer: string | null;
  reasoning: string;
  confidence: number;
  sampleIndex: number;
}

// Export helper functions
export function createCoTExample(question: string, reasoning: string, answer: string): CoTExample {
  return { question, reasoning, answer };
}

export const DEFAULT_COT_EXAMPLES = {
  coding: [
    createCoTExample(
      'How can I optimize this function for better performance?',
      'First, I need to identify the bottlenecks. Looking at the code, I see nested loops which create O(n²) complexity. I can optimize by using a Map for O(1) lookups instead of O(n) array searches. Also, I should avoid repeated calculations by memoizing results.',
      'Use a Map for lookups, memoize repeated calculations, and consider breaking early when possible.'
    ),
    createCoTExample(
      'What\'s the best way to handle errors in this async function?',
      'For async functions, I need to consider both synchronous and asynchronous errors. I should use try-catch blocks, handle Promise rejections, add proper logging, and ensure resources are cleaned up. It\'s also good to provide meaningful error messages.',
      'Use try-catch with proper cleanup, handle Promise rejections, add logging, and provide descriptive error messages.'
    )
  ],
  debugging: [
    createCoTExample(
      'Why is my application crashing with \'Cannot read property of undefined\'?',
      'This error occurs when trying to access a property on undefined/null. I need to check: 1) Is the object properly initialized? 2) Are there race conditions? 3) Is data coming from an async operation that hasn\'t completed? 4) Are there typos in property names?',
      'Check object initialization, add null checks, verify async operations complete, and validate property names.'
    )
  ]
};
