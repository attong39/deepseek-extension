// Test AI Agent functionality
import { OllamaService } from './aiAgent';

async function testAIAgent() {
  console.log('🧪 Testing AI Agent...');
  
  try {
    // Test Ollama connection first
    console.log('📡 Testing Ollama connection...');
    const ollama = new OllamaService();
    const response = await ollama.chat([
      { role: 'user', content: 'Reply with just "CONNECTION_OK"' }
    ]);
    
    console.log('✅ Ollama response:', response.trim());
    
    if (response.includes('CONNECTION_OK')) {
      console.log('🎉 AI Agent backend is ready!');
      console.log('');
      console.log('📋 Available commands in VS Code:');
      console.log('  • AI Agent: Interactive Mode');
      console.log('  • AI Agent: Review Code');
      console.log('  • AI Agent: Debug Code');
      console.log('  • AI Agent: Optimize Code');
      console.log('  • AI Agent: Check Status');
      console.log('');
      console.log('🚀 Ready to use! Press F5 in VS Code to test the extension.');
    } else {
      console.log('⚠️  Ollama responded but format unexpected');
    }
    
  } catch (error) {
    console.error('❌ AI Agent test failed:', error);
    console.log('');
    console.log('🔧 Troubleshooting:');
    console.log('  1. Make sure Ollama is running: ollama serve');
    console.log('  2. Check if DeepSeek R1 model is available: ollama list');
    console.log('  3. Test Ollama manually: ollama run deepseek-r1:latest');
  }
}

// Run test
testAIAgent();
