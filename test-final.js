// Simple test for Ollama API
async function testOllamaSimple() {
  console.log('🧪 Testing Ollama API directly...');
  
  try {
    const response = await fetch('http://127.0.0.1:11434/api/chat', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        model: 'deepseek-r1:latest',
        messages: [{ role: 'user', content: 'Reply with just "AI_READY"' }],
        stream: false
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    
    const data = await response.json();
    const content = data.message?.content || '';
    
    console.log('✅ Ollama API response:', content.trim());
    
    if (content.includes('AI_READY')) {
      console.log('🎉 AI Agent is ready for VS Code extension!');
    } else {
      console.log('⚠️  AI responded but different format');
    }
    
    console.log('');
    console.log('📋 Next steps:');
    console.log('  1. Open VS Code in this folder');
    console.log('  2. Press F5 to start extension development host'); 
    console.log('  3. Test commands: Ctrl+Shift+P → "AI Agent"');
    console.log('  4. Open test-sample.ts and try optimize command');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
    console.log('');
    console.log('🔧 Make sure Ollama is running: ollama serve');
  }
}

testOllamaSimple();
