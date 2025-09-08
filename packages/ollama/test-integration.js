/**
 * Simple Ollama test to verify integration
 */

import { execSync } from 'child_process';

async function testOllamaIntegration() {
  console.log('🧪 Testing Ollama Integration...\n');
  
  try {
    // Test 1: Check if ollama command exists
    console.log('1️⃣ Testing Ollama CLI...');
    const version = execSync('ollama --version', { encoding: 'utf-8' });
    console.log(`✅ Ollama CLI found: ${version.trim()}\n`);
    
    // Test 2: List models
    console.log('2️⃣ Testing model list...');
    const models = execSync('ollama list', { encoding: 'utf-8' });
    console.log('✅ Models available:');
    console.log(models);
    
    // Test 3: Test API connection
    console.log('3️⃣ Testing API connection...');
    const fetch = require('node-fetch');
    
    const response = await fetch('http://127.0.0.1:11434/api/version');
    if (response.ok) {
      const data = await response.json();
      console.log(`✅ API connection successful: v${data.version}\n`);
    } else {
      console.log(`❌ API connection failed: HTTP ${response.status}\n`);
    }
    
    // Test 4: Simple generation
    console.log('4️⃣ Testing text generation...');
    const generateResponse = await fetch('http://127.0.0.1:11434/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'phi3:mini',
        prompt: 'Hello! Just say "Hi" back.',
        stream: false
      })
    });
    
    if (generateResponse.ok) {
      const genData = await generateResponse.json();
      console.log(`✅ Generation successful: "${genData.response.trim()}"\n`);
    } else {
      console.log(`❌ Generation failed: HTTP ${generateResponse.status}\n`);
    }
    
    console.log('🎉 Ollama integration test completed successfully!');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  }
}

// Run the test
testOllamaIntegration();
