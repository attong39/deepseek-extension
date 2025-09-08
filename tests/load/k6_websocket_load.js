// k6 WebSocket Load Test Script
// Targets 10k messages/second with concurrent connections

import ws from 'k6/ws';
import { check, sleep } from 'k6';
import { Rate, Counter, Trend } from 'k6/metrics';

// Custom metrics
export let wsConnectionErrors = new Counter('ws_connection_errors');
export let wsMessageErrors = new Counter('ws_message_errors');
export let wsMessageLatency = new Trend('ws_message_latency');
export let wsSuccessRate = new Rate('ws_success_rate');

// Test configuration
export let options = {
  stages: [
    // Ramp up
    { duration: '30s', target: 50 },   // Ramp to 50 VUs
    { duration: '60s', target: 100 },  // Ramp to 100 VUs
    { duration: '60s', target: 200 },  // Ramp to 200 VUs
    
    // Load test
    { duration: '300s', target: 200 }, // Hold 200 VUs for 5 minutes
    
    // Stress test
    { duration: '60s', target: 400 },  // Spike to 400 VUs
    { duration: '120s', target: 400 }, // Hold spike
    
    // Ramp down
    { duration: '60s', target: 0 },    // Graceful shutdown
  ],
  
  thresholds: {
    // Performance requirements
    'ws_success_rate': ['rate>0.95'],           // 95% success rate
    'ws_message_latency': ['p(95)<1000'],       // P95 latency under 1s
    'ws_connection_errors': ['count<100'],       // Less than 100 connection errors
    'ws_message_errors': ['count<1000'],        // Less than 1000 message errors
    
    // Load requirements
    'iterations': ['rate>8000'],                 // Target 8k+ messages/second (allowing tolerance)
  },
};

// Test data
const TARGET_MSG_SIZE = 1024;
const MESSAGES_PER_CONNECTION = 50; // Messages per VU per iteration

function generateTestMessage(vu, iteration, messageId) {
  const baseMessage = {
    type: 'k6_load_test',
    vu_id: vu,
    iteration: iteration,
    message_id: messageId,
    timestamp: Date.now(),
    test_phase: 'load_test'
  };
  
  // Pad message to target size
  const baseSize = JSON.stringify(baseMessage).length;
  const paddingSize = Math.max(0, TARGET_MSG_SIZE - baseSize - 50);
  baseMessage.payload = 'x'.repeat(paddingSize);
  
  return JSON.stringify(baseMessage);
}

export default function() {
  const wsUrl = __ENV.WS_URL || 'ws://localhost:8000/ws';
  const vuId = __VU;
  const iteration = __ITER;
  
  let connectionSuccess = false;
  let messagesReceived = 0;
  
  const res = ws.connect(wsUrl, {}, function(socket) {
    connectionSuccess = true;
    
    socket.on('open', function() {
      console.log(`VU ${vuId}: WebSocket connection established`);
      
      // Send burst of messages
      for (let i = 0; i < MESSAGES_PER_CONNECTION; i++) {
        const startTime = Date.now();
        const message = generateTestMessage(vuId, iteration, i);
        
        socket.send(message);
        
        // Set up response handler for this message
        socket.on('message', function(data) {
          const endTime = Date.now();
          const latency = endTime - startTime;
          
          wsMessageLatency.add(latency);
          messagesReceived++;
          
          // Parse response and validate
          try {
            const response = JSON.parse(data);
            const success = response.type === 'load_test_response' || response.status === 'ok';
            wsSuccessRate.add(success);
            
            if (!success) {
              wsMessageErrors.add(1);
              console.log(`VU ${vuId}: Invalid response:`, data);
            }
          } catch (e) {
            wsMessageErrors.add(1);
            console.log(`VU ${vuId}: Failed to parse response:`, e.message);
          }
        });
        
        socket.on('error', function(e) {
          wsMessageErrors.add(1);
          console.log(`VU ${vuId}: WebSocket error:`, e.error());
        });
        
        // Small delay between messages to control rate
        sleep(0.01); // 10ms delay = ~100 msg/s per VU
      }
      
      // Keep connection open briefly to receive responses
      sleep(2);
      
      socket.close();
    });
    
    socket.on('close', function() {
      console.log(`VU ${vuId}: WebSocket connection closed. Messages received: ${messagesReceived}`);
    });
    
    socket.on('error', function(e) {
      wsConnectionErrors.add(1);
      console.log(`VU ${vuId}: Connection error:`, e.error());
    });
    
    // Timeout after 30 seconds
    setTimeout(function() {
      socket.close();
    }, 30000);
  });
  
  // Check connection success
  check(res, {
    'WebSocket connection successful': (r) => connectionSuccess,
  });
  
  if (!connectionSuccess) {
    wsConnectionErrors.add(1);
  }
}

// Chaos engineering scenarios
export function chaosScenario() {
  // This would be called by external chaos tools
  // For k6, we simulate chaos by varying load patterns
  
  const chaosTypes = ['cpu_spike', 'memory_pressure', 'network_delay'];
  const chaosType = chaosTypes[Math.floor(Math.random() * chaosTypes.length)];
  
  console.log(`Chaos scenario: ${chaosType}`);
  
  switch (chaosType) {
    case 'cpu_spike':
      // Simulate CPU-intensive operation
      let waste = 0;
      for (let i = 0; i < 1000000; i++) {
        waste += Math.random();
      }
      break;
      
    case 'memory_pressure':
      // Simulate memory allocation
      const largeArray = new Array(100000).fill('memory_pressure');
      sleep(0.1);
      break;
      
    case 'network_delay':
      // Simulate network delay
      sleep(Math.random() * 0.5); // 0-500ms delay
      break;
  }
}

// Teardown function for cleanup
export function teardown(data) {
  console.log('Load test completed');
  console.log('Summary metrics:');
  console.log(`- WS Connection Errors: ${wsConnectionErrors.count}`);
  console.log(`- WS Message Errors: ${wsMessageErrors.count}`);
  console.log(`- Average Message Latency: ${wsMessageLatency.avg}ms`);
  console.log(`- Success Rate: ${(wsSuccessRate.rate * 100).toFixed(2)}%`);
}