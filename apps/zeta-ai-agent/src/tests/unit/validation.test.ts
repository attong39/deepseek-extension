import { describe, it, expect } from '../testRunner';
import { 
  CodeValidator, 
  ConfigValidator, 
  DataValidator,
  isValidEmail,
  isValidUrl,
  sanitizeFileName,
  validateFileSize
} from '../../utils/validation';
import { SecurityPolicy } from '../../types/shared';
import FROM from "FROM";
import HTTP from "HTTP";
import HTTPS from "HTTPS";
import Hello from "Hello";
import Invalid from "Invalid";
import NaN from "NaN";
import SELECT from "SELECT";
import SQL from "SQL";
import URL from "URL";
import Utility from "Utility";
import WHERE from "WHERE";
import XSS from "XSS";

describe('CodeValidator', () => {
  let validator: CodeValidator;
  let securityPolicy: SecurityPolicy;

  beforeEach(() => {
    securityPolicy = {
      max_code_size: 1000,
      allowed_file_extensions: ['.ts', '.js', '.py'],
      blocked_patterns: [/eval\(/i, /exec\(/i],
      max_context_size: 5000,
      rate_limit_per_minute: 60
    };
    validator = new CodeValidator(securityPolicy);
  });

  describe('validateCode', () => {
    it('should validate clean code', () => {
      const code = 'function hello() { return "world"; }';
      const result = validator.validateCode(code);
      
      expect(result.valid).toBe(true);
      expect(result.errors.length).toBe(0);
    });

    it('should reject code exceeding size limit', () => {
      const code = 'a'.repeat(1500);
      const result = validator.validateCode(code);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBe(1);
      expect(result.errors[0]).toContain('exceeds maximum size');
    });

    it('should reject disallowed file extensions', () => {
      const code = 'console.log("test")';
      const result = validator.validateCode(code, 'test.exe');
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBe(1);
      expect(result.errors[0]).toContain('not allowed');
    });

    it('should accept allowed file extensions', () => {
      const code = 'console.log("test")';
      const result = validator.validateCode(code, 'test.ts');
      
      expect(result.valid).toBe(true);
    });

    it('should reject blocked patterns', () => {
      const code = 'eval("malicious code")';
      const result = validator.validateCode(code);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBe(1);
      expect(result.errors[0]).toContain('blocked pattern');
    });

    it('should warn about dangerous patterns', () => {
      const code = 'require("child_process")';
      const result = validator.validateCode(code);
      
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('command execution');
    });

    it('should detect SQL injection patterns', () => {
      const code = 'SELECT * FROM users WHERE id = "' + '" + userInput + "';
      const result = validator.validateCode(code);
      
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('SQL injection');
    });

    it('should detect XSS patterns', () => {
      const code = 'element.innerHTML = userInput + "<script>";';
      const result = validator.validateCode(code);
      
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('XSS');
    });
  });

  describe('validateInput', () => {
    it('should validate clean input', () => {
      const result = validator.validateInput('Hello world');
      expect(result.valid).toBe(true);
    });

    it('should reject empty input', () => {
      const result = validator.validateInput('');
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('non-empty string');
    });

    it('should reject null input', () => {
      const result = validator.validateInput(null as any);
      expect(result.valid).toBe(false);
    });

    it('should reject input exceeding length', () => {
      const longInput = 'a'.repeat(15000);
      const result = validator.validateInput(longInput);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('maximum length');
    });

    it('should reject malicious input', () => {
      const result = validator.validateInput('<script>alert("xss")</script>');
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('malicious content');
    });
  });

  describe('sanitizeInput', () => {
    it('should remove script tags', () => {
      const input = '<script>alert("xss")</script>Hello';
      const sanitized = validator.sanitizeInput(input);
      expect(sanitized).toBe('Hello');
    });

    it('should remove javascript: urls', () => {
      const input = 'javascript:alert("xss")';
      const sanitized = validator.sanitizeInput(input);
      expect(sanitized).toBe('');
    });

    it('should remove event handlers', () => {
      const input = 'onclick="alert(1)"';
      const sanitized = validator.sanitizeInput(input);
      expect(sanitized).toBe('');
    });
  });
});

describe('ConfigValidator', () => {
  describe('validateOllamaUrl', () => {
    it('should validate valid HTTP URL', () => {
      const result = ConfigValidator.validateOllamaUrl('http://localhost:11434');
      expect(result.valid).toBe(true);
    });

    it('should validate valid HTTPS URL', () => {
      const result = ConfigValidator.validateOllamaUrl('https://api.example.com:8080');
      expect(result.valid).toBe(true);
    });

    it('should reject invalid protocol', () => {
      const result = ConfigValidator.validateOllamaUrl('ftp://localhost:11434');
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('HTTP or HTTPS');
    });

    it('should reject malformed URL', () => {
      const result = ConfigValidator.validateOllamaUrl('not-a-url');
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('Invalid URL');
    });

    it('should warn about localhost', () => {
      const result = ConfigValidator.validateOllamaUrl('http://localhost:11434');
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('localhost');
    });
  });

  describe('validateModel', () => {
    it('should validate valid model name', () => {
      const result = ConfigValidator.validateModel('deepseek-coder');
      expect(result.valid).toBe(true);
    });

    it('should reject empty model name', () => {
      const result = ConfigValidator.validateModel('');
      expect(result.valid).toBe(false);
    });

    it('should reject null model name', () => {
      const result = ConfigValidator.validateModel(null as any);
      expect(result.valid).toBe(false);
    });

    it('should reject too long model name', () => {
      const longName = 'a'.repeat(150);
      const result = ConfigValidator.validateModel(longName);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('too long');
    });

    it('should reject invalid characters', () => {
      const result = ConfigValidator.validateModel('model@#$%');
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('invalid characters');
    });
  });

  describe('validateTimeout', () => {
    it('should validate reasonable timeout', () => {
      const result = ConfigValidator.validateTimeout(30000);
      expect(result.valid).toBe(true);
    });

    it('should reject non-number timeout', () => {
      const result = ConfigValidator.validateTimeout('30000' as any);
      expect(result.valid).toBe(false);
    });

    it('should reject NaN timeout', () => {
      const result = ConfigValidator.validateTimeout(NaN);
      expect(result.valid).toBe(false);
    });

    it('should warn about very short timeout', () => {
      const result = ConfigValidator.validateTimeout(500);
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('very short');
    });

    it('should warn about very long timeout', () => {
      const result = ConfigValidator.validateTimeout(400000);
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('very long');
    });
  });
});

describe('DataValidator', () => {
  describe('validateJson', () => {
    it('should validate valid JSON', () => {
      const result = DataValidator.validateJson('{"key": "value"}');
      expect(result.valid).toBe(true);
    });

    it('should reject invalid JSON', () => {
      const result = DataValidator.validateJson('{key: "value"}');
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('Invalid JSON');
    });
  });

  describe('validateCodeContext', () => {
    it('should validate valid context', () => {
      const context = {
        language: 'typescript',
        filePath: '/path/to/file.ts'
      };
      const result = DataValidator.validateCodeContext(context);
      expect(result.valid).toBe(true);
    });

    it('should reject null context', () => {
      const result = DataValidator.validateCodeContext(null);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('must be an object');
    });

    it('should reject missing required fields', () => {
      const context = { language: 'typescript' };
      const result = DataValidator.validateCodeContext(context);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('filePath'))).toBe(true);
    });

    it('should reject invalid field types', () => {
      const context = {
        language: 123,
        filePath: '/path/to/file.ts'
      };
      const result = DataValidator.validateCodeContext(context);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('must be a string');
    });
  });
});

