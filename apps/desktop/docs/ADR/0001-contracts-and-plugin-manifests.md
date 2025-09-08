# ADR-0001: Contracts and Plugin Manifests for v1.0.0

**Status**: ✅ Accepted  
**Date**: 2024-12-19  
**Authors**: Zeta Engineering Team  

## 📋 Context

Khi phát triển desktop_ai_zeta đến v1.0.0, chúng tôi cần:

1. **API Stability**: WebSocket contracts ổn định cho các third-party integrations
2. **Plugin Safety**: Plugin system an toàn, không cho phép arbitrary code execution
3. **Enterprise Readiness**: Compliance với enterprise security requirements

## 🎯 Decision

### 1. Contracts Freeze Strategy

**Schema Files**: 
- `contracts/ws/training-progress.schema.json` - WebSocket training progress events
- `contracts/plugins/plugin-manifest.schema.json` - Plugin manifest structure

**Validation**:
- Snapshot tests để detect breaking changes
- JSON Schema validation với Ajv
- Semantic versioning cho schema evolution

### 2. Plugin Manifest System

**Core Principles**:
- **Allowlist-based**: Chỉ load plugins có trong `config/plugins.allowlist.json`
- **Schema validation**: Mọi plugin manifest phải pass JSON schema
- **No arbitrary code**: Plugin chỉ là metadata + configuration, không chứa executable code

**Implementation**:
```typescript
// src/services/plugin.manifest.ts
export async function loadPluginManifests(): Promise<PluginManifest[]> {
  // 1. Read allowlist
  // 2. Validate manifest against schema  
  // 3. Return safe manifest objects
}
```

### 3. Security Boundaries

**Plugin Loading**:
- Manifest validation trước khi load
- Allowlist check mandatory
- No dynamic import() của plugin code
- Plugins chỉ là config/metadata

**Contract Enforcement**:
- Schema validation cho WebSocket messages
- Type safety với TypeScript interfaces
- Runtime validation với Ajv

## ✅ Consequences

### Positive
- **Security**: Plugin system không thể execute arbitrary code
- **Stability**: Contracts được freeze và snapshot tested
- **Enterprise**: Compliance với security requirements
- **DX**: Clear schema + types cho developers

### Negative  
- **Flexibility**: Plugin system bị giới hạn (tradeoff có chủ ý)
- **Overhead**: Schema validation có cost nhỏ
- **Migration**: Breaking schema changes sẽ cần major version bump

## 🔧 Implementation Details

### Files Created
```
contracts/
├── ws/
│   └── training-progress.schema.json
└── plugins/
    └── plugin-manifest.schema.json

config/
└── plugins.allowlist.json

src/
├── services/
│   └── plugin.manifest.ts
└── __tests__/
    ├── contracts.ws.training.test.ts
    └── contracts.plugin.manifest.test.ts
```

### Integration Points
1. **Main Process**: Load manifests trong `main.tsx` 
2. **WebSocket**: Validate messages against training-progress schema
3. **Plugin UI**: Render plugin metadata từ validated manifests
4. **Release**: Schema snapshot tests trong CI pipeline

### Schema Evolution Strategy
- **Patch**: Additive changes (new optional fields)
- **Minor**: Backward-compatible extensions  
- **Major**: Breaking changes (field removal/rename)

## 📚 References

- [JSON Schema Specification](https://json-schema.org/)
- [Ajv JSON Schema Validator](https://ajv.js.org/)
- [Electron Security Best Practices](https://www.electronjs.org/docs/tutorial/security)
- [Plugin Architecture Patterns](https://martinfowler.com/articles/plugins.html)

---

**Next ADR**: ADR-0002 sẽ cover AI model integration patterns và cost management strategies.