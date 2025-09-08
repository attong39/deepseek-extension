# VS Code Marketplace Publishing Guide

## Prerequisites
1. **Publisher Account**: Create a VS Code publisher account at https://marketplace.visualstudio.com/manage
2. **Azure DevOps PAT**: Generate a Personal Access Token with Marketplace permissions

## Publishing Steps

### 1. Install VSCE (if not already installed)
```bash
npm install -g vsce
```

### 2. Login to Marketplace
```bash
vsce login <publisher-name>
# Enter your Personal Access Token when prompted
```

### 3. Publish Extension
```bash
cd apps/zeta-ai-agent
vsce publish
```

### Alternative: Manual Upload
1. Go to https://marketplace.visualstudio.com/manage
2. Upload `zeta-ai-agent-1.0.0.vsix` manually
3. Fill in marketplace metadata

## Current Status
✅ **VSIX Package Built**: `zeta-ai-agent-1.0.0.vsix` (1.65MB, 741 files)
✅ **Extension Compiled**: No TypeScript errors
✅ **Package Validated**: All dependencies included

## Local Installation (Ready Now)
```bash
# Install from VSIX file
code --install-extension zeta-ai-agent-1.0.0.vsix

# Verify installation
code --list-extensions | grep zeta
```

## Marketplace Metadata (Ready)
- **Name**: Zeta AI Agent  
- **Version**: 1.0.0
- **Description**: Intelligent coding assistant powered by Ollama for code review, debugging, optimization, and AI chat
- **Keywords**: ai, ollama, code-review, debugging, optimization, assistant, copilot
- **Category**: Programming Languages, Machine Learning
- **License**: MIT

## Next Steps for Marketplace Publishing
1. Set up publisher account with appropriate organization
2. Configure Azure DevOps PAT with Marketplace permissions  
3. Run `vsce publish` command
4. Monitor marketplace analytics and user feedback

**Note**: Extension is production-ready and can be installed locally immediately. Marketplace publishing requires additional account setup.
