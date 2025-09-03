# Prompt Templates

This directory contains custom prompt templates for the DeepSeek AI Agent.

## Template Format

Templates use mustache syntax for variable interpolation:
- `{{goal}}` - The user's goal/objective
- `{{context}}` - Code context from workspace
- `{{framework}}` - Detected framework (React, Vue, Python, etc.)
- `{{dependencies}}` - Project dependencies

## Available Templates

- `system.md` - Default system prompt template
- `review.md` - Code review specific template  
- `debug.md` - Debug assistance template
- `optimize.md` - Performance optimization template

## Custom Templates

You can create custom templates by:
1. Creating a new `.md` file in this directory
2. Using mustache syntax for variables
3. Configuring the template path in VS Code settings