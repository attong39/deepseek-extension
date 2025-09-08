# AI Project Intelligence System

A smart AI-powered system that understands your project structure, maintains consistency, and automatically fixes issues.

## Features

- Project Understanding: Deep analysis of project structure and relationships
- Consistency Guard: Finds and fixes inconsistencies across files
- Auto Coding: AI-powered code generation to fix missing pieces
- Continuous Monitoring: Watches for changes and maintains consistency in real-time

## Quick Start

### One-time Analysis
```bash
npm run ai:brain
# or
python brain.py --root .
```

### Continuous Monitoring
```bash
npm run ai:monitor
# or
python continuous-monitor.py
```

### Check Consistency
```bash
npm run ai:consistency
# or
python consistency-guard.py --root .
```

## Output Files
- tools/ai-project-intelligence/out/brain-summary.json: Project analysis summary
- .vscode/ai-analysis.json: VSCode-compatible analysis results
- .vscode/ai-recommendations.json: Optimization recommendations

## Configuration
Edit `config.yml` to customize:

```yaml
ai:
  model: "deepseek-coder"  # AI model to use
  fallback_model: "codellama"  # Fallback model

monitoring:
  enabled: true  # Enable continuous monitoring
  debounce_ms: 2000  # Debounce time for file changes

auto_fix:
  enabled: true  # Enable automatic fixes
  min_confidence: 0.8  # Minimum confidence for auto-fixes
```

## Dependencies
Core dependencies (optional but recommended):

- ollama: For local AI processing
- watchdog: For continuous monitoring

Install with:

```bash
pip install ollama watchdog
```

## Integration with VSCode
Use the provided tasks in `.vscode/tasks.json` to run AI analysis directly from VSCode.

## Troubleshooting
- If you get import errors, make sure optional dependencies are installed
- For large projects, increase debounce time in config to avoid frequent re-analysis
- Check the output JSON files for detailed analysis results

## Testing

Run the test suite to ensure the AI intelligence system is working correctly:

```bash
# Run all AI intelligence tests
npm run test:ai-intelligence

# Run with coverage report
npm run test:coverage-ai

# Run specific test file
python -m pytest tests/ai-project-intelligence/test_consistency_guard.py -v
```

Tests cover:
- Broken reference detection
- Empty graph handling
- CLI functionality
- Error scenarios

### Usage

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run the tests
npm run test:ai-intelligence

# Or run directly
python -m pytest tests/ai-project-intelligence/ -v

# Run consistency guard with real data
npm run ai:brain  # First generate knowledge graph
npm run ai:consistency  # Then check for inconsistencies
```
