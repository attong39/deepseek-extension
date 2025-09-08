#!/usr/bin/env node

/**
 * Module 12: Test Execution Script
 * 
 * Easy-to-use script for running the complete autonomous AI system validation
 */

import { runMasterValidation } from './masterTestRunner';
import AI from "AI";
import Acting from "Acting";
import Auto from "Auto";
import Autonomous from "Autonomous";
import Chain from "Chain";
import CoT from "CoT";
import Complete from "Complete";
import Decision from "Decision";
import Detailed from "Detailed";
import Easy from "Easy";
import Embeddings from "Embeddings";
import Enable from "Enable";
import Engine from "Engine";
import Execution from "Execution";
import Exit from "Exit";
import Explainability from "Explainability";
import Extensibility from "Extensibility";
import Fatal from "Fatal";
import Feedback from "Feedback";
import Handle from "Handle";
import Human from "Human";
import Integration from "Integration";
import Learner from "Learner";
import Learning from "Learning";
import Loop from "Loop";
import Memory from "../../../desktop/src/Memory/index";
import Meta from "Meta";
import Module from "Module";
import Monitoring from "Monitoring";
import Observability from "Observability";
import Options from "Options";
import Performance from "Performance";
import Planner from "Planner";
import Please from "Please";
import Plugin from "Plugin";
import ReAct from "ReAct";
import Real from "Real";
import Reasoner from "Reasoner";
import Reasoning from "Reasoning";
import Registry from "Registry";
import Results from "Results";
import Running from "Running";
import Safety from "Safety";
import Save from "Save";
import Script from "Script";
import Self from "Self";
import Show from "Show";
import Stack from "Stack";
import Start from "Start";
import System from "System";
import Test from "../../../desktop/src/Test/index";
import Testing from "Testing";
import The from "The";
import This from "This";
import Thought from "Thought";
import Tuner from "Tuner";
import Unit from "Unit";
import Usage from "Usage";
import VERBOSE from "VERBOSE";
import Validation from "Validation";
import Vector from "Vector";
import Vietnamese from "Vietnamese";

async function main() {
  console.log('🚀 Autonomous AI System - Complete Validation');
  console.log('='.repeat(60));
  console.log('🎯 Vietnamese Autonomous AI: "AI cực kỳ thông minh – tự chủ mọi thứ"');
  console.log('📋 Running comprehensive validation of all 12 modules');
  console.log('');

  try {
    const report = await runMasterValidation();
    
    // Save report to file
    const fs = await import('fs');
    const reportPath = './validation-report.json';
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    console.log(`\n� Detailed report saved to: ${reportPath}`);
    
    // Exit with appropriate code
    if (report.deploymentReadiness) {
      console.log('\n✅ Validation successful - System ready for deployment!');
      process.exit(0);
    } else {
      console.log('\n⚠️ Validation completed with issues - Please review report');
      process.exit(1);
    }
    
  } catch (error: any) {
    console.error('\n❌ Validation failed with error:', error.message);
    console.error('Stack trace:', error.stack);
    process.exit(1);
  }
}

// Handle command line arguments
const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  console.log(`
🚀 Autonomous AI System Validation

Usage: node runTests.js [options]

Options:
  --help, -h     Show this help message
  --verbose, -v  Enable verbose output
  
This script runs comprehensive validation of the complete autonomous AI system,
testing all 12 modules including:

1. CoT Reasoner (Chain-of-Thought reasoning)
2. ReAct Planner (Reasoning and Acting)
3. Vector Memory (Embeddings and retrieval)
4. Auto-Tuner (Self-optimization)
5. Safety Engine (Safety and compliance)
6. Meta-Learner (Learning from experience)
7. Observability System (Monitoring and metrics)
8. Plugin Registry (Extensibility system)
9. Explainability Engine (Decision explanation)
10. Human Feedback Loop (Human-AI interaction)
11. Integration System (Module coordination)
12. System Testing and Validation (This module)

The validation includes:
- Unit tests for individual modules
- Integration tests for module interactions
- Performance benchmarking and scalability tests
- Safety validation and security testing
- Real-world scenario testing

Results are saved to validation-report.json for detailed analysis.
`);
  process.exit(0);
}

// Enable verbose mode if requested
if (args.includes('--verbose') || args.includes('-v')) {
  process.env.VERBOSE = 'true';
}

// Start validation
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

export { main as runTests };
