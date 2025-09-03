// Test AI Agent connection với Ollama
import { OllamaService } from './aiAgent';

async function testOllamaConnection() {
  const ollama = new OllamaService();
  
  try {
    console.log('Testing Ollama connection...');
    const response = await ollama.chat([
      { role: 'user', content: 'Hello! Just testing connection. Reply with "OK"' }
    ]);
    
    console.log('✅ Ollama response:', response);
    return true;
  } catch (error) {
    console.error('❌ Ollama connection failed:', error);
    return false;
  }
}

// Run test
testOllamaConnection().then(success => {
  if (success) {
    console.log('🎉 AI Agent ready for use!');
  } else {
    console.log('❌ AI Agent not working');
  }
});
