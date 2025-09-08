import { SecurityPolicy } from '../types/shared';
import Buffer from "Buffer";
import Check from "Check";
import Code from "Code";
import CodeValidator from "CodeValidator";
import ConfigValidator from "ConfigValidator";
import Context from "../../../desktop/src/Context/index";
import DELETE from "DELETE";
import DataValidator from "DataValidator";
import Dynamic from "Dynamic";
import Environment from "Environment";
import Error from "Error";
import FROM from "FROM";
import File from "File";
import Function from "Function";
import HTTP from "HTTP";
import HTTPS from "HTTPS";
import INSERT from "INSERT";
import INTO from "INTO";
import Input from "Input";
import Invalid from "Invalid";
import Language from "Language";
import Missing from "Missing";
import Model from "Model";
import Ollama from "Ollama";
import Partial from "Partial";
import Potential from "Potential";
import Required from "Required";
import SELECT from "SELECT";
import SET from "SET";
import SQL from "SQL";
import Timeout from "Timeout";
import UPDATE from "UPDATE";
import URL from "URL";
import Unknown from "Unknown";
import Using from "Using";
import Utility from "Utility";
import VALUES from "VALUES";
import Validate from "Validate";
import ValidationResult from "ValidationResult";
import WHERE from "WHERE";
import XSS from "XSS";
import Z0 from "Z0";

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

export class CodeValidator {
  private securityPolicy: SecurityPolicy;

  constructor(securityPolicy: SecurityPolicy) {
    this.securityPolicy = securityPolicy;
  }

  validateCode(code: string, filePath?: string): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    this.validateCodeSize(code, result);
    this.validateFileExtension(filePath, result);
    this.validateBlockedPatterns(code, result);
    this.validateSecurityPatterns(code, result);

