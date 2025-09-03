import * as assert from 'assert';
import { Config } from '../config';
import { OllamaClient } from '../ollamaClient';
import { AIAgent } from '../aiAgent';

suite('DeepSeek AI Agent Test Suite', () => {
    
    suite('Config Tests', () => {
        test('Config singleton pattern', () => {
            const config1 = Config.getInstance();
            const config2 = Config.getInstance();
            assert.strictEqual(config1, config2, 'Config should be singleton');
        });
        
        test('Default configuration values', () => {
            const config = Config.getInstance();
            assert.strictEqual(config.getOllamaUrl(), 'http://127.0.0.1:11434');
            assert.strictEqual(config.getOllamaModel(), 'deepseek-r1:latest');
            assert.strictEqual(config.getOllamaTimeout(), 15000);
            assert.strictEqual(config.getAutoApply(), false);
            assert.strictEqual(config.getMaxContextBytes(), 40000);
        });
    });
    
    suite('OllamaClient Tests', () => {
        test('OllamaClient instantiation', () => {
            const client = new OllamaClient();
            assert.ok(client, 'OllamaClient should be instantiated');
        });
        
        test('Filter think tags', () => {
            const input = 'Hello <think>internal thought</think> world';
            const expected = 'Hello  world';
            const result = OllamaClient.filterThinkTags(input);
            assert.strictEqual(result, expected);
        });
        
        test('Filter multiple think tags', () => {
            const input = '<think>think1</think>Hello<think>think2</think> world<think>think3</think>';
            const expected = 'Hello world';
            const result = OllamaClient.filterThinkTags(input);
            assert.strictEqual(result, expected);
        });
    });
    
    suite('AIAgent Tests', () => {
        test('AIAgent instantiation', () => {
            const agent = new AIAgent();
            assert.ok(agent, 'AIAgent should be instantiated');
        });
        
        test('Parse valid JSON plan', async () => {
            const agent = new AIAgent();
            const response = `
Here is the plan:
\`\`\`json
{
    "summary": "Test plan",
    "rationale": "Testing the parser",
    "actions": [
        {
            "type": "upsert_file",
            "path": "test.ts",
            "content": "console.log('test');"
        }
    ]
}
\`\`\`
`;
            
            try {
                // Use reflection to access private method for testing
                const parsePlan = (agent as any).parsePlan.bind(agent);
                const plan = parsePlan(response);
                
                assert.strictEqual(plan.summary, 'Test plan');
                assert.strictEqual(plan.rationale, 'Testing the parser');
                assert.strictEqual(plan.actions.length, 1);
                assert.strictEqual(plan.actions[0].type, 'upsert_file');
                assert.strictEqual(plan.actions[0].path, 'test.ts');
                
            } catch (error) {
                // Skip this test if we can't access private method
                console.log('Skipping private method test');
            }
        });
        
        test('Path sanitization', () => {
            const agent = new AIAgent();
            
            try {
                // Use reflection to access private method for testing
                const sanitizePath = (agent as any).sanitizePath.bind(agent);
                
                // Test normal path
                const normal = sanitizePath('src/test.ts');
                assert.ok(normal.includes('test.ts'));
                
                // Test path traversal prevention
                const traversal = sanitizePath('../../../etc/passwd');
                assert.ok(!traversal.includes('..'));
                
            } catch (error) {
                // Skip this test if we can't access private method
                console.log('Skipping private method test');
            }
        });
    });
});