# 🤖 Zeta AI - Ollama Integration Setup

## Overview

This guide provides complete setup instructions for integrating Ollama AI models with the Zeta AI Agent development environment. The setup includes automated PowerShell scripts for easy installation and testing.

## 🚀 Quick Start

### 1. Install Ollama
```powershell
.\setup_ollama.ps1 -Install
```
Restart your terminal after installation completes.

### 2. Setup the Model
```powershell
.\setup_ollama.ps1 -Setup
```

### 3. Test Integration
```powershell
.\test_ollama_integration.ps1 -Verbose
```

### 4. Push to Registry (Optional)
```powershell
.\setup_ollama.ps1 -Push
```

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `Modelfile` | Ollama model definition for attong39/zeta |
| `setup_ollama.ps1` | Automated setup script for Ollama and model creation |
| `test_ollama_integration.ps1` | Integration test script for development server |
| `OLLAMA_SETUP_GUIDE.md` | Detailed manual setup instructions |
| `.env` | Environment configuration for Ollama integration |

## 🔧 Manual Setup (Alternative)

If you prefer manual setup, follow these steps:

### Install Ollama
1. Download from: https://ollama.ai/download
2. Run the installer
3. Restart your terminal

### Create the Model
```bash
# Pull base model
ollama pull llama3.2

# Create custom model
ollama create -f Modelfile attong39/zeta
```

### Test the Model
```bash
# Test with Ollama CLI
ollama run attong39/zeta

# Test with API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "attong39/zeta", "prompt": "Hello!", "stream": false}'
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Ollama Configuration
OLLAMA_MODEL=attong39/zeta
OLLAMA_API_KEY=your_api_key_here
OLLAMA_BASE_URL=http://localhost:11434

# Development Server
FASTAPI_HOST=localhost
FASTAPI_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Model Configuration (Modelfile)
```dockerfile
FROM llama3.2

SYSTEM """
You are Zeta AI, a friendly and helpful AI assistant specialized in:
- Python development and programming
- Vietnamese language support
- Code explanation and debugging
- Development best practices

Always respond in a helpful, clear, and friendly manner.
If asked about programming, provide code examples when appropriate.
"""
```

## 🧪 Testing

### Automated Testing
```powershell
# Full integration test
.\test_ollama_integration.ps1 -Verbose

# Test specific components
.\test_ollama_integration.ps1 -ModelName "attong39/zeta" -ServerUrl "http://localhost:8000"
```

### Manual Testing

#### Test Ollama Direct
```bash
# Health check
curl http://localhost:11434/api/tags

# Generate response
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "attong39/zeta", "prompt": "Xin chào!", "stream": false}'
```

#### Test Development Server
```bash
# Server health
curl http://localhost:8000/health

# AI chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "model": "attong39/zeta"}'
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "ollama command not found"
```powershell
# Restart terminal after installation
# Or add Ollama to PATH manually
$env:Path += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama"
```

#### 2. "Model not found"
```powershell
# Recreate the model
.\setup_ollama.ps1 -Setup

# Or manually
ollama create -f Modelfile attong39/zeta
```

#### 3. "Connection refused"
```powershell
# Start Ollama service
ollama serve

# Check if service is running
netstat -ano | findstr :11434
```

#### 4. "Development server not responding"
```powershell
# Start development server
python apps/backend/metrics_server.py

# Or use VS Code debugger
# Press F5 in VS Code
```

### Debug Commands
```powershell
# Check Ollama status
ollama list
ollama ps

# Check environment
Get-ChildItem env: | Where-Object Name -like "OLLAMA*"

# Test network connectivity
Test-NetConnection localhost -Port 11434
Test-NetConnection localhost -Port 8000
```

## 📊 Performance Optimization

### Model Selection
- **llama3.2**: Fast, good for development (default)
- **llama3.1**: Better quality, slower
- **codellama**: Specialized for code

### Memory Management
```bash
# Check memory usage
ollama ps

# Stop unused models
ollama stop <model_name>

# Clean up
ollama system prune
```

### API Optimization
```python
# Use streaming for better performance
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": model, "prompt": prompt, "stream": True}
)
```

## 🚀 Deployment

### Local Development
```powershell
# Start all services
.\run_integration_mapper.ps1

# Or manually
Start-Process "ollama" "serve"
Start-Process "python" "apps/backend/metrics_server.py"
```

### Production Deployment
1. Use Docker for Ollama
2. Configure reverse proxy
3. Set up monitoring
4. Implement rate limiting

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Llama Models](https://ollama.ai/library)
- [API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Model Registry](https://ollama.ai/library)

## 🤝 Contributing

1. Test your changes with the integration test script
2. Update documentation for any configuration changes
3. Follow the existing code style and patterns

## 📝 License

This setup is part of the Zeta AI Agent project. See project license for details.

---

**🎯 Next Steps:**
1. Run the automated setup: `.\setup_ollama.ps1 -Install`
2. Test the integration: `.\test_ollama_integration.ps1`
3. Start developing with AI assistance!

For issues or questions, check the troubleshooting section or create an issue in the project repository.