    return result;
  }

  private validateCodeSize(code: string, result: ValidationResult): void {
    if (code.length > this.securityPolicy.max_code_size) {
      result.valid = false;
      result.errors.push(`Code exceeds maximum size of ${this.securityPolicy.max_code_size} characters`);
    }
  }

  private validateFileExtension(filePath: string | undefined, result: ValidationResult): void {
    if (filePath) {
      const extension = filePath.split('.').pop()?.toLowerCase();
      if (extension && !this.securityPolicy.allowed_file_extensions.includes(`.${extension}`)) {
        result.valid = false;
        result.errors.push(`File extension .${extension} is not allowed`);
      }
    }
  }

  private validateBlockedPatterns(code: string, result: ValidationResult): void {
    for (const pattern of this.securityPolicy.blocked_patterns) {
      if (pattern.test(code)) {
        result.valid = false;
        result.errors.push(`Code contains blocked pattern: ${pattern.source}`);
      }
    }
  }

  private validateSecurityPatterns(code: string, result: ValidationResult): void {
    this.checkDangerousPatterns(code, result);
    this.checkSqlInjectionPatterns(code, result);
    this.checkXssPatterns(code, result);
  }

  private checkDangerousPatterns(code: string, result: ValidationResult): void {
    const dangerousPatterns = [
      { pattern: /require\s*\(\s*['"`]child_process['"`]\s*\)/gi, message: 'Potential command execution' },
      { pattern: /require\s*\(\s*['"`]fs['"`]\s*\)/gi, message: 'File system access detected' },
      { pattern: /process\.env/gi, message: 'Environment variable access' },
      { pattern: /Buffer\.from\s*\(/gi, message: 'Buffer manipulation detected' },
      { pattern: /new\s+Function\s*\(/gi, message: 'Dynamic function creation' },
      { pattern: /setTimeout\s*\(\s*['"`]/gi, message: 'String-based timeout execution' },
      { pattern: /setInterval\s*\(\s*['"`]/gi, message: 'String-based interval execution' }
    ];

    for (const { pattern, message } of dangerousPatterns) {
      if (pattern.test(code)) {
        result.warnings.push(message);
      }
    }
  }

  private checkSqlInjectionPatterns(code: string, result: ValidationResult): void {
    const sqlPatterns = [
      /SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*\s*['"]\s*\+/gi,
      /INSERT\s+INTO\s+.*\s+VALUES\s*\(.*['"]\s*\+/gi,
      /UPDATE\s+.*\s+SET\s+.*\s*=\s*['"]\s*\+/gi,
      /DELETE\s+FROM\s+.*\s+WHERE\s+.*\s*['"]\s*\+/gi
    ];

    for (const pattern of sqlPatterns) {
      if (pattern.test(code)) {
        result.warnings.push('Potential SQL injection vulnerability detected');
        break;
      }
    }
  }

  private checkXssPatterns(code: string, result: ValidationResult): void {
    const xssPatterns = [
      /innerHTML\s*=\s*.*\+/gi,
      /document\.write\s*\(/gi,
      /\.html\s*\(\s*.*\+/gi,
      /\$\s*\(\s*.*\+.*\)/gi
    ];

    for (const pattern of xssPatterns) {
      if (pattern.test(code)) {
        result.warnings.push('Potential XSS vulnerability detected');
        break;
      }
    }
  }

  validateInput(input: string, maxLength = 10000): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    if (!input || typeof input !== 'string') {
      result.valid = false;
      result.errors.push('Input must be a non-empty string');
      return result;
    }

    if (input.length > maxLength) {
      result.valid = false;
      result.errors.push(`Input exceeds maximum length of ${maxLength} characters`);
    }

    // Check for potential injection attacks
    const injectionPatterns = [
      /<script/gi,
      /javascript:/gi,
      /on\w+\s*=/gi,
      /data:text\/html/gi,
      /vbscript:/gi
    ];

    for (const pattern of injectionPatterns) {
      if (pattern.test(input)) {
        result.valid = false;
        result.errors.push('Input contains potentially malicious content');
        break;
      }
    }

    return result;
  }

  sanitizeInput(input: string): string {
    return input
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/javascript:/gi, '')
      .replace(/on\w+\s*=/gi, '')
      .replace(/data:text\/html/gi, '')
      .replace(/vbscript:/gi, '')
      .trim();
  }

  updateSecurityPolicy(policy: Partial<SecurityPolicy>): void {
    this.securityPolicy = { ...this.securityPolicy, ...policy };
  }
}

export class ConfigValidator {
  static validateOllamaUrl(url: string): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    try {
      const parsedUrl = new URL(url);
      
      if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
        result.valid = false;
        result.errors.push('URL must use HTTP or HTTPS protocol');
      }

      if (!parsedUrl.hostname) {
        result.valid = false;
        result.errors.push('URL must have a valid hostname');
      }

      if (parsedUrl.hostname === 'localhost' || parsedUrl.hostname === '127.0.0.1') {
        result.warnings.push('Using localhost - ensure Ollama is running locally');
      }

    } catch (error) {
      result.valid = false;
      result.errors.push(`Invalid URL format: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    return result;
  }

  static validateModel(model: string): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    if (!model || typeof model !== 'string') {
      result.valid = false;
      result.errors.push('Model name must be a non-empty string');
      return result;
    }

    if (model.length > 100) {
      result.valid = false;
      result.errors.push('Model name is too long');
    }

    // Check for valid model name pattern
    if (!/^[a-zA-Z0-9\-_.]+$/.test(model)) {
      result.valid = false;
      result.errors.push('Model name contains invalid characters');
    }

    return result;
  }

  static validateTimeout(timeout: number): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    if (typeof timeout !== 'number' || isNaN(timeout)) {
      result.valid = false;
      result.errors.push('Timeout must be a valid number');
      return result;
    }

    if (timeout < 1000) {
      result.warnings.push('Timeout is very short, may cause failures');
    }

    if (timeout > 300000) { // 5 minutes
      result.warnings.push('Timeout is very long, may affect user experience');
    }

    return result;
  }
}

export class DataValidator {
  static validateJson(jsonString: string): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    try {
      JSON.parse(jsonString);
    } catch (error) {
      result.valid = false;
      result.errors.push(`Invalid JSON: ${error}`);
    }

    return result;
  }

  static validateCodeContext(context: any): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    if (!context || typeof context !== 'object') {
      result.valid = false;
      result.errors.push('Context must be an object');
      return result;
    }

    // Required fields
    const requiredFields = ['language', 'filePath'];
    for (const field of requiredFields) {
      if (!context[field]) {
        result.valid = false;
        result.errors.push(`Missing required field: ${field}`);
      }
    }

    // Validate language
    if (context.language && typeof context.language !== 'string') {
      result.valid = false;
      result.errors.push('Language must be a string');
    }

    // Validate file path
    if (context.filePath && typeof context.filePath !== 'string') {
      result.valid = false;
      result.errors.push('File path must be a string');
    }

    return result;
  }
}

// Utility functions
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function isValidUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

export function sanitizeFileName(fileName: string): string {
  return fileName.replace(/[<>:"/\\|?*]/g, '_').trim();
}

export function validateFileSize(size: number, maxSize = 10485760): ValidationResult {
  const result: ValidationResult = {
    valid: true,
    errors: [],
    warnings: []
  };

  if (size > maxSize) {
    result.valid = false;
    result.errors.push(`File size ${size} bytes exceeds maximum of ${maxSize} bytes`);
  }

  if (size > maxSize * 0.8) {
    result.warnings.push('File size is approaching the limit');
  }

  return result;
}
