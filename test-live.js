// Test AI Agent with actual optimization
const fs = require('fs');

async function testAIAgentOptimization() {
  console.log('🧪 Testing AI Agent Optimization...');
  
  try {
    console.log('📡 Sending request to Ollama...');
    
    // Test Ollama connection with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
    
    const response = await fetch('http://127.0.0.1:11434/api/chat', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        model: 'deepseek-r1:latest',
        messages: [
          {
            role: 'user',
            content: 'Analyze this TypeScript code and suggest improvements in JSON format: export class TestClass { processData(input: string) { if (input == null) return ""; return input.toUpperCase(); } }'
          }
        ],
        stream: false
      }),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    
    const data = await response.json();
    const content = data.message?.content || '';
    
    console.log('✅ AI Response received!');
    console.log('Response preview:', content.substring(0, 200) + '...');
    
    console.log('\n🎯 AI Agent working! Ready for VS Code extension testing.');
    console.log('\n📋 Next: Open VS Code and press F5 to test extension');
    
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('❌ Request timeout - DeepSeek R1 taking too long');
    } else {
      console.error('❌ Test failed:', error.message);
    }
    console.log('\n🔧 Troubleshooting:');
    console.log('  • Check if Ollama server is running: ollama serve');
    console.log('  • Test simple query: ollama run deepseek-r1:latest "hello"');
  }
}

testAIAgentOptimization();
