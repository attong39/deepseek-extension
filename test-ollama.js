// Simple Ollama test
async function testOllama() {
    console.log('🔥 Testing Ollama connection...');
    
    try {
        const response = await fetch('http://127.0.0.1:11434/api/chat', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({
                model: 'deepseek-r1:latest',
                messages: [
                    { role: 'user', content: 'Hello! Can you help me optimize this TypeScript code?' }
                ],
                stream: false
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${await response.text()}`);
        }
        
        const data = await response.json();
        console.log('✅ Ollama response:', data.message?.content?.slice(0, 200) + '...');
        
    } catch (error) {
        console.error('❌ Ollama test failed:', error);
    }
}

testOllama();
