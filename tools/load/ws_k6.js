import ws from 'k6/ws';
import { check, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

// Custom metrics for WebSocket performance
const wsConnections = new Counter('ws_connections_total');
const wsMessages = new Counter('ws_messages_total');
const wsErrors = new Rate('ws_error_rate');
const wsLatency = new Trend('ws_latency');
const wsConnectionDuration = new Trend('ws_connection_duration');

// Load test configuration
export const options = {
  stages: [
    { duration: '30s', target: 100 },   // Ramp up to 100 connections
    { duration: '60s', target: 200 },   // Scale to 200 connections
    { duration: '120s', target: 400 },  // Peak load: 400 connections
    { duration: '60s', target: 200 },   // Scale down
    { duration: '30s', target: 0 },     // Ramp down
  ],
  thresholds: {
    // Performance requirements for 10k msg/s
    'ws_messages_total': ['rate>25'],     // 25 msg/s per connection (400 * 25 = 10k)
    'ws_error_rate': ['rate<0.01'],       // <1% error rate
    'ws_latency': ['p(95)<200'],          // P95 latency <200ms
    'ws_connection_duration': ['avg>30'], // Connections last >30s on average
    'iterations': ['rate>10'],            // Minimum iteration rate
  },
};

// Environment configuration
const WS_URL = __ENV.WS_URL || 'ws://localhost:8000/api/v1/agents/teams/load-test/run';
const JWT_TOKEN = __ENV.JWT_TOKEN || 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...'; // Replace with test token
const MESSAGE_INTERVAL = parseInt(__ENV.MESSAGE_INTERVAL || '40'); // 40ms = 25 msg/s
const CONNECTION_TIMEOUT = parseInt(__ENV.CONNECTION_TIMEOUT || '5000');

export default function () {
  const connectionStart = Date.now();
  let messageCount = 0;
  let errorCount = 0;
  
  // WebSocket connection with authentication
  const params = {
    headers: {
      'Authorization': `Bearer ${JWT_TOKEN}`,
    },
    timeout: `${CONNECTION_TIMEOUT}ms`,
  };
  
  const response = ws.connect(WS_URL, params, function (socket) {
    wsConnections.add(1);
    
    socket.on('open', function () {
      console.log(`VU ${__VU}: WebSocket connection opened`);
      
      // Start sending messages at target rate
      socket.setInterval(function () {
        const messageStart = Date.now();
        
        const message = JSON.stringify({
          type: 'workflow_request',
          id: `msg-${__VU}-${messageCount++}`,
          timestamp: new Date().toISOString(),
          payload: {
            goal: `Load test message ${messageCount} from VU ${__VU}`,
            input: {
              test_data: `iteration-${messageCount}`,
              vu_id: __VU,
              connection_id: `conn-${__VU}-${Date.now()}`,
            },
            priority: 'normal',
            timeout: 30000,
          },
        });
        
        try {
          socket.send(message);
          wsMessages.add(1);
          
          // Record message send time for latency calculation
          socket.messageStart = messageStart;
        } catch (error) {
          console.error(`VU ${__VU}: Failed to send message:`, error);
          wsErrors.add(1);
          errorCount++;
        }
      }, MESSAGE_INTERVAL);
      
      // Send heartbeat pings
      socket.setInterval(function () {
        try {
          socket.ping();
        } catch (error) {
          console.error(`VU ${__VU}: Ping failed:`, error);
        }
      }, 20000); // 20 second intervals
    });
    
    socket.on('message', function (data) {
      try {
        const response = JSON.parse(data);
        
        // Calculate latency if this is a response to our message
        if (socket.messageStart && response.type === 'workflow_response') {
          const latency = Date.now() - socket.messageStart;
          wsLatency.add(latency);
        }
        
        // Handle different message types
        switch (response.type) {
          case 'workflow_response':
            console.log(`VU ${__VU}: Received workflow response: ${response.id}`);
            break;
          case 'step_update':
            console.log(`VU ${__VU}: Step update: ${response.step} - ${response.status}`);
            break;
          case 'error':
            console.error(`VU ${__VU}: Server error: ${response.message}`);
            wsErrors.add(1);
            errorCount++;
            break;
          case 'heartbeat':
            // Silent heartbeat acknowledgment
            break;
          default:
            console.log(`VU ${__VU}: Unknown message type: ${response.type}`);
        }
      } catch (error) {
        console.error(`VU ${__VU}: Failed to parse message:`, error);
        wsErrors.add(1);
        errorCount++;
      }
    });
    
    socket.on('pong', function () {
      // Heartbeat acknowledged
    });
    
    socket.on('close', function () {
      const connectionDuration = Date.now() - connectionStart;
      wsConnectionDuration.add(connectionDuration);
      
      console.log(`VU ${__VU}: WebSocket connection closed after ${connectionDuration}ms`);
      console.log(`VU ${__VU}: Sent ${messageCount} messages, ${errorCount} errors`);
    });
    
    socket.on('error', function (error) {
      console.error(`VU ${__VU}: WebSocket error:`, error);
      wsErrors.add(1);
      errorCount++;
    });
    
    // Keep connection alive for test duration
    sleep(1);
  });
  
  // Check connection success
  check(response, {
    'WebSocket connection successful': (r) => r && r.status === 101,
  });
  
  // Short sleep between iterations
  sleep(Math.random() * 2 + 1); // 1-3 second random sleep
}

// Teardown function to log final statistics
export function teardown(data) {
  console.log('='.repeat(50));
  console.log('WebSocket Load Test Results:');
  console.log('='.repeat(50));
  console.log(`Target: 10,000 messages/second with 400 concurrent connections`);
  console.log(`Expected per-connection rate: 25 messages/second`);
  console.log(`Message interval: ${MESSAGE_INTERVAL}ms`);
  console.log('');
  console.log('Check thresholds in k6 output for pass/fail status');
  console.log('Monitor the following metrics:');
  console.log('- ws_messages_total: Total messages sent');
  console.log('- ws_error_rate: WebSocket error rate (should be <1%)');
  console.log('- ws_latency: Message round-trip latency (P95 <200ms)');
  console.log('- ws_connection_duration: How long connections stay open');
  console.log('='.repeat(50));
}

// Setup function for test initialization
export function setup() {
  console.log('='.repeat(50));
  console.log('WebSocket Load Test Configuration:');
  console.log('='.repeat(50));
  console.log(`WebSocket URL: ${WS_URL}`);
  console.log(`Target: 10,000 messages/second`);
  console.log(`Peak concurrent connections: 400`);
  console.log(`Message interval: ${MESSAGE_INTERVAL}ms (${1000/MESSAGE_INTERVAL} msg/s per connection)`);
  console.log(`Connection timeout: ${CONNECTION_TIMEOUT}ms`);
  console.log('');
  console.log('Performance Thresholds:');
  console.log('- Message rate: >25 msg/s per connection');
  console.log('- Error rate: <1%');
  console.log('- P95 latency: <200ms');
  console.log('- Connection duration: >30s average');
  console.log('='.repeat(50));
  
  return {};
}
