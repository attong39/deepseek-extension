import API from "../../../apps/desktop/src/API/index";
import Access from "Access";
import Allow from "Allow";
import Buffer from "Buffer";
import C from "C";
import Check from "Check";
import Code from "Code";
import Execution from "Execution";
import For from "For";
import HTTP from "HTTP";
import HTTPS from "HTTPS";
import InputValidator from "InputValidator";
import Invalid from "Invalid";
import MB from "MB";
import Model from "Model";
import Ollama from "Ollama";
import Only from "Only";
import Path from "Path";
import Potentially from "Potentially";
import Remove from "Remove";
import Request from "Request";
import SecurityValidator from "SecurityValidator";
import System32 from "System32";
import URL from "URL";
import URLs from "URLs";
import Windows from "Windows";
import Z0 from "Z0";
export class InputValidator {
  static validateCodeInput(code: string): { valid: boolean; error?: string } {
    if (!code || typeof code !== 'string') {
      return { valid: false, error: 'Code input must be a non-empty string' };
    }

    if (code.length > 100000) {
      return { valid: false, error: 'Code too large (max 100KB)' };
    }

    // Check for potentially dangerous patterns
    const dangerousPatterns = [
      /system\s*\(/i,
      /exec\s*\(/i,
      /eval\s*\(/i,
      /require\s*\(\s*['"]child_process['"]/i,
      /import\s*os/i,
      /import\s*subprocess/i
    ];

    for (const pattern of dangerousPatterns) {
      if (pattern.test(code)) {
        return {
          valid: false,
          error: 'Potentially dangerous code detected. Execution blocked for security.'
        };
      }
    }

    return { valid: true };
  }

  static validatePath(path: string): { valid: boolean; error?: string } {
    if (!path || typeof path !== 'string') {
      return { valid: false, error: 'Path must be a non-empty string' };
    }

    // Check for directory traversal attempts
    if (path.includes('..') || path.includes('../') || path.includes('..\\')) {
      return { valid: false, error: 'Invalid path: directory traversal not allowed' };
    }

    // Check for system paths
    const systemPaths = ['/etc/', '/root/', '/bin/', 'C:\\Windows\\', 'C:\\System32\\'];
    for (const sysPath of systemPaths) {
      if (path.toLowerCase().includes(sysPath.toLowerCase())) {
        return { valid: false, error: 'Access to system directories not allowed' };
      }
    }

    return { valid: true };
  }

  static validateUrl(url: string): { valid: boolean; error?: string } {
    if (!url || typeof url !== 'string') {
      return { valid: false, error: 'URL must be a non-empty string' };
    }

    try {
      const parsedUrl = new URL(url);

      // Only allow http and https protocols
      if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
        return { valid: false, error: 'Only HTTP and HTTPS URLs are allowed' };
      }

      // Check for localhost/127.0.0.1 (allowed for Ollama)
      if (parsedUrl.hostname === 'localhost' || parsedUrl.hostname === '127.0.0.1') {
        return { valid: true };
      }

      // For other URLs, additional validation could be added
      return { valid: true };
    } catch {
      return { valid: false, error: 'Invalid URL format' };
    }
  }

  static validateModelName(modelName: string): { valid: boolean; error?: string } {
    if (!modelName || typeof modelName !== 'string') {
      return { valid: false, error: 'Model name must be a non-empty string' };
    }

    if (modelName.length > 100) {
      return { valid: false, error: 'Model name too long (max 100 characters)' };
    }

    // Allow alphanumeric, hyphens, underscores, and colons
    const validPattern = /^[a-zA-Z0-9\-_:]+$/;
    if (!validPattern.test(modelName)) {
      return { valid: false, error: 'Model name contains invalid characters' };
    }

    return { valid: true };
  }

  static sanitizeInput(input: string): string {
    if (!input) return '';

    // Remove null bytes and other control characters
    return input.replace(/[\x00-\x1F\x7F]/g, '').replace(/\x7F/g, '');
  }

  static validateJsonInput(jsonString: string): { valid: boolean; error?: string; data?: any } {
    if (!jsonString || typeof jsonString !== 'string') {
      return { valid: false, error: 'JSON input must be a non-empty string' };
    }

    try {
      const data = JSON.parse(jsonString);

      // Check for potentially dangerous JSON structures
      const dangerousKeys = ['__proto__', 'constructor', 'prototype'];
      const checkObject = (obj: any): boolean => {
        if (typeof obj !== 'object' || obj === null) return true;

        for (const key in obj) {
          if (dangerousKeys.includes(key)) {
            return false;
          }
          if (!checkObject(obj[key])) {
            return false;
          }
        }
        return true;
      };

      if (!checkObject(data)) {
        return { valid: false, error: 'JSON contains potentially dangerous keys' };
      }

      return { valid: true, data };
    } catch (error) {
      return { valid: false, error: `Invalid JSON: ${error}` };
    }
  }
}

export class SecurityValidator {
  static validateApiKey(apiKey: string): { valid: boolean; error?: string } {
    if (!apiKey) {
      return { valid: true }; // API key is optional
    }

    if (typeof apiKey !== 'string') {
      return { valid: false, error: 'API key must be a string' };
    }

    if (apiKey.length < 10) {
      return { valid: false, error: 'API key too short (minimum 10 characters)' };
    }

    if (apiKey.length > 200) {
      return { valid: false, error: 'API key too long (maximum 200 characters)' };
    }

    // Check for common patterns that might indicate a fake key
    if (/^(?:test|fake|dummy|example)/i.test(apiKey)) {
      return { valid: false, error: 'API key appears to be a test/fake key' };
    }

    return { valid: true };
  }

  static validateRequestSize(data: any): { valid: boolean; error?: string } {
    const sizeInBytes = Buffer.byteLength(JSON.stringify(data), 'utf8');
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (sizeInBytes > maxSize) {
      return {
        valid: false,
        error: `Request too large (${(sizeInBytes / 1024 / 1024).toFixed(2)}MB, max ${maxSize / 1024 / 1024}MB)`
      };
    }

    return { valid: true };
  }
}
