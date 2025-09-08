import Error from "Error";
import Expectation from "Expectation";
import Expected from "Expected";
import Failed from "Failed";
import Global from "Global";
import Helper from "Helper";
import NotExpectation from "NotExpectation";
import Passed from "Passed";
import RegExp from "RegExp";
import Results from "Results";
import Simple from "Simple";
import Suite from "Suite";
import Suites from "Suites";
import Test from "../../../desktop/src/Test/index";
import TestResult from "TestResult";
import TestRunner from "./TestRunner";
import TestSuite from "TestSuite";
import Tests from "../../../desktop/src/Tests/index";
export interface TestResult {
  name: string;
  passed: boolean;
  error?: string;
  duration: number;
}

export interface TestSuite {
  name: string;
  tests: TestResult[];
  totalPassed: number;
  totalFailed: number;
  duration: number;
}

export class TestRunner {
  private suites: TestSuite[] = [];
  private currentSuite: TestSuite | null = null;

  describe(name: string, fn: () => void): void {
    const suite: TestSuite = {
      name,
      tests: [],
      totalPassed: 0,
      totalFailed: 0,
      duration: 0
    };

    this.currentSuite = suite;
    const startTime = Date.now();
    
    try {
      fn();
    } catch (error) {
      console.error(`Suite "${name}" failed to run:`, error);
    }
    
    suite.duration = Date.now() - startTime;
    suite.totalPassed = suite.tests.filter(t => t.passed).length;
    suite.totalFailed = suite.tests.filter(t => !t.passed).length;
    
    this.suites.push(suite);
    this.currentSuite = null;
  }

  it(name: string, fn: () => void | Promise<void>): void {
    if (!this.currentSuite) {
      throw new Error('Tests must be run inside a describe block');
    }

    const startTime = Date.now();
    let passed = false;
    let error: string | undefined;

    try {
      const result = fn();
      if (result instanceof Promise) {
        result.catch(err => {
          error = err.toString();
        });
      }
      passed = true;
    } catch (err) {
      passed = false;
      error = err instanceof Error ? err.message : String(err);
    }

    const testResult: TestResult = {
      name,
      passed,
      error,
      duration: Date.now() - startTime
    };

    this.currentSuite.tests.push(testResult);
  }

  expect(actual: any): Expectation {
    return new Expectation(actual);
  }

  async run(): Promise<void> {
    const totalSuites = this.suites.length;
    const totalTests = this.suites.reduce((sum, suite) => sum + suite.tests.length, 0);
    const totalPassed = this.suites.reduce((sum, suite) => sum + suite.totalPassed, 0);
    const totalFailed = this.suites.reduce((sum, suite) => sum + suite.totalFailed, 0);

    console.log('=== Test Results ===');
    console.log(`Suites: ${totalSuites}, Tests: ${totalTests}, Passed: ${totalPassed}, Failed: ${totalFailed}`);
    console.log('');

    for (const suite of this.suites) {
      console.log(`📁 ${suite.name} (${suite.duration}ms)`);
      
      for (const test of suite.tests) {
        const icon = test.passed ? '✅' : '❌';
        console.log(`  ${icon} ${test.name} (${test.duration}ms)`);
        
        if (!test.passed && test.error) {
          console.log(`     Error: ${test.error}`);
        }
      }
      
      console.log(`  Passed: ${suite.totalPassed}, Failed: ${suite.totalFailed}`);
      console.log('');
    }

    if (totalFailed > 0) {
      process.exit(1);
    }
  }

  getSuites(): TestSuite[] {
    return [...this.suites];
  }

  clear(): void {
    this.suites = [];
    this.currentSuite = null;
  }
}

export class Expectation {
  not: NotExpectation;

  constructor(private readonly actual: any) {
    this.not = new NotExpectation(this.actual);
  }

  toBe(expected: any): void {
    if (this.actual !== expected) {
      throw new Error(`Expected ${this.actual} to be ${expected}`);
    }
  }

  toEqual(expected: any): void {
    if (JSON.stringify(this.actual) !== JSON.stringify(expected)) {
      throw new Error(`Expected ${JSON.stringify(this.actual)} to equal ${JSON.stringify(expected)}`);
    }
  }

  toBeNull(): void {
    if (this.actual !== null) {
      throw new Error(`Expected ${this.actual} to be null`);
    }
  }

  toBeTruthy(): void {
    if (!this.actual) {
      throw new Error(`Expected ${this.actual} to be truthy`);
    }
  }

  toBeFalsy(): void {
    if (this.actual) {
      throw new Error(`Expected ${this.actual} to be falsy`);
    }
  }

  toContain(expected: any): void {
    if (!Array.isArray(this.actual) || !this.actual.includes(expected)) {
      throw new Error(`Expected ${JSON.stringify(this.actual)} to contain ${expected}`);
    }
  }

  toBeGreaterThan(expected: number): void {
    if (typeof this.actual !== 'number' || this.actual <= expected) {
      throw new Error(`Expected ${this.actual} to be greater than ${expected}`);
    }
  }

  toThrow(expectedError?: string | RegExp): void {
    if (typeof this.actual !== 'function') {
      throw new Error('Expected value must be a function');
    }

    let threw = false;
    let error: any;

    try {
      this.actual();
    } catch (e) {
      threw = true;
      error = e;
    }

    if (!threw) {
      throw new Error('Expected function to throw an error');
    }

    if (expectedError) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      
      if (typeof expectedError === 'string') {
        if (!errorMessage.includes(expectedError)) {
          throw new Error(`Expected error to contain "${expectedError}", got "${errorMessage}"`);
        }
      } else if (expectedError instanceof RegExp) {
        if (!expectedError.test(errorMessage)) {
          throw new Error(`Expected error to match ${expectedError}, got "${errorMessage}"`);
        }
      }
    }
  }
}

export class NotExpectation {
  constructor(private readonly actual: any) {}

  toBe(expected: any): void {
    if (this.actual === expected) {
      throw new Error(`Expected ${this.actual} not to be ${expected}`);
    }
  }

  toEqual(expected: any): void {
    if (JSON.stringify(this.actual) === JSON.stringify(expected)) {
      throw new Error(`Expected ${JSON.stringify(this.actual)} not to equal ${JSON.stringify(expected)}`);
    }
  }

  toBeNull(): void {
    if (this.actual === null) {
      throw new Error(`Expected ${this.actual} not to be null`);
    }
  }

  toBeTruthy(): void {
    if (this.actual) {
      throw new Error(`Expected ${this.actual} not to be truthy`);
    }
  }

  toBeFalsy(): void {
    if (!this.actual) {
      throw new Error(`Expected ${this.actual} not to be falsy`);
    }
  }

  toContain(expected: any): void {
    if (Array.isArray(this.actual) && this.actual.includes(expected)) {
      throw new Error(`Expected ${JSON.stringify(this.actual)} not to contain ${expected}`);
    }
  }
}

// Global test runner instance
export const testRunner = new TestRunner();

// Global test functions
export const describe = testRunner.describe.bind(testRunner);
export const it = testRunner.it.bind(testRunner);
export const expect = testRunner.expect.bind(testRunner);

// Helper functions
export function beforeEach(fn: () => void): void {
  // Simple implementation - would be more sophisticated in real test framework
}

export function afterEach(fn: () => void): void {
  // Simple implementation - would be more sophisticated in real test framework
}