describe('Utility functions', () => {
  describe('isValidEmail', () => {
    it('should validate correct email', () => {
      expect(isValidEmail('test@example.com')).toBe(true);
    });

    it('should reject invalid email', () => {
      expect(isValidEmail('invalid-email')).toBe(false);
      expect(isValidEmail('test@')).toBe(false);
      expect(isValidEmail('@example.com')).toBe(false);
    });
  });

  describe('isValidUrl', () => {
    it('should validate correct URL', () => {
      expect(isValidUrl('https://example.com')).toBe(true);
      expect(isValidUrl('http://localhost:3000')).toBe(true);
    });

    it('should reject invalid URL', () => {
      expect(isValidUrl('not-a-url')).toBe(false);
      expect(isValidUrl('ftp://')).toBe(false);
    });
  });

  describe('sanitizeFileName', () => {
    it('should remove illegal characters', () => {
      const result = sanitizeFileName('file<>:"/\\|?*.txt');
      expect(result).toBe('file_________.txt');
    });

    it('should preserve legal characters', () => {
      const result = sanitizeFileName('valid-file_name.txt');
      expect(result).toBe('valid-file_name.txt');
    });
  });

  describe('validateFileSize', () => {
    it('should validate size within limit', () => {
      const result = validateFileSize(1000, 2000);
      expect(result.valid).toBe(true);
    });

    it('should reject size exceeding limit', () => {
      const result = validateFileSize(3000, 2000);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('exceeds maximum');
    });

    it('should warn when approaching limit', () => {
      const result = validateFileSize(1800, 2000);
      expect(result.warnings.length).toBe(1);
      expect(result.warnings[0]).toContain('approaching');
    });
  });
});
