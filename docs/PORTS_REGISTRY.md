# Ports Registry

_Package_: `zeta_vn.core.ports`

## Mục lục

- [alerts](#alerts)
- [backup](#backup)
- [cache](#cache)
- [documentation](#documentation)
- [feature_toggles](#feature_toggles)
- [memory](#memory)
- [metrics](#metrics)
- [mlops](#mlops)
- [observability](#observability)
- [security](#security)
- [testing](#testing)
- [uncategorized](#uncategorized)

## alerts

### AlertSystem  
`zeta_vn.core.ports.alerts.AlertSystem`
- **critical**`(self, title: 'str', message: 'str') -> 'None'`
- **info**`(self, title: 'str', message: 'str') -> 'None'`
- **page_oncall**`(self, service: 'str', message: 'str') -> 'None'`
- **warn**`(self, title: 'str', message: 'str') -> 'None'`

## backup

### BackupService  
`zeta_vn.core.ports.backup.BackupService`
- **create_snapshot**`(self, metadata: 'dict[str, Any] | None' = None) -> 'str'`
- **delete_snapshot**`(self, snapshot_id: 'str') -> 'None'`
- **list_snapshots**`(self) -> 'list[dict[str, Any]]'`
- **restore_snapshot**`(self, snapshot_id: 'str') -> 'None'`
- **verify_snapshot**`(self, snapshot_id: 'str') -> 'bool'`

## cache

### CacheBackend  
`zeta_vn.core.ports.cache.CacheBackend`
- **clear**`(self) -> 'None'`
- **delete**`(self, key: 'str') -> 'None'`
- **exists**`(self, key: 'str') -> 'bool'`
- **get**`(self, key: 'str') -> 'Any'`
- **ping**`(self) -> 'bool'`
- **set**`(self, key: 'str', value: 'Any', ttl: 'int | None' = None) -> 'None'`

## documentation

### APIDocumenter  
`zeta_vn.core.ports.documentation.APIDocumenter`
- **export_postman**`(self) -> 'dict[str, Any]'`
- **generate_changelog**`(self, since_version: 'str | None' = None) -> 'dict[str, Any]'`
- **generate_docs**`(self, format: 'str' = 'openapi') -> 'dict[str, Any]'`
- **validate_schema**`(self, schema: 'dict[str, Any]') -> 'bool'`

## feature_toggles

### FeatureToggleProvider  
`zeta_vn.core.ports.feature_toggles.FeatureToggleProvider`
- **get_variant**`(self, feature_name: 'str', user_id: 'str | None' = None, attrs: 'Mapping[str, str] | None' = None) -> 'str | None'`
- **is_enabled**`(self, feature_name: 'str', user_id: 'str | None' = None, attrs: 'Mapping[str, str] | None' = None) -> 'bool'`
- **list_features**`(self) -> 'list[dict[str, Any]]'`
- **track_exposure**`(self, feature_name: 'str', user_id: 'str | None' = None, variant: 'str | None' = None) -> 'None'`

## memory

### MemoryServiceProtocol  
`zeta_vn.core.ports.memory.MemoryServiceProtocol`
- **delete**`(self, *, namespace: 'str', ids: 'list[str] | None' = None, flt: 'Mapping[str, Any] | None' = None, hard: 'bool' = False) -> 'dict[str, Any]'`
- **get_stats**`(self, namespace: 'str') -> 'dict[str, Any]'`
- **list_namespaces**`(self) -> 'list[str]'`
- **query**`(self, *, namespace: 'str', query: 'str', top_k: 'int' = 10, filters: 'Mapping[str, Any] | None' = None) -> 'dict[str, Any]'`
- **rebuild_embeddings**`(self, *, namespace: 'str', target_model: 'str', batch_size: 'int' = 256) -> 'dict[str, Any]'`
- **upsert**`(self, *, namespace: 'str', records: 'list[Mapping[str, Any]]', embedding_model: 'str | None' = None) -> 'dict[str, Any]'`

## metrics

### BottleneckDetector  
`zeta_vn.core.ports.metrics.BottleneckDetector`
- **analyze_trends**`(self, time_series: 'list[Mapping[str, Any]]') -> 'dict[str, Any]'`
- **detect**`(self, metrics: 'Mapping[str, Any]') -> 'list[str]'`
- **recommend_optimizations**`(self, bottlenecks: 'list[str]') -> 'list[str]'`

### MetricsCollector  
`zeta_vn.core.ports.metrics.MetricsCollector`
- **gauge**`(self, name: 'str', value: 'float', tags: 'Mapping[str, str] | None' = None) -> 'None'`
- **histogram**`(self, name: 'str', value: 'float', tags: 'Mapping[str, str] | None' = None) -> 'None'`
- **incr**`(self, name: 'str', value: 'int' = 1, tags: 'Mapping[str, str] | None' = None) -> 'None'`
- **snapshot**`(self) -> 'dict[str, Any]'`
- **timing**`(self, name: 'str', ms: 'float', tags: 'Mapping[str, str] | None' = None) -> 'None'`

## mlops

### DeploymentStrategy  
`zeta_vn.core.ports.mlops.DeploymentStrategy`
- **deploy**`(self, artifact: 'dict[str, Any]', *, strategy: 'str', params: 'dict[str, Any] | None' = None) -> 'dict[str, Any]'`
- **health**`(self, deployment_id: 'str') -> 'dict[str, Any]'`
- **rollback**`(self, deployment_id: 'str', version: 'str') -> 'dict[str, Any]'`
- **scale**`(self, deployment_id: 'str', replicas: 'int') -> 'dict[str, Any]'`

### EvalService  
`zeta_vn.core.ports.mlops.EvalService`
- **benchmark**`(self, model_ref: 'str | dict[str, Any]') -> 'dict[str, Any]'`
- **compare**`(self, models: 'list[str | dict[str, Any]]', dataset: 'str') -> 'dict[str, Any]'`
- **run**`(self, model_ref: 'str | dict[str, Any]', preset: 'str') -> 'dict[str, Any]'`

### ModelRegistry  
`zeta_vn.core.ports.mlops.ModelRegistry`
- **archive**`(self, model_id: 'str') -> 'None'`
- **latest**`(self, family: 'str', stage: 'str' = 'production') -> 'dict[str, Any]'`
- **list_models**`(self, family: 'str | None' = None) -> 'list[dict[str, Any]]'`
- **promote**`(self, model_id: 'str', stage: 'str') -> 'None'`
- **register**`(self, artifact: 'dict[str, Any]') -> 'dict[str, Any]'`

## observability

### DistributedTracer  
`zeta_vn.core.ports.observability.DistributedTracer`
- **set_status_error**`(self, message: 'str') -> 'None'`
- **set_status_ok**`(self) -> 'None'`
- **span**`(self, name: 'str', attributes: 'Mapping[str, Any] | None' = None) -> 'AbstractContextManager[None]'`

### Metrics  
`zeta_vn.core.ports.observability.Metrics`
- **gauge**`(self, name: 'str', value: 'float', tags: 'Mapping[str, str] | None' = None) -> 'None'`
- **incr**`(self, name: 'str', value: 'int' = 1, tags: 'Mapping[str, str] | None' = None) -> 'None'`
- **timing_ms**`(self, name: 'str', ms: 'float', tags: 'Mapping[str, str] | None' = None) -> 'None'`

## security

### BehaviorAnalyticsEngine  
`zeta_vn.core.ports.security.BehaviorAnalyticsEngine`
- **anomalies**`(self, recent_events: 'list[Mapping[str, Any]]') -> 'list[Mapping[str, Any]]'`
- **get_patterns**`(self, user_id: 'str | None' = None) -> 'dict[str, Any]'`
- **score_event**`(self, event: 'Mapping[str, Any]') -> 'float'`
- **train_baseline**`(self, historical_events: 'Sequence[Mapping[str, Any]]') -> 'None'`

### SecurityEventFeed  
`zeta_vn.core.ports.security.SecurityEventFeed`
- **get_events_by_source**`(self, source_ip: 'str', hours: 'int' = 1) -> 'list[dict[str, Any]]'`
- **get_events_by_user**`(self, user_id: 'str', hours: 'int' = 24) -> 'list[dict[str, Any]]'`
- **recent**`(self, window_sec: 'int' = 300) -> 'list[dict[str, Any]]'`
- **submit_event**`(self, event: 'dict[str, Any]') -> 'None'`

### ThreatIntelDatabase  
`zeta_vn.core.ports.security.ThreatIntelDatabase`
- **add_indicator**`(self, indicator_type: 'str', value: 'str', confidence: 'float', metadata: 'dict[str, Any] | None' = None) -> 'None'`
- **get_recent_threats**`(self, hours: 'int' = 24) -> 'list[dict[str, Any]]'`
- **lookup_indicators**`(self, values: 'Sequence[str]') -> 'list[dict[str, Any]]'`
- **reputation**`(self, indicator: 'str') -> 'float'`

## testing

### QualityReporter  
`zeta_vn.core.ports.testing.QualityReporter`
- **generate_coverage**`(self) -> 'dict[str, Any]'`
- **report**`(self, results: 'list[dict[str, Any]]') -> 'dict[str, Any]'`

### TestCaseGenerator  
`zeta_vn.core.ports.testing.TestCaseGenerator`
- **generate**`(self, scenario: 'str | None' = None) -> 'list[dict[str, Any]]'`
- **generate_edge_cases**`(self) -> 'list[dict[str, Any]]'`

### TestRunner  
`zeta_vn.core.ports.testing.TestRunner`
- **run**`(self, cases: 'list[dict[str, Any]]') -> 'list[dict[str, Any]]'`
- **run_parallel**`(self, cases: 'list[dict[str, Any]]', workers: 'int' = 4) -> 'list[dict[str, Any]]'`

## uncategorized

### AIAlertSystem  
`zeta_vn.core.ports.advanced_alerts.AIAlertSystem`
- **get_insights**`(self, timeframe: 'str' = '24h') -> 'dict[str, Any]'`
- **notify**`(self, severity: 'str', title: 'str', message: 'str', meta: 'Mapping[str, Any] | None' = None) -> 'None'`
- **predict_anomalies**`(self, metrics: 'Mapping[str, Any]') -> 'list[Mapping[str, Any]]'`
- **train_model**`(self, historical_data: 'list[Mapping[str, Any]]') -> 'None'`
