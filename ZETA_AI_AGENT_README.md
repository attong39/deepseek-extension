# Zeta AI Agent

## Overview

Zeta AI Agent is an intelligent coding assistant that integrates with Ollama to provide AI-powered code analysis, debugging, optimization, and development assistance directly within VS Code.

## Features

### 🤖 AI-Powered Code Analysis
- **Code Review**: Comprehensive code quality assessment with actionable suggestions
- **Debugging**: Intelligent error analysis and step-by-step debugging solutions
- **Optimization**: Performance improvements and code refactoring recommendations
- **Documentation**: Automatic code documentation generation

### 🧠 Cognitive Capabilities
- **Context Awareness**: Understands project structure and coding patterns
- **Memory Management**: Learns from interactions to improve future responses
- **Action Planning**: Creates structured plans for complex development tasks

### 🛡️ Security & Performance
- **Input Validation**: Comprehensive security checks for all inputs
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Caching**: Intelligent response caching for improved performance
- **Monitoring**: Real-time performance tracking and health monitoring

### 🔧 Developer Experience
- **VS Code Integration**: Seamless integration with VS Code commands and UI
- **Real-time Feedback**: Instant suggestions and corrections
- **Multi-language Support**: Works with TypeScript, Python, JavaScript, and more
- **Customizable**: Extensive configuration options

## Architecture

```
apps/zeta-ai-agent/
├── src/
│   ├── core/
│   │   ├── ollama/          # Ollama API integration
│   │   ├── agent/           # Main AI agent logic
│   │   │   ├── cognitive/   # Code analysis capabilities
│   │   │   ├── memory/      # Memory management
│   │   │   └── planner/     # Action planning
│   │   ├── tools/           # Development tools
│   │   └── utils/           # Utility functions
│   ├── extension/           # VS Code extension
│   └── types/               # TypeScript definitions
```

## Installation

### Prerequisites
- VS Code 1.85.0+
- Node.js 18+
- Ollama installed and running locally

### Setup
1. Clone the repository
2. Install dependencies: `npm install`
3. Compile: `npm run compile`
4. Package: `npm run package`
5. Install the `.vsix` file in VS Code

### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull the recommended model
ollama pull deepseek-coder
```

## Usage

### Commands
- `Zeta: Review Code` - Analyze current file for issues and improvements
- `Zeta: Debug Code` - Debug selected code or errors
- `Zeta: Optimize Code` - Optimize code for performance and maintainability
- `Zeta: Open AI Chat` - Interactive AI chat interface

### Configuration
Configure Zeta AI Agent through VS Code settings:

```json
{
  "zeta.ollamaUrl": "http://localhost:11434",
  "zeta.defaultModel": "deepseek-coder",
  "zeta.maxContextSize": 1000,
  "zeta.enableCaching": true
}
```

## Development

### Building
```bash
npm run compile    # Compile TypeScript
npm run watch      # Watch mode
npm run package    # Create VSIX package
```

### Testing
```bash
npm test           # Run unit tests
npm run test:integration  # Run integration tests
```

### Code Quality
```bash
npm run lint       # Lint code
npm run lint:fix   # Auto-fix linting issues
```

## API Reference

### Core Classes

#### OllamaClient
```typescript
const client = new OllamaClient('http://localhost:11434');
const response = await client.chat(messages, options);
```

#### CodeAnalyzer
```typescript
const analyzer = new CodeAnalyzer(client);
const review = await analyzer.reviewCode(code, context);
```

#### AIAgent
```typescript
const agent = new AIAgent(context);
await agent.reviewCode();
```

### Types

#### ChatMessage
```typescript
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}
```

#### CodeReview
```typescript
interface CodeReview {
  issues: CodeIssue[];
  suggestions: CodeSuggestion[];
  overall_score: number;
  summary: string;
}
```

## Security

Zeta AI Agent implements multiple security measures:

- **Input Validation**: All inputs are validated for safety
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Path Validation**: Prevents directory traversal attacks
- **Content Filtering**: Blocks potentially dangerous code patterns

## Performance

### Optimization Features
- **Response Caching**: Intelligent caching of AI responses
- **Request Batching**: Efficient handling of multiple requests
- **Memory Management**: Automatic cleanup of old data
- **Performance Monitoring**: Real-time metrics collection

### Metrics
- Response times (average, p95, p99)
- Memory usage
- Cache hit rates
- Error rates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: This README and inline code documentation

---

**Zeta AI Agent** - Making AI-powered development accessible and secure for everyone.
