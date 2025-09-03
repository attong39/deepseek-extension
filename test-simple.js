// Simple test cho Ollama API
async function testOllamaAPI() {
  try {
    console.log('Testing Ollama API connection...');
    
    const response = await fetch('http://127.0.0.1:11434/api/chat', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        model: 'deepseek-r1:latest',
        messages: [{ role: 'user', content: 'Hello! Reply with just "OK"' }],
        stream: false
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    
    const data = await response.json();
    const content = data.message?.content || '';
    
    console.log('✅ Ollama response:', content);
    console.log('🎉 AI Agent backend is working!');
    
  } catch (error) {
    console.error('❌ Ollama connection failed:', error);
  }
}

// Run test
testOllamaAPI();
