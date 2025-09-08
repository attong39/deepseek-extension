# Auto-Fix Report
Generated: 2025-09-09T06:36:09.176420

## Summary
- **Python**: imports_added=3279, reqs_added=6288
- **TypeScript**: imports_added=363, deps_added=2669
- **Unresolved**: 0

## Python Imports Added
```
E:\zeta-monorepo\ai_auto_optimizer.py: Exception, SyntaxError, all, bool, child, description, dict, e, f, file_path, float, func, int, isinstance, len, line, list, node, open, passed, pattern, print, project_root, r, replacement, self, sorted, str, sum, v, validation, x
E:\zeta-monorepo\ai_auto_refactor.py: Exception, ImportError, bool, call_next, client, conn, dict, e, exc, getattr, hasattr, import_path, int, list, locals, payload, prefix, r, request, router_attr, str, tags, ve
E:\zeta-monorepo\ai_optimize_project.py: Exception, description, dict, e, f, isinstance, list, open, print, project_root, self, step_name, step_results, str, sum
E:\zeta-monorepo\ai_project_scanner.py: Exception, OSError, SyntaxError, alias, any, child, chr, d, dict, dirs, e, enumerate, f, fa, filename, filenames, float, i, imp, int, isinstance, item, len, line, list, max, message, min, node, open, pattern, print, project_root, root, self, sorted, str, sum, tuple, x
E:\zeta-monorepo\api_endpoint_discovery.py: Exception, e, endpoint, f, len, matches, open, print, provider
E:\zeta-monorepo\api_status.py: print
E:\zeta-monorepo\check_ollama_vscode.py: Exception, FileNotFoundError, ImportError, e, f, len, model, open, print
E:\zeta-monorepo\cicd_generator.py: Exception, dict, f, filename, open, print, project_root, py_file, req_file, self, str, test_dir
E:\zeta-monorepo\cleanup_redundant_files.py: Exception, OSError, PermissionError, any, bool, cache_dir, category, e, file_path, input, int, len, path, pattern, patterns, print, protected, root_path, self, sorted, str, x
E:\zeta-monorepo\configure_turbo_ollama.py: Exception, FileNotFoundError, ImportError, KeyboardInterrupt, e, f, input, key, len, line, model, open, package, print, value
E:\zeta-monorepo\consolidate_monorepo.py: Exception, OSError, ValueError, action, bool, bytes_, copied_bytes, copied_files, d, dict, dir_path, dirs, dst, dst_bytes, dst_files, e, exclude_set, f, filenames, files, fname, input, int, item, list, note, open, package_json, path, print, root, script_dir, self, set, sorted, src, src_bytes, src_files, str, tsconfig, tuple
E:\zeta-monorepo\directory_structure.py: FileNotFoundError, PermissionError, dir_name, enumerate, file_name, i, indent, item, len, print
E:\zeta-monorepo\e2e_smoke_test.py: Exception, all, base_url, bool, comp, e, exit, field, float, isinstance, key, len, list, metric, print, r, result, self, str, sum, value, websocket
E:\zeta-monorepo\finalize_ollama_setup.py: f, open, print
E:\zeta-monorepo\find_turbo_endpoint.py: Exception, e, endpoint, f, key, open, print, str, test_url, value
E:\zeta-monorepo\fix_continue.py: Exception, e, f, false, len, model, model_name, open, print
E:\zeta-monorepo\fix_imports.py: Exception, bool, e, f, file_path, open, print, py_file, str
E:\zeta-monorepo\fix_imports_exports.py: Exception, SyntaxError, UnicodeDecodeError, alias, any, bool, e, f, file_path, imp, import_path, isinstance, len, list, node, open, p, path, pattern, print, project_root, replacement, self, set, skip, str, tuple
E:\zeta-monorepo\fix_syntax_errors.py: Exception, SyntaxError, UnicodeDecodeError, any, bool, directory, e, enumerate, error_msg, f, file_path, filename, filenames, has_error, i, j, k, len, list, min, open, print, range, root, skip, str, tuple
E:\zeta-monorepo\integration_mapper.py: Exception, alias, any, cmd, command, config_file, count, d, dep, description, dict, dirs, e, enumerate, exclude, f, file, file_path, files, filter, i, imp, integration, isinstance, issue, len, line, list, match, next, node, open, output_file, path, pkg, print, project_root, rec, req, script, self, sorted, step, str, ts_file, version
E:\zeta-monorepo\master_optimizer.py: Exception, bool, dict, e, enumerate, executor, f, finding, float, future, i, int, issue, len, list, open, print, project_root, r, range, rec, self, str, sum, tool_name, tools, tuple
E:\zeta-monorepo\network_diagnostics.py: Exception, FileNotFoundError, all, any, bool, dict, domain, e, endpoint, ep, len, m, model, name, print, self, str, success, url
E:\zeta-monorepo\ollama_online_auth.py: Exception, KeyboardInterrupt, e, f, len, m, model, open, print, self
E:\zeta-monorepo\ollama_smart_setup.py: Exception, e, endpoint, f, health_path, open, path, print, status, str
E:\zeta-monorepo\performance_profiler.py: Exception, SyntaxError, bool, child, dict, e, enumerate, f, float, i, int, isinstance, len, line_num, list, max, module, node, obj, open, parent, pattern, peak, print, project_root, rec, script, self, stat, str, tool
E:\zeta-monorepo\prometheus_dashboard_config.py: f, open, output_dir, print, str
E:\zeta-monorepo\security_auditor.py: Exception, bandit_result, bool, config_file, description, dict, e, enumerate, f, i, int, len, line, line_num, list, open, pattern, print, project_root, rec, replacement, result_item, self, str, tool, vuln
E:\zeta-monorepo\setup_turbo_ollama.py: Exception, FileNotFoundError, e, f, input, len, line, model, open, print, self, title, var_value
E:\zeta-monorepo\setup_vscode_continue.py: Exception, all, bool, check, e, f, int, name, open, path, print, status, str
E:\zeta-monorepo\switch_numpy.py: bool, cmd, cwd, e, len, list, print, str
E:\zeta-monorepo\test_numpy_switch.py: cmd, cwd, e, len, list, print, str
E:\zeta-monorepo\test_turbo_upgrade.py: Exception, all, any, cmd, cwd, dict, e, f, len, open, print, r, self, str, target
E:\zeta-monorepo\turbo_api_online_auth.py: Exception, ImportError, bool, current_user, dict, e, getattr, i, int, isinstance, iter, len, list, orchestrator, range, request, request_id, result, self, str, token
E:\zeta-monorepo\.cleanup_backup\redundant_1757367219\backup_dirs\consolidation_trash\20250908_182850\apps\backend\app\middleware\api_version.backup_20250829_072431.py: API_VERSION, call_next, request, str
E:\zeta-monorepo\.cleanup_backup\redundant_1757367219\backup_dirs\consolidation_trash\20250908_182850\apps\backend\app\middleware\logging.backup_20250829_072431.py: call_next, request, str
E:\zeta-monorepo\.cleanup_backup\redundant_1757367219\backup_dirs\consolidation_trash\20250908_182850\apps\backend\app\middleware\metrics_middleware.backup_20250829_072431.py: Exception, app, call_next, hasattr, metrics_collector, request, self, str, super
E:\zeta-monorepo\.cleanup_backup\redundant_1757367219\backup_dirs\consolidation_trash\20250908_182850\apps\backend\app\middleware\request_id.backup_20250829_072431.py: call_next, request, str
E:\zeta-monorepo\.dup_backup\20250909_042457\ai_auto_optimizer.py: Exception, SyntaxError, all, bool, child, description, dict, e, f, file_path, float, func, int, isinstance, len, line, list, node, open, passed, pattern, print, project_root, r, replacement, self, sorted, str, sum, v, validation, x
E:\zeta-monorepo\.dup_backup\20250909_042457\ai_auto_refactor.py: Exception, ImportError, code, dict, e, enumerate, f, file, func, func_info, function_info, i, len, list, open, print, r, self, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\ai_project_scanner.py: Exception, OSError, SyntaxError, alias, any, child, chr, d, dict, dirs, e, enumerate, f, fa, filename, filenames, float, i, imp, int, isinstance, item, len, line, list, max, message, min, node, open, pattern, print, project_root, root, self, sorted, str, sum, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\final_project_demo.py: Exception, capability, chr, config_file, dict, e, f, file, json_file, len, list, metric, open, print, self, step, str, text, value
E:\zeta-monorepo\.dup_backup\20250909_042457\gen_project_map.py: Exception, PermissionError, argv, bool, c, d, depth, dict, dir_counts, e, enumerate, ext, exts, hints, idx, int, k, lang_counts, len, level, list, max, max_items, n, pat, path, prefix, print, set, sorted, str, sum, tree_lines, tuple, uniq, v, x
E:\zeta-monorepo\.dup_backup\20250909_042457\metrics_server.py: Exception, client, dict, e, int, print, request, str
E:\zeta-monorepo\.dup_backup\20250909_042457\ollama_benchmark.py: Exception, base_url, exc, float, i, int, len, list, max, min, model, print, prompt, range, str, timeout, times
E:\zeta-monorepo\.dup_backup\20250909_042457\production_deploy.py: Exception, component, directory, e, f, file, open, print, self, status, step
E:\zeta-monorepo\.dup_backup\20250909_042457\quick_duplicate_checker.py: IOError, OSError, enumerate, f, file_path, files, h, i, len, list, open, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\quick_start_turbo.py: Exception, ImportError, client, e, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\safe_backup_cleanup.py: OSError, any, dir_name, dirs, e, file_path, input, len, list, log, open, print, root
E:\zeta-monorepo\.dup_backup\20250909_042457\setup_dev.py: Exception, bool, command, config, cwd, description, e, name, print, req_file, step_func, step_name, str, title, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\setup_one_click_learning.py: Exception, FileNotFoundError, bool, command, dep, description, e, ignore_errors, print, self, str, tool
E:\zeta-monorepo\.dup_backup\20250909_042457\setup_vscode_ollama.py: Exception, FileNotFoundError, KeyboardInterrupt, e, ext, f, line, open, print
E:\zeta-monorepo\.dup_backup\20250909_042457\setup_vscode_turbo_api.py: Exception, e, f, open, print
E:\zeta-monorepo\.dup_backup\20250909_042457\simple_turbo_setup.py: Exception, e, f, len, model, open, print, round
E:\zeta-monorepo\.dup_backup\20250909_042457\smart_refactorer.py: Exception, SyntaxError, any, block, bool, child, cond_num, count, dict, e, enumerate, f, file_path, func, hasattr, i, if_node, int, isinstance, len, list, node, open, original_name, part_num, print, project_root, range, refactoring_type, self, sorted, stmt, str, template, tuple, type, x
E:\zeta-monorepo\.dup_backup\20250909_042457\turbo_api_online_auth.py: Exception, KeyboardInterrupt, e, f, len, m, open, print, self
E:\zeta-monorepo\.dup_backup\20250909_042457\turbo_demo.py: Exception, ImportError, abs, all, dict, e, f, k, len, min, model, open, part, print, r, self, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\turbo_ollama_client.py: Exception, ValueError, attempt, bool, cache_entry, chunk, client, code_prompt, dict, e, float, hash, int, language, model, print, range, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\turbo_ollama_login.py: Exception, bool, dict, f, input, len, m, new_mode, open, print, self, str, url
E:\zeta-monorepo\.dup_backup\20250909_042457\turbo_setup.py: Exception, FileNotFoundError, dict, e, f, input, key, len, model, open, print, prompt, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\verify_ai_setup.py: Exception, available_models, e, error, f, len, line, model, ollama_running, open, output, print, success, test_prompt, var
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\test_ollama_client.py: Exception, ImportError, e, print
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\di_container.py: Exception, ImportError, RuntimeError, ValueError, agent, agent_data, agent_id, agent_repository, bool, call_next, cfg_exc, cleanup_func, config, data, database_service, db_session, dep_name, dict, e, email, exc, factory, gemini_service, getattr, hasattr, int, isinstance, key, list, memory_repository, name, owner_id, param_name, repository, request, self, service, service_name, session, status, str, svc_name, telemetry_service, type, user, user_id, user_repository, value
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\main.py: Exception, ImportError, bool, call_next, client, conn, dict, e, exc, getattr, hasattr, import_path, int, list, locals, payload, prefix, r, request, router_attr, str, tags, ve
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\test_blueprint.py: len, print
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\admin.py: Exception, active, audit, bool, cursor, dict, f, getattr, hasattr, int, isinstance, key, limit, list, me, next_cursor, object, payload, q, r, role, str, svc, target_user_id, tuple, u, user, user_id
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\agents.py: Exception, agent, agent_id, cap, dict, e, getattr, int, len, limit, list, offset, payload, q, req, step_dict, step_dicts, str, svc, updated_agent
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\assistant.py: Exception, bool, claims, dict, e, float, inp, len, list, request, resp, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\auth.py: Exception, ValueError, auth, dict, e, getattr, list, payload, str, tokens, user
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\autonomy.py: Exception, bool, completed_session, dict, e, event, event_streamer, float, goal_repo, hasattr, int, learning_pipeline, len, list, perception, planner, request, result, safety_policy, session, session_id, session_repo, skill_name, skill_registry, status, str, user_id, websocket
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\demo_di.py: Exception, agent, agent_data, agent_id, agent_repository, agent_service, container, dict, dir, e, hasattr, len, list, method, pagination, service_health, session, str, type, user, user_id, user_repository, user_service
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\files.py: Exception, TypeError, bytes, callable, chunk_size, dict, e, file, file_id, hasattr, headers, int, isinstance, request, s, status_code, str, svc, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\health.py: dict, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\learning.py: bool, dict, e, getattr, int, it, job_id, len, list, max, ok, page, page_items, page_size, payload, response, status_filter, str, svc, total, u
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\memory.py: Exception, dict, e, file, float, getattr, int, isinstance, len, list, memory_id, object, payload, q, r, request, request_id, str, svc, top_k, typed_results
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\planning.py: dict, list, payload, plan_id, str, svc
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\reflexion.py: dict, int, list, payload, result, str, svc
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\system.py: bool, dict, str, svc
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\voice.py: audio, float, payload, result, str, svc
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\_common_audit.py: actor, dict, event, payload, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\_common_cache.py: Exception, args, dict, float, fn, int, kwargs, ns, parts, str, ttl, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\_common_idempotency.py: Exception, idempotency_key, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\_common_rate_limit.py: Exception, int, limit, request, window
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\_common_security.py: Exception, allowed, any, creds, e, list, r, str, user
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\auth\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, module, name, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\endpoints\plans_example.py: Exception, ImportError, NotImplementedError, bool, dict, exc, getattr, hasattr, int, limit, offset, payload, plan_id, result, service, status_eq, str, user
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v1\_common\security.py: bool, creds, e, list, roles, set, str, token
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\advanced_memory.py: Exception, bool, cache, current_user, dict, e, float, getattr, int, list, memory_id, payload, query, request, result, str, svc
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\advanced_memory_optimized.py: background_tasks, bool, content, dict, enumerate, float, i, int, k, key, len, level, list, memory, memory_data, min, query, range, request, self, sorted, staticmethod, str, sum, target_layer, user, v, x
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\federated_learning.py: Exception, bool, client_data, config, deploy_data, dict, e, float, int, list, round_data, round_id, str, svc, update_data
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\federated_learning_optimized.py: ValueError, abs, active_rounds, bits, bool, budget, client_id, client_ids, client_updates, clip_norm, config, cost, delta, dict, dist, enumerate, epsilon, float, i, int, j, k_ratio, len, list, max, method, min, privacy_budgets, property, result, s, samples, self, sensitivity, staticmethod, str, sum, threshold, trim_ratio, tuple, u, update_i, update_j, user, w, weight_max, weight_min, zip
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\multi_agent.py: Exception, aggregation, assignment, bool, capability, dict, e, execution, execution_id, float, int, list, payload, str, svc, workflow_id
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\multi_agent_optimized.py: Exception, TimeoutError, agent, agent_type, agents, all, best_agent, bool, dep_id, dict, e, float, from_agent, int, len, list, max, property, registration, self, set, staticmethod, str, sub_id, subtask, subtask_id, sum, task_request, task_type, tasks, user, websocket, x
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\real_time_collab.py: Exception, bool, config_data, dict, e, float, int, invite_data, list, message_data, presence_data, session_data, session_id, str, svc, sync_data
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\api\v2\security_ai_optimized.py: Exception, ValueError, a, action, active_alerts, alert_id, any, attempts, background_tasks, bool, dict, domain, e, event_data, events, f, float, ind, ind_data, int, intel_update, ip_address, len, limit, list, match, max, min, progress, scan_request, scan_result, scan_results, security_events, self, set, staticmethod, status, str, threat_level, tuple, update_request, user, v, window_minutes, x
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\auth\__init__.py: AttributeError, Exception, ImportError, RuntimeError, bool, dict, e, globals, module_name, name, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\common\__init__.py: AttributeError, Exception, ImportError, RuntimeError, bool, dict, e, globals, module_name, name, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\containers\__init__.py: AttributeError, Exception, ImportError, RuntimeError, bool, dict, e, globals, module_name, name, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\middleware\observability.py: Exception, call_next, e, getattr, request, round, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\services\assistant_svc.py: Exception, bool, context, dict, e, float, force_teacher, inp, input_text, inputs, list, local_result, meta, output_text, rules, str, team_id, user_id, user_input
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\services\collab_service.py: ValueError, actor_id, bool, change, changes, content_data, description, dict, id, int, is_online, len, limit, list, m, name, new_role, owner_id, role, s, self, settings, str, uid, user_id
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\services\dataset_svc.py: dict, f, file_path, i, id, input_text, int, len, limit, list, meta, min_samples, output_text, range, rules, s, self, str, sum, team_id, user_id
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\services\federated_service.py: ValueError, aggregation_strategy, artifact_ref, base_model_hash, capabilities, client_id, config, dict, float, id, int, key, len, list, m, metrics, min_participants, model, parent_version, participants, payload_ref, self, set, sha256, str, sum, timeout_duration, user_id, version
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\services\local_model_svc.py: Exception, dict, e, float, input_text, len, max, output_text, rules, score_tensor, str, text
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\app\services\teacher_client.py: Exception, attempt, client, context, dict, e, error, float, int, len, range, rules, str, user_text
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\config\advanced_settings.py: bool, dir_path, float, int, isinstance, list, property, self, str, v, x
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\config\external_services.py: Exception, ValueError, all, bool, classmethod, dict, e, float, int, list, provider, self, service, service_name, str, v
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\domain\autonomy.py: Exception, action_name, bool, dict, float, int, len, list, notes, property, result, self, step, str, success, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\interfaces\autonomy.py: Exception, dict, int, list, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\security\authentication\factory_fixed.py: ImportError, ValueError, backend, body, bool, enable_metrics, enable_tracing, print, redis_kwargs, redis_url, storage_backend, str, subject, to, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\security\authentication\quick_validation.py: Exception, ImportError, e, len, line, print, repr, span, type
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\security\authentication\simple_validation.py: Exception, FileNotFoundError, e, file, hasattr, len, print
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\security\authentication\test_enhanced_system.py: ImportError, attempt, category, count, device_trust, email_manager, enabled, enumerate, event, feature, hasattr, i, issue, len, line, metrics, mfa_manager, print, range, sms_manager, span, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\services\asr_service.py: asr, audio_path, dict, lang, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\services\autonomy_planner.py: Exception, ImportError, any, best_pattern, bool, context, description, dict, e, fallback_planner, fb, feedback, float, goal, keyword, len, list, llm_planner, min, mode, observation, pattern, rag_service, result, rule_planner, self, set, similar_plan, skill_name, str, word, x
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\services\autonomy_safety.py: action, blocked_cmd, blocked_path, blocked_pattern, context, dict, goal, int, isinstance, keyword, len, limit, list, p, param_key, param_value, pii_pattern, self, str, text, user_context, v
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\services\autonomy_skills.py: Exception, action, context, dict, e, hash, i, int, isinstance, len, list, max_file_size, metadata, min, name, range, result, self, str, type
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\services\ai\rag\optimized.py: dict, list, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\core\use_cases\autonomy.py: Exception, ValueError, a, action, action_results, bool, budget_seconds, dict, e, enumerate, event_streamer, goal_description, goal_repo, i, include_perception, int, learning_pipeline, len, list, perception, planner, result, s, safety_policy, self, session, session_id, session_repo, skill_registry, str, sum, user_id
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\adapters\asr_whisper.py: audio_path, lang, model_size, s, segments, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\implementations\advanced_targeting.py: ImportError, RuntimeError, ValueError, canny_high, canny_low, contours, float, hsv_ranges, int, len, list, lower, m, max, max_loc, max_val, min_line_length, result, self, str, template_path, threshold, tuple, upper, x, y, zip
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\implementations\input_control_fast.py: Exception, ValueError, bool, bufs, button, delta, dx, dy, inputs, int, len, list, max, range, repeat, reversed, self, str, tuple, vh, vk, vks, vw, vx, vy
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\implementations\screen_capture_dxgi.py: Exception, RuntimeError, bottom, h, int, left, monitor, region, right, self, target_fps, top, tuple, w
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\implementations\screen_control_manager.py: color_bgr, float, int, self, tuple, x, y
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\implementations\screen_targeting.py: bgr, frame, int, self, tol, tuple, xs, ys
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\implementations\windows_keycodes.py: int, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\instrumentation\latency_timer.py: Exception, float, getattr, property, round, self, str, type
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\data\instrumentation\performance_benchmark.py: dict, filename, float, func, input_control, int, iterations, len, list, manager, max, min, name, print, range, result, screen_capture, self, str, t, times
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\tests\integration\test_di_integration.py: Exception, ImportError, KeyError, RuntimeError, ValueError, client, collector, dict, e, exc_info, hasattr, isinstance, list, mock_session, name, request, scope, scope1, scope2, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\tests\integration\test_di_simple.py: RuntimeError, ValueError, dict, exc_info, isinstance, name, scope1, scope2, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\backend\trainer\demo_ai_learning.py: print, task
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\dev_server.py: Exception, ImportError, ai_request, call_next, conn, count, dict, e, exc, feedback, float, int, len, list, maxsize, metric, model, print, prompt, request, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\fix_errors.py: f, open, print
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\metrics_server.py: Exception, METRICS, count, d, dict, durations, durations_by_model, e, entry, feedback, float, int, isinstance, len, list, round, row, score, stats, status, str, sum, value
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\metrics_server_optimized.py: Exception, all, bool, call_next, check_func, conn, count, dict, e, exc, feedback, float, int, len, list, m, maxsize, metric, name, older_than, request, self, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\optimize.py: Exception, KeyboardInterrupt, bool, description, e, f, len, name, open, print, step_func, step_name, str, title
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\performance_test.py: print, round, self
E:\zeta-monorepo\.dup_backup\20250909_042457\apps\zeta-ai-agent\config\settings.py: ValueError, bool, classmethod, cls, dict, float, int, isinstance, kwargs, list, origin, print, property, self, str, super, v
E:\zeta-monorepo\.dup_backup\20250909_042457\docs\examples\python-assistant\assistant.py: Exception, KeyboardInterrupt, ValueError, any, body, bool, cfg, chat_history, dict, exc, getattr, input, int, language, len, list, m, max_tokens, mode, payload, print, self, staticmethod, str
E:\zeta-monorepo\.dup_backup\20250909_042457\docs\examples\python-assistant\benchmark.py: Exception, base_url, exc, float, i, int, len, list, max, min, model, print, prompt, range, str, timeout, times
E:\zeta-monorepo\.dup_backup\20250909_042457\docs\examples\python-assistant\examples_turbo_usage.py: bool, list, print, q, queries, str
E:\zeta-monorepo\.dup_backup\20250909_042457\docs\examples\python-assistant\turbo_api_client.py: api_key, base_url, dict, endpoint, exc, int, language, message, model, print, prompt, self, str, timeout
E:\zeta-monorepo\.dup_backup\20250909_042457\docs\examples\python-assistant\turbo_cli.py: print
E:\zeta-monorepo\.dup_backup\20250909_042457\docs\examples\python-assistant\turbo_ollama_integration.py: Exception, bool, data, dict, exc, print, prompt, self, str, use_turbo
E:\zeta-monorepo\.dup_backup\20250909_042457\examples\turbo_ollama_usage_examples.py: Exception, KeyboardInterrupt, chunk, client, e, enumerate, example, i, len, print, q, question, size, zip
E:\zeta-monorepo\.dup_backup\20250909_042457\production\scripts\health_check.py: Exception, all, e, f, open, print, service, status, str, url
E:\zeta-monorepo\.dup_backup\20250909_042457\production\src\final_project_demo.py: Exception, capability, chr, config_file, dict, e, f, file, json_file, len, list, metric, open, print, self, step, str, text, value
E:\zeta-monorepo\.dup_backup\20250909_042457\production\src\turbo_demo.py: Exception, ImportError, abs, all, dict, e, f, k, len, min, model, open, part, print, r, self, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\apply_consolidation_plan.py: Exception, SystemExit, ValueError, actions, bool, canonical_file, create_py, create_ts, dict, dry, e, ext, file_path, from_file, int, isinstance, item, len, list, p, path, print, r, redundant, src, str, to_file
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\benchmark_latency.py: Exception, any, avail, bool, char, dict, e, enumerate, f, filename, float, i, int, keyword, len, list, max, min, model, num_tests, ollama_url, open, print, prompt, self, sorted, str, sum, timeout, x
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\cleanup_reports.py: Exception, SystemExit, child, d, deletions, e, int, list, out, print, r, s, str
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\consolidation_audit.py: Exception, alias, argv, base_file, bool, chunk, content, current_file, d, data, dict, dirnames, dirpath, e, enable_near, exact_cnt, f, filenames, fn, fp, getattr, idx, int, is_local, isinstance, issues, it, k, len, list, name, near_cnt, node, packages, print, range, s, self, set, sorted, spec, str, title, total_files, tuple, v
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\consolidation_plan_builder.py: Exception, SystemExit, any, data, dict, enumerate, exact_dup, f, fh, files, glist, groups, h, i, int, item, lang, len, lines, list, near_dup, object, path, paths, print, r, seg, sorted, str, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\dedupe_scan.py: Exception, argv, bool, by_hash, by_name, by_norm, bytes, d, data, dict, dirnames, dirpath, dup_hash_groups, e, enc, f, fi, filenames, files, fn, g, int, len, lines, list, max_norm_size, n, name, name_dups, ng, norm_dups, occ, print, set, sorted, str, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\lo_finetune.py: Exception, e, examples, f, float, getattr, int, len, line, max, min, open, p, range, self, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\prepare_vn_dataset.py: Exception, any, bool, char, complexity, count, dict, e, enumerate, f, file_path, func_info, hasattr, instruction, isinstance, len, list, node, open, output_path, pattern, print, py_file, self, str, template, text, variation, x
E:\zeta-monorepo\.dup_backup\20250909_042457\scripts\update_references.py: Exception, SystemExit, ValueError, changes, d, dict, dirnames, dirpath, dst_mod, e, exact_groups, ext, file_path, filenames, fn, fp, from_file, int, isinstance, item, len, list, m, n, n1, n2, pat, path, print, py_map, r, rep, set, sorted, src_mod, str, to_file, ts_map, tuple, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tests\run_ai_codemod_tests.py: bool, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tests\run_ai_intelligence_tests.py: bool, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tests\ai-codemod\unit\test_ci_reporter.py: RuntimeError, comment, dict, object, range, results, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tests\ai-project-intelligence\test_consistency_guard.py: any, dependencies, dict, entity_id, entity_type, i, item, len, list, name, object, path, r, set, str, test_data, tmp_path
E:\zeta-monorepo\.dup_backup\20250909_042457\tests\ai-project-intelligence\test_knowledge_graph_serialization.py: isinstance, list, name, path, set, sorted, str, tmp_path
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\cleanup_duplicates.py: Exception, NotImplementedError, a, actions, alias_shim, all, any, b, bool, bytes, e, enumerate, f, g, i, int, isinstance, k, l, len, list, p, path, print, report_path, self, shim_paths, shim_pytest, sorted, sp, src, str, tag, target, target_ts
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\find_duplicate_files.py: Exception, OSError, algo, argv, bool, by_full, by_head, by_size, chunk_size, d, dict, dirnames, dirpath, e, enumerate, ex, excludes, f, filenames, float, fn, follow_symlinks, fut, g, groups, head_bytes, i, include_hidden, int, len, list, lst, max, max_size, min, min_size, nbytes, num, p, path, paths, print, set, sorted, str, sum, tuple, unit, workers
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\reference_updater.py: Exception, any, apply, bool, data, dict, e, fc, int, len, list, n, p, part, pat, path, pattern, print, repl, report, set, str, strict, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\run_ai_optimization.py: SystemExit, bool, check, cmd, cwd, int, list, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-codemod\ci_reporter.py: dict, finding, findings, len, lines, list, object, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-codemod\engine.py: Exception, FileNotFoundError, action_type, alias, any, arg, bool, by_file, config_path, default_config, dict, dry_run, e, excluded, f, ff, file_findings, file_path, finding, getattr, isinstance, len, list, mapping, n, next, node, object, open, path, print, r, result_payload, results, root_dir, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-analyzer\analyzer.py: Exception, ValueError, any, bool, cfg_path, dep, dep_graph_json, dependency, deps, dict, e, exports, ext, file_path, files, getattr, isinstance, k, len, list, m, metadata, name, node, path, pattern, print, root_path, self, set, sorted, source_file, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-analyzer\duplicates.py: Exception, ValueError, any, bool, cfg_path, clusters, config, dict, f, file_path, getattr, hash, int, isinstance, k, len, list, ln, m, max, n, node, occ, p, path, print, results, root, set, str, sum, tuple, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-analyzer\per_file_optimizer.py: any, bool, dict, dry_run, f, files, findings, int, len, list, object, p, print, root, seg, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-analyzer\project-graph.py: deps, dict, k, lines, list, out_path, print, src, str, targets, tgt, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-analyzer\smart-optimizer.py: Exception, all, analysis_results, bool, dict, enriched, enumerate, f, file_path, idx, int, k, len, list, meta, model, part, path, print, r, self, str, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-analyzer\vs-code-helper.py: AnalyzerCls, Exception, ImportError, OSError, ValueError, data, dict, e, exc, isinstance, k, list, load_config_fn, obj, path, r, set, sorted, str, tasks, tuple, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\auto-coder.py: dict, issue, knowledge_graph, print, project_root, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\auto_fixer.py: Exception, alias, applied, bool, dict, int, isinstance, issue, issues, list, n, node, p, project_root, self, set, stmt, str, updated_node
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\brain.py: Exception, ImportError, any, dict, e, file_path, files, len, list, path, print, project_root, seg, self, set, str, sum, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\consistency-guard.py: dep_id, deps, dict, inconsistencies, int, k, knowledge_graph, len, list, print, relationships, root, self, set, sorted, source_id, str, tuple, v, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\knowledge-graph.py: data, dict, entities_serialized, entity, int, k, list, relationships_serialized, self, set, sorted, source_id, storage_path, str, target_id, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\reporter.py: counts, dict, i, int, issue, issues, k, key, len, lines, list, output_path, project_root, self, str, tuple, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\ai-project-intelligence\setup.py: dep, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\add_test_type_annotations.py: Exception, bool, e, file_path, len, list, pattern, print, replacement, test_file
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\aggressive_optimization.py: dupe, mgr, print, repo
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\analyze_duplicate_name_similarity.py: Exception, SystemExit, dict, flagged, groups, i, int, item, j, len, line, list, name, object, p, paths, print, range, round, sims, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\analyze_f821.py: count, dict, enumerate, error, file_errors, files_errors, i, int, len, list, print, sorted, str, sum, undefined_names, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\analyze_init_patterns.py: Exception, any, class_name, e, f, file_rel_path, init_node, isinstance, item, len, list, node, open, print, rel_path, self, stmt, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\analyze_middleware.py: enumerate, i, len, print, r, row, sum, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\api_auto_fixer.py: Exception, any, code, dict, exc_dir, k, len, message, original_content, p, print, py_file, self, set, sorted, str, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\api_consistency_optimizer.py: Exception, dict, exc_dir, file_name, i, issue, len, list, print, py_file, r, rec, self, set, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\apply_base_classes.py: Exception, e, f, file_rel_path, open, print, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\apply_refactor_plan.py: Exception, ValueError, act, action, actions, any, argv, bool, c, ch, cmd, cwd, d, dict, dry, e, fh, int, isinstance, len, list, m, merge, mv, p, pat, path, print, raw, results, rewrite_rules, rewritten, rule, rules, s, set, sorted, str, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\autobarrel_python.py: d, dir_path, f, item, len, list, m, print, s, sorted, str, t
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\auto_fix_regression_guard.py: Exception, SystemExit, any, bool, cmd, dict, e, f, filepath, files_checked, float, i, int, isinstance, len, list, n, new, node, old, print, round, s0, s1, str, sum, text
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\backup_database.py: Exception, FileNotFoundError, OSError, backup, backup_dir, backup_file, bool, database_url, drop_existing, e, hasattr, int, keep_count, len, list, print, self, str, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\backup_inits.py: d, init_file, len, print, sorted, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\batch_fix_errors.py: Exception, OSError, UnicodeDecodeError, bool, dict, dir_name, e, enumerate, file_path, i, int, len, line, pattern, phase, print, py_file, replacement, root_path, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\benchmark_desktop_control.py: Exception, e, print, r, result, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\benchmark_fast_control.py: Exception, KeyboardInterrupt, cap, e, f, float, frame, int, iterations, len, list, max, method_func, method_name, min, operation, operation_name, print, range, self, str, target_name, target_value, tol, warmup
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check.py: Exception, all, bool, cmd, description, e, file_path, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_backend_duplicates_ci.py: int, p, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_conformance.py: AttributeError, Exception, ImportError, NameError, SystemExit, TypeError, ValueError, count, dict, e, func, impl_cls, int, issue, issues, len, list, method, method_name, name, p, print, problem, protocol_cls, protocol_method, set, sorted, str, sum, tuple, type, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_duplicates.py: Exception, FileNotFoundError, SystemExit, any, argv, bool, c, combined_logs, cwd, err, err2, exc, f, fail_if_above, float, int, lf, list, map, min_lines, min_tokens, mode, name, next, open, out, p, path, pout, print, script_path, sorted, str, summary, t, text, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_env_sync.py: SystemExit, e, errors, lines, list, ln, out, print, set, sorted, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_external_dependencies.py: Exception, ImportError, alias, dir_name, e, enumerate, f, file_path, i, import_name, isinstance, len, list, missing, node, open, package, pkg, print, py_file, req, self, set, sorted, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_missing_dependencies.py: Exception, ImportError, alias, e, enumerate, f, i, import_name, isinstance, len, list, node, open, print, req, req_file, self, set, sorted, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_quality.py: Exception, bool, cmd, description, e, len, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\check_related_files.py: Exception, SystemExit, any, argv, bool, candidate, dict, e, f, files, int, k, len, list, name, path, print, rc, related, rx, s, set, sorted, src, staged, str, suggestions, t, targets, tgt_set, tok, ts, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\cleanup_backups.py: EXCLUDE_DIRS, Exception, FILE_PATTERNS, any, bool, d, dict, dirnames, dirpath, f, filenames, files, flat, fname, int, len, list, name, out_dir, p, pat, paths, print, root, set, sorted, str, sum, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\cleanup_project.py: Exception, dict, e, error, int, len, list, pattern, print, py_file, replacement, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\cleanup_tools.py: dict, file, files, len, list, print, root, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\completeness_score.py: Exception, SystemExit, any, bool, e, float, getattr, int, isinstance, len, list, max, min, n, path, pattern, print, r, root, severity, sorted, str, sum, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\complete_fix_f_strings.py: enumerate, line, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\component_consistency_checker.py: Exception, any, c, call, comp, comp_file, count, dict, e, exp, file_path, hook, imp, int, issue, len, lines, list, method, name, print, rec, s, self, set, sorted, str, sum, url, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\comprehensive_project_enhancement.py: Exception, bool, e, file_path, init_file, int, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\consolidate_backend_backups.py: SystemExit, bool, dict, dup_contents, file_path, int, len, list, m, p, print, r, rels, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\consolidate_chunking.py: Exception, bool, cmd, e, f, new_pattern, old_pattern, open, print, step_func, step_name, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\copilot_guard.py: any, enumerate, f, i, len, line, list, must_trigger_pat, pattern, print, required_pat, str, suggestion, trigger_pattern, violation
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\copilot_intelligence_check.py: Exception, dict, dir_name, dir_path, e, f, feature, file_path, info, len, list, open, print, round, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\cross_project_guard.py: Exception, ValueError, bool, category, dict, dir_name, endpoints, enumerate, env_file, error, errors, event_name, f, grouped_errors, i, i18n_keys, isinstance, json_file, key, len, list, max, message, method, model, name, obj, path, prefix, print, py_file, schema_file, self, set, str, suggestion, suggestions, ts_file, types, value, var
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_ai_trainer.py: Exception, ImportError, e, len, model, print, report, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_ai_trainer_basic.py: Exception, ImportError, component, dep, description, e, len, model, print, str, success, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_autonomous_complete.py: Exception, action_data, count, e, enumerate, event, i, is_safe, key, len, print, reason, request, self, skill, status, str, value
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_autonomous_simple.py: Exception, action, e, enumerate, i, key, len, print, skill_name, value
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_breaking_changes.py: diff, diffs, len, m, method, p, print, proto, same, sorted
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_fast_control.py: Exception, KeyboardInterrupt, bgr, cap, color_name, demo_func, demo_name, e, len, max, min, operation, operation_name, print, range, sum, timer, x, y
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\demo_missing_code_system.py: Exception, category, cmd, conformance_exit, count, description, e, enumerate, f, file, i, int, issue, kind, len, list, max_issues, min, missing_code_exit, open, print, report_path, report_type, sorted, str, test_exit, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\dependency_safety.py: Exception, bool, dict, e, f, isinstance, len, list, max, pkg, print, project_root, rec, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\deploy.py: Exception, ImportError, attempt, bool, dict, e, environment, f, image, k8s_file, key, list, manifest_file, open, placeholder, range, revision, self, step_func, step_name, str, value
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\deploy_production.py: Exception, FileNotFoundError, all, bool, config_path, dict, e, endpoint, f, int, open, secret_name, self, skip_validations, str, tag, timeout
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\deploy_production_automated.py: Exception, KeyboardInterrupt, check, e, isinstance, service_name, shell, str, url
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\detect_backend_duplicates.py: Exception, SystemExit, by_hash, by_name, chunk, dict, e, f, files, int, iter, k, len, list, name, p, paths, print, sorted, str, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\diagnose_environment_comprehensive.py: Exception, ImportError, any, cmd, dict, dir_path, e, enumerate, ext, f, fix, i, issue, len, list, open, p, path, pkg, print, tool
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\diagnose_venv_detailed.py: Exception, e, enumerate, ext, f, i, j, len, line, open, p, print, range, req_ext
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\diagnose_vscode_issues.py: Exception, ImportError, PermissionError, any, config_file, count, d, dirname, e, enumerate, ext, f, fmt, i, item, keyword, len, line, lint, list, log_file, max, open, package, print, sorted, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\duplicate_code_analyzer.py: Exception, alias, any, arg, base, block, block1, block2, blocks, chr, count, dict, e, enumerate, f, file_path, files, float, i, imp, int, isinstance, len, lines, list, node, open, output_dir, pattern, print, project_root, py_file, self, similarity_threshold, sorted, str, suggestion, sum, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\duplicate_optimizer.py: Exception, app_file, core_file, dict, e, enumerate, f, file_path, i, len, list, open, optimization, pattern, print, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\enhance_api_endpoints.py: Exception, bool, content, e, file_path, int, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\enhance_dependencies_repos.py: Exception, bool, content, e, file_path, int, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\enhance_domain_layer.py: Exception, bool, content, e, file_path, int, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\enhance_middleware.py: SystemExit, bool, file_path_str, imp, int, len, print, str, template_key
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\enhance_repositories_schemas.py: Exception, bool, content, e, file_path, int, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\export_openapi.py: Exception, SystemExit, e, print, r, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fast_duplicate_check.py: Exception, d, data, directory, dirs, e, enumerate, error, f, file, file_info, file_path, files, func, i, len, line, list, loc, locations, open, pattern_hash, print, root, signature, sorted, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\file_integrity_full_check.py: Exception, SystemExit, dict, e, int, print, report_file, script_name, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\final_enhancement.py: Exception, description, e, enumerate, f, file_path, float, i, init_file, int, isinstance, len, line, open, print, row, sorted, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\final_optimization.py: OSError, any, dir_path, dst, dupe, mgr, print, src, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\find_duplicate_files.py: DEFAULT_EXTS, DEFAULT_OUT, DEFAULT_ROOTS, OSError, SKIP_DIR_NAMES, SKIP_PATH_CONTAINS, SystemExit, algo, any, chunk, dict, enumerate, exts, f, files, fp, groups, i, int, len, list, p, part, path, print, r, root, sorted, str, sum, tuple, v, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\find_duplicate_files_tool.py: RuntimeError, any, c, check, cwd, d, dict, enumerate, err, exts, f, float, g, globs, i, ig, int, len, list, m, open, out, print, rc, str, sum, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_all_f_strings.py: new, old, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_all_inits.py: Exception, bool, dir_path, e, enumerate, f, file_path, i, int, j, len, line, list, open, part, print, py_file, range
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_all_issues.py: Exception, bool, e, f, file_path, isinstance, item, node, open, print, py_file, set, str, target
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_common_f821.py: Exception, e, enumerate, file_path, i, import_stmt, int, line, m, new, old, pattern, print, replacement, reversed, sorted, str, var_name
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_critical_issues.py: Exception, KeyboardInterrupt, any, bool, cmd, dict, dry_run, e, exit_code, file_path, fix, imports, indent, int, line, list, module, pattern, print, self, sorted, stderr, stdout, str, tool, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_f821_errors.py: Exception, KeyboardInterrupt, any, count, dict, e, enumerate, error, errs, f, file_errors, i, import_line, input, int, j, len, list, open, pattern, print, range, reversed, set, sorted, str, sum, var_name, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_f_string.py: print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_graphql_resolvers.py: Exception, e, file_path, int, pattern, print, replacement, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_middleware_advanced.py: SystemExit, bool, file_path_str, int, len, print, str, template_key
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_repo_safe.py: Exception, apply, bool, cwd, details, directory, e, error, exclude_patterns, f, file_path, force_all, include_patterns, int, len, list, no_auto_all, output_path, path_filter, pattern, print, py_file, root_package, self, set, sorted, step, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_repo_safe_v2.py: Exception, apply, bool, cwd, details, dst, e, exclude_tests, f, int, item, list, path, path_filter, pattern, print, py_file, root_package, self, src, step, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_repo_safe_v3.py: Exception, bool, cat_name, category, dict, dry_run, e, error, f, label, len, list, open, print, root_path, self, set, sorted, str, test_after, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_undefined_variables.py: Exception, SyntaxError, alias, arg, bool, dict, e, enumerate, error, file, file_path, func_node, hasattr, i, int, isinstance, item, len, list, node, print, root_path, self, set, sorted, str, subnode, target, undefined, var
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_underscore_vars.py: Exception, callable, e, error, int, len, m, pattern, print, replacement, set, sorted, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_v2_dependencies.py: Exception, e, enumerate, f, file_rel_path, i, len, line, open, print, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_venv_recognition.py: Exception, dict, e, enumerate, ext, fix, i, len, line, list, print, step, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\fix_vscode_venv.py: Exception, dict, e, f, isinstance, open, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\focus_guard.py: ValueError, abs, any, base, base_file, bool, bus, count, dict, dup, f, file_path, files, float, group_files, int, layer, len, list, max, mgr, min, model, model_file, model_groups, output_json, part, print, py_file, repo, root, round, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\focus_index.py: Exception, any, c, cmd, d, dict, f, float, hits, int, len, list, m, max, min, module_map, path, print, r, ref, rows, s, seg, str, tuple, v, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\focus_optimization.py: dup, mgr_file, print, repo, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\generate_copilot_manifest.py: Exception, SystemExit, all_cmds, any, bool, c, cmds, commands, dict, enumerate, f, i, indexed, indexed_files, int, line, list, ln, manifest_path, new_summary_text, p, path, print, r, s, sl, snippets_map, str, summary_path, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\generate_copilot_manifest_hook.py: Exception, SystemExit, any, bool, exc, int, isinstance, line, list, manifest_path, msg, p, paths, print, str, summary_path, tuple, valid
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\generate_expectations_from_project_map.py: SystemExit, data, dict, f, int, k, len, line, m, mod, pkgs, print, s, set, spec, str, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\gen_ports_docs.py: int, lines, list, m, p, print, sorted, str, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\guard_full_file_read.py: OSError, SyntaxError, UnicodeDecodeError, f, file_path, group, int, isinstance, item, line, list, match, node, print, problem, seq, set, sorted, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\main_tsx_analyzer.py: any, bool, dict, enumerate, imp, issue, len, line, list, max, print, r, rec, self, str, sum, url
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\manage_inits.py: Exception, ImportError, KeyboardInterrupt, bool, e, init_file, len, print, quick, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\master_quality_check.py: Exception, FileNotFoundError, bool, check, command, critical, cwd, e, int, len, list, name, output, print, self, str, sum, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\missing_code_audit.py: Exception, SystemExit, all_issues, any, bool, count, dict, e, enumerate, file_path, i, int, isinstance, issue, kind, len, line, list, n, node, part, print, root, root_path, self, sorted, str, sum, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\missing_code_baseline.py: Exception, SystemExit, e, i, int, issue, len, print, set, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\missing_code_diff_gate.py: Exception, SystemExit, any, bool, cmd, dict, e, f, file_path, file_ranges, i, int, issue, issues_by_owner, item, kind, len, line_num, list, owner, owner_issues, path, path_variant, pattern_owners, print, r, range, set, sorted, str, sum, tuple, variant
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\missing_code_owner_report.py: Exception, SystemExit, e, i, int, issue, issues, len, owner, print, sorted, sum, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\normalize_imports.py: Exception, alias, any, bool, changed_files, d, dict, e, err, f, file_mod, fp, getattr, int, isinstance, issues, k, len, list, map_path, mapping, module, name, new_aliases, p, print, py_path, reversed, root, seg, self, staticmethod, str, tuple, updated, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\paddle_ocr_cli.py: Exception, SystemExit, argv, e, int, isinstance, line, lines, list, page, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\patch_apply.py: Exception, KeyboardInterrupt, ValueError, any, bool, c, e, fence_starts, header_end, input, int, len, list, match, p, path, print, require_markers, root, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\phase0_consolidation.py: action, any, base_file, bool, bus, dict, dry_run, dup, f, keep, legacy, len, list, manager_file, model_name, p, path, print, r, repo_file, repo_groups, repos, self, skip, sorted, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\phase1_cleanup_duplicates.py: Exception, any, bool, config, duplicate_file, e, enumerate, f, file_path, int, len, line, new_import, next_line, old_import, open, print, py_file, source, str, success, target, tline, total, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\phase2_layer_reorganization.py: Exception, base_dir, content, e, file_path, print, source, str, subdir, subdirs, target
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\phase3_domain_consolidation.py: Exception, domain, e, f, int, new_import, old_import, open, print, py_file
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\ports_audit.py: d, diffs, i, int, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\predeploy_check.py: Exception, ValueError, allow_fail, args, bool, check_func, check_name, code, e, env, float, int, len, line, print, stderr, stdout, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\project_summary.py: f, open, print
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\quality_full_check.py: Exception, bool, capture, code, cwd, dict, e, env, float, int, len, level, list, msg, name, print, round, self, step, step_duration, str, tool, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\quick_check.py: Exception, bool, cmd, desc, description, e, len, list, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\quick_critical_fixer.py: Exception, any, bool, e, enumerate, int, len, level, line, message, pattern, print, replacement, self, str, unused
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\quick_duplicate_check.py: blocks, len, print, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\quick_fix_stubs.py: Exception, SystemExit, any, e, enumerate, file_path, i, int, isinstance, item, len, line, list, node, part, pattern, print, replacement, root, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\quick_fix_underscore.py: Exception, e, file_path, int, new, old, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\reinstall_vscode_paths.py: Exception, ImportError, KeyboardInterrupt, bool, dict, e, f, int, issue, message, open, print, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\restore_candidate_patch.py: Exception, SystemExit, cmd, commit, e, from_commit, i, int, issue, len, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\restructure_project.py: Exception, bool, critical_file, dict, dup_file, e, f, item, len, missing, open, pattern, print, py_file, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\restructure_zeta_project.py: Exception, any, base_path, check, content, dict, dir_name, e, f, file_path, isinstance, item, len, list, name, open, parent, pattern, print, self, skip, src_pattern, str, structure
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\roadmap_implementation.py: ValueError, action, bool, component, dict, dry_run, e, int, len, list, phase_num, print, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\roadmap_implementation_guide.py: IMPLEMENTATION_GUIDES, SystemExit, chr, dict, int, key, len, list, module_key, print, prompt, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\safety_audit.py: Exception, bool, check_name, check_result, cmd, dict, e, f, int, isinstance, len, line, list, output_file, print, project_root, py_file, self, str, sub_check
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\safety_dashboard.py: Exception, IndexError, ValueError, bool, dict, e, f, int, isinstance, issue, len, line, list, max, min, print, project_root, py_file, self, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\safe_chunking_discovery.py: Exception, all, bool, cmd, d, deps, dict, dir_path, e, f, file_path, len, line, list, open, passed, print, rec, stdout, str, test_name, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\safe_cleanup.py: Exception, bool, cmd, description, e, file, file_path, len, list, path, pattern, print, project_root, required_file, self, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\safe_error_fixer.py: Exception, OSError, any, bool, cmd, desc, description, e, final_mypy, final_ruff, initial_mypy, initial_ruff, int, len, line, list, new_name, old_name, project_root, self, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\scaffold_missing_dirs.py: Exception, SystemExit, action, e, f, file_name, int, len, package_name, package_path, print, spec, str, template_name
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\scaffold_missing_modules.py: Exception, SystemExit, action, bool, content, dict, e, f, filepath, int, len, list, miss, print, root, str, sum, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\setup_development.py: Exception, FileNotFoundError, ImportError, bool, directory, e, self, step_func, step_name, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\system_upgrade.py: Exception, any, e, error, file_path, len, list, old_file, pattern, print, py_file, self, str, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\test_safety.py: Exception, bool, dict, e, f, int, isinstance, len, list, max, min, print, project_root, self, str, sub_result, sub_type, sum, test_type, xml_file
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\ultimate_completion.py: Exception, bool, cmd, desc, description, e, len, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\update_init_files.py: Exception, PACKAGE_CONFIGS, any, comp, components, description, dict, e, f, feature, features, len, list, open, package_path, print, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\upgrade_analyzer.py: any, bool, categories, category, dep, dict, enumerate, f, float, gap, i, icon, int, len, list, min, p, phase_name, print, py_file, rec, self, set, str, sum
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\used_but_missing.py: Exception, ImportError, SystemExit, alias, dict, e, filepath, files_processed, hasattr, i, int, isinstance, len, list, node, pattern, print, root, source_code, str, sum, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\validate_infrastructure.py: Exception, FileNotFoundError, KeyboardInterrupt, all, bool, description, doc_path, e, error, f, file_path, len, list, open, script_path, self, step_name, str, validation_func, var, warning
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\validate_inits.py: Exception, SyntaxError, bool, dict, e, enumerate, error, f, file_path, int, len, line, list, open, path, print, py_file, self, set, sorted, str, warning
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\validate_new_files.py: any, bool, folder, int, len, line, list, m, p, print, root, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\verify_core_export_contracts.py: CORE_CONTRACTS, ImportError, SystemExit, bool, contract, e, hasattr, int, len, list, message, module_name, name, names, print, str, success, symbol, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\verify_enhanced_roadmap_contracts.py: ENHANCED_CONTRACTS, Exception, ImportError, SystemExit, any, bool, budget_ms, contract, dir, e, getattr, hasattr, int, len, list, min_coverage, module, module_name, module_path, msg, name, passed, print, result, set, str, sym, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\verify_imports.py: Exception, any, bad, e, err, k, len, list, m, n, print, repr, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\verify_middleware_enhancement.py: Exception, bool, count, dict, e, file_path, float, found, int, isinstance, len, line, list, max, min, node, pattern, pattern_name, pattern_text, print, str, sum, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\verify_module_symbols.py: Exception, ImportError, SystemExit, all_misses, dict, e, filename, hasattr, int, len, list, m, misses, module_name, pkg_name, print, r, spec, str, sum, symbol_name
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\vscode_final_guide.py: Exception, ImportError, bool, e, int, name, print, status
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\whisper_server.py: Exception, i, range, ws
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\workflow_health_check.py: Exception, any, description, dict, e, env_value, f, file, filename, files, i, isinstance, issue, issue_type, job_config, job_name, key, len, list, max, open, pattern, print, self, sorted, step, str, trigger, workflow, yaml_file
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\bench\bench_api.py: Exception, client, dict, float, int, len, list, max, min, p, print, range, self, sorted, str, sum, url
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\bench\bench_rag.py: Exception, client, dict, float, h, headers, int, len, list, max, min, object, p, print, range, round, self, sorted, str, url, v
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\consolidation\consolidate_repo.py: Exception, dict, e, f, from_module, int, len, list, mod, module_name, name, print, pyfile, rule, str, target
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\deployment\production_deploy_complete.py: Exception, ValueError, bool, check_func, check_name, config_path, dict, e, endpoint, f, host, image, int, kwargs, len, name, node, open, pod, port, resource, s, self, step_func, step_name, str, sum, var
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\maintenance\backup_data.py: Exception, FileNotFoundError, backup, backup_dir, bool, database_path, dict, e, int, keep_count, len, list, locals, print, self, str, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\metrics\focus_index.py: Exception, ImportError, e, float, int, len, print, str
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\monitoring\health_check.py: Exception, KeyboardInterrupt, all, any, check, dict, e, endpoint_name, exit, f, float, int, isinstance, len, list, open, print, round, self, str, sum, url
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\monitoring\performance_check.py: Exception, ImportError, ValueError, abs, api_metrics, change, db_metrics, dict, e, endpoint, f, float, int, isinstance, len, list, m, max, metric, metric_name, min, monitor, op_name, open, operation, print, query, query_name, range, redis_metrics, response, self, str, sum, trend, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\qa\check_zero_trust.py: Exception, base_url, bool, e, int, jwt, len, list, path, print, protected_paths, public_paths, response, status, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\qa\preflight.py: Exception, ImportError, bool, command, e, error, free, host, int, len, list, package, packages_ok, port, print, resource_msg, resources_ok, str, tuple, warning
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\qa\warm_and_probe_rag.py: Exception, base_url, bool, bytearray, bytes, dict, e, exit, float, i, ingest_path, int, isinstance, latency, len, method, min, print, query, range, response, round, s, search_path, status, str, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\refactor\copilot_refactor.py: Exception, SystemExit, ValueError, d, dict, e, int, issues, len, list, m, max, md, moves, mp, p, print, results, s, src, str, sum, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\repo\cleanup_plan.py: Exception, bool, dict, dir_path, e, f, file_path, len, list, open, print, reason, self, str, target, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\repo\find_duplicates.py: Exception, bool, checked_pairs, chunk, data, dict, enumerate, f, f1, f2, file1, file2, file_path, files, float, i, iter, len, list, open, pattern, print, round, self, set, similarity_threshold, str, sum, tuple
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\repo\verify_client_api.py: Exception, any, bool, cmd, data, dict, e, enumerate, f, file_path, i, key, keyword, len, line, list, mismatch, open, print, py_file, rec, self, str, try_codegen, ts_file
E:\zeta-monorepo\.dup_backup\20250909_042457\tools\scripts\testing\load_test.py: Exception, TimeoutError, ValueError, bool, dict, e, error, f, float, int, len, list, max, min, open, percentile, print, r, range, response, self, set, sorted, stats, str, tester, user_id
E:\zeta-monorepo\.dup_backup\20250909_042810\ai_auto_optimizer.py: Exception, SyntaxError, all, bool, child, description, dict, e, f, file_path, float, func, int, isinstance, len, line, list, node, open, passed, pattern, print, project_root, r, replacement, self, sorted, str, sum, v, validation, x
E:\zeta-monorepo\.dup_backup\20250909_042810\ai_auto_refactor.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\ai_project_scanner.py: Exception, OSError, SyntaxError, alias, any, child, chr, d, dict, dirs, e, enumerate, f, fa, filename, filenames, float, i, imp, int, isinstance, item, len, line, list, max, message, min, node, open, pattern, print, project_root, root, self, sorted, str, sum, tuple, x
E:\zeta-monorepo\.dup_backup\20250909_042810\final_project_demo.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\gen_project_map.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\metrics_server.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\ollama_api_optimization_guide.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\ollama_benchmark.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\ollama_turbo_integration.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\optimized_turbo_client.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\production_deploy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\quick_duplicate_checker.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\quick_start_turbo.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\safe_backup_cleanup.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\setup_dev.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\setup_one_click_learning.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\setup_vscode_ollama.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\setup_vscode_turbo_api.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\simple_turbo_setup.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\smart_refactorer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\turbo_api_implementation.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\turbo_api_online_auth.py: Exception, ImportError, bool, current_user, dict, e, getattr, i, int, isinstance, iter, len, list, orchestrator, range, request, request_id, result, self, str, token
E:\zeta-monorepo\.dup_backup\20250909_042810\turbo_demo.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\turbo_ollama_client.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\turbo_ollama_login.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\turbo_setup.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\verify_ai_setup.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\test_ollama_client.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\deps_compat.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\di_container.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\main.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\test_blueprint.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\admin.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\agents.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\assistant.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\auth.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\autonomy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\demo_di.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\files.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\health.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\learning.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\memory.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\planning.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\reflexion.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\static_router.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\system.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\voice.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\_common_audit.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\_common_cache.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\_common_idempotency.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\_common_rate_limit.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\_common_security.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\agent\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, module, name, str
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\auth\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, module, name, str
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\endpoints\plans_example.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v1\_common\security.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\advanced_memory.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\advanced_memory_optimized.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\federated_learning.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\federated_learning_optimized.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\multi_agent.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\multi_agent_optimized.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\real_time_collab.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\router.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\v2\security_ai_optimized.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\api\websockets\router.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\auth\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\common\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\containers\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\middleware\observability.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\realtime\training_ws.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\services\assistant_svc.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\services\collab_service.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\services\dataset_svc.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\services\federated_service.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\services\local_model_svc.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\app\services\teacher_client.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\config\advanced_settings.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\config\external_services.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\domain\autonomy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\domain\entities\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\domain\value_objects\agent\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\domain\value_objects\memory\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\domain\value_objects\user\__init__.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\interfaces\autonomy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\security\authentication\factory_fixed.py: ImportError, ValueError, backend, body, bool, enable_metrics, enable_tracing, print, redis_kwargs, redis_url, storage_backend, str, subject, to, tuple
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\security\authentication\quick_validation.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\security\authentication\simple_validation.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\security\authentication\test_enhanced_system.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\services\asr_service.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\services\autonomy_planner.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\services\autonomy_safety.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\services\autonomy_skills.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\services\ai\rag\optimized.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\core\use_cases\autonomy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\adapters\asr_whisper.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\implementations\advanced_targeting.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\implementations\input_control_fast.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\implementations\screen_capture_dxgi.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\implementations\screen_control_manager.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\implementations\screen_targeting.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\implementations\windows_keycodes.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\instrumentation\latency_timer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\instrumentation\performance_benchmark.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\data\models\models.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\tests\test_asr_smoke.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\tests\integration\test_di_integration.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\tests\integration\test_di_simple.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\tests\stubs\openai.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\backend\trainer\demo_ai_learning.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\dev_server.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\fix_errors.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\metrics_server.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\metrics_server_optimized.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\optimize.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\performance_test.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\apps\zeta-ai-agent\config\settings.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\docs\examples\python-assistant\assistant.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\docs\examples\python-assistant\benchmark.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\docs\examples\python-assistant\examples_turbo_usage.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\docs\examples\python-assistant\turbo_api_client.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\docs\examples\python-assistant\turbo_cli.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\docs\examples\python-assistant\turbo_ollama_integration.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\examples\turbo_ollama_usage_examples.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\production\scripts\health_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\production\src\final_project_demo.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\production\src\turbo_demo.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\apply_consolidation_plan.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\benchmark_latency.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\cleanup_reports.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\consolidation_audit.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\consolidation_plan_builder.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\dedupe_scan.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\lo_finetune.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\prepare_vn_dataset.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\scripts\update_references.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tests\run_ai_codemod_tests.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tests\run_ai_intelligence_tests.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tests\ai-codemod\unit\test_ci_reporter.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tests\ai-project-intelligence\test_consistency_guard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tests\ai-project-intelligence\test_knowledge_graph_serialization.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\cleanup_duplicates.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\find_duplicate_files.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\reference_updater.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\run_ai_optimization.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-codemod\ci_reporter.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-codemod\engine.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-analyzer\analyzer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-analyzer\duplicates.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-analyzer\per_file_optimizer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-analyzer\project-graph.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-analyzer\smart-optimizer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-analyzer\vs-code-helper.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\auto-coder.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\auto_fixer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\brain.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\consistency-guard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\continuous-monitor.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\knowledge-graph.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\reporter.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\ai-project-intelligence\setup.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\add_test_type_annotations.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\aggressive_optimization.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\analyze_duplicate_name_similarity.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\analyze_f821.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\analyze_init_patterns.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\analyze_middleware.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\api_auto_fixer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\api_consistency_optimizer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\apply_base_classes.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\apply_refactor_plan.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\autobarrel_python.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\auto_fix_regression_guard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\backup_data.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\backup_database.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\backup_inits.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\batch_fix_errors.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\benchmark_desktop_control.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\benchmark_fast_control.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_backend_duplicates_ci.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_conformance.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_duplicates.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_env_sync.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_external_dependencies.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_missing_dependencies.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_quality.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\check_related_files.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\cleanup_backups.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\cleanup_project.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\cleanup_tools.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\completeness_score.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\complete_fix_f_strings.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\component_consistency_checker.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\comprehensive_project_enhancement.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\consolidate_backend_backups.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\consolidate_chunking.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\copilot_guard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\copilot_intelligence_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\cross_project_guard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deepseek_agent.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_ai_trainer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_ai_trainer_basic.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_autonomous_complete.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_autonomous_simple.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_breaking_changes.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_fast_control.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\demo_missing_code_system.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\dependency_safety.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deploy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deploy_deepseek.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deploy_production.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deploy_production_automated.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\detect_backend_duplicates.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\diagnose_environment_comprehensive.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\diagnose_venv_detailed.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\diagnose_vscode_issues.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\duplicate_code_analyzer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\duplicate_optimizer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\enhance_api_endpoints.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\enhance_dependencies_repos.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\enhance_domain_layer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\enhance_middleware.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\enhance_repositories_schemas.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\export_openapi.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fast_duplicate_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\file_integrity_full_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\final_enhancement.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\final_optimization.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\find_duplicate_files.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\find_duplicate_files_tool.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_all_f_strings.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_all_inits.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_all_issues.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_common_f821.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_critical_issues.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_f821_errors.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_f_string.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_graphql_resolvers.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_middleware_advanced.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_repo_safe.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_repo_safe_v2.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_repo_safe_v3.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_undefined_variables.py: Exception, SyntaxError, alias, arg, bool, dict, e, enumerate, error, file, file_path, func_node, hasattr, i, int, isinstance, item, len, list, node, print, root_path, self, set, sorted, str, subnode, target, undefined, var
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_underscore_vars.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_v2_dependencies.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_venv_recognition.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\fix_vscode_venv.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\focus_guard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\focus_index.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\focus_optimization.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\generate_copilot_manifest.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\generate_copilot_manifest_hook.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\generate_expectations_from_project_map.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\gen_ports_docs.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\guard_full_file_read.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\main_tsx_analyzer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\manage_inits.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\master_quality_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\missing_code_audit.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\missing_code_baseline.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\missing_code_diff_gate.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\missing_code_owner_report.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\normalize_imports.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\paddle_ocr_cli.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\patch_apply.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\phase0_consolidation.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\phase1_cleanup_duplicates.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\phase2_layer_reorganization.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\phase3_domain_consolidation.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\ports_audit.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\predeploy_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\project_summary.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\quality_full_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\quick_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\quick_critical_fixer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\quick_duplicate_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\quick_fix_stubs.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\quick_fix_underscore.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\reinstall_vscode_paths.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\restore_candidate_patch.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\restore_data.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\restructure_project.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\restructure_zeta_project.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\roadmap_implementation.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\roadmap_implementation_guide.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\safety_audit.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\safety_dashboard.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\safe_chunking_discovery.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\safe_cleanup.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\safe_error_fixer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\scaffold_missing_dirs.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\scaffold_missing_modules.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\setup_development.py: Exception, ImportError, bool, current_user, dict, e, getattr, i, int, isinstance, iter, len, list, orchestrator, range, request, request_id, result, self, str, token
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\system_upgrade.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\test_desktop_control_standalone.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\test_safety.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\ultimate_completion.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\update_init_files.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\upgrade_analyzer.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\used_but_missing.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\validate_infrastructure.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\validate_inits.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\validate_new_files.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_core_export_contracts.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_enhanced_roadmap_contracts.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_imports.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_middleware_enhancement.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_module_symbols.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_vscode_config.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\verify_vscode_config_simple.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\vscode_final_guide.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\whisper_server.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\workflow_health_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\bench\bench_api.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\bench\bench_rag.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\consolidation\consolidate_repo.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deployment\production_deploy.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\deployment\production_deploy_complete.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\maintenance\backup_data.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\metrics\focus_index.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\monitoring\health_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\monitoring\performance_check.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\qa\check_zero_trust.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\qa\preflight.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\qa\warm_and_probe_rag.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\refactor\copilot_refactor.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\repo\cleanup_plan.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\repo\find_duplicates.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\repo\verify_client_api.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\testing\load_test.py: DeprecationWarning
E:\zeta-monorepo\.dup_backup\20250909_042810\tools\scripts\testing\run_tests.py: DeprecationWarning
E:\zeta-monorepo\.github\gen_project_map.py: Exception, PermissionError, argv, bool, c, d, depth, dir_counts, e, enumerate, ext, exts, hints, idx, int, k, lang_counts, len, level, max, max_items, n, pat, path, prefix, print, set, sorted, str, sum, tree_lines, tuple, uniq, v, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\__init__.py: args, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\__pip-runner__.py: SystemExit, classmethod, fullname, str, target, v, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\build_env.py: BaseException, NotImplementedError, a, args, b, extra_index, finder, format_control, fp, getattr, hasattr, host, isinstance, kind, link, list, name, old_value, open, pip_runnable, prefix_as_string, req_str, reqs, requirements, reversed, self, set, sorted, spinner, staticmethod, str, varname
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cache.py: Exception, NotImplementedError, bool, cache_dir, candidate, d, download_info, e, link, min, package_name, persistent, self, staticmethod, str, super, supported_tags, wheel_dir, wheel_name
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\configuration.py: IndexError, KeyError, OSError, UnicodeDecodeError, bool, dict, error, f, files, fname, isolated, load_only, map, open, path, property, repr, section, self, str, super, val, value, variant
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\exceptions.py: AttributeError, Exception, KeyError, OSError, UnicodeDecodeError, a, allowed, bool, classmethod, cls, command_description, config, console, dist, e, error, error_msg, errors_of_cls, exit_code, expecteds, f_val, field, fname, found, getattr, gots, gotten_hash, hasattr, hash_name, hint_stmt, indent, int, ireq, isinstance, key, kind, lang, len, link, location, m_val, message, metadata_name, name, next, note_stmt, options, output_lines, package_details, reason, request, response, s, self, sep, staticmethod, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\main.py: args, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\pyproject.py: all, bool, error, f, isinstance, item, list, obj, open, pyproject_toml, req_name, requirement, setup_py, str, unpacked_source_directory
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\self_outdated_check.py: Exception, KeyError, OSError, ValueError, bool, cache_dir, current_time, f, get_remote_version, isodate, local_version, open, options, pkg, property, pypi_version, self, session, statefile, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\wheel_builder.py: Exception, OSError, base, bool, build_failures, build_options, build_successes, e, editable, global_options, isinstance, length, need_wheel, output_dir, req, requirements, s, str, temp_dir, verify, wheel_cache, wheel_hash
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\__init__.py: args, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\autocompletion.py: IndexError, any, directory, dist, f, i, int, k, list, o, opt_str, option, path, print, str, v, word, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\base_command.py: BaseException, KeyboardInterrupt, NotImplementedError, args, bool, exc, hasattr, int, isinstance, isolated, name, options, print, run_func, self, set, sorted, str, summary, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\cmdoptions.py: ValueError, abis, algo, all, any, bool, cache_dir, cert, check_target, client_cert, cmd_opts, debug_mode, digest, disable_pip_version_check, error_msg, exc, getattr, group, help_, implementation, index_url, int, isinstance, isolated_mode, key, keyring_provider, len, list, log, no_cache, no_color, no_index, no_input, no_python_version_warning, opt_str, option, options, package, parser, part, platforms, proxy, python, python_version, quiet, require_virtualenv, retries, sep, set, setattr, str, timeout, tuple, use_deprecated_feature, use_new_feature, val, verbose, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\command_context.py: context_provider, self, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\main.py: DeprecationWarning, cmd_args, cmd_name, e, exc, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\main_parser.py: OSError, args, args_else, command_info, exc, exe, general_options, len, name, python, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\parser.py: ValueError, bool, epilog, err, exc, getattr, hasattr, heading, i, idx, indent, int, isinstance, isolated, key, len, line, list, mvarfmt, name, optsep, print, property, section, section_items, section_key, self, set, str, super, text, usage, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\progress_bars.py: bar_type, bytes, chunk, float, int, iter, iterable, len, size, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\req_command.py: Exception, ImportError, any, args, bool, build_tracker, classmethod, cls, dict, download_dir, e, fallback_to_certifi, filename, finder, force_reinstall, func, getattr, hasattr, ignore_installed, ignore_requires_python, int, kw, min, options, parsed_req, preparer, py_version_info, registry, req, requirements, retries, self, staticmethod, str, super, t, target_python, temp_build_dir, timeout, upgrade_strategy, use_pep517, use_user_site, verbosity, wheel_cache
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\cli\spinners.py: Exception, KeyboardInterrupt, NotImplementedError, bool, final_status, float, len, message, min_update_interval_seconds, next, self, spin_chars, status, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\cache.py: args, e, filename, int, len, options, self, sorted, str, subdir
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\check.py: conflicting, dep_name, dep_version, dependency, int, missing, package_set, parsing_probs, project_name, req, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\completion.py: int, options, print, self, shell, sorted, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\configuration.py: Exception, FileNotFoundError, any, args, bool, e, example, files, int, len, n, name, need_value, options, self, site_config_file, sorted, str, variant
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\debug.py: ImportError, config, dict, expected_version, f, getattr, globals, int, key, len, level, line, locals, name, options, self, str, tag, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\download.py: args, downloaded, int, options, req, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\freeze.py: bool, int, line, options, self, set, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\hash.py: archive, args, chunk, int, open, options, path, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\help.py: IndexError, args, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\index.py: args, bool, candidate, e, ignore_requires_python, int, len, options, self, session, set, sorted, str, ver, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\inspect.py: dist, int, options, res, self, set, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\install.py: Exception, KeyError, OSError, all, any, args, bool, build_failures, conflict_details, conflicting, d, dep_name, dep_version, dependency, error, f, home, int, isolated, isolated_mode, len, lib_dir, missing, open, options, package_set, prefix, prefix_path, project_name, r, req, resolver_variant, result, root, root_path, s, self, set, sorted, str, target_dir, upgrade, use_user_site, user, using_user_site
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\list.py: any, candidate, d, dep, dist, int, len, list, map, n, options, pkg, pkg_strings, pkgs, proj, self, session, set, sizes, sorted, str, val, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\search.py: UnicodeEncodeError, args, fault, hit, int, isinstance, len, list, max, options, packages, self, str, versions
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\show.py: FileNotFoundError, KeyError, args, bool, classifier, current_dist, d, distributions, entry, enumerate, i, int, line, list_files, name, options, pkg, project_url, query_name, req, self, sorted, str, verbose, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\uninstall.py: args, filename, int, name, options, parsed_req, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\wheel.py: OSError, args, build_failures, build_successes, e, int, len, options, req, reqs_to_build, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\commands\__init__.py: class_name, commands_dict, getattr, kwargs, module_path, str, summary
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\distributions\base.py: NotImplementedError, bool, req, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\distributions\installed.py: bool, property, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\distributions\sdist.py: bool, build_isolation, check_build_deps, conflicting, conflicting_reqs, conflicting_with, finder, installed, map, missing, property, repr, self, sorted, str, wanted
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\distributions\wheel.py: bool, property, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\distributions\__init__.py: install_req
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\index\collector.py: Exception, anchor, attrs, bool, bytes, cache_link_parsing, cacheable_page, candidates_from_page, classmethod, content, dict, exc, file, fn, hash, headers, int, isinstance, len, list, loc, location, name, object, options, other, page, path, project_name, property, request_desc, response, s, scheme, self, session, str, super, suppress_no_index, tag, type, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\index\package_finder.py: Exception, ValueError, allow_yanked, bool, c, cand_iter, classmethod, cls, detail, eggs, enumerate, fragment, host_port, i, idx, int, iter, len, link_collector, links, list, map, max, no_eggs, project_name, project_url, property, req, result, seen, selection_prefs, self, set, sorted, source, sources, str, tag, upgrade, v, version_info
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\index\sources.py: NotImplementedError, bool, cache_link_parsing, candidates_from_page, entry, expand_dir, file_url, list, location, page_validator, project_name, property, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\locations\base.py: AttributeError, OSError, bool, new_root, pathname, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\locations\_distutils.py: AttributeError, ImportError, UnicodeDecodeError, bool, dist_args, dist_name, getattr, home, ignore_config_files, isolated, key, p, root, str, user
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\locations\_sysconfig.py: bool, getattr, home, k, key, prefix, root, set, setattr, str, user
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\locations\__init__.py: KeyError, all, any, bool, cmd, dist_name, getattr, home, isolated, k, key, len, p, prefix, root, scheme, str, tuple, user, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\base.py: FileNotFoundError, NotImplementedError, OSError, UnicodeDecodeError, ValueError, bool, bytes, classmethod, d, dep, dist, e, editables_only, include_editables, local_only, object, p, property, row, self, skip, str, stream, user_only
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\pkg_resources.py: AttributeError, FileNotFoundError, UnicodeDecodeError, base_dir, bool, bytes, classmethod, cls, directory, dist_dir_name, e, entries, entry_point, extra, filename, frozenset, group, info_dir, isinstance, metadata_contents, path, paths, project_name, property, repr, self, str, value, wheel, wheel_name, ws, zf
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\_json.py: UnicodeDecodeError, bytes, field, h, isinstance, msg, multi, str, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\__init__.py: KeyError, ValueError, bool, bytes, canonical_name, directory, filename, getattr, metadata_contents, object, paths, str, wheel
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py: NotImplementedError, ValueError, d, dist, getattr, isinstance, property, reason, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py: FileNotFoundError, KeyError, UnicodeDecodeError, any, bool, bytes, child, classmethod, cls, context, contexts, directory, e, extra, extras, filename, fullpath, info_dir, isinstance, iter, metadata_contents, path, property, provided_extra, relpath, req_string, self, stem, str, suffix, zf
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py: bool, child, classmethod, cls, dist, distribution, e, entry, f, it, line, location, name, next, paths, self, set, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\candidate.py: link, name, self, str, super, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\direct_url.py: Exception, ValueError, bool, classmethod, cls, commit_id, d, default, dict, editable, expected_type, hash_name, hash_value, hashes, info, isinstance, k, key, kwargs, len, netloc_no_user_pass, property, requested_revision, s, self, str, subdirectory, url, user_pass, v, vcs
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\format_control.py: NotImplemented, all, bool, canonical_name, frozenset, getattr, isinstance, k, object, other, self, set, staticmethod, str, target, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\index.py: file_storage_domain, path, self, str, super, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\installation_report.py: classmethod, install_requirements, ireq, self, sorted, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\link.py: IndexError, KeyError, all, anchor_attribs, any, base_url, bool, cache_link_parsing, classmethod, cls, comes_from, dict, file_data, hashname, hashval, isinstance, iter, k, link, link1, link2, n, next, page_url, part, property, query, requires_python, reserved, self, sep, str, super, to_clean, v, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\scheme.py: data, headers, platlib, purelib, scripts, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\search_scope.py: bool, built_find_links, classmethod, cls, find_links, index_urls, no_index, project_name, self, str, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\selection_prefs.py: allow_all_prereleases, allow_yanked, bool, format_control, prefer_binary, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\target_python.py: abis, implementation, int, key, map, part, platforms, self, set, str, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\models\wheel.py: StopIteration, ValueError, bool, enumerate, filename, i, int, min, next, self, sorted, str, t, tag, tag_to_priority, tags, x, y, z
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\auth.py: AttributeError, Exception, FileNotFoundError, ImportError, ValueError, allow_keyring, allow_netrc, bool, exc, hasattr, index_url_user_password, index_urls, kwargs, netloc, original_url, prompting, property, pw, resp, self, service_name, str, un, url_user_password
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\cache.py: OSError, body, bool, bytes, data, directory, f, getattr, int, key, list, name, open, response, self, str, super, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\download.py: KeyError, TypeError, ValueError, bytes, chunk, content_file, default_filename, e, int, link, links, location, open, progress_bar, self, session, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\lazy_wheel.py: Exception, base_headers, bool, bytes, chunk, chunk_size, exc, int, j, k, length, lslice, max, min, offset, property, range, reversed, rslice, self, session, size, str, url, whence, zf, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\session.py: Exception, OSError, SECURE_ORIGINS, ValueError, any, args, block, bool, cache, cert, conn, connections, data, dict, distro_infos, exc, filter, float, host, index_urls, int, kwargs, location, maxsize, method, name, new_index_urls, open, origin_host, origin_port, parsed_host, parsed_port, pool_kwargs, port, secure_host, secure_origin, secure_port, secure_protocol, self, source, ssl_context, str, super, suppress_logging, trusted_hosts, type, url, x, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\utils.py: AttributeError, UnicodeDecodeError, bytes, chunk_size, int, isinstance, resp, response, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\network\xmlrpc.py: bool, exc, handler, host, index_url, isinstance, request_body, self, session, str, super, use_datetime, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\check.py: OSError, ValueError, any, bool, conflicting_deps, dep, e, inst_req, isinstance, list, missing_deps, package_detail, package_details, package_name, project_name, req, set, should_ignore, sorted, spec, str, to_install
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\freeze.py: bool, classmethod, cls, dist, emitted_options, ex, exc, exclude_editable, files, installation, installations, isinstance, isolated, len, list, local_only, name, open, paths, req_file, req_file_path, req_files, requirement, self, set, skip, sorted, str, type, user_only, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\prepare.py: bool, build_dir, build_isolation, build_tracker, check_build_deps, download, download_dir, exc, f, filepath, finder, int, isinstance, lazy_wheel, legacy_resolver, links_to_fully_download, location, open, parallel_builds, partially_downloaded_reqs, path, progress_bar, require_hashes, self, session, skip_reason, src_dir, str, super, use_user_site, verbosity, warn_on_hash_mismatch
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\build_tracker.py: BaseException, FileNotFoundError, KeyError, LookupError, changes, ctx, fp, isinstance, key, list, name, new_value, object, open, original_value, req, saved_values, self, str, tracker
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\metadata.py: backend, build_env, details, error, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py: backend, build_env, details, error, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\metadata_legacy.py: bool, build_env, details, directory, error, f, isolated, len, setup_py_path, source_dir, spinner, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\wheel.py: Exception, backend, metadata_directory, name, str, tempd
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py: Exception, backend, e, metadata_directory, name, str, tempd
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\build\wheel_legacy.py: Exception, build_options, command_args, command_output, global_options, len, name, setup_py_path, sorted, source_dir, spinner, str, temp_dir, tempd
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\install\editable_legacy.py: bool, build_env, global_options, home, isolated, name, prefix, setup_py_path, str, unpacked_source_directory, use_user_site
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\operations\install\wheel.py: KeyError, ValueError, any, blocksize, bool, changed, data_scheme_paths, dest, dest_dir_path, dest_subpath, destfile, dir_scripts, direct_url, direct_url_file, dist, e, entry_point, f, file, generated, getattr, grouped_by_dir, gui, h, hash_, i, info_dir, installed, installed_path, installed_record_path, installed_rows, installer_file, int, k, key, kwargs, len, list, map, metadata, mode, modified, old_csv_rows, open, options, other_scheme_paths, outrows, pycompile, record_file, req_description, requested, root_scheme_paths, row, scheme, scheme_key, script, script_scheme_paths, scripts, self, set, size, sorted, sorted_scripts, specification, src_record_path, srcfile, stdout, str, super, target_path, warn_for, warn_script_location, wheel_path, wheel_zip, z, zip_file
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\req\constructors.py: any, bool, comes_from, config_settings, constraint, editable_req, extras_override, f, filename, global_options, hash_options, ireq, isolated, len, line_source, match, new_extras, next, op, open, p, parsed_req, permit_editable_wheels, post, pre, req_string, requirement, self, set, sorted, spec, str, text, use_pep517, user_supplied, version_control
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\req\req_file.py: Exception, OSError, SUPPORTED_OPTIONS, SUPPORTED_OPTIONS_EDITABLE_REQ, SUPPORTED_OPTIONS_REQ, ValueError, args_str, bool, comes_from, constraint, dest, e, enumerate, env_var, exc, f, filename, finder, host, int, is_editable, line_number, lineno, o, open, option_factory, options_str, opts, parsed_line, requirement, self, session, str, token, url, var_name
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\req\req_install.py: AssertionError, any, archive_source, attr, auto_confirm, autodelete, backend, backend_path, bool, build_dir, check, config_settings, constraint, dirname, dirnames, dirpath, editable, extra, extras, filenames, getattr, global_options, hasattr, hash_options, home, isinstance, isolated, iter, len, next, option, options, parallel_builds, parent_dir, parentdir, permit_editable_wheels, prefix, property, pycompile, req, reqs, requires, root, rootdir, self, set, sorted, str, trust_internet, use_pep517, use_user_site, user_supplied, vars, verbose, warn_script_location
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\req\req_set.py: KeyError, any, bool, check_supported_wheels, dep, install_req, isinstance, len, list, name, property, req, self, sorted, spec, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\req\req_uninstall.py: FileNotFoundError, KeyError, NotADirectoryError, OSError, ValueError, a, all_files, all_subdirs, any, args, auto_confirm, bool, bytes, classmethod, cls, d, dirfiles, dirname, dirpath, dist, dn, entry_point, ex, f, fh, fn, fname, folder, installed_file, is_gui, item, kw, len, line, map, old_head, open, p, paths, property, pth, root, s, script, script_name, seen, self, set, short_paths, shortpath, sorted, str, subdirs, tail, top_level_pkg, verbose, w, wildcards
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\req\__init__.py: Exception, bool, global_options, home, name, prefix, pycompile, req, req_name, requirement, requirements, root, self, str, use_user_site, warn_script_location
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\base.py: NotImplementedError, bool, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py: FileNotFoundError, KeyError, add_to_parent, bool, check_supported_wheels, dep, discovered_reqs, e, exc, extras_requested, finder, force_reinstall, ignore_dependencies, ignore_installed, ignore_requires_python, install_req, int, list, make_install_req, map, missing, more_reqs, ordered_reqs, preparer, req, req_set, req_to_install, root_reqs, self, set, sorted, str, subreq, super, to_scan_again, tuple, upgrade_strategy, use_user_site, version_info, wheel_cache
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py: NotImplemented, NotImplementedError, all, bool, candidate, classmethod, extras, frozenset, ireq, isinstance, link, other, project, property, self, sorted, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py: NotImplementedError, bool, c, candidate, comes_from, e, exc, extra, extras, frozenset, hash, int, isinstance, other, property, py_version_info, r, requested, rest, self, sorted, str, super, template, valid, with_requires
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py: KeyError, all, base_requirements, bool, c, cause, causes, comes_from, constraint, constraints, e, enumerate, explicit_candidates, extras, finder, frozenset, hashes, i, ican, id, identifier, ignore_installed, ignore_requires_python, incompatibilities, incompatible_ids, int, ireqs, isinstance, key, len, link, list, lookup_cand, make_install_req, parent, parts, prefers_installed, preparer, property, py_version_info, r, req, requested_extras, reversed, root_ireqs, self, set, sorted, sp, str, use_user_site, v, versions_set, wheel_cache, yanked_versions_set
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py: NotImplementedError, any, bool, c, func, get_infos, id, incompatible_ids, installed, int, prefers_installed, self, set, version, versions_found
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py: KeyError, StopIteration, any, backtrack_causes, bool, candidate, constraints, d, default, float, identifier, ignore_dependencies, incompatibilities, information, int, ireq, ireqs, iter, mapping, min, name, next, op, open_bracket, parent, r, requirement, requirement_or_candidate, requirements, self, specifier, specifier_set, staticmethod, str, upgrade_strategy, user_requested, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py: candidate, criterion, index, int, parent, req, req_info, requirement, self, state, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py: bool, candidate, e, frozenset, ireq, len, match, property, s, self, specifier, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py: KeyError, bool, c, candidate, check_supported_wheels, child, e, finder, force_reinstall, ignore_dependencies, ignore_installed, ignore_requires_python, int, item, key, leaf, len, make_install_req, max, node, path, preparer, py_version_info, requirement_keys, resolver, root_reqs, self, set, sorted, str, super, upgrade_strategy, use_user_site, wheel_cache
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\appdirs.py: appname, bool, roaming, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\compat.py: ImportError, OSError, bool, hasattr, int, path, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\compatibility_tags.py: abis, actual_arch, arch, arch_prefix, arch_sep, arch_suffix, c, impl, int, len, major, map, minor, name, p, set, str, supported, version_info
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\datetime.py: bool, day, int, month, year
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\deprecation.py: Warning, category, feature_flag, file, filename, format_str, gone_in, int, issubclass, issue, line, lineno, reason, replacement, str, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py: bool, direct_url, isinstance, link, link_is_in_wheel_cache, name, requested_revision, source_dir, str, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\egg_link.py: egg_link_name, path_item, raw_name, site, sites, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\encoding.py: BOMS, bom, bytes, data, len, line, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\entrypoints.py: args, int, parts, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\filesystem.py: FileExistsError, OSError, PermissionError, bool, f, filename, files, float, hasattr, int, kwargs, pattern, range, root, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\filetypes.py: BZ2_EXTENSIONS, TAR_EXTENSIONS, XZ_EXTENSIONS, ZIP_EXTENSIONS, bool, name, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\glibc.py: AttributeError, ImportError, OSError, ValueError, isinstance, str, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\hashes.py: NotImplemented, TypeError, ValueError, alg, bool, bytes, chunk, chunks, digest, digest_list, digests, file, got, hash, hash_name, hashes, hex_digest, int, isinstance, len, object, open, other, path, property, self, sorted, str, sum, super, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\logging.py: BaseException, BrokenPipeError, Exception, OSError, add_timestamp, args, bool, console, exc, exc_class, getattr, int, isinstance, kwargs, levelno, line, no_color, num, options, record, rich_renderable, self, str, stream, super, tuple, user_log_file, verbosity
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\misc.py: AttributeError, BaseException, Exception, IndexError, OSError, TypeError, ValueError, action, args, auth, backend_path, block, blocksize, bool, build_backend, bytes, classmethod, cls, col, config_holder, dict, dir, e, exc_info, f, file, filter, float, func, getattr, handler, head, ignore_errors, input, int, isinstance, iter, key, len, map, max, message, metadata_directory, modifying_pip, msg, named, new, old, open, options, orig_stream, other, port, pred, print, property, python_executable, range, req, resolve_symlinks, row, runner, scheme, sdist_directory, secret, self, sequential, setattr, size, source_dir, str, stream_name, super, t1, t2, tail, transform_netloc, tuple, type, url_without_auth, value, wheel_directory, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\models.py: NotImplemented, bool, defining_class, hash, int, isinstance, key, method, other, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\packaging.py: bool, extra, int, map, req_string, requires_python, str, version_info
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\setuptools_build.py: bool, build_options, destination_dir, egg_info_dir, global_options, home, no_user_config, prefix, setup_py_path, str, unbuffered_output, use_user_site
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\subprocess.py: Exception, ValueError, arg, args, bool, cmd, command_args, command_desc, cwd, err, err_line, exc, extra_environ, int, isinstance, list, log_failed_cmd, message, name, on_returncode, out, out_line, show_stdout, spinner, stdout_only, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\temp_dir.py: BaseException, OSError, bool, candidate, classmethod, cls, errors, ex, exc_val, func, globally_managed, i, ignore_cleanup_errors, kind, len, name, old_tempdir_manager, original, property, range, root, self, stack, str, super, type, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\unpacking.py: AttributeError, Exception, ImportError, KeyError, bool, content_type, destfp, directory, exc, flatten, info, int, location, member, open, paths, str, target
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\urls.py: ValueError, len, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\virtualenv.py: OSError, bool, f, getattr, hasattr, line, open, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\wheel.py: KeyError, RuntimeError, UnicodeDecodeError, ValueError, bytes, dist_info_dir, e, int, len, map, name, p, s, source, str, tuple, wheel_data, wheel_zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\_jaraco_text.py: StopIteration, filter, iter, iterable, line, map, next, str, text
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\utils\_log.py: args, kwargs, msg, name, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\vcs\bazaar.py: bool, classmethod, cls, dest, int, location, rev, rev_options, self, staticmethod, str, super, user_pass, verbosity, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\vcs\git.py: IndexError, ValueError, bool, classmethod, cls, dest, fragment, getattr, int, is_branch, len, location, netloc, path, query, ref_name, ref_sha, remote, scheme, self, staticmethod, str, super, user_pass, verbosity
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\vcs\mercurial.py: OSError, bool, classmethod, cls, config_file, dest, exc, int, location, open, rev, rev_options, self, staticmethod, str, super, verbosity
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\vcs\subversion.py: ValueError, bool, classmethod, cls, d, dest, dirs, dirurl, extra_args, f, int, len, list, localrev, m, map, max, netloc, open, password, rev_options, scheme, self, staticmethod, str, super, tuple, user_pass, username, verbosity
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_internal\vcs\versioncontrol.py: Exception, FileNotFoundError, NotImplementedError, PermissionError, ValueError, args, backend, bool, classmethod, cls, cwd, dest, drive, extra_environ, extra_ok_returncodes, hasattr, int, len, list, log_failed_cmd, max, netloc, on_returncode, path, project_name, property, query, remote_url, repo, repo_dir, repo_root, secret_password, secret_url, self, show_stdout, spinner, staticmethod, stdout_only, str, super, url1, url2, user_pass, username, vc_class, vcs_backend, verbosity
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\six.py: AttributeError, ImportError, KeyError, NameError, OverflowError, TypeError, ValueError, any, arg, args, assigned, attr, bases, basestring, bs, buf, bytes, chr, classmethod, cls, d, delattr, doc, encoding, enumerate, exec, file, fullname, fullnames, func, getattr, globals, hasattr, i, importer, int, isinstance, it, iter, klass, kw, kwargs, len, long, meta, move, name, obj, object, old, old_mod, ord, s, self, setattr, six_module_name, slots_var, spec, str, super, tp, type, unbound, unicode, updated, wrapped
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\typing_extensions.py: AssertionError, AttributeError, DeprecationWarning, Ellipsis, ImportError, NotImplemented, TypeError, ValueError, Warning, a, all, annotation_key, any, arg, attr, b, base, bool, bound, bytearray, bytes, callable, category, classmethod, cls, cls_or_fn, complex, constraints, contravariant, covariant, d, default, defaults, depth, dict, doc, eq_default, field_name, field_specifiers, float, frozen_default, frozenset, func, g, getattr, getitem, globalns, hasattr, hash, include_extras, infer_variance, instance, int, isinstance, issubclass, k, key, kw_only_default, kwds, left, len, list, localns, mcls, memoryview, mro_entries, n, namespace, obj, object, order_default, other, p, pair, print, property, repr, right, self, set, setattr, stacklevel, staticmethod, str, sum, super, total, tp, tuple, type, type_param, type_params, typename, typevarlike, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\__init__.py: ImportError, base, globals, head, locals, modulename, setattr
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py: args, bool, bytes, cache, cache_etags, cacheable_methods, cert, controller_class, float, heuristic, int, kw, proxies, request, self, serializer, str, stream, super, timeout, tuple, type, verify
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\cache.py: NotImplementedError, bytes, init_dict, int, key, self, str, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\controller.py: Exception, IndexError, KeyError, ValueError, body, bool, bytes, cache, cache_etags, cc_directive, classmethod, cls, dict, headers, int, isinstance, k, len, max, query, request, required, response, response_headers, retval, self, serializer, status_codes, str, tuple, typ, uri, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py: AttributeError, amt, bool, bytes, callback, closed, data, getattr, int, memoryview, name, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py: dict, dt, kw, max, min, resp, response, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py: AttributeError, TypeError, ValueError, body_file, bytes, dict, getattr, headers, k, len, request, response, response_headers, self, str, v, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py: bool, cache_etags, cacheable_methods, controller_class, heuristic, serializer, sess, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py: cache_controller, print
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py: FileNotFoundError, ImportError, OSError, body, bool, bytes, data, directory, dirmode, fh, filecache, filemode, filename, fmode, forever, hasattr, int, list, open, path, self, staticmethod, str, suffix, type, url, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py: bytes, conn, expires, int, isinstance, key, self, str, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\certifi\core.py: data, encoding, open, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\certifi\__main__.py: print
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\big5prober.py: property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\chardistribution.py: bool, byte_str, bytearray, bytes, char_len, float, int, second_char, self, super, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\charsetgroupprober.py: byte_str, bytearray, bytes, float, lang_filter, prober, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\charsetprober.py: NotImplementedError, buf_char, bytearray, bytes, curr, enumerate, float, lang_filter, memoryview, property, self, staticmethod, str, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\codingstatemachine.py: c, int, property, self, sm, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\codingstatemachinedict.py: dict, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\cp949prober.py: property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\enums.py: classmethod, int
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\escprober.py: byte_str, bytearray, bytes, c, coding_sm, float, lang_filter, len, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\eucjpprober.py: byte, byte_str, bytearray, bytes, enumerate, float, i, max, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\euckrprober.py: property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\euctwprober.py: property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\gb2312prober.py: property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\hebrewprober.py: bool, bytearray, bytes, c, cur, int, logical_prober, property, self, str, super, visual_prober
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\johabprober.py: property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\jpcntx.py: bool, byte_str, bytearray, bytes, float, int, len, num_bytes, order, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\latin1prober.py: bytearray, bytes, c, float, int, max, property, self, str, sum, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\macromanprober.py: bytearray, bytes, c, float, int, max, property, self, str, sum, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\mbcharsetprober.py: byte, byte_str, bytearray, bytes, enumerate, float, i, lang_filter, self, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\mbcsgroupprober.py: lang_filter, self, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\resultdict.py: dict, float, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\sbcharsetprober.py: bool, bytearray, bytes, char, float, int, is_reversed, model, name_prober, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\sbcsgroupprober.py: self, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\sjisprober.py: byte, byte_str, bytearray, bytes, enumerate, float, i, max, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\universaldetector.py: bool, bytearray, bytes, group_prober, int, isinstance, lang_filter, prober, property, self, should_rename_legacy
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\utf1632prober.py: bool, byte_str, bytearray, bytes, c, float, int, max, pair, property, quad, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\utf8prober.py: byte_str, bytearray, bytes, c, float, property, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\__init__.py: TypeError, bool, bytearray, bytes, ignore_threshold, isinstance, len, p, prober, probers, result, results, should_rename_legacy, sorted, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\cli\chardetect.py: argv, bool, bytearray, bytes, f, lines, minimal, name, print, should_rename_legacy, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\chardet\metadata\languages.py: ValueError, bool, charsets, iso_code, k, name, self, set, sorted, str, super, use_ascii, v, wiki_start_pages
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\ansi.py: code, dir, getattr, mode, n, name, object, self, setattr, str, title, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\ansitowin32.py: AttributeError, Exception, ValueError, autoreset, command, converter, dict, end, getattr, int, len, match, name, object, p, param, paramstring, property, self, start, state, tuple, wrapped, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\initialise.py: AttributeError, ValueError, any, args, autoreset, convert, kwargs, strip, wrap
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\win32.py: AttributeError, ImportError, adjust, any, attr, attrs, bool, h, self, start, stream_id, title
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\winterm.py: ImportError, OSError, TypeError, fd, light, object, on_stderr, self, title, value, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\tests\ansitowin32_test.py: AttributeError, ImportError, a, args, autoreset, b, code, convert, datum, expected, fp, object, self, stack, winterm
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\tests\ansi_test.py: self, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\tests\initialise_test.py: ImportError, ValueError, isinstance, len, mockATW32, mockRegister, native_ansi, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\tests\isatty_test.py: self, stream
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\tests\utils.py: name, stream
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\colorama\tests\winterm_test.py: ImportError, mockWin32, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\compat.py: AttributeError, ImportError, KeyError, LookupError, NameError, StopIteration, SyntaxError, TypeError, UnicodeDecodeError, ValueError, any, args, basestring, bytes, cert, classmethod, cls, cmd, config, dict, dict_delitem, dict_setitem, dir, dn, e, ext, fillvalue, fn, frag, get_ident, getattr, hasattr, hostname, id, input, int, isinstance, iter, iterable, k, kwds, leftmost, len, line, list, map, mapping, maps, max_wildcards, mode, node, obj, object, orig_enc, property, readline, remainder, repr, set, setattr, staticmethod, str, sub, tb, thefile, tuple, type, unicode, user_function, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\database.py: Exception, IOError, KeyError, LookupError, ValueError, absolute, adjs, c, category, checksum, classmethod, destination, distribution, dists, dry_run, e, entry, env, fp, getattr, hasattr, hash, include_egg, isinstance, k, key, kwargs, label, len, level, list, metadata_filename, n, ns, object, open, other, p_name, p_ver, paths, pred, property, provider, range, record_reader, relative, relative_path, req_attr, requirement, resources_reader, row, self, set, skip_disconnected, sorted, str, stream, succ, super, t, type, v, value, writer, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\index.py: ImportError, OSError, data_filename, destfile, dfp, digest, doc_dir, f, filename, filetype, frag, getattr, input_data, int, isinstance, k, key, len, list, metadata, name, netloc, object, open, operator, outbuf, params, pyversion, query, reporthook, req, scheme, self, sign_password, signature_filename, signer, sink, str, stream, tuple, url, v, value, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\locators.py: Exception, ImportError, NotImplementedError, UnicodeError, algo, b, code, distpath, ext, fp, frag, frozenset, getattr, hasattr, infos, isinstance, k, kwargs, len, link, list, locator, locators, msg, n, name1, name2, netloc, num_workers, object, ord, p, params, prereleases, project_name, property, pyver, query, range, referrer, reqt, requirement, root, self, set, sorted, super, timeout, type, url1, url2, v, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\manifest.py: anchor, d, directive, dirpattern, end, f, is_regex, isinstance, len, list, name, object, parent, path, path_tuple, pattern, prefix, self, set, start, str, wantdirs, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\markers.py: Exception, NotImplementedError, SyntaxError, dict, e, execution_context, expr, hasattr, info, isinstance, marker, o, object, rest, s, self, str, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\metadata.py: AttributeError, IndexError, KeyError, NotImplementedError, TypeError, ValueError, any, attr, controller, dict, entries, entry, exclusions, f, field, fileob, fileobj, fileobject, filepath, filesafe, for_filename, hasattr, int, isinstance, k, kwargs, legacy, len, list, lk, maker, mapping, object, ok, open, other, path, pattern, property, r, requirements, self, skip_missing, skip_unknown, sorted, strict, tuple, u, v, val, warnings
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\resources.py: AttributeError, ImportError, IndexError, f, getattr, hasattr, isinstance, len, name, object, open, package, resource_name, self, set, sorted, staticmethod, str, super, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\scripts.py: Exception, IOError, OSError, UnicodeDecodeError, ValueError, add_launchers, dict, dn, e, encoding, env, exename, fileop, fp, int, kind, len, names, object, open, options, property, self, set, source_dir, specification, specifications, target_dir, value, zf
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\util.py: Exception, ImportError, KeyError, OSError, SyntaxError, ValueError, abs_base, abs_path, allowed_chars, append, archive_filename, base, bits, callable, check, cmd, con, curval, default, dict, directory, dotted_path, dry_run, duration, e, edges, eh, encoding, enumerate, error_prompt, event, exc, exports, f, files, final, float, force, func, getattr, h, hasattr, hashed_invalidation, host, incr, infile, instream, int, isinstance, iter, k, key, len, list, marker_string, mask, maxval, member, min, minval, module_name, netloc, node, o, obj, object, open, optimize, other, outfile, path_glob, pathname, pred, project_name, prompt, property, req, resources_root, reversed, rhs, rules, seconds, self, seq, set, setattr, sorted, source, specification, str, subscriber, succ, super, target, tarinfo, tuple, type, unit, version, zf
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\version.py: NotImplementedError, TypeError, ValueError, absent, any, build, c, constraint, dict, getattr, hash, i, int, isinstance, key, len, major, matcher, minor, name, object, op, operator, orig, other, pat, patch, property, repl, self, set, str, suggester, t, tuple, type, v, vn
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\wheel.py: AttributeError, Exception, ImportError, KeyError, ValueError, append, archive_record_path, bf, bwf, current_version, data_after_shebang, dest_dir, dict, dirname, dirs, enumerate, f, fd, fullname, getattr, hasattr, int, isinstance, kind, kwargs, len, list, maker, match, modifier, name, newdigest, o, object, open, original_version, property, range, reader, record_path, relpath, root, self, set, sign, sorted, str, suffix, t, tuple, v, value, where, writer, zf, zinfo
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distlib\__init__.py: Exception, ImportError, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\distro\distro.py: DeprecationWarning, FileNotFoundError, ImportError, KeyError, OSError, ValueError, attribute, best, bool, bytes, bytestring, dict, distro_release_file, f, fp, full_distribution_name, include_lsb, include_oslevel, include_uname, k, len, line, lines, list, major, minor, obj, open, os_release_file, pretty, release_file, root_dir, self, staticmethod, str, table, token, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\idna\codec.py: bool, bytes, data, errors, final, int, label, len, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\idna\compat.py: NotImplementedError, bytearray, bytes, decode, encode, label, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\idna\core.py: IndexError, UnicodeDecodeError, UnicodeEncodeError, UnicodeError, ValueError, bool, bytearray, bytes, char, check_ltr, chr, cp, domain, enumerate, i, idx, int, isinstance, len, ord, pos, range, repr, script, std3_rules, str, strict, transitional, uts46
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\idna\intranges.py: bool, end, i, int, int_, left, len, list_, r, range, right, sorted, start, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\idna\uts46data.py: int, str, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\msgpack\exceptions.py: Exception, OverflowError, ValueError, extra, self, unpacked
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\msgpack\ext.py: AttributeError, TypeError, ValueError, b, bytes, cls, code, divmod, dt, hash, int, isinstance, len, long, object, other, self, staticmethod, super, type, unix_ns, unix_sec
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\msgpack\fallback.py: ImportError, OverflowError, RuntimeError, StopIteration, TypeError, ValueError, autoreset, bool, bytearray, callable, check_type_strict, d, default, dict, e, execute, ext_hook, f, file_like, float, fmt, hasattr, int, isinstance, k, kwargs, len, list, list_hook, long, max, memoryview, min, nest_limit, next_bytes, o, object, object_hook, object_pairs_hook, packed, pairs, raise_outofdata, range, raw, read_size, self, size, str, strict_map_key, strict_types, t, timestamp, tuple, type, typecode, use_bin_type, use_list, use_single_float, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\msgpack\__init__.py: ImportError, kwargs, o, stream
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\markers.py: NotImplementedError, ValueError, all, any, bool, e, environment, first, groups, i, info, isinstance, item, len, lhs, list, m, marker, markers, name, op, oper, results, rhs, self, str, t, tuple, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\requirements.py: ValueError, e, parts, requirement_string, s, self, set, sorted, str, t
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\specifiers.py: DeprecationWarning, NotImplemented, ValueError, all, any, bool, filtered, fn, frozenset, getattr, hash, int, isinstance, iter, left, left_split, len, list, max, object, op, operator_callable, padded_prospective, padded_spec, parsed, property, result, right, right_split, s, segment, self, set, sorted, spec_str, specifiers, str, super, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\tags.py: INTERPRETER_SHORT_NAMES, NotImplemented, ValueError, bool, cpu_arch, explicit_abi, frozenset, hasattr, hash, id, int, interpreters, is_32bit, isinstance, len, list, major_version, map, minor, minor_version, object, other, platform_, property, range, self, set, str, string, tag, tuple, version_str, warn
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\utils.py: ValueError, int, isinstance, len, sep, str, version_part, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\version.py: DeprecationWarning, NotImplemented, ValueError, bool, bytes, hash, i, int, isinstance, len, list, object, other, property, reversed, s, self, str, tuple, version, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\_manylinux.py: AssertionError, AttributeError, ImportError, OSError, RuntimeWarning, TypeError, ValueError, arch, bool, bytes, f, file, fmt, glibc_major, glibc_max, hasattr, int, isinstance, linux, open, range, self, str, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\_musllinux.py: KeyError, OSError, arch, bytes, e_fmt, e_phentsize, e_phnum, e_phoff, executable, fmt, i, int, len, minor, n, open, output, p_filesz, p_fmt, p_idx, p_offset, p_type, print, range, stack, str, t, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\packaging\_structures.py: bool, hash, int, isinstance, object, other, repr, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py: AssertionError, AttributeError, DeprecationWarning, Exception, IOError, ImportError, KeyError, NameError, NotADirectoryError, NotImplementedError, OSError, PermissionError, RuntimeError, RuntimeWarning, SyntaxError, SystemError, TypeError, UnicodeDecodeError, UserWarning, ValueError, Warning, any, archive_name, attr, base, basename, by_key, callback, callbacks, child, classes, classmethod, compile, dep, dict, dir, dist_spec, distribution_finder, e, e_k_b_n_c, enumerate, ex, exc, exec, existing, ext, extra, extras_spec, f, fallback, fid, file_path, filter, float, frozenset, full_env, getattr, globals, hasattr, hash, importer_type, insert, installer, int, isinstance, iter, k, kw, kwargs, len, list, loader_type, locals, location, map, modname, moduleOrReq, module_name, namespace, namespace_handler, new_requirement, next, normalized_to_canonical_keys, ob, object, only, open, orig_path, other, outf, package, packageName, package_name, package_or_requirement, pkg, plugin_env, precedence, project, property, provided, provider_factory, py_version, python, r, ref, registry, replace, replace_conflicting, repr, req_spec, required, requirement, requirement_string, resource_name, script_name, self, set, setattr, sorted, src, staticmethod, str, stream, strs, subitem, super, t, tempname, text, tmpnam, tuple, type, v, val, vartype, zfile, zip_stat
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\android.py: Exception, property, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\api.py: appauthor, appname, base, bool, ensure_exists, list, multipath, opinion, property, roaming, self, str, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\macos.py: property, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\unix.py: RuntimeError, env_var, fallback_tilde_path, int, key, p, property, self, str, stream
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\windows.py: ImportError, NotImplementedError, ValueError, any, c, csidl_name, directory, getattr, hasattr, opinion_value, ord, property, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\__init__.py: appauthor, appname, bool, ensure_exists, multipath, opinion, roaming, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\platformdirs\__main__.py: getattr, print, prop
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\cmdline.py: AttributeError, BrokenPipeError, Exception, ImportError, KeyboardInterrupt, ValueError, any, arg, args, bool, err, exts, f_str, f_strs, filenames, fname, fopts, fullname, hasattr, i, indent_increment, infp, isinstance, k, len, max_help_position, mimetypes, names, o_str, o_strs, open, opt, p_opt, print, prog, requested_items, self, set, v, value, vars, what
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\console.py: color_key, d, l, text, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\filter.py: NotImplementedError, TypeError, f, filter_, filters, getattr, hasattr, lexer, options, self, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatter.py: isinstance, options, self, str, style, tokensource
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\lexer.py: Exception, ImportError, IndexError, NotImplementedError, StopIteration, ValueError, abs, action, arg, args, bases, bom, c, callable, cls, context, d, e, encoding, endpos, enumerate, err, hasattr, i, index, int, isinstance, istate, it_token, it_value, item, iter, kwargs, kwds, len, lexer, list, match, mcs, n, next, options, prefix, print, r, repr, rexmatch, self, sorted, stack, state, staticmethod, str, suffix, sum, t, tdef, tuple, type, unfiltered, unprocessed, v, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\modeline.py: buf, i, l, len, max_lines, range
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\plugin.py: ImportError, OSError, entrypoint, group_name, hasattr
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\regexopt.py: group, len, letters, list, m, open_paren, s, sorted
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\scanner.py: RuntimeError, flags, len, pattern, property, self, text
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\sphinxext.py: Exception, app, bytes, c, classname, column, columns, data, fn, getattr, isinstance, l, len, lexers, max, name, print, row, self, set, sorted, url, x, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\style.py: bases, bool, cls, dct, len, list, mcs, name, set, styledef, text, token, ttype, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\token.py: getattr, isinstance, item, len, other, s, self, set, setattr, ttype, tuple, type, val
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\unistring.py: a, arg, args, b, char_list, chr, code, fp, globals, len, open, ord, range, sorted
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\util.py: Exception, IndexError, KeyError, LookupError, NotImplementedError, TypeError, UnicodeDecodeError, ValueError, allowed, already_seen, bool, c, default, f, float, getattr, hash, i, indent_level, int, isinstance, it, line, list, map, max, min, normcase, obj, options, optname, raw, repr, self, seq, set, staticmethod, str, term, tuple, var_name, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\__init__.py: TypeError, code, formatter, getattr, isinstance, issubclass, lexer, outfile, tokens, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\__main__.py: KeyboardInterrupt
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py: Exception, TypeError, default, end, filtername, getattr, i, isinstance, issubclass, len, match, name, options, range, self, set, setattr, specialttype, start, str, stream, tag, ttype, wschar, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\bbcode.py: ndef, options, outfile, self, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\groff.py: char, color, i, len, ndef, options, outfile, range, self, set, sorted, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\html.py: AttributeError, ImportError, KeyError, OSError, RuntimeError, ValueError, abs, base, bytes, cf, color, dict, enumerate, err, extension, inner, inner_line, int, isinstance, len, level, lineno, linenumber, list, ndef, open, options, ord, outfile, part, piece, print, property, range, repr, self, set, str, t, table, text, token, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\img.py: Exception, ImportError, NotImplementedError, OSError, ValueError, basename, bold, dict, enumerate, err, f, fail, font_dir, font_name, font_size, hasattr, int, keyname, len, line, linenumber, max, maxlineno, oblique, options, outfile, p, pos, posno, range, self, stdout, str, stylename, styles, suffix, temp_width, text, text_bg, text_fg, tokensource, val
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\irc.py: len, line, options, outfile, self, str, text, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\latex.py: KeyError, a, abs, b, col, commandprefix, definition, dict, enumerate, i, i2, int, it, lang, left, len, line, ndef, options, part, pred, range, reversed, right, self, sep1, sep2, step, t, t2, tokensource, v, v2
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\other.py: KeyError, TypeError, ValueError, options, self, text, tokensource, ttype, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\pangomarkup.py: options, ord, outfile, self, style, stylebegin, styleend, table, text, token, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\rtf.py: c, color, int, options, ord, outfile, self, str, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\svg.py: int, options, outfile, part, self, text, tokensource, ttype
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\terminal.py: line, options, outfile, self, tokensource, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\terminal256.py: KeyError, ValueError, bg, bold, color, fg, i, int, italic, len, line, ndef, off, on, options, outfile, range, self, str, tokensource, underline, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py: AttributeError, Exception, OSError, alias, aliases, err, exec, f, filename, filenames, formatter, formatter_name, formattername, getattr, glob, list, modname, module_name, name, open, options, self, setattr
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\lexers\python.py: index, options, self, super, text, token, ttype, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py: AttributeError, Exception, OSError, aliases, bytes, err, exec, f, filename, filenames, getattr, glob, isinstance, item, key, len, lexer, lexer_name, lexername, list, lname, mimetypes, modname, module_name, name, open, options, plugins, self, set, setattr, sorted, str, t
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py: AttributeError, ImportError, found_name, getattr, name, style
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\actions.py: args, attrName, attrValue, attr_dict, classname, k, l, locn, method_call, n, namespace, object, repl_str, s, self, strg, t, tokens, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\common.py: Combine, FollowedBy, LineEnd, Literal, OneOrMore, Opt, ParseException, ParseResults, ParserElement, Regex, ValueError, White, Word, float, fmt, hexnums, identbodychars, identchars, int, isinstance, l, ll, nums, printables, quoted_string, s, ss, staticmethod, str, sum, t, token_map, tokens, tt, v, vars, ve
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\core.py: AttributeError, DeprecationWarning, Ellipsis, Exception, HIT, ImportError, IndexError, KeyError, MISS, NotImplemented, NotImplementedError, ParseBaseException, ParseException, ParseFatalException, ParseSyntaxException, RecursiveGrammarException, RuntimeError, TypeError, UserWarning, ValueError, adjacent, all, allResults, allow_trailing_delim, any, args, as_group_list, as_keyword, as_match, asdict, aslist, body_chars, bool, break_flag, bytes, c, cache_hit, cache_size_limit, callPreParse, callable, caseless, chars, charset, chr, class_kwargs, classmethod, cls, cmd_line_warn_options, col, colno, combine, convert_whitespace_escapes, copy_defaults, cur_, debug, default, delim, diag_enum, diag_file, dict, doActions, do_actions, e, embed, encoding, end_quote_char, endloc, enumerate, err, esc_char, esc_quote, exact, exception_action, exclude_chars, expr1, exprs_arg, exprtokens, fail_on, failure_tests, flag, flags, fns, force, frm, full_dump, func, getattr, grouped, hasattr, hex, i, id, ident_chars, ie, ignore_fn, include, include_separators, init_chars, instance, int, isinstance, issubclass, iter, join_string, k, kwargs, l, len, line, lineno, list, list_all_matches, loc1, loc_, locals, mat, match, matchString, max_limit, max_matches, max_mismatches, maxsplit, message, minElements, multiline, n, new_loc, new_peek, next, nextLoc, notChars, not_chars, o, obj, offset, open, optElements, ord, output_html, overlap, p, paArgs, parseElementList, parse_action_exc, parse_all, part, pattern, pbe, pe, pfe, post_parse, prev, prev_loc, prev_peek, prev_result, print, print_results, property, quoteChar, raise_fatal, range, recursive, ref_col, repl, replace_with, repr, resultlist, reversed, s_m, savelist, self, seq, setattr, show_groups, show_results_names, skipto_arg, slice, sorted, src, start_action, staticmethod, str, str_type, success_action, sum, super, te, test_line, test_string, tmptokens, tok, tokenlist, tokn, toks, tuple, type, unquote_results, v, var, vars, vertical, w_action, w_category, w_message, w_module, warn_env_var, warn_opt, warning_type, with_line_numbers, word_chars, ws, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\exceptions.py: Exception, classmethod, cls, elem, enumerate, exc, ff, id, int, isinstance, len, loc, marker_string, msg, parseElementList, pe, property, pstr, self, set, staticmethod, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\helpers.py: And, CaselessKeyword, CaselessLiteral, CharsNotIn, Combine, DelimitedList, Diagnostics, Dict, Empty, Enum, FollowedBy, Forward, Group, Iterable, Keyword, LineEnd, List, Literal, MatchFirst, NoMatch, OneOrMore, Opt, ParseAction, ParseException, ParserElement, Regex, SkipTo, Suppress, TokenConverter, Tuple, TypeError, Union, ValueError, Word, ZeroOrMore, a, all, allow_trailing_delim, alphanums, alphas, any, any_close_tag, any_open_tag, arity, as_keyword, as_string, b, backup_stacks, base_expr, blockStatementExpr, bool, caseless, col, combine, dbl_quoted_string, delim, empty, enumerate, expr, ignore_expr, indent, indentStack, instring, int, int_expr, isinstance, j, k, key, l, len, list, ll, loc, max, min, nums, opExpr1, opExpr2, op_list, operDef, other, pa, printables, quoted_string, re_flags, remove_quotes, rightLeftAssoc, s, self, str, str_type, suppress_GT, suppress_LT, sym, t, tag_str, tt, tuple, use_regex, v, value, vars, warnings, xml
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\results.py: AttributeError, Exception, IndexError, KeyError, TypeError, a, any, bool, bytes, classmethod, cls, default_value, dict, dir, enumerate, full, inAccumNames, include_list, indent, ins_string, int, isinstance, item, itemseq, iter, j, k, key, kwargs, len, list, modal, next, obj, object, occurrences, other, p1, p2, par, position, range, repr, res, sep, set, slice, sorted, state, str, str_type, type, value, vlist, vv
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\testing.py: Exception, bool, c, dict, enumerate, exc_type, exp, expand_tabs, expected, expected_parse_results, expr, getattr, i, int, isinstance, issubclass, len, line, list, mark_spaces, max, min, msg, name, next, ord, print, range, rpt, run_test_results, run_test_success, run_tests_report, self, staticmethod, str, test_string, type, u, value, verbose, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\unicode.py: any, c, cc, chr, filter, fn, getattr, hasattr, int, obj, range, rr, self, set, sorted, str, superclass, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\util.py: KeyError, ValueError, args, bool, c, capacity, chars, chr, classmethod, cls, compat_name, dict, dname, getattr, hasattr, int, isinstance, iter, key, kwargs, len, list, ll, loc, name, next, object, ord, other, prev, range, re_escape, self, set, setattr, size, sorted, str, strg, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\__init__.py: globals, int, nv, property, self, str, type, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyparsing\diagram\__init__.py: AttributeError, any, bool, child, classmethod, converted, d, diag, diagram, diagram_kwargs, diagrams, dict, e, element, embed, expr, fn, force, func, id, index, int, isinstance, key, len, list, name_hint, number, parent, parent_index, partial, property, self, set, show_groups, show_results_names, sorted, specification, state, str, super, type, value, vertical, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py: Exception, ValueError, backend_name, build_backend, cmd, config_settings, cwd, f, hook_name, kwargs, message, obj, open, p, path, requested, script, sdist_directory, self, source_dir, source_tree, str, super, td, traceback, wheel_directory
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py: AttributeError, Exception, ImportError, any, config_settings, e, f, getattr, globals, hasattr, kwargs, len, message, metadata_directory, mod_path, obj_path, open, path, path_part, print, sdist_directory, self, super, wheel_directory, whl_zip, zipf
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py: AttributeError
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\adapters.py: ImportError, NotImplementedError, OSError, ValueError, attr, block, bytes, cert, connect, connections, e, err, getattr, isinstance, max_retries, maxsize, password, pool_block, pool_connections, pool_kwargs, pool_maxsize, proxies, proxy_kwargs, read, req, request, self, setattr, state, stream, super, tuple, username, value, verify
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\api.py: data, json, kwargs, method, params, session, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\auth.py: AttributeError, DeprecationWarning, NotImplementedError, all, d, getattr, hasattr, isinstance, kwargs, method, other, r, self, type, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\certs.py: print
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\compat.py: float, int
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\cookies.py: AttributeError, ImportError, KeyError, NotImplementedError, RuntimeError, TypeError, ValueError, args, bool, cookie, cookie_dict, cookie_in_jar, cookies, default, dict, domain, hasattr, headers, int, isinstance, iter, jar, kwargs, list, morsel, name, other, overwrite, path, property, request, response, self, super, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\exceptions.py: DeprecationWarning, IOError, TypeError, ValueError, Warning, args, hasattr, kwargs, self, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\help.py: ImportError, OSError, getattr, print
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\hooks.py: event, hasattr, hook, key, kwargs
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\models.py: AttributeError, LookupError, NotImplementedError, OSError, RuntimeError, TypeError, UnicodeDecodeError, UnicodeError, ValueError, all, any, attr, bool, bytearray, bytes, chunk_size, decode_unicode, delimiter, e, event, field, fragment, getattr, h, hasattr, hook, int, isinstance, k, kwargs, len, link, list, method, name, object, port, property, scheme, self, setattr, state, staticmethod, str, tuple, type, value, ve
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\packages.py: len, list, locals, mod, package
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\sessions.py: KeyError, RuntimeError, StopIteration, ValueError, adapter_kwargs, attr, data, dict_class, files, getattr, header, isinstance, json, k, key, kwargs, len, new_url, next, old_url, params, password, prefix, request_hooks, request_setting, response, self, session_hooks, session_setting, setattr, timeout, username, v, value, yield_requests
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\status_codes.py: code, n, setattr, sorted, title, titles
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\structures.py: NotImplemented, casedkey, default, dict, isinstance, key, keyval, kwargs, len, lowerkey, name, self, str, super, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\utils.py: AttributeError, BaseException, DeprecationWarning, ImportError, KeyError, OSError, TypeError, UnicodeError, ValueError, archive, bool, chr, chunk, cj, content, cookie, data, env_name, f, file_handler, filename, fragment, frozenset, getattr, hasattr, header, header_part, header_validator_index, headers, i, int, ip, is_filename, isinstance, iterator, len, list, max, net, netaddr, new_scheme, o, obj, params, prefix, prepared_request, proxy_ip, proxy_key, query, r, raise_errors, range, request, string, string_ip, string_network, tmp_descriptor, tmp_handler, tmp_name, trust_env, type, uri, val
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\_internal_utils.py: UnicodeEncodeError, bytes, encoding, isinstance, str, string, u_string
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\requests\__init__.py: AssertionError, Exception, ImportError, ValueError, getattr, int, len, list, major, map, minor
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\resolvelib\providers.py: Exception, NotImplementedError, object, provider, reporter, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\resolvelib\reporters.py: object
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\resolvelib\resolvers.py: AttributeError, Exception, IndexError, KeyError, RuntimeError, all, c, candidate, d, e, i, id, k, key, len, list, max_rounds, min, object, p, parent, parents, property, provider, r, range, reporter, repr, req, requirement, round_count, round_index, self, set, super, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\resolvelib\structs.py: KeyError, StopIteration, ValueError, accessor, appends, bool, callable, children, current, f, factory, isinstance, iter, k, key, len, list, mapping, next, object, self, sequence, set, sum, t, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\resolvelib\compat\collections_abc.py: ImportError
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\abc.py: bool, classmethod, hasattr, isinstance, other, print, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\align.py: ValueError, bool, classmethod, cls, count, int, len, line, list, min, options, range, renderable, self, str, vertical
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\ansi.py: StopIteration, ansi_text, bytes, code, end, fd, int, iter, len, link, match, min, next, osc, plain_text, print, self, semicolon, sgr, start, str, terminal_text
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\bar.py: begin, bgcolor, end, float, int, len, max, min, options, self, size, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\box.py: ASCII, ASCII2, ASCII_DOUBLE_HEAD, HEAVY, HEAVY_EDGE, HEAVY_HEAD, MINIMAL, MINIMAL_DOUBLE_HEAD, MINIMAL_HEAVY_HEAD, ROUNDED, SIMPLE, SIMPLE_HEAVY, SQUARE, SQUARE_DOUBLE_HEAD, ValueError, ascii, bool, box_name, edge, getattr, int, iter, last, level, line1, line2, line3, line4, line5, line6, line7, line8, options, parts, safe, self, sorted, str, width, widths
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\cells.py: character, codepoint, int, len, line, lines, max_size, n, ord, position, print, range, reversed, str, sum, text, total, width
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\color.py: Exception, all, b1, b2, back, blue, bool, classmethod, cls, color1, color2, color_24, color_8, color_rgb, component, cross_fade, float, fore, foreground, g1, g2, green, hex_color, int, k, l, len, name, property, r1, r2, red, round, s, self, sorted, str, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\color_triplet.py: blue, float, green, int, property, red, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\columns.py: bool, col_no, column_first, column_lengths, enumerate, equal, expand, i, index, int, isinstance, left, len, list, max, options, range, renderable, renderable_width, right, s, self, sorted, start, str, sum, title, width, widths, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\console.py: AttributeError, BaseException, Exception, NameError, OSError, TypeError, UnicodeEncodeError, ValueError, allow_nan, args, attribs, batch, bool, characters, check_circular, classes, code_format, colors, count, currentframe, data, default, emoji_variant, enable, end, ensure_ascii, enumerate, error, exc_type, file_descriptor, filename, fit, float, font_aspect_ratio, force_interactive, force_jupyter, force_terminal, format, fragments, get_datetime, get_ipython, get_time, getattr, hasattr, hide_cursor, highlight, home, hook, indent, inherit, inline_styles, int, isatty, isinstance, iter, json, justify, k, key, kwargs, len, line_no, links, list, locals, log_locals, log_path, log_time, log_time_format, max, max_frames, max_width, method, min, min_width, name, new_file, new_line_start, new_lines, new_segments, new_size, no_color, object, offset, open, output, pad, password, prompt, property, quiet, range, raw_output, record, refresh_per_second, render_output, repr, rule_no, safe_box, self, sep, show, show_locals, skip_keys, sort_keys, speed, spinner, spinner_style, staticmethod, stderr, str, stream, style_cache, style_rule, stylesheet_rules, suppress, svg_main_code, system, tab_size, text_backgrounds, text_group, title, v, value, word_wrap, write_file
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\constrain.py: int, min, renderable, self, width
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\containers.py: dimension, enumerate, int, iter, len, line, line_index, lines, list, max, next_word, options, overflow, range, renderable, renderables, self, slice, str, sum, tokens, value, width, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\control.py: CONTROL_CODES_FORMAT, CONTROL_ESCAPE, STRIP_CONTROL_CODES, abs, bool, classmethod, cls, code, codes, control_codes, enable, i, int, isinstance, param, parameters, range, self, show, str, text, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\default_styles.py: DEFAULT_STYLES, bool, html, print, str, style_name
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\diagnose.py: name
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\emoji.py: Exception, KeyError, classmethod, len, name, self, sorted, str, text, variant
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\errors.py: Exception
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\filesize.py: base, enumerate, i, int, precision, separator, size, str, suffix, suffixes
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\file_proxy.py: TypeError, file, getattr, int, isinstance, len, line, lines, name, new_line, property, self, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\highlighter.py: TypeError, end, isinstance, len, match, re_highlight, regexes, self, start, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\json.py: Exception, allow_nan, bool, check_circular, classmethod, cls, default, ensure_ascii, error, highlight, indent, int, json_instance, self, skip_keys, sort_keys, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\jupyter.py: ModuleNotFoundError, args, control, exclude, fragments, include, k, kwargs, list, self, str, style, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\layout.py: Exception, KeyError, bool, child, child_and_region, child_height, child_width, int, isinstance, layout_height, layout_lines, layout_name, layout_row, layouts, line, minimum_size, options, property, range, ratio, row, self, size, sorted, splitter, stack, str, text, visible, x, y, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\live.py: BaseException, Exception, ImportError, auto_refresh, bool, dest, exchange, exchange_rate, exchange_rate_dict, float, index, isinstance, len, list, live_table, next, property, range, redirect_stderr, redirect_stdout, refresh_per_second, self, source, str, super, transient, vertical_overflow
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\live_render.py: height, int, last, line, list, options, self, vertical_overflow
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\logging.py: Exception, bool, dict, enable_link_path, exc_traceback, exc_type, exc_value, getattr, hasattr, int, isinstance, keywords, locals_max_length, locals_max_string, log_time_format, markup, omit_repeated_times, record, rich_tracebacks, self, show_level, show_path, show_time, str, super, tracebacks_extra_lines, tracebacks_show_locals, tracebacks_suppress, tracebacks_theme, tracebacks_width, tracebacks_word_wrap
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\markup.py: Exception, IndexError, KeyError, SyntaxError, backslashes, bool, divmod, emoji_variant, end, enumerate, equals, error, escaped, escapes, full_text, index, int, isinstance, len, match, match_parameters, open_tag, property, reversed, self, sorted, spans, start, str, style_stack, tag, tag_text, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\measure.py: classmethod, get_console_width, getattr, int, isinstance, max, max_width, maximum, min, min_width, options, property, renderables, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\padding.py: ValueError, bool, bottom, classmethod, expand, int, isinstance, len, level, line, measure_max, measure_min, min, options, pad, pad_right, pad_top, renderable, self, staticmethod, str, top
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\pager.py: content, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\palette.py: b1, b2, blue1, blue2, colors, enumerate, float, g1, g2, green1, green2, index, int, len, min, number, options, r1, r2, range, red1, red2, repr, self, str, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\panel.py: any, bool, character, classmethod, cls, expand, height, highlight, int, isinstance, line, max, min, options, property, right, safe_box, self, str, subtitle, subtitle_align, title, title_align
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\pretty.py: Exception, ImportError, OSError, TypeError, arg, attr, bool, bytes, callable, capture, child, class_or_tuple, close_brace, container_type, crop, default, depth, dict, empty, enumerate, error, expand_all, field, float, frozenset, get_ipython, getattr, globals, hasattr, id, indent_guides, indent_size, index, insert_line, int, isinstance, iter, justify, key, last, len, list, margin, max, max_depth, max_length, max_string, max_width, name, no_wrap, obj, object, open_brace, options, overflow, property, repr, repr_callable, rich_args, root, self, set, str, token, tuple, type, visited_ids
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\progress.py: BaseException, KeyError, RuntimeWarning, ValueError, all, auto_refresh, b, bar_width, binary_units, bool, bytearray, bytes, classmethod, close_handle, column, columns, compact, complete_style, description, dict, disable, divmod, elapsed_when_finished, encoding, errors, exc_tb, exc_type, exc_val, expand, fields, file, finished_style, finished_text, float, hint, hours, int, isinstance, iter, justify, len, list, map, markup, max, memoryview, min, minutes, newline, next, offset, property, pulse_style, redirect_stderr, redirect_stdout, refresh_per_second, sample, seconds, self, separator, sequence, show_speed, size, sorted, speed_estimate_period, spinner_name, spinner_style, str, suffix, sum, super, table_column, text_format_no_percentage, timestamp, track_thread, transient, unit, value, visible, whence
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\progress_bar.py: animation_time, bool, color_system, finished_style, float, index, int, len, max, min, n, no_color, options, property, pulse, pulse_style, range, self, str, total
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\prompt.py: Exception, ValueError, bool, classmethod, cls, default, error, float, int, isinstance, len, message, no, self, show_choices, show_default, str, stream, type, yes
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\protocol.py: bool, check_object, getattr, hasattr, isinstance, object, repr, rich_visited_set, set, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\region.py: int
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\repr.py: Exception, angular, arg, bool, cls, default, error, getattr, hasattr, isinstance, key, len, name, param, repr, repr_str, self, str, tuple, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\rule.py: IndexError, ValueError, end, int, isinstance, max, options, self, str, title
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\scope.py: bool, float, indent_guides, int, item, key, locals, max_length, max_string, scope, sort_keys, sorted, str, title, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\screen.py: application_mode, bool, height, last, line, options, renderables, self, width
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\segment.py: AssertionError, StopIteration, bool, cache, classmethod, cls, control, cuts, filter, height, include_new_lines, int, iter, len, length, list, max, new_lines, next, pad, post_style, property, segment, segment_style, segments, self, split_segments, str, sum, width
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\spinner.py: KeyError, float, int, isinstance, len, name, options, repr, self, sorted, speed, spinner_name, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\status.py: BaseException, float, property, refresh_per_second, self, speed, spinner_style, status, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\style.py: NotImplemented, ValueError, bit, bit_no, bool, bytes, classmethod, cls, color_system, css, default_style, error, handlers, hash, int, isinstance, iter, key, legacy_windows, new_style, next, obj, original_word, other, property, range, self, sgr, str, style_definition, styles, sum, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\styled.py: options, renderable, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\syntax.py: ANSI_DARK, ANSI_LIGHT, KeyError, NotImplementedError, StopIteration, blend, bool, classmethod, cls, dedent, encoding, end_line, enumerate, ext, first, float, highlight_lines, indent_guides, int, isinstance, iter, justify, left, len, line, line_end, line_number, line_numbers, line_range, line_start, line_token, list, match, max, min, name, next, options, path, position, property, right, self, set, start_line, str, style_map, stylized_range, syntax_line, tab_size, token_type, tuple, word_wrap, wrapped_line
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\table.py: allow_wrap, any, bool, caption, caption_justify, caption_style, cell, classmethod, cls, col, column_index, enumerate, first, first_row, footer, getattr, headers, index, int, isinstance, iter, justify, last, last_cell, last_row, len, line_no, list, max, max_widths, min, min_width, min_widths, next, no_wrap, options, overflow, pad, pad_right, property, range, ratio, raw_cells, renderable, renderables, rendered_cell, row_cell, row_cells, row_styles, safe_box, self, str, sum, title, title_justify, title_style, type, wrapable, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\terminal_theme.py: background, bright, foreground, int, normal, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\text.py: DEFAULT_JUSTIFY, DEFAULT_OVERFLOW, NotImplemented, TypeError, ValueError, allow_blank, amount, bool, callable, case_sensitive, character, classmethod, closing, cls, content, divmod, emoji_variant, enumerate, full_indents, handlers, include_separator, indent_size, index, int, isinstance, key, last, leaving, len, line, line_end, line_no, line_start, list, max, max_width, min, name, new_length, next_offset, object, options, other, output, part, property, range, re_highlight, remaining_space, self, separator, size, slice, sorted, span, span_end, span_start, span_style, stack, step, stop, str, style_cache, style_id, style_prefix, suffix, tokens, tuple, value, width, word, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\theme.py: Exception, bool, classmethod, cls, config_file, encoding, inherit, isinstance, len, name, open, path, print, property, self, sorted, source, str, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\traceback.py: BaseException, Exception, SyntaxError, ValueError, a, any, args, bool, classmethod, cls, enumerate, extra_lines, frame_index, frame_summary, get_ipython, getattr, indent_guides, int, is_syntax, isinstance, iter_locals, key, kwargs, last, len, line_no, list, locals_hide_dunder, locals_max_length, locals_max_string, max, max_frames, min, object, print, range, reversed, self, show_locals, slfkjsldkfj, stacks, str, suppress, suppress_entity, syntax_error, type_, value, width, word_wrap
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\tree.py: CONTINUE, END, FORK, SPACE, StopIteration, bool, expanded, first, hide_root, highlight, index, int, iter, label, last, len, levels, max, max_measure, min_measure, next, options, range, self, stack, sum
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py: KeyError, default_variant, emoji_code, emoji_name, match, str, text, variant
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_fileno.py: Exception, file_like, fileno, getattr, int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_inspect.py: Exception, OSError, TypeError, ValueError, all, attr_name, bool, callable, dir, error, fully_qualified_types_names, getattr, hasattr, help, item, key, len, name, object, object_, paragraph, repr, self, sort, str, title, type, type_, type_name, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_log_render.py: bool, callable, int, len, level, level_width, line_no, link_path, omit_repeated_times, path, renderables, row, self, show_level, show_path, show_time, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_loop.py: StopIteration, bool, iter, next
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_null_file.py: BaseException, bool, int, iter, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_pick.py: bool, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_ratio.py: distributed_total, divmod, edge, edges, enumerate, index, int, len, max, maximum, maximums, min, minimum, minimums, print, ratio, result, round, size, sum, total, value, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_stack.py: item, property, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_timer.py: print, str, subject
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_win32_console.py: Exception, ImportError, attributes, bool, char, classmethod, column, coord, coords, file, int, len, length, new_position, print, property, row, self, std_handle, str, text, title, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_windows.py: AttributeError, ImportError, ValueError, bool, repr
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py: buffer, column, control, control_code, control_codes, int, mode, str, style, term, text, title, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\_wrap.py: bool, divides, end, fold, int, last, len, line, print, start, str, text, width
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\__init__.py: FileNotFoundError, all, allow_nan, args, bool, check_circular, data, default, docs, dunder, end, ensure_ascii, file, help, highlight, indent, int, json, kwargs, methods, obj, objects, private, sep, skip_keys, sort, sort_keys, str, title, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\rich\__main__.py: b1, b2, g1, g2, options, print, r1, r2, range, renderable1, renderable2, round, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\after.py: int, log_level, logger, retry_state, sec_format, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\before.py: int, log_level, logger, retry_state
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\before_sleep.py: BaseException, RuntimeError, bool, exc_info, int, log_level, logger, retry_state, value, verb
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\nap.py: event, float, seconds, self, timeout
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\retry.py: BaseException, Exception, RuntimeError, TypeError, all, any, args_, bool, e, exception_types, isinstance, kwargs_, match, message, other, r, retries, retry_state, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\stop.py: RuntimeError, all, any, bool, event, int, max_attempt_number, max_delay, other, retry_state, self, stops, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\tornadoweb.py: BaseException, args, fn, isinstance, kwargs, self, sleep, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\wait.py: OverflowError, exp_base, float, increment, initial, int, len, max, min, multiplier, other, retry_state, self, start, strategies, sum, super, wait, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\_asyncio.py: BaseException, StopAsyncIteration, TypeError, args, float, isinstance, kwargs, self, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\_utils.py: AttributeError, cb, float, int, isinstance, pos_num, repr, str, time_unit
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tenacity\__init__.py: AttributeError, BaseException, Exception, args, attempt_number, bool, callable, classmethod, cls, dargs, dkw, exc_info, exc_type, exc_value, f, field, first, float, fn, getattr, has_exception, hasattr, id, int, isinstance, kw, kwargs, last_attempt, len, object, property, repr, retry_error_callback, retry_error_cls, retry_object, round, second, self, str, super, traceback, val, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tomli\_parser.py: AttributeError, IndexError, KeyError, TypeError, ValueError, access_lists, array, bool, chars, chr, codepoint, cont_key, dict, e, error_on_eof, expect, flag, float, float_str, frozenset, header, hex_len, i, int, isinstance, k, key, key_parent, key_part, len, list, literal, msg, multiline, parsed_escape, range, recursive, self, str, tuple, val, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tomli\_re.py: day, day_str, hour, hour_str, int, match, micros_str, minute, minute_str, month, month_str, offset_hour_str, offset_minute_str, offset_sign_str, parse_float, sec, sec_str, sign_str, str, year, year_str, zulu_time
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\tomli\_types.py: int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\truststore\_api.py: AttributeError, Exception, ImportError, NotImplementedError, alpn_protocols, bool, bytes, cadata, cafile, capath, cert, certfile, dict, do_handshake_on_connect, hasattr, incoming, int, keyfile, list, npn_protocols, outgoing, password, property, purpose, self, server_hostname, server_side, session, setattr, sock, sock_or_sslobj, str, super, suppress_ragged_eofs, type, unverified_chain, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\truststore\_macos.py: AttributeError, ImportError, MemoryError, NotImplementedError, OSError, args, bytes, cert_chain, cert_data, cf_string_ref, ctx, ctx_ca_certs_der, int, len, list, macos10_16_path, map, name, server_hostname, ssl_context, str, tuple, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\truststore\_openssl.py: bool, bytes, cafile, capath, ctx, list, name, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\truststore\_ssl_constants.py: object, ssl_context, super, type, verify_mode
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\truststore\_windows.py: args, bool, bytes, cert_bytes, cert_chain, ctx, custom_ca_certs, int, len, list, pPeerCertContext, result, server_hostname, ssl_context, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\truststore\__init__.py: ImportError
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\connection.py: AttributeError, BaseException, DeprecationWarning, Exception, ImportError, NameError, ValueError, any, args, assert_hostname, bytearray, bytes, cert_file, e, getattr, hasattr, header, hex, isinstance, k, key_file, key_password, kw, kwargs, len, map, method, object, port, property, self, set, sorted, str, strict, super, timeout, url, v, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py: AttributeError, BaseException, IOError, TypeError, assert_fingerprint, assert_hostname, assert_same_host, block, body, bool, ca_cert_dir, ca_certs, cert_file, cert_reqs, chunked, conn_kw, getattr, hasattr, hpe, httplib_request_kw, isinstance, key_file, key_password, kw, maxsize, object, old_pool, path, pool_timeout, redirect, response_kw, self, ssl_error, ssl_version, str, strict, super, timeout_value, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\exceptions.py: AssertionError, Exception, ValueError, Warning, args, defects, error, expected, length, location, partial, pool, reason, response, retries, self, super, unparsed_data, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\fields.py: UnicodeDecodeError, UnicodeEncodeError, any, cc, ch, classmethod, cls, content_disposition, content_location, default, dict, fieldname, header_formatter, header_name, header_parts, header_value, headers, isinstance, len, match, name, needle, needles_and_replacements, object, range, self, sort_key, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\filepost.py: dict, field, int, isinstance, iter, k, str, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py: KeyError, connection_pool_kw, field, frozenset, header, isinstance, key, key_class, kw, list, num_pools, override, parsed_url, pool_kwargs, proxy_headers, proxy_ssl_context, redirect, self, super, tuple, url, url_scheme, use_forwarding_for_https, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\request.py: NotImplementedError, TypeError, body, content_type, encode_multipart, fields, multipart_boundary, object, self, url, urlopen_kw
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\response.py: DeprecationWarning, IOError, ResponseCls, ValueError, amt, auto_close, b, body, bytearray, bytes, classmethod, d, default, e, enc, enforce_content_length, getattr, hasattr, int, isinstance, len, m, min, mode, modes, msg, name, object, original_response, pool, preload_content, property, r, reason, request_method, request_url, response_kw, retries, reversed, self, set, str, val, version, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\_collections.py: ImportError, KeyError, NotImplementedError, TypeError, args, classmethod, cls, default, dict, dispose_func, hasattr, isinstance, k, key, kwargs, len, line, list, maxsize, message, object, self, super, type, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\__init__.py: DeprecationWarning, ImportError, category, level
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\appengine.py: ImportError, body, bool, e, headers, isinstance, redirect, response_kw, self, str, timeout, url, urlfetch_resp, urlfetch_retries, validate_certificate
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\ntlmpool.py: DeprecationWarning, Exception, NegotiateFlags, ServerChallenge, args, assert_same_host, authurl, body, dict, kwargs, method, pw, redirect, retries, s, self, super, url, user
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py: DeprecationWarning, Exception, ImportError, UnicodeError, args, binary_form, bufsize, cadata, certfile, connection, dict, e, err_no, getattr, hasattr, isinstance, k, keyfile, kwargs, len, map, mode, object, p, peer_cert, prefix, property, protocol, self, sock, str, suppress_ragged_eofs, v, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\securetransport.py: Exception, ImportError, NotImplementedError, ValueError, alpn_protocols, args, binary_form, bufsiz, bufsize, bytes, cadata, cafile, capath, certfile, client_cert, client_key, connection_id, data_length_pointer, do_handshake_on_connect, e, exception, f, hasattr, id, isinstance, keyfile, kwargs, len, max_version, min_version, mode, object, open, p, password, property, protocols, self, server_side, sock, suppress_ragged_eofs, value, verify
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py: ImportError, ValueError, args, connection_pool_kw, e, headers, isinstance, kwargs, len, num_pools, password, proxy_url, self, super, username
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\bindings.py: AttributeError, ImportError, OSError, int, macos10_16_path, map, name, object, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\low_level.py: BaseException, Exception, MemoryError, OSError, bytestring, der_bytes, e, error, f, file_path, index, len, lst, match, new_certs, new_identities, obj, open, path, py_bstr, range, t, tuples, value, ver_maj, ver_min, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\packages\six.py: AttributeError, ImportError, KeyError, NameError, OverflowError, TypeError, ValueError, any, arg, args, assigned, attr, bases, basestring, bs, buf, bytes, chr, classmethod, cls, d, delattr, doc, encoding, enumerate, exec, file, fullname, fullnames, func, getattr, globals, hasattr, i, importer, int, isinstance, it, iter, klass, kw, kwargs, len, long, meta, move, name, obj, object, old, old_mod, ord, s, self, setattr, six_module_name, slots_var, spec, str, super, tp, type, unbound, unicode, updated, wrapped
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\packages\backports\makefile.py: ValueError, encoding, errors, mode, newline, self, set
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\packages\backports\weakref_finalize.py: Exception, args, bool, classmethod, cls, func, i, id, item, kwargs, next, object, property, self, type, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\connection.py: Exception, UnicodeError, address, af, conn, e, getattr, opt, options, port, proto, res, sa, socket_options, socktype, source_address, timeout
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py: ca_cert_data, ca_cert_dir, ca_certs, cert_reqs, destination_scheme, hasattr, proxy_config, proxy_url, ssl_version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\queue.py: item, len, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\request.py: IOError, OSError, ValueError, basic_auth, body, body_pos, disable_cache, frozenset, getattr, isinstance, keep_alive, list, object, proxy_basic_auth, str, type, user_agent
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\response.py: AttributeError, TypeError, ValueError, bytes, defect, getattr, headers, int, isinstance, obj, response, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\retry.py: AttributeError, DeprecationWarning, ValueError, backoff_factor, bool, classmethod, cls, default, dict, error, filter, frozenset, getattr, h, has_retry_after, int, isinstance, item, kw, len, list, method, method_whitelist, min, object, property, raise_on_status, respect_retry_after_header, response, reversed, self, set, status_code, status_forcelist, super, tuple, type, url, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py: ValueError, args, binary_form, byte_view, data, e, encoding, errors, flags, func, hasattr, len, memoryview, mode, newline, self, server_hostname, set, ssl_context, staticmethod, suppress_ragged_eofs, value, view
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py: IOError, ImportError, NotImplementedError, OSError, a, abs, b, bool, bytearray, bytes, ca_cert_data, ca_cert_dir, ca_certs, cadata, cafile, candidate, capath, cert, certfile, cipher_suite, ciphers, e, f, getattr, hasattr, isinstance, key_file, key_password, keyfile, left, len, line, object, open, protocol_version, right, self, server_hostname, server_side, sock, socket, ssl_context, str, tls_in_tls, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py: AttributeError, ImportError, UnicodeError, ValueError, cert, dn, frag, hostname, ipname, isinstance, key, len, map, max_wildcards, repr, str, sub, unicode, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py: TypeError, ValueError, bool, classmethod, cls, connect, float, getattr, isinstance, max, min, name, object, property, read, self, timeout, total, type, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\url.py: AttributeError, ImportError, ValueError, allowed_chars, any, authority, bytearray, cls, d, delims, encoding, end, hex, host_port, i, int, isinstance, label, len, name, ord, percent_encodings, property, range, s, segment, self, set, start, str, super, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\urllib3\util\wait.py: AttributeError, Exception, ImportError, OSError, RuntimeError, args, bool, e, float, hasattr, kwargs, read, rready, sock, t, wready, write, xready
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\webencodings\mklabels.py: ImportError, category, encoding, label, len, max, name, print, repr, string, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\webencodings\tests.py: AssertionError, LookupError, args, exception, fallback_encoding, function, input, kwargs, label, list, name, output, repeat, set
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\webencodings\x_user_defined.py: errors, input, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pip\_vendor\webencodings\__init__.py: LookupError, bom_encoding, chunck, encoding_or_label, errors, final, hasattr, iter, len, next, object, self, string
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\__init__.py: AssertionError, AttributeError, DeprecationWarning, Exception, IOError, ImportError, KeyError, NameError, NotADirectoryError, NotImplementedError, OSError, PermissionError, RuntimeError, RuntimeWarning, SyntaxError, TypeError, UnicodeDecodeError, UserWarning, ValueError, Warning, any, archive_name, attr, base, basename, by_key, callback, callbacks, child, classes, classmethod, compile, dep, dict, dir, dist_spec, distribution_finder, e, e_k_b_n_c, enumerate, exc, exec, existing, ext, extra, extras_spec, f, fallback, fid, file_path, filter, float, frozenset, full_env, getattr, globals, hasattr, hash, importer_type, insert, installer, int, isinstance, iter, k, kw, kwargs, len, list, loader_type, locals, location, map, modname, moduleOrReq, module_name, namespace, namespace_handler, new_requirement, next, normalized_to_canonical_keys, ob, object, only, open, orig_path, other, outf, package, packageName, package_name, package_or_requirement, part, pkg, plugin_env, precedence, project, property, provided, provider_factory, py_version, python, r, ref, registry, replace, replace_conflicting, repr, req_spec, required, requirement, requirement_string, resource_name, script_name, self, set, setattr, sorted, src, staticmethod, str, stream, strs, subitem, super, t, tempname, text, tmpnam, tuple, type, v, val, vars, vartype, zfile, zip_stat
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\extern\__init__.py: ImportError, any, fullname, locals, map, prefix, property, root, root_name, self, set, spec, target, vendor_pkg, vendored_names
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\appdirs.py: ImportError, UnicodeError, c, csidl_name, getattr, map, multipath, object, opinion, ord, print, prop, property, roaming, self, str, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\zipp.py: AttributeError, FileNotFoundError, IsADirectoryError, ValueError, args, at, classmethod, dict, filter, isinstance, kwargs, list, map, minuend, mode, other, p, property, pwd, root, self, set, source, staticmethod, str, strm, subtrahend, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\abc.py: FileNotFoundError, bool, child, encoding, item, path, resource, self, str, strm
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\readers.py: FileNotFoundError, KeyError, NotADirectoryError, ValueError, all, child, exc, file, iter, list, loader, map, module, namespace_path, path, property, resource, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\simple.py: IsADirectoryError, RuntimeError, args, kwargs, map, mode, next, parent, property, reader, self, traversable
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_adapters.py: AttributeError, FileNotFoundError, ValueError, adapter, args, attr, file, getattr, hasattr, iter, kwargs, len, mode, other, package, path, path_parts, property, self, spec
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_common.py: FileNotFoundError, TypeError, cand, fd, getattr, isinstance, package, path, raw_path, str, suffix
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_compat.py: AttributeError, ImportError, TypeError, ValueError, cls, hasattr, package, property, self, spec
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_itertools.py: element, iterable, key, seen, set
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_legacy.py: DeprecationWarning, ValueError, any, args, bool, bytes, encoding, errors, file_name, fp, func, kwargs, name, package, parent, str, traversable
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\jaraco\context.py: Exception, args, bool, branch, dest_ctx, dict, dir, exceptions, func, issubclass, kwargs, open, property, quiet, remover, repo_dir, self, trap, url, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\jaraco\functools.py: TypeError, action, args, bound_method, cache_wrapper, cleanup, eval, exceptions, f, f1, f2, f_args, f_kwargs, float, func1, func2, funcs, getattr, hasattr, isinstance, k, kwargs, map, max, max_rate, method, method_name, more_itertools, namespace, obj, object, param, print, r_args, r_kwargs, range, replace, retries, self, setattr, target, transform, trap, use, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py: ImportError, StopIteration, UnicodeDecodeError, args, bytes, classmethod, cls, filter, hash, identifier, isinstance, iter, iterable, len, line, map, match, maxsplit, min, new, next, object, old, other, para, part, prefix_lines, rest, reversed, s, s1, s2, self, slice, splitter, staticmethod, str, string, sub, subject, suffix, super, text, tuple, value, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\more_itertools\more.py: A, BaseException, DeprecationWarning, IndexError, M, N, RuntimeError, StopIteration, TypeError, ValueError, after, any, args, base_type, before, bool, bytes, callback_kwd, child, chunk, chunk_size, combo, context_manager, cur_idx, d, default, delta, delta_primary, deltas_secondary, details, divmod, e, elem, enumerate, exception, exceptions, f, fillvalue, filter, func, func_else, function, g, getattr, group_tuple, hasattr, hash, i1, i2, initial, int, isinstance, iter, iter_primary, iterable_or_value, iterable_positions, iters_secondary, keep_separator, keyfunc, kwargs, len, levels, limit_seconds, list, longest, map, max, maxlen, maxsplit, min, next, next_item, next_multiple, node, obj, object, objects, offsets, ordering, other, others, p, pred, predicate, property, range, reducefunc, repr, result_index, reverse, reversed, s, scalar_positions, scalar_types, scalars, self, set, sizes, slice, smallest_weight_key, sorted, staticmethod, str, strict, sum, super, tail, target, tmp, tuple, type, val, validator, value_list, w, wait_seconds, weight, window_size, wrapping_args, wrapping_func, wrapping_kwargs, x, x_key, y, y_key, zip, zipped_items
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\more_itertools\recipes.py: DeprecationWarning, ImportError, IndexError, StopIteration, TypeError, ValueError, a, b, bool, cond, default, elem, element, exception, fillvalue, filter, first, func, function, i, index, int, isinstance, iter, iterable, iterables, iterator, key, len, list, listOfLists, map, min, next, predicate, range, set, signal, sorted, start, sum, t1, t2, times, tuple, value, vec1, vec2, x, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\markers.py: NotImplementedError, ValueError, all, any, bool, e, environment, first, groups, i, info, isinstance, item, len, lhs, list, m, marker, markers, name, op, oper, results, rhs, self, str, t, tuple, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\requirements.py: ValueError, e, parts, requirement_string, s, self, set, sorted, str, t
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\specifiers.py: DeprecationWarning, NotImplemented, ValueError, all, any, bool, filtered, fn, frozenset, getattr, hash, int, isinstance, iter, left, left_split, len, list, max, object, op, operator_callable, padded_prospective, padded_spec, parsed, property, result, right, right_split, s, segment, self, set, sorted, spec_str, specifiers, str, super, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\tags.py: INTERPRETER_SHORT_NAMES, NotImplemented, ValueError, bool, cpu_arch, explicit_abi, frozenset, hasattr, hash, id, int, interpreters, is_32bit, isinstance, len, list, major_version, map, minor, minor_version, object, other, platform_, property, range, self, set, str, string, tag, tuple, version_str, warn
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\utils.py: ValueError, int, isinstance, len, sep, str, version_part, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\version.py: DeprecationWarning, NotImplemented, ValueError, bool, bytes, hash, i, int, isinstance, len, list, object, other, property, reversed, s, self, str, tuple, version, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\_manylinux.py: AssertionError, AttributeError, ImportError, OSError, RuntimeWarning, TypeError, ValueError, arch, bool, bytes, f, file, fmt, glibc_major, glibc_max, hasattr, int, isinstance, linux, open, range, self, str, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\_musllinux.py: KeyError, OSError, arch, bytes, e_fmt, e_phentsize, e_phnum, e_phoff, executable, fmt, i, int, len, minor, n, open, output, p_filesz, p_fmt, p_idx, p_offset, p_type, print, range, stack, str, t, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\packaging\_structures.py: bool, hash, int, isinstance, object, other, repr, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\actions.py: args, attrName, attrValue, attr_dict, classname, k, l, locn, method_call, n, namespace, object, repl_str, s, self, strg, t, tokens, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\common.py: Combine, FollowedBy, LineEnd, Literal, OneOrMore, Opt, ParseException, ParseResults, ParserElement, Regex, ValueError, White, Word, float, fmt, hexnums, identbodychars, identchars, int, isinstance, l, ll, nums, printables, quoted_string, s, ss, staticmethod, str, sum, t, token_map, tokens, tt, v, vars, ve
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\core.py: AttributeError, Ellipsis, Exception, HIT, ImportError, IndexError, KeyError, MISS, NotImplementedError, ParseBaseException, ParseException, ParseFatalException, ParseSyntaxException, RecursiveGrammarException, RuntimeError, TypeError, UserWarning, ValueError, adjacent, all, any, args, as_group_list, as_keyword, as_match, asdict, aslist, body_chars, bool, break_flag, bytes, c, cache_hit, cache_size_limit, callPreParse, callable, caseless, chars, charset, chr, classmethod, cls, cmd_line_warn_options, col, colno, convert_whitespace_escapes, copy_defaults, cur_, debug, default, diag_enum, diag_file, dict, doActions, e, encoding, end_quote_char, endloc, enumerate, err, esc_char, esc_quote, exact, exception_action, exclude_chars, expr1, exprs_arg, exprtokens, fail_on, failure_tests, file_or_filename, flag, flags, fns, force, frm, full_dump, func, getattr, grouped, hasattr, hex, i, id, ident_chars, ie, include, include_separators, init_chars, instance, int, isinstance, issubclass, item, iter, join_string, k, kwargs, l, len, line, lineno, list, list_all_matches, loc1, loc_, locals, mat, matchString, max, max_limit, max_matches, max_mismatches, maxsplit, message, min, minElements, multiline, n, new_loc, new_peek, next, nextLoc, notChars, not_chars, o, offset, open, optElements, ord, output_html, overlap, p, paArgs, parseElementList, parse_action_exc, parse_all, part, pattern, pbe, pe, pfe, post_parse, prev, prev_loc, prev_peek, prev_result, print, print_results, property, quoteChar, raise_fatal, range, recursive, ref_col, repl, replace_with, repr, resultlist, reversed, s_m, savelist, self, set, setattr, show_groups, show_results_names, skipto_arg, slice, sorted, src, start_action, staticmethod, stop_on, str, str_type, success_action, sum, super, te, test_line, test_string, tmptokens, tok, tokenlist, tokn, toks, tuple, type, unquote_results, v, var, vars, vertical, w_action, w_category, w_message, w_module, warn_env_var, warn_opt, warning_type, with_line_numbers, word_chars, ws, wschar, wslit, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\exceptions.py: Exception, classmethod, cls, elem, enumerate, exc, ff, id, int, isinstance, len, loc, marker_string, msg, parseElementList, pe, property, pstr, self, set, staticmethod, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\helpers.py: And, CaselessKeyword, CaselessLiteral, CharsNotIn, Combine, Diagnostics, Dict, Empty, Enum, FollowedBy, Forward, Group, Iterable, Keyword, LineEnd, List, Literal, MatchFirst, NoMatch, OneOrMore, Opt, ParseAction, ParseException, ParserElement, Regex, SkipTo, Suppress, TokenConverter, Tuple, TypeError, Union, ValueError, Word, ZeroOrMore, a, all, allow_trailing_delim, alphanums, alphas, any, any_close_tag, any_open_tag, arity, as_keyword, as_string, b, backup_stacks, base_expr, blockStatementExpr, bool, caseless, closer, col, combine, dbl_quoted_string, empty, enumerate, ignore_expr, indent, indentStack, instring, int, int_expr, isinstance, j, k, key, l, len, list, ll, loc, max, min, nums, opExpr1, opExpr2, op_list, opener, operDef, other, pa, printables, quoted_string, re_flags, remove_quotes, rightLeftAssoc, s, self, str, str_type, strs, suppress_GT, suppress_LT, sym, t, tag_str, thisExpr, tt, tuple, use_regex, v, value, vars, warnings, xml
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\results.py: AttributeError, Exception, IndexError, KeyError, TypeError, a, any, bool, bytes, classmethod, cls, default_value, dict, dir, enumerate, full, inAccumNames, include_list, indent, ins_string, int, isinstance, item, itemseq, iter, j, k, key, kwargs, len, list, modal, next, obj, object, occurrences, other, p1, p2, position, range, repr, res, sep, set, slice, sorted, state, str, str_type, type, value, vlist, vv
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\testing.py: Exception, bool, c, dict, enumerate, exc_type, exp, expand_tabs, expected, expected_parse_results, expr, getattr, i, int, isinstance, issubclass, len, line, list, mark_control, mark_spaces, max, min, msg, name, next, print, range, rpt, run_test_results, run_test_success, run_tests_report, self, staticmethod, str, test_string, type, u, value, verbose, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\unicode.py: any, c, cc, chr, filter, fn, getattr, hasattr, int, obj, range, rr, self, set, sorted, str, superclass, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\util.py: KeyError, ValueError, bool, c, capacity, chars, chr, classmethod, cls, dict, dname, getattr, i, int, isinstance, iter, key, len, list, ll, loc, name, next, object, ord, prev, re_escape, self, set, setattr, size, sorted, str, strg
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py: globals, int, nv, property, self, str, type, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py: any, bool, child, classmethod, converted, d, diag, diagram, diagram_kwargs, diagrams, dict, e, element, expr, fn, force, func, id, index, int, isinstance, key, label, len, list, name_hint, number, parent, parent_index, partial, property, self, set, show_groups, show_results_names, sorted, specification, state, str, super, type, value, vertical, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\archive_util.py: LookupError, d, dirs, driver, drivers, dst, e, extract_dir, filename, files, info, open, progress_filter, src, tar_obj, z, zipfile_obj
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\build_meta.py: BaseException, ValueError, a_dir, arg, classmethod, cls, config_settings, directory, dirs, e, exec, extension, f, file, flag, getattr, isinstance, key, len, list, locals, long_and_short, metadata_directory, name, open, opt, parent, requirements, result_extension, sdist_directory, self, setup_command, setup_script, specifiers, str, suffix, super, tmp_dist_dir, wheel_directory
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\depends.py: ImportError, byte_code, compile, default, f, getattr, globals, kind, list, locals, module, name, path, paths, self, str, symbol
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\dep_util.py: ValueError, i, len, range, sources_groups, targets
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\discovery.py: NotImplementedError, all, any, bool, classmethod, cls, detected, dir, dirs, distribution, enumerate, field, file, force, getattr, hasattr, i, include, kind, len, list, module, n, other, p, package_name, package_path, parent_dir, pat, path, patterns, pkg, pkg_dir, property, range, reversed, root, root_pkg, self, sorted, staticmethod, str, tuple, where
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\dist.py: AssertionError, AttributeError, Exception, TypeError, ValueError, args, attr, bool, cls, cmd, command_obj, content, default, dict, e, error, ext, f, field, file, filename, filter, frozenset, getattr, hasattr, hook, ignore_option_errors, inifiles, isinstance, item, k, len, license_file, license_files, list, locals, map, marker, module, neg, nsp, o, open, option, option_order, opts, p, package, packages, parent, path, pattern, pkg, pkgname, platform, pos, project_url, r, reader, req, reqs, requires, section, self, set, setattr, sorted, source, src, staticmethod, str, super, tuple, v, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\errors.py: RuntimeError
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\extension.py: Exception, args, kw, list, map, name, self, sources, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\glob.py: OSError, basename, bytes, drive, isinstance, list, name, next, pattern, recursive, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\installer.py: e, egg_dist, isinstance, link, list, str, tmpdir, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\launch.py: compile, dict, exec, fid, getattr, open
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\logging.py: hasattr, level, record
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\monkey.py: AssertionError, ImportError, attr, candidate, cls, func_name, getattr, hasattr, isinstance, item, mod_name, module, next, replacement, setattr, target_mod, type, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\msvc.py: IOError, ImportError, IndexError, KeyError, LookupError, OSError, TypeError, UnicodeDecodeError, ValueError, args, bits, crt_dir, dict, dir_name, exc, exists, filter, float, getattr, hkey, i, int, kwargs, line, list, locals, name, next, plat_spec, platform_info, prefix, property, range, registry_info, reversed, self, set, sorted, spec_path_lists, state_file, staticmethod, subkeys, v, value, vc_dir, vc_min_ver, vt, x64, x86
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\namespaces.py: f, filename, list, locals, map, open, parent, pkg, repr, self, sorted, staticmethod, str, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\package_index.py: Exception, UserWarning, ValueError, address, any, arg, args, classmethod, cls, d, delim, develop_ok, dict, e, egg_path, entry, expected, ext, fatal, filter, fn, force_scan, frag, frag2, func, getattr, h2, hash_name, host, hosts, index_url, installer, int, isinstance, item, kw, kwargs, len, line, list, local_index, location, m, map, max, message, metadata, meth, nested, open, opener, p, param2, params, password, path2, platform, precedence, property, pw, py_version, q, query, query2, range, raw_lines, rel, reporter, repository, req, requirement, retrieve, s2, search_path, section, self, server, set, source, staticmethod, status, str, super, tag, template, text, tfp, timeout, tmpdir, urls, user, username, v, vars, warning, win_base
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\py34compat.py: AttributeError, ImportError, spec
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\sandbox.py: Exception, NameError, SystemExit, a, any, args, compile, dict, dir, dist, dst, exc, exception, exceptions, exec, file, filename, filepath, filter, flags, func, getattr, globals, hasattr, kw, list, map, mod_name, module_names, name, operation, pattern, repl, replacement, repr, sandbox, saved_exc, self, setattr, setup_script, source, src, staticmethod, stream, target, tb, type, v, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\unicode_utils.py: UnicodeDecodeError, UnicodeEncodeError, UnicodeError, enc, isinstance, str, string
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\version.py: Exception
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\wheel.py: ValueError, d, destination_eggdir, dict, dirnames, dirpath, dst_dir, entry, enumerate, extra, f, filename, filenames, filter, fp, k, list, map, member, mod, n, name, next, open, req, reversed, self, set, setattr, src_dir, staticmethod, str, t, v, zf
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\windows_support.py: func, path
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_deprecation_warning.py: Warning
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_entry_points.py: ep, eps, group, map, sorted, str, type, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_imp.py: ImportError, hasattr, isinstance, issubclass, list, module, open, paths, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_importlib.py: AttributeError, ImportError, isinstance, item, ob
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_itertools.py: ValueError, element, iterable, key, set, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_path.py: bool, p1, p2, path, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_reqs.py: map, strs
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\__init__.py: Exception, all, attrs, base, cfg, command, default, dir, file, filenames, filter, getattr, isinstance, k, kw, list, map, option, path, pathname, reinit_subcommands, self, set, setattr, str, super, v, vars, what
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\alias.py: arg, c, len, map, name, print, repr, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\bdist_egg.py: OSError, bad, base, base_dir, bdf, bool, cmdname, compress, const, dict, dir, dirname, dirs, dry_run, egg_dir, enumerate, ext, ext_name, files, flag, getattr, isinstance, kw, len, mode, name, names, next, old, open, resource, self, str, stubs, target_dir, tuple, zip_filename
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\bdist_rpm.py: line, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\build.py: bool, cmd, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\build_clib.py: build_info, dict, isinstance, lib_name, libraries, list, self, source, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\build_ext.py: ImportError, any, base, bool, build_temp, compile, d, debug, dict, export_symbols, extra_postargs, extra_preargs, fn, fnext, getattr, hasattr, isinstance, len, lib, libname, libraries, library_dirs, list, macro, name, objects, old_inplace, open, output_dir, output_file, output_libname, runtime_library_dirs, s, self, sorted, str, suffix, target_lang, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\build_py.py: KeyError, all, attr, bool, copied, d, df, dict, egg_info, file, filter, fn, getattr, include_bytecode, len, level, link, list, map, module, module_file, p, package_dir, parent, path, pattern, preserve_mode, preserve_times, self, set, sorted, spec, staticmethod, str, super, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\develop.py: egg_base, f, getattr, install_dir, line, name, open, self, staticmethod, strm
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\dist_info.py: bool, component, dir_name, dir_path, dst, opts, requires_bkp, self, src, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\easy_install.py: AttributeError, Exception, IOError, ImportError, KeyError, OSError, SyntaxError, SystemExit, TypeError, UnicodeError, UserWarning, ValueError, arg, attr, attrs, base, basename, cache, cfglen, classmethod, cls, compile, counter, d, deps, dev_path, dict, dist_path, download, e, ev, exe_filename, filter, fix_zipimporter_caches, force_windows, fp, func, getattr, ignore_errors, info, inputs, int, isinstance, item, k, key, last, len, list, locals, m, map, new, npath, onerror, open, orig_header, orig_script, p, param, path_item, prefix, print, q, range, res, script_name, self, setattr, show_deprecation, staticmethod, str, string, super, tag, text, type, type_, updater, vars, wheel_path, wininst, x, y
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\editable_wheel.py: AttributeError, Exception, NotImplementedError, OSError, UserWarning, ValueError, all, any, base_dir, bool, bytes, category, classmethod, cmd_name, dict, dir_, distribution, editable_name, ex, filename, files, getattr, hasattr, i, installation_dir, iter, k, key, len, lib, link, list, map, mod, module, namespaces_, next, ns, other, other_path, output_mapping, outputs, p, package, parent_path, path1, path2, path_entries, pkg, pkg_path, pkg_roots, pth_prefix, range, relative_output, repr, reversed, self, set, sorted, src, src_file, str, super, tmp, tmp_dir, type, unpacked, v, value, wheel_obj, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\egg_info.py: KeyError, UnicodeEncodeError, ValueError, action, basename, bool, build_py, c, chunk, cmd, debug_print, dict, dir, dir_pattern, e, enumerate, ep, extra, filename, filter, force, getattr, hasattr, ignore_egg_info_dir, int, isinstance, k, len, lf, line, list, map, match_dir, oldname, oldver, open, paths, pattern, predicate, property, range, reqs, self, sorted, staticmethod, str, stream, super, vars, what
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\install.py: caller, dict, frame, run_frame, self, staticmethod
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\install_egg_info.py: dst, self, skip, src
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\install_lib.py: dst, exclusion_path, f, hasattr, infile, ns_pkg, outfile, pkg, pkg_name, preserve_mode, preserve_symlinks, preserve_times, self, set, src, staticmethod
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\install_scripts.py: ImportError, args, contents, getattr, mode, open, script_name, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\py36compat.py: directory, filename, filenames, filter, fn, fspath, hasattr, isinstance, pattern, self, src_dir, staticmethod, str, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\register.py: self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\rotate.py: ValueError, e, f, int, isinstance, len, p, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\saveopts.py: cmd, opt, self, src, val
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\sdist.py: Exception, TypeError, UnicodeDecodeError, base_dir, c, cmd_name, data_files, dirname, ep, ext, f, file, filenames, fp, getattr, hasattr, item, list, name, open, self, set, setattr, src_dir, staticmethod, super, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\setopt.py: ValueError, dry_run, f, filename, kind, len, open, option, options, section, self, settings, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\test.py: dist, fget, file, filter, func, getattr, hasattr, k, len, list, map, module, obj, object, property, self, set, staticmethod, v, val
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\upload.py: self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\upload_docs.py: AssertionError, body, bool, classmethod, cls, cmd_name, ct, dict, e, f, filename, files, fragments, isinstance, item, key, len, list, map, netloc, open, params, print, query, root, s, schema, self, staticmethod, str, tuple, url
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\command\__init__.py: TypeError
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\expand.py: AttributeError, Exception, ModuleNotFoundError, all, any, attr, attr_desc, bytes, callable, char, data_files, dest, dict, distribution, e, f, filepath, filepaths, getattr, hasattr, int, isinstance, iter, k, key, kwargs, len, list, locals, map, namespaces, next, obtain_mapping_value, package_data, packages, parent, patterns, property, qualified_class_name, self, sorted, statement, str, target, text, text_source, v, vars, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\pyprojecttoml.py: Exception, UserWarning, ValueError, any, bool, cfg, classmethod, cls, container, dict, directive, distribution, ensure_discovered, ex, exc_type, exc_value, field, file, fn, getattr, group, hasattr, ignore_option_errors, isinstance, k, line, list, open, project_cfg, self, set, setuptools_cfg, specifier, str, super, traceback, tuple, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\setupcfg.py: Exception, KeyError, NotImplementedError, UserWarning, ValueError, args, bool, chunk, classmethod, cls, command_options, config_dict, dict, distribution, ensure_discovered, find_others, func, getattr, handler, ignore_option_errors, isinstance, k, key, kwargs, label, len, line, list, locals, method, name, option, orig_value, other_files, parse_methods, path, property, root_dir, section_options, section_parser_method, sections, self, sep, setattr, str, super, tuple, v, val, values_parser, warning_class
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_apply_pyprojecttoml.py: EMPTY, Exception, PYPROJECT_CORRESPONDENCE, UserWarning, ValueError, acc, attr, callable, classmethod, cls, cmd_class, config, desc, dict, dist, ep, ex, ext, fancy_option, file, filename, getattr, getter, group, hasattr, i, isinstance, k, kind, list, name, next, obj, person, pyproject, set, setattr, str, v, val, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\__init__.py: args, fn, kwargs
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_validate_pyproject\error_reporting.py: all, any, bad, bool, buffer, classmethod, cls, dict, e, enumerate, ex, i, isinstance, jargon, k, len, list, name, p, parent_prefix, parents, path, prefix, property, repl, repr, schemas, self, str, substring, t, term, v, w, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_validate_pyproject\extra_validations.py: field, pyproject
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_exceptions.py: ValueError, definition, item, message, name, property, rule, self, super, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_validations.py: all, bool, custom_formats, data, data__authors_item, data__buildsystem__backendpath_item, data__buildsystem__requires_item, data__classifiers_item, data__cmdclass_key, data__cmdclass_val, data__datafiles_key, data__datafiles_val, data__datafiles_val_item, data__dependencies_item, data__dynamic__optionaldependencies_key, data__dynamic__optionaldependencies_val, data__dynamic_item, data__dynamic_key, data__eagerresources_item, data__entrypoints_key, data__entrypoints_val, data__excludepackagedata_key, data__excludepackagedata_val, data__excludepackagedata_val_item, data__file_item, data__find__exclude_item, data__find__include_item, data__find__where_item, data__keywords_item, data__licensefiles_item, data__maintainers_item, data__namespacepackages_item, data__obsoletes_item, data__optionaldependencies_key, data__optionaldependencies_val, data__optionaldependencies_val_item, data__packagedata_key, data__packagedata_val, data__packagedata_val_item, data__packagedir_key, data__packagedir_val, data__packages_item, data__platforms_item, data__provides_item, data__pymodules_item, data__scriptfiles_item, data__urls_key, data__urls_val, data_key, data_val, dict, enumerate, isinstance, len, list, locals, name_prefix, prop, set, str, tuple, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_validate_pyproject\formats.py: Exception, ImportError, all, any, bool, c, e, extras_, i, m, module, name, response, rest, self, set, str, value, version, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py: FORMAT_FUNCTIONS, acc, bool, callable, data, fn, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\extern\__init__.py: ImportError, any, fullname, locals, map, prefix, property, root, root_name, self, set, spec, target, vendor_pkg, vendored_names
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\archive_util.py: DeprecationWarning, ImportError, KeyError, RuntimeError, ValueError, arg, compress, dirnames, dirpath, dry_run, filenames, format, formats, group, name, owner, root_dir, tarinfo, val, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\bcppcompiler.py: DeprecationWarning, KeyError, build, debug, depends, dir, dirs, dry_run, ell, export_symbols, ext, extra_postargs, extra_preargs, file, force, include_dirs, lib, libraries, library_dirs, macros, map, modname, msg, name, output_file, output_libname, print, runtime_library_dirs, self, source, source_filenames, sources, src_name, str, strip_dir, super, sym, tail, target_desc, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\ccompiler.py: ImportError, KeyError, LookupError, NotImplementedError, TypeError, ValueError, args, before, build_temp, class_name, cmd, debug, definitions, defn, depends, dict, dirs, dry_run, dst, eval, export_symbols, extra_postargs, extra_preargs, fd, fn, fname, force, func, funcname, getattr, incdirs, incl, isinstance, key, kwargs, len, lib, lib_dir, lib_name, lib_type, libname, libnames, list, macro, mode, name, object, outdir, output_file, output_filename, output_libname, output_progname, pattern, print, property, range, self, setattr, source, source_filenames, src_name, staticmethod, str, strip_dir, target_lang, tuple, value, vars, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\cmd.py: AttributeError, RuntimeError, TypeError, all, args, attr, base_dir, base_name, cmd, cmd_name, command, create, default, dist, dst, dst_option, error_fmt, format, func, getattr, group, hasattr, infile, isinstance, level, link, list, method, mode, msg, name, option_pairs, outfile, owner, preserve_mode, preserve_symlinks, preserve_times, print, reinit_subcommands, root_dir, search_path, self, setattr, src, src_cmd, src_option, str, tester, tuple, v, what
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\config.py: default, f, key, password, response, self, username
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\core.py: KeyboardInterrupt, OSError, RuntimeError, SystemExit, ValueError, attrs, exc, exec, f, locals, msg, print, script_args, script_name, stop_after, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\cygwinccompiler.py: DeprecationWarning, OSError, ValueError, build_temp, cc, cc_args, debug, details, dll_name, dry_run, exc, export_symbols, ext, extra_postargs, force, int, library_dirs, msg, obj, open, output_dir, output_filename, property, runtime_library_dirs, self, src, src_name, status, strip_dir, super, sym, target_desc, target_lang, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\dep_util.py: ValueError, i, len, missing, range, source, sources, target, targets
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\dir_util.py: OSError, base_dir, cmd, d, dir, directory, drive, dry_run, dst, e, exc, f, file, files, isinstance, mode, n, preserve_mode, preserve_symlinks, preserve_times, set, sorted, src, str, tail, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\dist.py: AttributeError, ImportError, SystemExit, TypeError, ValueError, arg, attr, attrs, base_dir, basename, callable, cmd, cmd_name, cmd_options, command_obj, create, elm, file, frozenset, func, getattr, hasattr, header, help_option, help_tuple, isinstance, issubclass, key, len, level, line, list, locals, name, o, open, option, opts, path, pkg, pkg_info, pkgname, print, reinit_subcommands, repr, section, self, setattr, sorted, source, str, sub, type, v, vars, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\errors.py: Exception
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\extension.py: AssertionError, all, define_macros, depends, export_symbols, extra_compile_args, extra_link_args, extra_objects, filename, id, include_dirs, isinstance, kw, language, len, libraries, library_dirs, list, name, option, optional, repr, runtime_library_dirs, self, sorted, sources, str, swig_opts, undef_macros, v, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\fancy_getopt.py: RuntimeError, ValueError, aliases, ch, dict, getattr, header, help, help_string, isinstance, len, line, long_option, msg, negative_alias, negative_opt, option_table, options, opts, ord, print, self, setattr, short_option, str, w, what, width
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\filelist.py: allfiles, anchor, base, classmethod, cls, dirs, end, file, i, is_regex, isinstance, item, len, line, list, map, name, path, pattern, prefix, print, range, self, set, sort_tuple, sorted, start, str, w, walk_item
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\file_util.py: KeyError, OSError, ValueError, buffer_size, contents, dry_run, e, filename, line, link, msg, num, open, preserve_mode, preserve_times, src, verbose
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\log.py: UnicodeEncodeError, ValueError, args, level, self, str, threshold, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\msvc9compiler.py: DeprecationWarning, KeyError, OSError, UnicodeError, ValueError, arch, arg, build, classmethod, cls, debug, depends, dir, dirs, dll_name, dry_run, exe, export_symbols, ext, extra_postargs, extra_preargs, force, getattr, include_dirs, int, len, lib, libraries, library_dirs, list, macro, macros, manifest_file, mffilename, msg, obj, objects, open, output_libname, path, paths, pp_opts, runtime_library_dirs, self, source_filenames, sources, src_name, staticmethod, stderr, str, strip_dir, super, sym, target_desc, v, variable, verbose, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\msvccompiler.py: DeprecationWarning, ImportError, KeyError, UnicodeError, build, debug, depends, dir, dirs, dll_name, dry_run, exe, export_symbols, ext, extra_postargs, extra_preargs, force, getattr, include_dirs, int, len, lib, libraries, library_dirs, macro, macros, msg, obj, objects, output_libname, paths, platform, pp_opts, runtime_library_dirs, self, source_filenames, sources, src_name, str, strip_dir, super, sym, target_desc, v, value, verbose, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\py38compat.py: ImportError, osname, release, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\py39compat.py: vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\spawn.py: AttributeError, OSError, ValueError, dict, dry_run, exc, ext, list, p, search_path
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\sysconfig.py: AttributeError, DeprecationWarning, KeyError, ValueError, any, ar_flags, args, beg, ccshared, compiler, d, dir_a, dir_b, end, fn, getattr, globals, int, isinstance, k, len, list, next, plat_specific, shlib_suffix, spec_prefix, standard_lib, str, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\text_file.py: KeyError, RuntimeError, ValueError, filename, isinstance, list, msg, opt, options, self, setattr, str, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\unixccompiler.py: TypeError, aix, cc_args, cmd, compiler_cmd, compiler_cxx_ne, debug, dir, dirs, env, extra_postargs, extra_preargs, filter, include_dirs, isinstance, len, lib, lib_name, libraries, library_dirs, linker_cmd, linker_exe_ne, linker_na, linker_ne, macros, map, msg, next, obj, objects, output_dir, output_file, output_libname, root, runtime_library_dirs, self, source, src, staticmethod, str, target_desc, target_lang, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\util.py: DeprecationWarning, ImportError, KeyError, RuntimeError, ValueError, args, base_dir, beg, dict, dry_run, exc, file, force, func, hasattr, header, int, len, local_vars, map, match, n, name, new_root, open, optimize, osname, pathname, prefix, py_files, release, repr, script_fd, script_name, str, value, var, verbose, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\version.py: DeprecationWarning, NotImplemented, ValueError, ctx, enumerate, i, int, isinstance, major, map, minor, obj, patch, prerelease, prerelease_num, self, str, tuple, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\versionpredicate.py: ValueError, aPred, comp, cond, pred, self, verStr, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\_collections.py: KeyError, c, iter, key, len, list, other, reversed, scope, self, set, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\_functools.py: args, func, kwargs, param
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\_macos_compat.py: cmd
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\_msvccompiler.py: ImportError, KeyError, OSError, TypeError, UnicodeDecodeError, ValueError, base, build, classmethod, cls, cmd, debug, depends, dict, dir, dirs, dll_name, dry_run, exc, exe, export_symbols, ext, extra_postargs, extra_preargs, fallback, float, force, i, include_dirs, int, lib, libraries, library_dirs, line, macros, msg, name, obj, objects, output_libname, p, pp_opts, property, runtime_library_dirs, self, sources, staticmethod, str, super, sym, target_desc, tuple, type, v, val, value, vc_dir, verbose, vt
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\__init__.py: ImportError
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\bdist.py: DeprecationWarning, KeyError, dict, format, i, len, range, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\bdist_dumb.py: KeyError, repr, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\bdist_rpm.py: attr, changelog, d, default, f, field, getattr, isinstance, len, list, open, path, print, readme, repr, rpm_opt, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\build.py: ValueError, cmd_name, hasattr, int, isinstance, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\build_clib.py: build_info, dict, isinstance, len, lib, lib_name, libraries, list, macro, name, self, str, tuple, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\build_ext.py: ImportError, UnicodeEncodeError, ValueError, base, build_info, dict, e, enumerate, executor, ext_name, extension, extensions, fut, hasattr, i, int, isinstance, key, len, list, macro, o, self, setattr, sorted, source, str, symbol, tuple, undef, value, vers, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\build_py.py: AssertionError, KeyError, TypeError, ValueError, f, file, fn, include_bytecode, int, isinstance, len, list, name, package_, pattern, self, str, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\build_scripts.py: OSError, UnicodeEncodeError, ValueError, encoding, file, open, outf, self, staticmethod
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\check.py: AttributeError, ImportError, TypeError, attr, children, debug, e, encoding, error_handler, exc, getattr, globals, halt_level, kwargs, level, message, msg, report_level, self, source, str, stream, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\clean.py: OSError, directory, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\config.py: OSError, call, decl, exe, func, head, header, headers, include_dirs, isinstance, lang, libraries, library, library_dirs, obj, open, other_libraries, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\install.py: AttributeError, Exception, KeyError, attrs, cmd_name, counter, dict, exec_prefix, getattr, hasattr, isinstance, key, len, map, msg, name, names, ob, opt, path, print, range, self, set, setattr, str, value, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\install_data.py: isinstance, out, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\install_egg_info.py: f, name, open, property, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\install_headers.py: header, out, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\install_lib.py: AssertionError, ValueError, cmd_option, file, files, getattr, has_any, int, isinstance, len, output_dir, py_file, py_filenames, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\install_scripts.py: file, self
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\py37compat.py: args, f1, f2, kwargs, list
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\register.py: DeprecationWarning, ValueError, action, cmd_name, code, e, input, key, len, print, self, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\sdist.py: PendingDeprecationWarning, ValueError, cmd_name, directory, filename, filenames, filter, fmt, fn, format, fspath, hasattr, isinstance, manifest, open, pattern, self, src_dir, staticmethod, str, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\upload.py: AssertionError, OSError, ValueError, command, digest_cons, digest_name, e, filename, fragments, getattr, isinstance, key, len, list, open, params, pyversion, query, schema, self, str, tuple, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_distutils\command\_framework_compat.py: dict, locals, name
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\ordered_set.py: ImportError, KeyError, TypeError, ValueError, all, enumerate, hasattr, idx, isinstance, item, iter, iterable, k, key, len, list, map, obj, reversed, self, sequence, set, sets, slice, state, str, subkey, tuple, type, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\typing_extensions.py: AttributeError, C, DeprecationWarning, Ellipsis, ImportError, NotImplemented, TypeError, ValueError, a, all, any, arg, attr, b, base, bool, bound, callable, classmethod, contravariant, covariant, dct, dict, extra, f, frozenset, g, getattr, getitem, globalns, hasattr, hash, include_extras, instance, int, isinstance, issubclass, k, kwds, len, list, localns, map, n, name, namespace, obj, object, orig_bases, other, p, property, repr, scls, set, setattr, slot, str, subclass, super, t, total, tuple, type, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\zipp.py: AttributeError, FileNotFoundError, IsADirectoryError, ValueError, args, at, classmethod, dict, filter, isinstance, kwargs, list, map, minuend, mode, other, p, property, pwd, root, self, set, source, staticmethod, str, strm, subtrahend, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_adapters.py: cls, dict, key, map, orig, property, self, set, super, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_collections.py: classmethod, cls, getattr, key, map, self, str, super, text
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_compat.py: ImportError, cls, filter, finder, getattr, hasattr, staticmethod, val
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_functools.py: args, func, kwargs, method, param, self, setattr
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_itertools.py: TypeError, base_type, bytes, element, isinstance, iter, iterable, key, obj, set, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_meta.py: bool, int, property, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\_text.py: hash, maxsplit, other, self, splitter, str, sub, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_metadata\__init__.py: AttributeError, DeprecationWarning, Exception, FileNotFoundError, IsADirectoryError, KeyError, ModuleNotFoundError, NotADirectoryError, OSError, PermissionError, StopIteration, ValueError, all, args, bool, child, classmethod, cls, default, dict, distribution_name, encoding, ep, ext, extra, f, filename, filter, filter_, finder, getattr, group, hash, int, isinstance, item, iter, kwargs, len, line, list, locals, map, method_name, next, param, params, paths, pkg, property, req, resolver, root, sections, self, size_str, sorted, spec, staticmethod, str, stream, super, tuple, value, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\abc.py: FileNotFoundError, bool, child, encoding, item, path, resource, self, str, strm
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\readers.py: FileNotFoundError, KeyError, NotADirectoryError, ValueError, all, child, exc, file, iter, list, loader, map, module, namespace_path, path, property, resource, self, str, super
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\simple.py: IsADirectoryError, RuntimeError, args, kwargs, map, mode, next, parent, property, reader, self, traversable
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\_adapters.py: AttributeError, FileNotFoundError, ValueError, adapter, args, attr, file, getattr, hasattr, iter, kwargs, len, mode, other, package, path, path_parts, property, self, spec
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\_common.py: FileNotFoundError, TypeError, cand, fd, getattr, isinstance, package, path, raw_path, str, suffix
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\_compat.py: AttributeError, ImportError, TypeError, ValueError, cls, hasattr, package, property, self, spec
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\_itertools.py: element, iterable, key, seen, set
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\importlib_resources\_legacy.py: DeprecationWarning, ValueError, any, args, bool, bytes, encoding, errors, file_name, fp, func, kwargs, name, package, parent, str, traversable
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\jaraco\context.py: Exception, args, bool, branch, dest_ctx, dict, dir, exceptions, func, issubclass, kwargs, open, property, quiet, remover, repo_dir, self, trap, url, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\jaraco\functools.py: TypeError, action, args, bound_method, cache_wrapper, cleanup, eval, exceptions, f, f1, f2, f_args, f_kwargs, float, func1, func2, funcs, getattr, hasattr, isinstance, k, kwargs, map, max, max_rate, method, method_name, more_itertools, namespace, obj, object, param, print, r_args, r_kwargs, range, replace, retries, self, setattr, target, transform, trap, use, vars
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py: ImportError, StopIteration, UnicodeDecodeError, args, bytes, classmethod, cls, filter, hash, identifier, isinstance, iter, iterable, len, line, map, match, maxsplit, min, new, next, object, old, other, para, part, prefix_lines, rest, reversed, s, s1, s2, self, slice, splitter, staticmethod, str, string, sub, subject, suffix, super, text, tuple, value, word
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\more_itertools\more.py: A, BaseException, DeprecationWarning, IndexError, M, RuntimeError, StopIteration, TypeError, ValueError, after, any, args, base_type, before, bool, bytes, callback_kwd, child, chunk, chunk_size, combo, context_manager, cur_idx, d, default, details, divmod, e, elem, enumerate, exceptions, f, fillvalue, filter, func, function, g, hasattr, hash, i1, i2, initial, int, isinstance, iter, keep_separator, keyfunc, kwargs, len, levels, limit_seconds, list, longest, map, max, maxlen, maxsplit, min, next, next_item, next_multiple, node, obj, object, offsets, ordering, other, p, pred, predicate, property, range, reducefunc, repr, result_index, reverse, reversed, s, self, set, sizes, slice, smallest_weight_key, sorted, staticmethod, str, strict, super, tail, target, tmp, too_long, too_short, tuple, type, val, validator, value_list, w, wait_seconds, weight, window_size, wrapping_args, wrapping_func, wrapping_kwargs, x, y, zip, zipped_items
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\more_itertools\recipes.py: DeprecationWarning, ImportError, IndexError, StopIteration, TypeError, ValueError, a, b, bool, cond, default, element, exception, fillvalue, filter, first, func, function, i, index, int, isinstance, it, iter, iterable, iterables, iterator, key, len, list, listOfLists, map, min, next, range, set, signal, sorted, start, sum, t1, t2, times, tuple, value, vec1, vec2, x, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\markers.py: NotImplementedError, ValueError, all, any, bool, e, environment, first, groups, i, info, isinstance, item, len, lhs, list, m, marker, markers, name, op, oper, results, rhs, self, str, t, tuple, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\requirements.py: ValueError, e, parts, requirement_string, s, self, set, sorted, str, t
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py: DeprecationWarning, NotImplemented, ValueError, all, any, bool, filtered, fn, frozenset, getattr, hash, int, isinstance, iter, left, left_split, len, list, max, object, op, operator_callable, padded_prospective, padded_spec, parsed, property, result, right, right_split, s, segment, self, set, sorted, spec_str, specifiers, str, super, value, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\tags.py: INTERPRETER_SHORT_NAMES, NotImplemented, ValueError, bool, cpu_arch, explicit_abi, frozenset, hasattr, hash, id, int, interpreters, is_32bit, isinstance, len, list, major_version, map, minor, minor_version, object, other, platform_, property, range, self, set, str, string, tag, tuple, version_str, warn
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\utils.py: ValueError, int, isinstance, len, sep, str, version_part, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\version.py: DeprecationWarning, NotImplemented, ValueError, bool, bytes, hash, i, int, isinstance, len, list, object, other, property, reversed, s, self, str, tuple, version, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\_manylinux.py: AssertionError, AttributeError, ImportError, OSError, RuntimeWarning, TypeError, ValueError, arch, bool, bytes, f, file, fmt, glibc_major, glibc_max, hasattr, int, isinstance, linux, open, range, self, str, version
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\_musllinux.py: KeyError, OSError, arch, bytes, e_fmt, e_phentsize, e_phnum, e_phoff, executable, fmt, i, int, len, minor, n, open, output, p_filesz, p_fmt, p_idx, p_offset, p_type, print, range, stack, str, t, tuple
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\packaging\_structures.py: bool, hash, int, isinstance, object, other, repr, self, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\actions.py: args, attrName, attrValue, attr_dict, classname, k, l, locn, method_call, n, namespace, object, repl_str, s, self, strg, t, tokens, v
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\common.py: Combine, FollowedBy, LineEnd, Literal, OneOrMore, Opt, ParseException, ParseResults, ParserElement, Regex, ValueError, White, Word, float, fmt, hexnums, identbodychars, identchars, int, isinstance, l, ll, nums, printables, quoted_string, s, ss, staticmethod, str, sum, t, token_map, tokens, tt, v, vars, ve
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\core.py: AttributeError, Ellipsis, Exception, HIT, ImportError, IndexError, KeyError, MISS, NotImplementedError, ParseBaseException, ParseException, ParseFatalException, ParseSyntaxException, RecursiveGrammarException, RuntimeError, TypeError, UserWarning, ValueError, adjacent, all, any, args, as_group_list, as_keyword, as_match, asdict, aslist, body_chars, bool, break_flag, bytes, c, cache_hit, cache_size_limit, callPreParse, callable, caseless, chars, charset, chr, classmethod, cls, cmd_line_warn_options, col, colno, convert_whitespace_escapes, copy_defaults, cur_, debug, default, diag_enum, diag_file, dict, doActions, e, encoding, end_quote_char, endloc, enumerate, err, esc_char, esc_quote, exact, exception_action, exclude_chars, expr1, exprs_arg, exprtokens, fail_on, failure_tests, file_or_filename, flag, flags, fns, force, frm, full_dump, func, getattr, grouped, hasattr, hex, i, id, ident_chars, ie, include, include_separators, init_chars, instance, int, isinstance, issubclass, item, iter, join_string, k, kwargs, l, len, line, lineno, list, list_all_matches, loc1, loc_, locals, mat, matchString, max, max_limit, max_matches, max_mismatches, maxsplit, message, min, minElements, multiline, n, new_loc, new_peek, next, nextLoc, notChars, not_chars, o, offset, open, optElements, ord, output_html, overlap, p, paArgs, parseElementList, parse_action_exc, parse_all, part, pattern, pbe, pe, pfe, post_parse, prev, prev_loc, prev_peek, prev_result, print, print_results, property, quoteChar, raise_fatal, range, recursive, ref_col, repl, replace_with, repr, resultlist, reversed, s_m, savelist, self, set, setattr, show_groups, show_results_names, skipto_arg, slice, sorted, src, start_action, staticmethod, stop_on, str, str_type, success_action, sum, super, te, test_line, test_string, tmptokens, tok, tokenlist, tokn, toks, tuple, type, unquote_results, v, var, vars, vertical, w_action, w_category, w_message, w_module, warn_env_var, warn_opt, warning_type, with_line_numbers, word_chars, ws, wschar, wslit, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\exceptions.py: Exception, classmethod, cls, elem, enumerate, exc, ff, id, int, isinstance, len, loc, marker_string, msg, parseElementList, pe, property, pstr, self, set, staticmethod, str, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\helpers.py: And, CaselessKeyword, CaselessLiteral, CharsNotIn, Combine, Diagnostics, Dict, Empty, Enum, FollowedBy, Forward, Group, Iterable, Keyword, LineEnd, List, Literal, MatchFirst, NoMatch, OneOrMore, Opt, ParseAction, ParseException, ParserElement, Regex, SkipTo, Suppress, TokenConverter, Tuple, TypeError, Union, ValueError, Word, ZeroOrMore, a, all, allow_trailing_delim, alphanums, alphas, any, any_close_tag, any_open_tag, arity, as_keyword, as_string, b, backup_stacks, base_expr, blockStatementExpr, bool, caseless, closer, col, combine, dbl_quoted_string, empty, enumerate, ignore_expr, indent, indentStack, instring, int, int_expr, isinstance, j, k, key, l, len, list, ll, loc, max, min, nums, opExpr1, opExpr2, op_list, opener, operDef, other, pa, printables, quoted_string, re_flags, remove_quotes, rightLeftAssoc, s, self, str, str_type, strs, suppress_GT, suppress_LT, sym, t, tag_str, thisExpr, tt, tuple, use_regex, v, value, vars, warnings, xml
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\results.py: AttributeError, Exception, IndexError, KeyError, TypeError, a, any, bool, bytes, classmethod, cls, default_value, dict, dir, enumerate, full, inAccumNames, include_list, indent, ins_string, int, isinstance, item, itemseq, iter, j, k, key, kwargs, len, list, modal, next, obj, object, occurrences, other, p1, p2, position, range, repr, res, sep, set, slice, sorted, state, str, str_type, type, value, vlist, vv
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\testing.py: Exception, bool, c, dict, enumerate, exc_type, exp, expand_tabs, expected, expected_parse_results, expr, getattr, i, int, isinstance, issubclass, len, line, list, mark_control, mark_spaces, max, min, msg, name, next, print, range, rpt, run_test_results, run_test_success, run_tests_report, self, staticmethod, str, test_string, type, u, value, verbose, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\unicode.py: any, c, cc, chr, filter, fn, getattr, hasattr, int, obj, range, rr, self, set, sorted, str, superclass, type
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\util.py: KeyError, ValueError, bool, c, capacity, chars, chr, classmethod, cls, dict, dname, getattr, i, int, isinstance, iter, key, len, list, ll, loc, name, next, object, ord, prev, re_escape, self, set, setattr, size, sorted, str, strg
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py: globals, int, nv, property, self, str, type, zip
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py: any, bool, child, classmethod, converted, d, diag, diagram, diagram_kwargs, diagrams, dict, e, element, expr, fn, force, func, id, index, int, isinstance, key, label, len, list, name_hint, number, parent, parent_index, partial, property, self, set, show_groups, show_results_names, sorted, specification, state, str, super, type, value, vertical, x
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\tomli\_parser.py: AttributeError, IndexError, KeyError, TypeError, ValueError, access_lists, array, bool, chars, chr, codepoint, cont_key, dict, e, error_on_eof, expect, flag, float, float_str, frozenset, header, hex_len, i, int, isinstance, k, key, key_parent, key_part, len, list, literal, msg, multiline, parsed_escape, range, recursive, self, str, tuple, val, value
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\tomli\_re.py: day, day_str, hour, hour_str, int, match, micros_str, minute, minute_str, month, month_str, offset_hour_str, offset_minute_str, offset_sign_str, parse_float, sec, sec_str, sign_str, str, year, year_str, zulu_time
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\setuptools\_vendor\tomli\_types.py: int, str
E:\zeta-monorepo\.venv-optimized\Lib\site-packages\_distutils_hack\__init__.py: Exception, ValueError, all, any, classmethod, cls, frame, fullname, getattr, locals, name, pat, path, patterns, self, setattr, staticmethod, string
E:\zeta-monorepo\apps\backend\application.py: config, dict, self, str
E:\zeta-monorepo\apps\backend\dev_assistant.py: Exception, client, dict, exc, payload, str
E:\zeta-monorepo\apps\backend\enhanced_main.py: call_next, edge, event, len, node, print, request
E:\zeta-monorepo\apps\backend\protocols.py: config, dict, self, str
E:\zeta-monorepo\apps\backend\quick_fix_imports.py: Exception, e, enumerate, f, i, line, open, print
E:\zeta-monorepo\apps\backend\quick_test.py: client, len, print
E:\zeta-monorepo\apps\backend\simple_ollama_test.py: Exception, client, e, print
E:\zeta-monorepo\apps\backend\test_full_integration.py: Exception, client, e, len, model, print
E:\zeta-monorepo\apps\backend\test_prometheus.py: ImportError, print
E:\zeta-monorepo\apps\backend\validate_imports.py: Exception, description, e, exec, import_statement, import_stmt, len, print
E:\zeta-monorepo\apps\backend\__init__.py: APIHandler, DatabaseManager, Exception, KeyboardInterrupt, RuntimeError, ValueError, config_override, dict, e, float, get_config, isinstance, key, list, logger, self, str, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\typing_extensions.py: AssertionError, AttributeError, BaseException, DeprecationWarning, Ellipsis, Exception, ImportError, NameError, NotImplemented, NotImplementedError, RuntimeError, TypeError, ValueError, Warning, a, allow_special_forms, annotation_key, any, ast, attr, b, base, bool, bound, bytearray, bytes, callable, classmethod, cls, cls_or_fn, collected, complex, constraints, contravariant, covariant, default, depth, dict, doc, documentation, e, enumerate, eq_default, eval_str, field_name, field_specifiers, float, forward_ref, frozen_default, frozenset, func, getattr, getitem, hasattr, hash, hints, include_extras, infer_variance, inst, instance, int, isinstance, issubclass, k, key, kw_only_default, kwds, len, list, mcls, memoryview, message, min, n, namespace, nparams, obj, object, order_default, other, p, pair, param, print, property, recursion, repr, self, set, setattr, sorted, staticmethod, str, sum, super, t, total, tp, tuple, tvar, type, type_param, typename, typevarlike, typing_is_inline, vars, x, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\from_thread.py: AttributeError, BaseException, Exception, NotImplementedError, RuntimeError, args, async_cm, backend, backend_options, bool, cancel_remaining, cm, dict, exc_tb, exc_type, exc_val, f, func, future, id, int, isinstance, kwargs, name, object, portal_, self, str, task_status_future, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\lowlevel.py: KeyError, LookupError, ValueError, default, dict, name, object, property, self, str, value, var
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\pytest_plugin.py: KeyboardInterrupt, OSError, SystemExit, TypeError, any, arg, backend_name, bool, collector, config, dict, exc, excgrp, family, fixturedef, getattr, has_backend_arg, has_request_arg, hasattr, int, isinstance, kwargs, len, name, obj, object, property, pyfuncitem, request, runner, self, set, stack, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\to_process.py: BaseException, EOFError, LookupError, ProcessLookupError, RuntimeError, SystemExit, args, bool, bytes, cancellable, exc, float, func, getattr, int, isinstance, killed_process, killed_processes, len, length, list, object, open, pickled_cmd, process_to_kill, set, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\to_thread.py: DeprecationWarning, args, bool, cancellable, func, limiter
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\__init__.py: AttributeError, DeprecationWarning, attr, getattr, list, locals, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_eventloop.py: BaseException, StrOrBytesPath, bool, bytes, classmethod, cls, dict, float, int, object, set, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_resources.py: BaseException, self, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_sockets.py: BaseException, IPSockAddrType, OSError, SockAddrType, TypeError, UDPPacketType, UNIXDatagramPacketType, ValueError, addr_family, attributes, bool, bytes, classmethod, data, dict, exc, handler, host, int, isinstance, list, path, port, property, require_bound, require_connected, self, sock_or_fd, sock_type, stack, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_streams.py: StopAsyncIteration, bytes, int, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_subprocesses.py: int, property
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_tasks.py: BaseException, bool, object, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\_testing.py: BaseException, bool, dict, self, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\abc\__init__.py: getattr, list, locals
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\streams\buffered.py: bool, bytearray, bytes, connectable, delimiter, exc, int, isinstance, item, len, max, max_bytes, nbytes, property, self, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\streams\file.py: OSError, ValueError, append, attributes, bool, bytes, classmethod, cls, dict, exc, hasattr, int, item, max_bytes, path, position, property, self, str, whence
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\streams\memory.py: AttributeError, BaseException, ResourceWarning, bool, event, float, getattr, id, int, len, list, self, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\streams\stapled.py: attributes, bytes, dict, handler, int, isinstance, item, list, listener, listeners, max_bytes, property, self, task_group, tg
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\streams\text.py: bytes, connectable, encoding, errors, int, item, property, self, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\streams\tls.py: BaseException, Exception, NotImplementedError, OSError, TypeError, args, bool, bytes, classmethod, cls, connectable, dict, exc, float, func, handler, hasattr, hostname, int, isinstance, item, list, major, max_bytes, minor, property, self, standard_compatible, staticmethod, str, task_group, transport_stream, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_backends\_trio.py: BaseException, LookupError, OSError, ReferenceError, RuntimeError, StopAsyncIteration, ValueError, abandon_on_cancel, addr, ancdata, args, bool, borrower, bytes, classmethod, cls, cmsg_data, cmsg_level, cmsg_type, command, coro, delay, dict, exc, exc_tb, exc_type, exc_val, fast_acquire, fd, filenos, fixture_func, fixturevalue, flags, float, func, future, host, id, initial_value, int, isinstance, item, kwargs, len, list, local_address, max_bytes, maxfds, memoryview, message, msglen, name, new_nurseries, nursery, obj, object, options, original, outcome_holder, path, port, property, proto, raw_socket, receive_stream, remote_address, remote_path, reuse_port, self, signals, sock, sockaddr, staticmethod, str, super, test_func, tuple, type, workers
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_asyncio_selector_thread.py: BlockingIOError, KeyError, OSError, RuntimeError, ValueError, bool, callback, events, fd, new_events, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_contextmanagers.py: BaseException, RuntimeError, TypeError, bool, exc_tb, exc_type, exc_val, isinstance, object, self, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_eventloop.py: BaseException, ImportError, KeyError, LookupError, RuntimeError, args, backend, backend_class, deadline, delay, dict, exc, float, func, loaded_backends, max, object, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_exceptions.py: BaseException, Exception, LookupError, OSError, action, exc, exception, excinfo, int, isinstance, max_bytes, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_fileio.py: FileNotFoundError, OSError, StopAsyncIteration, StopIteration, ValueError, args, b, bool, buffering, bytes, case_sensitive, classmethod, closefd, cls, data, dirs, encoding, errors, exist_ok, file, follow_symlinks, getattr, int, isinstance, lines, list, missing_ok, mode, newline, next, object, offset, on_error, opener, other, p, path_pattern, paths, pathsegments, pattern, preserve_metadata, property, self, size, str, strict, target_dir, target_is_directory, top_down, tuple, uri, walk_up, whence
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_resources.py: resource, scope
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_signals.py: signals
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_sockets.py: BaseException, OSError, TypeError, UnicodeEncodeError, ValueError, addr, af, bool, bytes, canonname, e, exc, fam, flags, float, getattr, happy_eyeballs_delay, int, isinstance, kind, len, list, listeners, local_mode, local_path, local_port, min, mode, obj, object, oserrors, port, proto, remote, remote_host, remote_port, reuse_port, sa, scope_id, self, set, socktype, sorted, ssl_context, str, tg, tls, tls_standard_compatible, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_streams.py: DeprecationWarning, ValueError, float, int, isinstance, item_type, max_buffer_size, object, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_subprocesses.py: StrOrBytesPath, ValueError, bool, bytes, check, chunk, command, creationflags, cwd, dict, env, errors, extra_groups, group, index, input, int, kwargs, list, output, pass_fds, process, start_new_session, startupinfo, stderr, stdin, stdout, str, stream, stream_contents, tg, umask, user
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_synchronization.py: BaseException, IndexError, NotImplementedError, RuntimeError, TypeError, ValueError, action, bool, borrower, cls, exc_tb, exc_type, exc_val, fast_acquire, float, initial_value, int, isinstance, len, lock, n, object, property, range, self, str, super, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_tasks.py: BaseException, NotImplementedError, TimeoutError, bool, cancel_scope, delay, float, object, property, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_tempfile.py: BaseException, b, bool, buffering, bytes, delete, delete_on_close, dict, dir, encoding, errors, exc_type, exc_value, ignore_cleanup_errors, int, lines, list, max_size, mode, newline, offset, params, prefix, property, self, size, str, suffix, super, text, traceback, tuple, type, whence
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_testing.py: NotImplemented, bool, coro, hash, id, int, isinstance, list, name, object, other, parent_id, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\anyio\_core\_typedattr.py: KeyError, TypeError, attribute, attrname, cls, default, dict, dir, getattr, object, property, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\certifi\core.py: str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\certifi\__main__.py: print
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_abnf.py: globals
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_connection.py: BaseException, RuntimeError, ValueError, args, bool, bytes, data, dict, exc, framing_type, getattr, hasattr, int, io_dict, isinstance, len, list, max_incomplete_event_size, our_role, property, request_method, response, role, self, set, sorted, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_events.py: bool, bytes, chunk_end, chunk_start, data, http_version, int, isinstance, list, name, object, reason, self, status_code, str, super, target, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_headers.py: ImportError, bool, bytes, found_name, found_raw_name, full_items, headers, idx, int, isinstance, len, length, list, new_value, new_values, object, other, out, repr, request, self, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_readers.py: buf, bytearray, bytes, class_, dict, int, isinstance, iter, len, length, line, list, self, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_receivebuffer.py: IndexError, bool, bytearray, bytes, byteslike, count, int, len, line, list, max, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_state.py: ConnectionClosed, Data, EVENT_TRIGGERED_TRANSITIONS, EndOfMessage, Event, InformationalResponse, KeyError, Request, Response, STATE_TRIGGERED_TRANSITIONS, dict, role, self, server_switch_event, set, switch_event, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_util.py: Exception, TypeError, bases, bytearray, bytes, cls, data, dict, error_status_hint, format_args, int, isinstance, kwds, memoryview, name, namespace, regex, self, str, super, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\h11\_writers.py: bytes, data, dict, event, headers, int, len, length, name, raw_name, request, response, self, str, tuple, type, value, write
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_api.py: bytes, content, extensions, headers, method, pool, response, str, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_exceptions.py: Exception, exc, from_exc, isinstance, map, to_exc, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_models.py: RuntimeError, TypeError, UnicodeEncodeError, auth, bool, bytes, chunk, extensions, hasattr, int, isinstance, k, len, list, method, name, other, part, property, self, set, ssl_context, status, str, target, tuple, type, url, v, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_synchronization.py: BaseException, ImportError, NotImplementedError, RuntimeError, TimeoutError, anyio_exc_map, bound, exc_type, exc_value, float, int, self, str, traceback, trio_exc_map, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_trace.py: BaseException, TypeError, dict, exc_value, key, kwargs, logger, name, request, self, str, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_utils.py: bool, getattr, rready, sock
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\__init__.py: ImportError, RuntimeError, locals, setattr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\connection.py: BaseException, RuntimeError, bool, exc, factor, float, http1, int, keepalive_expiry, local_address, n, network_backend, next, origin, request, retries, self, socket_options, str, trace, type, uds
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\connection_pool.py: BaseException, bool, bytes, exc, float, hasattr, http1, http2, int, isinstance, keepalive_expiry, len, list, local_address, max_connections, max_keepalive_connections, min, network_backend, part, pool, property, proxy, request, retries, self, socket_options, ssl_context, str, stream, type, uds
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\http11.py: BaseException, RuntimeError, bool, bytes, chunk, connection, exc, float, int, isinstance, keepalive_expiry, leading_data, list, max_bytes, reason_phrase, request, self, server_hostname, ssl_context, status, str, stream, trace, trailing_data, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\http2.py: BaseException, Exception, RuntimeError, any, bool, bytes, chunk, connection, dict, exc, float, int, isinstance, k, keepalive_expiry, len, list, min, range, request, self, status, str, stream, trace, tuple, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\http_proxy.py: RuntimeError, bool, bytes, float, http1, int, keepalive_expiry, key, list, local_address, max_connections, max_keepalive_connections, network_backend, origin, proxy_auth, proxy_headers, proxy_origin, proxy_ssl_context, proxy_url, remote_origin, request, retries, self, set, socket_options, str, super, trace, tuple, uds, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\interfaces.py: NotImplementedError, bool, bytes, content, extensions, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\socks_proxy.py: Exception, auth, bool, bytes, exc, float, host, http1, int, isinstance, keepalive_expiry, max_connections, max_keepalive_connections, network_backend, origin, password, port, proxy_auth, proxy_origin, proxy_url, remote_origin, request, retries, self, str, super, trace, tuple, username
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_async\__init__.py: ImportError, RuntimeError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_backends\anyio.py: Exception, OSError, TimeoutError, buffer, bytes, exc, float, host, info, int, local_address, max_bytes, option, path, port, seconds, self, server_hostname, ssl_context, str, stream, timeout
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_backends\auto.py: float, hasattr, host, int, local_address, path, port, seconds, self, socket_options, str, timeout
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_backends\mock.py: bool, buffer, bytes, float, http2, info, int, list, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_backends\sync.py: Exception, NotImplementedError, OSError, RuntimeError, bytes, e, exc, exc_map, float, func, host, info, int, isinstance, local_address, max_bytes, option, path, port, self, server_hostname, ssl_context, str, timeout
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_backends\trio.py: Exception, OSError, buffer, bytes, data, exc, exc_map, float, host, info, int, isinstance, local_address, max_bytes, option, path, port, seconds, self, server_hostname, ssl_context, str, timeout
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\connection.py: BaseException, RuntimeError, bool, exc, factor, float, http1, int, keepalive_expiry, local_address, n, network_backend, next, origin, request, retries, self, socket_options, str, trace, type, uds
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\connection_pool.py: BaseException, bool, bytes, exc, float, hasattr, http1, http2, int, isinstance, keepalive_expiry, len, list, local_address, max_connections, max_keepalive_connections, min, network_backend, part, pool, property, proxy, request, retries, self, socket_options, ssl_context, str, stream, type, uds
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\http11.py: BaseException, RuntimeError, bool, bytes, chunk, connection, exc, float, int, isinstance, keepalive_expiry, leading_data, list, max_bytes, reason_phrase, request, self, server_hostname, ssl_context, status, str, stream, trace, trailing_data, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\http2.py: BaseException, Exception, RuntimeError, any, bool, bytes, chunk, connection, dict, exc, float, int, isinstance, k, keepalive_expiry, len, list, min, range, request, self, status, str, stream, trace, tuple, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\http_proxy.py: RuntimeError, bool, bytes, float, http1, int, keepalive_expiry, key, list, local_address, max_connections, max_keepalive_connections, network_backend, origin, proxy_auth, proxy_headers, proxy_origin, proxy_ssl_context, proxy_url, remote_origin, request, retries, self, set, socket_options, str, super, trace, tuple, uds, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\interfaces.py: NotImplementedError, bool, bytes, content, extensions, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\socks_proxy.py: Exception, auth, bool, bytes, exc, float, host, http1, int, isinstance, keepalive_expiry, max_connections, max_keepalive_connections, network_backend, origin, password, port, proxy_auth, proxy_origin, proxy_url, remote_origin, request, retries, self, str, super, trace, tuple, username
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpcore\_sync\__init__.py: ImportError, RuntimeError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_api.py: auth, bool, client, content, cookies, data, files, follow_redirects, headers, json, method, params, proxy, response, str, timeout, trust_env, url, verify
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_auth.py: KeyError, NotImplementedError, StopIteration, auth_header, bytes, challenge, data, dict, enumerate, exc, field, fields, file, func, header_dict, header_fields, i, int, key, next, nonce_count, password, scheme, self, str, username, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_client.py: BaseException, DeprecationWarning, ImportError, RuntimeError, StopAsyncIteration, StopIteration, TypeError, bool, bytes, callable, cert, chunk, content, data, default_encoding, dict, exc, exc_type, exc_value, files, float, hook, http1, http2, int, isinstance, json, key, len, limits, list, max_redirects, mounts, next, other, password, pattern, property, self, sorted, str, super, traceback, tuple, type, username, verify
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_config.py: DeprecationWarning, ValueError, bool, bytes, cert, connect, dict, float, int, isinstance, keepalive_expiry, len, max_connections, max_keepalive_connections, other, pool, property, read, self, ssl_context, str, timeout, trust_env, tuple, verify, write
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_content.py: DeprecationWarning, TypeError, boundary, bytes, content, data, dict, files, hasattr, html, isinstance, item, key, len, list, part, self, str, stream, text, tuple, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_decoders.py: ImportError, NotImplementedError, bool, bytes, child, children, chunk_size, content, encoding, exc, hasattr, i, int, len, list, range, reversed, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_exceptions.py: Exception, RuntimeError, exc, property, response, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_main.py: ValueError, auth, bool, bytes, cert, chunk, client, content, cookies, ctx, dict, download, exc, files, float, follow_redirects, http2, info, int, isinstance, item, key, len, list, mime_type, name, params, progress, proxy, response, status, str, sub_item, timeout, tuple, type, url, username, value, verbose, verify
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_models.py: KeyError, LookupError, RuntimeError, TypeError, UnicodeDecodeError, ValueError, auto_headers, bool, byte_content, bytes, chunk, data, decoders, default, default_encoding, default_headers, dict, domain, enumerate, extensions, files, hasattr, header_value, history, html, i, int, isinstance, item, item_key, item_value, iter, k, key, len, line, list, max, method, name, other, param, params, part, path, property, range, raw_bytes, raw_key, raw_stream_bytes, response, reversed, self, setattr, sorted, split_commas, state, status_code, str, stream, super, tuple, type, val, values_dict
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_multipart.py: TypeError, any, bytes, c, chr, dict, field, files, float, getattr, hasattr, header_name, header_value, int, isinstance, item, key, len, list, match, range, section, self, str, tuple, type, val
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_status_codes.py: ValueError, bool, classmethod, cls, code, int, phrase, self, setattr, str, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_types.py: NotImplementedError, bool, bytes, dict, float, int, list, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_urlparse.py: ValueError, any, bool, byte, chr, component, end_position, i, int, isinstance, key, kwargs, len, list, match, next, output, parsed_frag, parsed_host, parsed_path, parsed_port, parsed_query, parsed_scheme, parsed_userinfo, property, range, safe, self, seperator, start_position, str, string, url, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_urls.py: RuntimeError, TypeError, args, bool, bytes, default, dict, hash, i, int, isinstance, item, iter, k, key, kwargs, len, list, object, other, property, self, sorted, str, tuple, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_utils.py: AttributeError, Exception, OSError, ValueError, bool, bytes, dict, encoding, hash, host, int, isinstance, len, match_type_of, mounts, other, pattern, property, scheme, self, str, stream, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\__init__.py: ImportError, locals, print, setattr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_transports\asgi.py: Exception, ImportError, StopAsyncIteration, app, bool, bytes, client, dict, int, isinstance, k, list, message, raise_app_exceptions, request, root_path, self, str, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_transports\base.py: BaseException, NotImplementedError, self, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_transports\default.py: BaseException, Exception, ImportError, ValueError, bool, bytearray, bytes, cert, dict, exc, exc_type, exc_value, from_exc, hasattr, http1, http2, httpcore_stream, int, isinstance, issubclass, len, limits, local_address, part, request, retries, self, socket_options, str, to_exc, traceback, trust_env, tuple, type, uds, verify
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_transports\mock.py: TypeError, handler, isinstance, request, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\httpx\_transports\wsgi.py: app, bool, bytes, chunk, exc_info, getattr, header_key, header_value, int, iter, list, part, raise_app_exceptions, remote_addr, request, response_headers, script_name, self, status, str, tuple, value, wsgi_errors
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\idna\codec.py: bool, bytes, errors, final, int, isinstance, label, len, name, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\idna\compat.py: NotImplementedError, bytearray, bytes, label, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\idna\core.py: IndexError, UnicodeDecodeError, UnicodeEncodeError, UnicodeError, ValueError, bool, bytearray, bytes, char, check_ltr, chr, cp, domain, enumerate, i, idx, int, isinstance, len, ord, pos, range, repr, script, std3_rules, str, strict, transitional, uts46
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\idna\intranges.py: bool, end, enumerate, i, int, int_, left, len, list, list_, r, right, sorted, start, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\idna\uts46data.py: int, list, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\__init__.py: args, int, list, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\__pip-runner__.py: SystemExit, classmethod, fullname, str, target, v, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\build_env.py: BaseException, NotImplementedError, a, args, b, extra_index, for_req, format_control, fp, getattr, hasattr, host, installer, isinstance, kind, link, list, name, old_value, open, prefix_as_string, req_str, reqs, requirements, reversed, self, set, sorted, spinner, str, tuple, type, varname
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cache.py: Exception, NotImplementedError, bool, cache_dir, candidate, d, dict, download_info, e, link, list, min, package_name, persistent, self, staticmethod, str, super, supported_tags, wheel_dir, wheel_name
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\configuration.py: IndexError, KeyError, OSError, UnicodeDecodeError, bool, clean_config, dict, error, f, file_values, files, fname, isolated, list, load_only, map, open, path, property, repr, section, self, str, super, tuple, val, value, variant
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\exceptions.py: AttributeError, Exception, KeyError, OSError, UnicodeDecodeError, a, allowed, bool, classmethod, cls, command_description, config, console, dict, dist, distribution, download, e, error, error_msg, errors_of_cls, exit_code, expecteds, f_val, failed, field, fname, found, getattr, gots, gotten_hash, hasattr, hash_name, hint_stmt, indent, int, invalid_exc, ireq, isinstance, key, kind, lang, len, link, list, location, m_val, metadata_name, name, next, note_stmt, options, output_lines, package_details, r, reason, request, response, s, self, sep, staticmethod, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\main.py: args, int, list, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\pyproject.py: all, bool, error, f, isinstance, item, list, obj, open, pyproject_toml, req_name, requirement, setup_py, str, unpacked_source_directory
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\self_outdated_check.py: KeyError, OSError, ValueError, bool, cache_dir, current_time, dict, f, get_remote_version, isodate, local_version, open, options, pkg, property, pypi_version, self, session, statefile, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\wheel_builder.py: Exception, OSError, base, bool, build_failures, build_options, build_successes, e, editable, global_options, isinstance, length, list, output_dir, req, requirements, s, str, temp_dir, tuple, verify, wheel_cache, wheel_hash
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\__init__.py: args, int, list, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\autocompletion.py: IndexError, any, directory, dist, f, handler_name, i, int, k, list, name, o, opt_str, option, path, print, str, v, word, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\base_command.py: BaseException, KeyboardInterrupt, NotImplementedError, args, bool, dict, exc, hasattr, int, isinstance, isolated, list, name, options, print, self, set, sorted, str, summary, super, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\cmdoptions.py: ValueError, abis, algo, all, any, bool, cache_dir, cert, check_target, client_cert, cmd_opts, debug_mode, dict, digest, disable_pip_version_check, error_msg, exc, getattr, group, groupname, help_, implementation, index_url, int, isinstance, isolated_mode, key, keyring_provider, len, list, log, no_cache, no_color, no_index, no_input, no_python_version_warning, opt_str, option, options, package, parser, part, platforms, proxy, python, python_version, quiet, require_virtualenv, resume_retries, retries, sep, set, setattr, str, timeout, tuple, use_deprecated_feature, use_new_feature, val, verbose, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\command_context.py: context_provider, self, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\index_command.py: Exception, ImportError, classmethod, getattr, hasattr, int, list, min, options, retries, self, str, super, timeout
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\main.py: DeprecationWarning, cmd_args, cmd_name, e, exc, int, list, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\main_parser.py: OSError, args, args_else, command_info, exc, exe, general_options, len, list, name, python, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\parser.py: ValueError, bool, dict, epilog, err, exc, getattr, hasattr, heading, i, idx, indent, int, isinstance, isolated, key, len, line, list, mvarfmt, name, optsep, print, property, section, section_items, section_key, self, set, str, super, text, tuple, usage, v, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\progress_bars.py: bar_type, bytes, chunk, float, initial_progress, int, iter, iterable, len, req, size, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\req_command.py: any, args, bool, build_tracker, classmethod, cls, dict, download_dir, filename, finder, force_reinstall, func, getattr, ignore_installed, ignore_requires_python, int, kw, list, options, parsed_req, preparer, py_version_info, registry, req, requirements, self, session, staticmethod, str, super, t, target_python, temp_build_dir, tuple, upgrade_strategy, use_pep517, use_user_site, verbosity, wheel_cache
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\cli\spinners.py: Exception, KeyboardInterrupt, NotImplementedError, SPINNER_CHARS, SPINS_PER_SECOND, bool, final_status, float, label, len, message, min_update_interval_seconds, next, options, self, spin_chars, status, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\cache.py: args, dict, e, filename, int, len, list, options, self, sorted, str, subdir
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\check.py: conflicting, dep_name, dep_version, dependency, int, list, missing, package, package_set, parsing_probs, project_name, req, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\completion.py: int, list, options, print, self, shell, sorted, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\configuration.py: Exception, FileNotFoundError, any, args, bool, confname, confvalue, dict, e, example, files, int, len, list, n, name, need_value, options, self, site_config_file, sorted, str, variant
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\debug.py: ImportError, config, dict, expected_version, f, getattr, globals, int, key, len, level, line, list, locals, name, options, self, str, tag, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\download.py: args, downloaded, int, list, options, req, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\freeze.py: bool, int, line, list, options, self, set, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\hash.py: archive, args, chunk, int, list, open, options, path, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\help.py: IndexError, args, int, list, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\index.py: args, bool, candidate, dict, e, ignore_requires_python, int, len, list, options, self, session, set, sorted, str, ver, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\inspect.py: dict, dist, int, list, options, res, self, set, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\install.py: Exception, KeyError, OSError, all, any, args, bool, build_failures, conflict_details, conflicting, d, dep_name, dep_version, dependency, distribution, error, f, home, int, isolated, isolated_mode, item, len, lib_dir, list, missing, open, options, package, package_set, part, prefix, prefix_path, project_name, r, req, resolver_variant, root, root_path, s, self, set, sorted, str, target_dir, type, upgrade, use_user_site, user, using_user_site
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\list.py: FileNotFoundError, any, candidate, d, dep, dist, enumerate, i, int, len, list, map, n, options, p, pkg, pkg_strings, pkgs, proj, self, session, set, sizes, sorted, str, super, tuple, val, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\lock.py: args, int, list, options, req, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\search.py: UnicodeEncodeError, args, dict, fault, hit, int, isinstance, len, list, max, options, packages, self, str, versions
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\show.py: FileNotFoundError, KeyError, args, bool, classifier, current_dist, d, distributions, entry, enumerate, i, int, label, line, list, list_files, map, name, options, pkg, project_url, query_name, req, self, sorted, str, tuple, url, url_label, verbose, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\uninstall.py: args, filename, int, list, name, options, parsed_req, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\wheel.py: OSError, args, build_failures, build_successes, e, int, len, list, options, req, reqs_to_build, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\commands\__init__.py: class_name, commands_dict, dict, getattr, kwargs, module_path, str, summary
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\distributions\base.py: NotImplementedError, bool, req, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\distributions\installed.py: bool, property, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\distributions\sdist.py: bool, build_env_installer, build_isolation, check_build_deps, conflicting, conflicting_reqs, conflicting_with, installed, map, missing, property, repr, self, set, sorted, str, tuple, wanted
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\distributions\wheel.py: bool, property, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\distributions\__init__.py: install_req
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\index\collector.py: Exception, anchor, attrs, bool, bytes, cache_link_parsing, cacheable_page, candidates_from_page, classmethod, dict, exc, file, fn, hash, headers, int, isinstance, len, list, loc, location, name, object, options, other, page, path, project_name, property, request_desc, response, s, scheme, self, session, str, super, suppress_no_index, tag, tuple, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\index\package_finder.py: Exception, ValueError, allow_yanked, bool, c, cand_iter, classmethod, cls, detail, dict, eggs, enumerate, fragment, frozenset, host_port, i, idx, int, isinstance, len, link_collector, links, list, map, max, no_eggs, project_name, project_url, property, req, result, s, seen, selection_prefs, self, set, sorted, source, sources, str, tag, tuple, upgrade, v, version_info
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\index\sources.py: NotImplementedError, bool, cache_link_parsing, candidates_from_page, dict, entry, expand_dir, file_url, list, location, page_validator, project_name, property, self, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\locations\base.py: AttributeError, OSError, bool, new_root, pathname, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\locations\_distutils.py: AttributeError, ImportError, UnicodeDecodeError, bool, dict, dist_args, dist_name, getattr, home, i, ignore_config_files, isolated, key, list, p, root, str, user
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\locations\_sysconfig.py: bool, getattr, home, k, key, prefix, root, set, str, user
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\locations\__init__.py: KeyError, all, any, bool, cmd, dict, dist_name, getattr, home, isolated, k, key, len, p, prefix, root, scheme, str, user, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\base.py: FileNotFoundError, NotImplementedError, OSError, UnicodeDecodeError, ValueError, bool, bytes, classmethod, d, dep, dict, dist, e, editables_only, include_editables, list, local_only, p, property, row, self, skip, str, stream, tuple, user_only
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\pkg_resources.py: AttributeError, FileNotFoundError, UnicodeDecodeError, base_dir, bool, bytes, classmethod, cls, directory, dist_dir_name, e, entries, entry_point, extra, filename, group, info_dir, isinstance, list, map, metadata_contents, path, paths, project_name, property, repr, self, set, str, value, wheel, wheel_name, ws, zf
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\_json.py: UnicodeDecodeError, bytes, dict, field, h, isinstance, list, msg, multi, str, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\__init__.py: KeyError, ValueError, bool, bytes, canonical_name, directory, filename, getattr, hasattr, list, metadata_contents, paths, str, type, wheel
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py: NotImplementedError, ValueError, d, dist, getattr, isinstance, property, reason, self, sep, stem, str, suffix, tuple, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py: FileNotFoundError, KeyError, NotImplementedError, UnicodeDecodeError, any, bool, bytes, child, classmethod, cls, context, contexts, dict, directory, e, extra, extras, filename, fullpath, info_dir, isinstance, iter, metadata_contents, name, path, property, relpath, req_string, self, str, zf
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py: bool, child, classmethod, cls, dist, distribution, e, f, line, list, location, next, paths, self, set, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\candidate.py: link, name, object, self, str, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\direct_url.py: Exception, ValueError, bool, classmethod, cls, d, default, dict, expected_type, hash_name, hash_value, hashes, info, isinstance, k, key, kwargs, len, netloc_no_user_pass, property, s, self, str, type, user_pass, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\format_control.py: NotImplemented, all, bool, canonical_name, frozenset, getattr, isinstance, k, object, other, self, set, staticmethod, str, target, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\index.py: file_storage_domain, path, self, str, super, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\installation_report.py: classmethod, dict, install_requirements, ireq, self, sorted, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\link.py: IndexError, KeyError, NotImplemented, all, anchor_attribs, any, base_url, bool, cache_link_parsing, classmethod, cls, comes_from, dict, file_data, hashname, hashval, int, isinstance, iter, k, link, link1, link2, list, n, next, other, page_url, part, property, query, requires_python, reserved, self, sep, str, to_clean, tuple, v, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\pylock.py: NotImplementedError, bool, classmethod, cls, data, dict, install_requirements, ireq, isinstance, key, list, p, path, self, sorted, str, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\scheme.py: str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\search_scope.py: bool, built_find_links, classmethod, cls, find_links, index_urls, list, no_index, project_name, self, str, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\selection_prefs.py: allow_all_prereleases, allow_yanked, bool, format_control, prefer_binary, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\target_python.py: abis, implementation, int, key, list, map, part, platforms, self, set, str, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\models\wheel.py: StopIteration, ValueError, abi, bool, dict, e, enumerate, filename, frozenset, i, int, list, min, next, plat, property, py, self, sorted, str, t, tag, tag_to_priority, tags
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\auth.py: AttributeError, Exception, FileNotFoundError, ImportError, ValueError, allow_keyring, allow_netrc, bool, dict, exc, hasattr, index_url_user_password, index_urls, kwargs, list, netloc, original_url, prompting, property, pw, resp, self, service_name, str, tuple, un, url_user_password
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\cache.py: OSError, body, body_file, bool, bytes, data, directory, f, getattr, int, key, list, name, open, response, self, source_file, str, super, value, writer_func
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\download.py: ConnectionError, KeyError, OSError, TypeError, ValueError, bool, bytes, chunk, content_file, data, default_filename, e, f, identifier, int, isinstance, key, len, link, links, location, open, original_response, progress_bar, range_start, resume_retries, self, session, should_match, str, total_length, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\lazy_wheel.py: Exception, base_headers, bool, bytes, chunk, chunk_size, dict, exc, int, j, k, length, list, lslice, max, min, offset, property, range, reversed, rslice, self, session, size, str, tuple, url, whence, zf, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\session.py: Exception, OSError, SECURE_ORIGINS, ValueError, any, args, block, bool, cache, cert, conn, connections, data, dict, distro_infos, exc, filter, float, host, index_urls, int, kwargs, list, location, maxsize, method, name, new_index_urls, open, origin_host, origin_port, parsed_host, parsed_port, pool_kwargs, port, proxy, proxy_kwargs, secure_host, secure_origin, secure_port, secure_protocol, self, source, ssl_context, str, super, suppress_logging, trusted_hosts, tuple, type, url, x, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\utils.py: AttributeError, UnicodeDecodeError, bytes, chunk_size, dict, int, isinstance, resp, response, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\network\xmlrpc.py: bool, exc, handler, host, index_url, isinstance, request_body, self, session, str, super, tuple, use_datetime, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\check.py: FileNotFoundError, OSError, ValueError, bool, conflicting_deps, dict, e, frozenset, inst_req, list, map, missing_deps, p, package_detail, package_name, packages, req, set, should_ignore, sorted, str, supported_tags, to_install, tuple, wheel_tags
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\freeze.py: bool, classmethod, cls, dict, dist, emitted_options, ex, exc, exclude_editable, files, installation, installations, isolated, len, list, local_only, name, open, paths, property, req_file, req_file_path, req_files, requirement, self, set, skip, sorted, str, tuple, type, user_only, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\prepare.py: OSError, bool, build_dir, build_env_installer, build_isolation, build_isolation_installer, build_tracker, check_build_deps, dict, download, download_dir, exc, f, filepath, finder, int, isinstance, lazy_wheel, legacy_resolver, links_to_fully_download, list, location, open, parallel_builds, partially_downloaded_reqs, progress_bar, require_hashes, resume_retries, self, session, skip_reason, src_dir, str, super, use_user_site, verbosity, warn_on_hash_mismatch
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\build_tracker.py: BaseException, FileNotFoundError, KeyError, LookupError, changes, ctx, dict, fp, isinstance, key, list, name, new_value, object, open, original_value, req, saved_values, self, str, tracker, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\metadata.py: backend, build_env, details, error, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py: backend, build_env, details, error, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\metadata_legacy.py: bool, build_env, details, directory, error, f, isolated, len, setup_py_path, source_dir, spinner, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\wheel.py: Exception, backend, metadata_directory, name, str, tempd
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py: Exception, backend, e, metadata_directory, name, str, tempd
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\build\wheel_legacy.py: Exception, build_options, command_args, command_output, global_options, len, list, name, setup_py_path, sorted, source_dir, spinner, str, temp_dir, tempd
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\install\editable_legacy.py: bool, build_env, global_options, home, isolated, name, prefix, setup_py_path, str, unpacked_source_directory, use_user_site
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\operations\install\wheel.py: KeyError, ValueError, any, bool, changed, data_scheme_paths, dest, dest_dir_path, dest_subpath, destfile, dict, dir_scripts, direct_url, direct_url_file, dist, e, entry_point, f, file, generated, getattr, grouped_by_dir, gui, h, hash_, i, info_dir, installed, installed_path, installed_record_path, installed_rows, installer_file, int, k, key, kwargs, len, list, map, metadata, min, mode, modified, old_csv_rows, open, options, other_scheme_paths, outrows, pycompile, record_file, req_description, requested, root_scheme_paths, row, scheme, scheme_key, script, script_scheme_paths, scripts, self, set, size, sorted, sorted_scripts, specification, src_record_path, srcfile, stdout, str, super, target_path, tuple, warn_for, warn_script_location, wheel_path, wheel_zip, z, zip_file
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\constructors.py: any, bool, comes_from, config_settings, constraint, dict, editable_req, exc, extras_override, f, filename, global_options, hash_options, ireq, isolated, len, line_source, list, match, new_extras, next, op, open, p, parsed_req, permit_editable_wheels, post, pre, req_string, set, sorted, str, text, tuple, use_pep517, user_supplied, version_control
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\req_dependency_group.py: FileNotFoundError, LookupError, OSError, TypeError, ValueError, dict, e, fp, groupname, groups, isinstance, list, open, path, paths, req, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\req_file.py: BOMS, Exception, OSError, SUPPORTED_OPTIONS, SUPPORTED_OPTIONS_EDITABLE_REQ, SUPPORTED_OPTIONS_REQ, UnicodeDecodeError, ValueError, args_str, bom, bool, bytes, constraint, data, dest, dict, e, enumerate, env_var, exc, f, filename, finder, host, int, len, line_number, lineno, list, o, open, option_factory, options_str, opts, parsed_files_stack, parsed_line, property, self, session, str, token, tuple, url, var_name
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\req_install.py: AssertionError, any, archive_source, attr, auto_confirm, autodelete, backend, backend_path, bool, build_dir, check, config_settings, constraint, dict, dirname, dirnames, dirpath, editable, extra, extras, filenames, getattr, global_options, hasattr, hash_options, home, isinstance, isolated, iter, len, list, next, option, options, parallel_builds, parent_dir, parentdir, permit_editable_wheels, prefix, property, pycompile, req, reqs, requires, root, rootdir, self, set, sorted, str, trust_internet, use_pep517, use_user_site, user_supplied, vars, verbose, warn_script_location
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\req_set.py: KeyError, bool, check_supported_wheels, dict, install_req, len, list, name, property, req, self, sorted, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\req_uninstall.py: FileNotFoundError, KeyError, NotADirectoryError, OSError, ValueError, a, all_files, all_subdirs, any, args, auto_confirm, bool, bytes, classmethod, cls, d, dict, dirfiles, dirname, dirpath, dist, dn, entry_point, ex, f, fh, fn, fname, folder, installed_file, is_gui, item, kw, len, line, list, map, msg, old_head, open, p, paths, property, pth, root, s, script, script_name, seen, self, set, short_paths, shortpath, sorted, str, subdirs, tail, top_level_pkg, tuple, verbose, w, wildcards
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\req\__init__.py: Exception, bool, global_options, home, iter, len, list, prefix, progress_bar, pycompile, req, requirement, requirements, root, str, tuple, use_user_site, warn_script_location
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\base.py: NotImplementedError, bool, list, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py: FileNotFoundError, KeyError, add_to_parent, bool, check_supported_wheels, dep, discovered_reqs, e, exc, extras_requested, finder, force_reinstall, ignore_dependencies, ignore_installed, ignore_requires_python, install_req, int, list, make_install_req, map, missing, more_reqs, ordered_reqs, preparer, req, req_set, req_to_install, root_reqs, self, set, sorted, str, subreq, super, to_scan_again, tuple, upgrade_strategy, use_user_site, version_info, wheel_cache
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py: NotImplemented, NotImplementedError, all, bool, candidate, classmethod, extras, frozenset, ireq, isinstance, link, other, project, property, self, sorted, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py: NotImplemented, NotImplementedError, bool, c, candidate, comes_from, e, exc, extra, extras, frozenset, hash, int, isinstance, list, object, other, property, py_version_info, r, rest, self, sorted, str, super, template, tuple, with_requires
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py: KeyError, all, base_requirements, bool, c, cause, causes, comes_from, constraint, constraints, dict, e, enumerate, explicit_candidates, extras, finder, frozenset, hashes, i, ican, id, identifier, ignore_installed, ignore_requires_python, incompatibilities, incompatible_ids, int, ireqs, is_satisfied_by, isinstance, iter, key, len, link, list, lookup_cand, make_install_req, next, parent, parts, prefers_installed, preparer, property, py_version_info, r, req, requested_extras, reversed, root_ireqs, self, set, sorted, sp, str, tuple, use_user_site, v, versions_set, wheel_cache, yanked_versions_set
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py: NotImplementedError, any, bool, c, e, func, get_infos, id, incompatible_ids, installed, int, prefers_installed, self, set, tuple, version, versions_found
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py: StopIteration, any, backtrack_causes, bool, candidate, constraints, default, dict, directs, identifier, identifiers, ignore_dependencies, incompatibilities, info, information, int, ireq, ireqs, isinstance, iter, list, mapping, name, next, op, open_bracket, operators, r, requirement, requirement_or_candidate, self, set, specifier, specifier_set, staticmethod, str, tuple, upgrade_strategy, user_requested, ver, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py: candidate, criterion, index, int, parent, req, req_info, requirement, self, state, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py: NotImplemented, bool, candidate, e, frozenset, hash, int, ireq, isinstance, len, match, object, other, property, s, self, specifier, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py: KeyError, bool, c, candidate, check_supported_wheels, child, dict, e, finder, force_reinstall, ignore_dependencies, ignore_installed, ignore_requires_python, int, item, key, leaf, len, list, make_install_req, max, node, path, preparer, py_version_info, requirement_keys, resolver, root_reqs, self, set, sorted, str, super, tuple, upgrade_strategy, use_user_site, wgts, wheel_cache
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\appdirs.py: appname, bool, list, roaming, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\compat.py: ImportError, OSError, bool, encoding, errors, hasattr, int, package, path, resource, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\compatibility_tags.py: abi, abis, actual_arch, actual_multiarch, api_level, arch, arch_prefix, arch_sep, arch_suffix, c, impl, int, len, list, major, map, minor, name, p, set, str, supported, tuple, version_info
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\datetime.py: bool, day, int, month, year
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\deprecation.py: Warning, category, feature_flag, file, filename, format_str, gone_in, int, issubclass, issue, line, lineno, reason, replacement, str, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py: bool, direct_url, isinstance, link, link_is_in_wheel_cache, name, requested_revision, source_dir, str, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\egg_link.py: egg_link_name, list, path_item, raw_name, site, sites, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\entrypoints.py: args, int, list, parts, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\filesystem.py: FileExistsError, OSError, PermissionError, bool, f, filename, files, float, hasattr, int, kwargs, list, pattern, range, root, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\filetypes.py: BZ2_EXTENSIONS, TAR_EXTENSIONS, XZ_EXTENSIONS, ZIP_EXTENSIONS, bool, name, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\glibc.py: AttributeError, ImportError, OSError, ValueError, isinstance, str, tuple, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\hashes.py: NotImplemented, TypeError, ValueError, alg, bool, bytes, chunk, chunks, dict, digest, digest_list, digests, file, got, hash, hash_name, hashes, hex_digest, int, isinstance, k, len, list, object, open, other, path, property, self, sorted, str, sum, super, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\logging.py: BaseException, BrokenPipeError, Exception, OSError, add_timestamp, args, bool, console, exc, exc_class, getattr, int, isinstance, kwargs, levelno, line, list, no_color, num, options, record, rich_renderable, self, stderr, str, super, tuple, type, user_log_file, verbosity
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\misc.py: AttributeError, BaseException, Exception, IndexError, OSError, TypeError, ValueError, action, args, auth, backend_path, block, blocksize, bool, build_backend, bytes, classmethod, cls, col, config_holder, dict, dir, e, exc_info, f, file, filter, float, func, handler, hasattr, head, ignore_errors, input, int, isinstance, iter, key, len, list, map, max, message, metadata_directory, modifying_pip, msg, named, new, old, open, options, orig_stream, other, port, pred, print, property, python_executable, range, req, resolve_symlinks, row, runner, scheme, sdist_directory, self, sequential, size, source_dir, str, super, t1, t2, tail, transform_netloc, tuple, type, url_without_auth, value, wheel_directory, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\packaging.py: bool, int, map, req_string, requires_python, str, tuple, version_info
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\retry.py: Exception, args, float, func, kwargs, stop_after_delay, wait
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\setuptools_build.py: bool, build_options, destination_dir, egg_info_dir, global_options, home, list, no_user_config, prefix, setup_py_path, str, unbuffered_output, use_user_site
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\subprocess.py: Exception, ValueError, arg, args, bool, cmd, command_args, command_desc, cwd, err, err_line, exc, extra_environ, int, isinstance, list, log_failed_cmd, message, name, on_returncode, out, out_line, show_stdout, spinner, stdout_only, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\temp_dir.py: BaseException, OSError, bool, candidate, classmethod, cls, dict, enumerate, errors, ex, exc_val, func, globally_managed, i, ignore_cleanup_errors, kind, len, list, name, old_tempdir_manager, original, property, range, root, self, stack, str, super, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\unpacking.py: AttributeError, Exception, ImportError, KeyError, bool, content_type, destfp, directory, exc, flatten, info, int, list, lnk_lead, lnk_rest, location, name_lead, name_rest, open, paths, str, target
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\urls.py: ValueError, len, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\virtualenv.py: OSError, bool, f, getattr, hasattr, line, list, open, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\wheel.py: KeyError, RuntimeError, UnicodeDecodeError, ValueError, bytes, dist_info_dir, e, int, len, map, name, p, s, source, str, tuple, wheel_data, wheel_zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\_jaraco_text.py: StopIteration, filter, iter, iterable, line, map, next, str, text
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\utils\_log.py: args, kwargs, msg, name, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\vcs\bazaar.py: bool, classmethod, cls, dest, int, list, location, rev, rev_options, self, staticmethod, str, super, tuple, user_pass, verbosity, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\vcs\git.py: IndexError, ValueError, bool, classmethod, cls, dest, fragment, getattr, int, is_branch, kwargs, len, list, location, netloc, path, query, ref_name, ref_sha, remote, scheme, self, staticmethod, str, super, tuple, user_pass, verbosity
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\vcs\mercurial.py: OSError, bool, classmethod, cls, config_file, dest, exc, int, list, location, open, rev, rev_options, self, staticmethod, str, super, tuple, verbosity
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\vcs\subversion.py: ValueError, bool, classmethod, cls, d, dest, dirs, dirurl, extra_args, f, int, len, list, localrev, m, map, max, netloc, open, password, rev_options, scheme, self, staticmethod, str, super, tuple, user_pass, username, verbosity
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_internal\vcs\versioncontrol.py: Exception, FileNotFoundError, NotADirectoryError, NotImplementedError, PermissionError, ValueError, args, backend, bool, classmethod, cls, cwd, dest, dict, drive, extra_environ, extra_ok_returncodes, hasattr, int, len, list, log_failed_cmd, max, netloc, on_returncode, path, project_name, property, query, remote_url, repo, repo_dir, repo_root, secret_password, secret_url, self, show_stdout, spinner, staticmethod, stdout_only, str, super, tuple, type, url1, url2, user_pass, username, vcs_backend, verbosity
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\__init__.py: ImportError, base, globals, head, locals, modulename, setattr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py: args, bool, bytes, cache, cache_etags, cacheable_methods, cert, controller_class, float, heuristic, int, kw, proxies, request, serializer, str, stream, super, timeout, tuple, type, verify, weak_self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\cache.py: NotImplementedError, bytes, init_dict, int, key, self, str, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\controller.py: Exception, IndexError, KeyError, ValueError, body, bool, bytes, cache, cache_etags, cc_directive, classmethod, cls, dict, headers, int, isinstance, k, len, max, query, request, required, response_headers, response_or_ref, retval, self, serializer, status_codes, str, tuple, typ, uri, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py: AttributeError, amt, bool, bytes, callback, closed, data, getattr, int, memoryview, name, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py: dict, dt, kw, max, min, resp, response, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py: TypeError, ValueError, body_file, bytes, dict, headers, k, len, request, response, response_headers, self, str, v, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py: bool, cache_etags, cacheable_methods, controller_class, heuristic, serializer, sess, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py: cache_controller, print
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py: FileNotFoundError, ImportError, body, bool, bytes, data, directory, dirmode, fd, fh, filecache, filemode, forever, int, list, open, path, self, staticmethod, str, suffix, type, url, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py: bytes, conn, expires, int, isinstance, key, self, str, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\certifi\core.py: str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\certifi\__main__.py: print
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\dependency_groups\_implementation.py: LookupError, NotImplementedError, TypeError, ValueError, dependency_groups, dict, elements, group_name, groups, isinstance, item, iter, len, list, name, names, next, normed_name, original_names, r, requested_group, self, str, super, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\dependency_groups\_lint_dependency_groups.py: LookupError, SystemExit, TypeError, ValueError, argv, e, errors, fp, groupname, list, msg, open, print, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\dependency_groups\_pip_wrapper.py: LookupError, SystemExit, TypeError, ValueError, argv, deps, e, errors, fp, groupname, list, msg, open, print, r, resolved, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\dependency_groups\_toml_compat.py: ImportError, ModuleNotFoundError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\dependency_groups\__main__.py: SystemExit, fp, open, print
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\distlib\compat.py: AttributeError, ImportError, KeyError, LookupError, NameError, StopIteration, SyntaxError, TypeError, UnicodeDecodeError, ValueError, any, args, basestring, bytes, cert, classmethod, cls, cmd, config, dict, dict_delitem, dict_setitem, dir, dn, e, ext, fillvalue, fn, frag, get_ident, getattr, hasattr, hostname, id, input, int, isinstance, iter, iterable, k, kwds, leftmost, len, line, list, map, mapping, maps, max_wildcards, mode, node, obj, object, orig_enc, property, readline, remainder, repr, set, setattr, staticmethod, str, sub, tb, thefile, tuple, type, unicode, user_function, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\distlib\resources.py: AttributeError, ImportError, IndexError, f, getattr, hasattr, isinstance, len, name, open, package, resource_name, self, set, sorted, staticmethod, super, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\distlib\scripts.py: Exception, OSError, UnicodeDecodeError, ValueError, add_launchers, dict, dn, e, encoding, env, exename, fileop, fp, getattr, int, kind, len, names, open, options, property, r, self, set, source_dir, specification, specifications, target_dir, value, zf
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\distlib\util.py: Exception, ImportError, KeyError, OSError, SyntaxError, ValueError, abs_base, abs_path, allowed_chars, append, archive_filename, base, bits, callable, check, cmd, con, curval, default, dict, directory, dotted_path, dry_run, duration, e, edges, eh, encoding, enumerate, error_prompt, event, exc, exports, f, files, final, float, force, func, getattr, h, hasattr, host, incr, infile, instream, int, isinstance, iter, k, key, len, list, marker_string, mask, maxval, member, min, minval, module_name, netloc, node, o, obj, object, open, optimize, other, outfile, path_glob, pathname, pred, project_name, prompt, property, req, resources_root, reversed, rhs, rules, seconds, self, seq, set, setattr, sorted, source, specification, str, subscriber, succ, super, target, tarinfo, tuple, type, unit, use_abspath, version, zf
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\distlib\__init__.py: Exception, ImportError, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\distro\distro.py: DeprecationWarning, FileNotFoundError, ImportError, KeyError, OSError, ValueError, attribute, best, bool, bytes, bytestring, dict, distro_release_file, f, fp, full_distribution_name, include_lsb, include_oslevel, include_uname, k, len, line, lines, list, major, minor, obj, open, os_release_file, pretty, release_file, root_dir, self, staticmethod, str, table, token, tuple, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\idna\codec.py: bool, bytes, errors, final, int, isinstance, label, len, name, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\idna\compat.py: NotImplementedError, bytearray, bytes, label, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\idna\core.py: IndexError, UnicodeDecodeError, UnicodeEncodeError, UnicodeError, ValueError, bool, bytearray, bytes, char, check_ltr, chr, cp, domain, enumerate, i, idx, int, isinstance, len, ord, pos, range, repr, script, std3_rules, str, strict, transitional, uts46
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\idna\intranges.py: bool, end, enumerate, i, int, int_, left, len, list, list_, r, right, sorted, start, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\idna\uts46data.py: int, list, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\msgpack\exceptions.py: Exception, OverflowError, ValueError, extra, self, unpacked
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\msgpack\ext.py: TypeError, ValueError, b, bytes, cls, code, divmod, dt, hash, int, isinstance, len, other, self, staticmethod, super, type, unix_ns, unix_sec
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\msgpack\fallback.py: OverflowError, RecursionError, StopIteration, TypeError, ValueError, autoreset, bool, bytearray, callable, check_type_strict, default, dict, execute, ext_hook, file_like, float, fmt, hasattr, int, isinstance, k, kwargs, len, list, list_hook, max, memoryview, min, nest_limit, next_bytes, object_hook, object_pairs_hook, packed, pairs, raise_outofdata, range, raw, read_size, self, size, str, strict_map_key, strict_types, t, timestamp, tuple, type, typecode, use_bin_type, use_list, use_single_float, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\msgpack\__init__.py: ImportError, kwargs, o, stream
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\markers.py: NotImplemented, ValueError, all, any, bool, context, dict, e, env, environment, first, frozenset, groups, hash, info, int, isinstance, item, key, len, list, m, marker, markers, op, oper, other, results, self, str, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\metadata.py: AttributeError, Exception, KeyError, UnicodeDecodeError, ValueError, added, bin, bool, bytes, cause, chunks, classmethod, cls, content_type, converter, data, dict, dynamic_field, exc_group, exceptions, frozenset, getattr, h, instance, isinstance, k, key, label, len, list, map, max, metadata_version_exc, msg, object, p, pair, parameters, path, raw, repr, req, self, source, str, super, tuple, type, unparsed, unparsed_key, url, validate
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\requirements.py: NotImplemented, ValueError, bool, e, hash, int, isinstance, name, other, requirement_string, self, set, sorted, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\specifiers.py: NotImplemented, ValueError, all, any, bool, components, epoch, filtered, frozenset, getattr, hash, installed, int, isinstance, iter, left, left_split, len, list, map, max, object, op, operator_callable, padded_prospective, property, rest, result, right, right_split, s, segment, self, sorted, spec_str, specifiers, str, tuple, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\tags.py: INTERPRETER_SHORT_NAMES, NotImplemented, SystemError, TypeError, ValueError, bool, cpu_arch, dict, explicit_abi, frozenset, hasattr, hash, id, int, interpreters, is_32bit, isinstance, len, list, major, map, minor, object, other, platform_, property, range, release, self, set, str, string, tag, tuple, value, ver, warn
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\utils.py: ValueError, bool, e, frozenset, int, len, sep, str, strip_trailing_zero, tuple, validate, version_part
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\version.py: NotImplemented, ValueError, bool, bytes, enumerate, hash, i, index, int, isinstance, len, list, max, object, other, part, property, reversed, self, str, super, tuple, val, version, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\_elffile.py: KeyError, ValueError, bytes, e, e_fmt, f, fmt, index, int, property, range, self, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\_manylinux.py: AssertionError, AttributeError, ImportError, OSError, RuntimeWarning, TypeError, ValueError, any, arch, archs, bool, dict, executable, f, glibc_major, glibc_max, hasattr, int, isinstance, open, path, range, set, str, tuple, version, version_string
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\_musllinux.py: OSError, TypeError, ValueError, arch, archs, executable, f, int, len, minor, n, open, output, print, range, str, t
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\_parser.py: NotImplementedError, after, env_var, int, list, python_str, self, source, str, tokenizer, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\_structures.py: bool, hash, int, isinstance, object, other, repr, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\_tokenizer.py: Exception, around, bool, close_token, dict, expected, int, len, message, name, open_token, pattern, peek, rules, self, source, span_end, span_start, str, super, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\licenses\_spdx.py: bool, dict, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\packaging\licenses\__init__.py: Exception, ValueError, ast, globals, len, locals, raw_license_expression, ref, str, token
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py: AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, FileExistsError, ImportError, KeyError, NotADirectoryError, NotImplementedError, OSError, PermissionError, RuntimeError, RuntimeWarning, SyntaxError, SystemError, TypeError, UnicodeDecodeError, UserWarning, ValueError, Warning, any, archive_name, attr, base, basename, bool, by_key, bytes, callback, callbacks, child, classes, classmethod, compile, data, dep, deps, dict, dir, distribution_finder, distributions, e, e_k_b_n_c, egg_info, enumerate, error_info, ex, exc, existing, ext, extra, extras_spec, f, fallback, fallback_encoding, fh, file, file_path, filter, float, frozenset, full_env, getattr, globals, hasattr, hash, importer_type, initial_value, insert, installer, int, isinstance, iter, k, kw, kwargs, len, list, loader_type, locals, location, map, maps, modname, moduleOrReq, module_name, namespace, namespace_handler, new_requirement, next, normalized_to_canonical_keys, ob, object, only, open, orig_path, other, outf, package, packageName, package_name, package_or_requirement, pkg, plugin_env, precedence, project, property, provided, provider_factory, py_version, python, r, ref, registry, replace, replace_conflicting, repr, req_spec, required, requirement, requirement_string, resource_name, script_name, self, set, setattr, sorted, src, staticmethod, str, stream, strs, subitem, super, t, tempname, text, this, tmpnam, tuple, type, v, val, varname, vartype, zfile, zip_stat
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\android.py: Exception, property, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\api.py: appauthor, appname, base, bool, ensure_exists, list, multipath, opinion, property, roaming, self, str, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\macos.py: property, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\unix.py: RuntimeError, env_var, fallback_tilde_path, key, list, p, property, self, str, stream
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\version.py: int, object, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\windows.py: ImportError, NotImplementedError, ValueError, any, c, csidl_name, directory, getattr, hasattr, opinion_value, ord, property, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\__init__.py: appauthor, appname, bool, ensure_exists, multipath, opinion, roaming, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\platformdirs\__main__.py: getattr, print, prop
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\console.py: color_key, dark, light, text, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\filter.py: NotImplementedError, TypeError, f, filter_, filters, hasattr, lexer, options, self, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\formatter.py: cls, isinstance, options, self, str, style, tokensource
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\lexer.py: Exception, ImportError, IndexError, NotImplementedError, StopIteration, ValueError, abs, action, arg, args, bases, bom, c, callable, chardet, cls, context, d, e, encoding, endpos, enumerate, err, hasattr, i, index, int, isinstance, istate, it_token, it_value, item, iter, kwargs, kwds, len, lexer, list, match, mcs, n, next, options, prefix, print, r, repr, rexmatch, self, sorted, stack, state, staticmethod, str, suffix, sum, t, tdef, tuple, type, unfiltered, unprocessed, v, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\modeline.py: buf, i, l, len, line, max_lines, range
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\plugin.py: entrypoint, group_name, hasattr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\regexopt.py: group, len, letters, list, m, open_paren, s, sorted
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\scanner.py: RuntimeError, flags, len, pattern, property, self, text
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\sphinxext.py: Exception, app, bytes, c, classname, col, column, columns, data, fn, getattr, isinstance, len, length, lexers, line, max, name, print, row, self, set, sorted, url, x, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\style.py: bases, bool, cls, dct, len, list, mcs, set, styledef, text, token, ttype, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\token.py: getattr, isinstance, item, len, other, s, self, set, setattr, ttype, tuple, type, val
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\unistring.py: a, arg, args, b, char_list, chr, code, fp, globals, len, open, ord, range, sorted
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\util.py: Exception, IndexError, KeyError, LookupError, NotImplementedError, TypeError, UnicodeDecodeError, ValueError, allowed, already_seen, bool, c, default, f, float, getattr, hash, i, indent_level, int, isinstance, it, line, list, map, max, min, normcase, obj, options, optname, raw, repr, self, seq, set, staticmethod, str, term, tuple, var_name, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\__init__.py: TypeError, code, formatter, getattr, isinstance, issubclass, lexer, outfile, tokens, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\__main__.py: KeyboardInterrupt
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py: Exception, TypeError, default, end, filtername, getattr, i, isinstance, issubclass, len, match, name, options, range, self, set, setattr, specialttype, start, str, stream, tag, ttype, wschar, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\lexers\python.py: index, k, options, self, super, text, token, ttype, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py: AttributeError, ImportError, found_name, getattr, k, name, style, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py: Exception, ValueError, backend_name, bool, build_backend, cmd, config_settings, cwd, f, hook_name, kwargs, message, obj, open, p, path, requested, script, sdist_directory, self, source_dir, source_tree, str, super, td, traceback, wheel_directory
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py: AttributeError, Exception, ImportError, backend_module, config_settings, e, f, fullname, getattr, globals, hasattr, kwargs, len, message, metadata_directory, mod_path, obj_path, open, path, path_part, print, sdist_directory, self, super, wheel_directory, whl_zip, zipf
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py: AttributeError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\adapters.py: DeprecationWarning, ImportError, NotImplementedError, OSError, ValueError, attr, block, bytes, cert, client_cert, connect, connections, e, err, getattr, isinstance, len, max_retries, maxsize, password, pool_block, pool_connections, pool_maxsize, poolmanager, proxies, proxy_kwargs, read, req, request, self, setattr, state, str, stream, super, tuple, username, value, verify
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\api.py: data, json, kwargs, method, params, session, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\auth.py: AttributeError, DeprecationWarning, NotImplementedError, all, d, getattr, hasattr, isinstance, kwargs, method, other, r, self, type, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\certs.py: print
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\compat.py: AttributeError, TypeError, float, int
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\cookies.py: AttributeError, ImportError, KeyError, NotImplementedError, RuntimeError, TypeError, ValueError, args, bool, cookie, cookie_dict, cookie_in_jar, cookies, default, dict, domain, hasattr, headers, int, isinstance, iter, jar, kwargs, list, morsel, name, other, overwrite, path, property, request, response, self, super, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\exceptions.py: DeprecationWarning, IOError, TypeError, ValueError, Warning, args, hasattr, kwargs, self, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\help.py: ImportError, OSError, getattr, print
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\hooks.py: callable, event, hook, key, kwargs
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\models.py: AttributeError, LookupError, NotImplementedError, OSError, RuntimeError, TypeError, UnicodeDecodeError, UnicodeError, ValueError, all, any, attr, bool, bytearray, bytes, chunk_size, decode_unicode, delimiter, e, event, field, fragment, getattr, h, hasattr, hook, int, isinstance, k, kwargs, len, link, list, method, name, object, port, property, scheme, self, setattr, state, staticmethod, str, tuple, type, value, ve
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\packages.py: len, list, locals, package
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\sessions.py: KeyError, RuntimeError, StopIteration, ValueError, adapter_kwargs, attr, data, dict_class, files, getattr, header, isinstance, json, k, key, kwargs, len, new_url, next, old_url, params, password, prefix, request_hooks, request_setting, response, self, session_hooks, session_setting, setattr, timeout, username, v, value, yield_requests
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\status_codes.py: code, n, setattr, sorted, title, titles
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\structures.py: NotImplemented, casedkey, default, dict, isinstance, key, keyval, kwargs, len, lowerkey, name, self, str, super, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\utils.py: AttributeError, BaseException, DeprecationWarning, ImportError, OSError, TypeError, UnicodeError, ValueError, archive, bool, chr, chunk, cj, content, cookie, data, env_name, f, file_handler, filename, filter, fragment, frozenset, getattr, hasattr, header, header_part, header_validator_index, headers, i, int, ip, is_filename, isinstance, iterator, len, list, max, net, netaddr, new_scheme, obj, params, prefix, prepared_request, proxy_ip, proxy_key, query, r, raise_errors, range, request, string, string_ip, string_network, tmp_descriptor, tmp_handler, tmp_name, trust_env, type, uri, val
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\_internal_utils.py: UnicodeEncodeError, bytes, encoding, isinstance, str, string, u_string
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\requests\__init__.py: AssertionError, ImportError, ValueError, getattr, int, len, list, major, map, minor, patch
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\providers.py: NotImplementedError, bool, identifiers
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\reporters.py: int
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\structs.py: KeyError, StopIteration, ValueError, accessor, appends, bool, callable, children, current, dict, f, factory, int, isinstance, iter, k, key, len, list, mapping, next, object, self, sequence, set, str, sum, t, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\resolvers\abstract.py: Exception, NotImplementedError, provider, reporter, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\resolvers\criterion.py: candidates, i, incompatibilities, information, parent, req, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\resolvers\exceptions.py: Exception, candidate, causes, int, r, repr, round_count, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\resolvelib\resolvers\resolution.py: AttributeError, IndexError, KeyError, RuntimeError, all, all_keys, bool, c, candidate, candidates, connected, criteron, d, dict, e, float, graph, i, id, incompatible_reqs, int, k, key, len, list, max_rounds, min, p, parent, parents, property, provider, r, range, reporter, requirement, requirements, round_index, s, self, set, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\abc.py: bool, classmethod, hasattr, isinstance, other, print, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\align.py: ValueError, bool, classmethod, cls, count, int, len, line, list, min, options, range, renderable, self, str, vertical
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\ansi.py: StopIteration, ansi_text, bytes, code, end, fd, int, iter, len, link, match, min, next, osc, plain_text, print, self, semicolon, sgr, start, str, terminal_text
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\bar.py: begin, bgcolor, end, float, int, len, max, min, options, self, size, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\box.py: ASCII, ASCII2, ASCII_DOUBLE_HEAD, HEAVY, HEAVY_EDGE, HEAVY_HEAD, MINIMAL, MINIMAL_DOUBLE_HEAD, MINIMAL_HEAVY_HEAD, ROUNDED, SIMPLE, SIMPLE_HEAVY, SQUARE, SQUARE_DOUBLE_HEAD, ValueError, ascii, bool, box_name, edge, getattr, int, iter, last, level, line1, line2, line3, line4, line5, line6, line7, line8, list, options, parts, safe, self, sorted, str, width, widths
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\cells.py: bool, character, chr, frozenset, int, len, line, lines, list, map, n, ord, print, range, str, sum, text, total, tuple, width
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\color.py: Exception, all, b1, b2, back, blue, bool, classmethod, cls, color1, color2, color_24, color_8, color_rgb, component, cross_fade, float, fore, foreground, g1, g2, green, hex_color, int, k, l, len, name, property, r1, r2, red, round, s, self, sorted, str, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\color_triplet.py: blue, float, green, int, property, red, self, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\columns.py: bool, col_no, column_first, column_lengths, dict, enumerate, equal, expand, i, index, int, isinstance, left, len, list, max, options, range, renderable, renderable_width, right, s, self, sorted, start, str, sum, title, tuple, width, widths, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\console.py: AttributeError, BaseException, BrokenPipeError, Exception, NameError, OSError, SystemExit, TypeError, UnicodeEncodeError, ValueError, allow_nan, args, attribs, batch, bool, characters, check_circular, classes, code_format, colors, count, currentframe, data, default, dict, emoji_variant, enable, end, ensure_ascii, enumerate, error, exc_type, file_descriptor, filename, fit, float, font_aspect_ratio, force_jupyter, force_terminal, format, fragments, get_datetime, get_ipython, get_time, getattr, hasattr, hide_cursor, highlight, home, hook, indent, inherit, inline_styles, int, isatty, isinstance, iter, json, justify, k, key, kwargs, len, line_no, links, list, locals, log_locals, log_path, log_time, log_time_format, max, max_frames, max_width, method, min, min_width, name, new_file, new_line_start, new_lines, new_segments, new_size, no_color, object, offset, open, output, pad, password, prompt, property, quiet, range, raw_output, record, refresh_per_second, render_output, repr, rule_no, safe_box, self, sep, show, show_locals, skip_keys, sort_keys, speed, spinner, spinner_style, staticmethod, stderr, str, stream, style_cache, style_rule, stylesheet_rules, suppress, svg_main_code, system, tab_size, text_backgrounds, text_group, title, tuple, type, v, value, word_wrap, write_file
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\constrain.py: int, min, renderable, self, width
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\containers.py: dimension, enumerate, int, iter, len, line, line_index, lines, list, max, next_word, options, overflow, range, renderable, renderables, self, slice, str, sum, tokens, value, width, word
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\control.py: CONTROL_CODES_FORMAT, CONTROL_ESCAPE, STRIP_CONTROL_CODES, abs, bool, classmethod, cls, code, codes, control_codes, dict, enable, i, int, isinstance, list, param, parameters, range, self, show, str, text, x, y
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\default_styles.py: DEFAULT_STYLES, bool, dict, html, print, str, style_name
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\diagnose.py: name
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\emoji.py: Exception, KeyError, classmethod, len, name, self, sorted, str, text, variant
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\errors.py: Exception
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\filesize.py: base, enumerate, i, int, list, precision, separator, size, str, suffix, suffixes, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\file_proxy.py: TypeError, file, getattr, int, isinstance, len, line, lines, list, name, new_line, property, self, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\highlighter.py: TypeError, end, isinstance, len, list, match, re_highlight, regexes, self, start, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\json.py: Exception, allow_nan, bool, check_circular, classmethod, cls, default, ensure_ascii, error, highlight, indent, int, json_instance, self, skip_keys, sort_keys, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\jupyter.py: ModuleNotFoundError, args, control, dict, exclude, fragments, include, k, kwargs, list, self, str, style, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\layout.py: Exception, KeyError, bool, child, child_and_region, child_height, child_width, dict, int, isinstance, layout_height, layout_lines, layout_name, layout_row, layouts, line, list, minimum_size, options, property, range, ratio, row, self, size, sorted, splitter, stack, str, text, tuple, visible, x, y, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\live.py: BaseException, Exception, ImportError, auto_refresh, bool, dest, dict, exchange, exchange_rate, exchange_rate_dict, float, index, isinstance, len, list, live_table, next, property, range, redirect_stderr, redirect_stdout, refresh_per_second, self, source, str, super, transient, tuple, type, vertical_overflow
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\live_render.py: height, int, last, line, list, options, self, tuple, vertical_overflow
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\logging.py: Exception, bool, dict, enable_link_path, exc_traceback, exc_type, exc_value, getattr, hasattr, int, isinstance, keywords, list, locals_max_length, locals_max_string, log_time_format, markup, omit_repeated_times, record, rich_tracebacks, self, show_level, show_path, show_time, str, super, tracebacks_code_width, tracebacks_extra_lines, tracebacks_max_frames, tracebacks_show_locals, tracebacks_suppress, tracebacks_theme, tracebacks_width, tracebacks_word_wrap, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\markup.py: Exception, IndexError, KeyError, SyntaxError, backslashes, bool, divmod, emoji_variant, end, enumerate, equals, error, escaped, escapes, full_text, index, int, isinstance, len, list, literal_ast, match, match_parameters, open_tag, property, reversed, self, sorted, spans, start, str, style_stack, tag, tag_text, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\measure.py: classmethod, get_console_width, getattr, int, isinstance, max, max_width, maximum, min, min_width, options, property, renderables, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\padding.py: ValueError, bool, bottom, classmethod, expand, int, isinstance, len, level, line, list, measure_max, measure_min, min, options, pad, pad_right, pad_top, renderable, self, staticmethod, str, top, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\pager.py: content, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\palette.py: b1, b2, blue1, blue2, colors, enumerate, float, g1, g2, green1, green2, index, int, len, min, number, options, r1, r2, range, red1, red2, repr, self, str, tuple, x, y
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\panel.py: any, bool, character, classmethod, cls, expand, height, highlight, int, isinstance, line, max, min, options, property, right, safe_box, self, str, subtitle, subtitle_align, title, title_align
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\pretty.py: Exception, ImportError, NameError, OSError, TypeError, arg, attr, bool, bytes, callable, capture, child, class_or_tuple, close_brace, container_type, crop, default, depth, dict, empty, enumerate, error, expand_all, field, float, frozenset, get_ipython, getattr, hasattr, id, indent_guides, indent_size, index, insert_line, int, isinstance, iter, justify, key, last, len, list, margin, max, max_depth, max_length, max_string, max_width, name, no_wrap, obj, object, open_brace, options, overflow, property, repr, repr_callable, rich_args, root, self, set, str, token, tuple, type, visited_ids
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\progress.py: BaseException, KeyError, RuntimeWarning, ValueError, all, auto_refresh, b, bar_width, binary_units, bool, bytearray, bytes, classmethod, close_handle, column, columns, compact, complete_style, description, dict, disable, divmod, elapsed_when_finished, encoding, errors, exc_tb, exc_type, exc_val, expand, fields, file, finished_style, finished_text, float, hint, hours, int, isinstance, iter, justify, len, list, map, markup, max, memoryview, min, minutes, newline, next, offset, property, pulse_style, redirect_stderr, redirect_stdout, refresh_per_second, sample, seconds, self, separator, sequence, show_speed, size, sorted, speed_estimate_period, spinner_name, spinner_style, str, suffix, sum, super, table_column, text_format_no_percentage, timestamp, track_thread, transient, tuple, type, unit, value, visible, whence
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\progress_bar.py: animation_time, bool, color_system, finished_style, float, index, int, len, list, max, min, n, no_color, options, property, pulse, pulse_style, range, self, str, total
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\prompt.py: Exception, ValueError, bool, case_sensitive, choice, classmethod, cls, default, error, float, int, isinstance, len, list, message, no, self, show_choices, show_default, str, stream, type, yes
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\protocol.py: bool, check_object, hasattr, isinstance, object, repr, rich_visited_set, set, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\region.py: int
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\repr.py: Exception, angular, arg, bool, cls, default, error, getattr, hasattr, isinstance, key, len, list, name, param, repr, repr_str, self, str, tuple, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\rule.py: IndexError, ValueError, end, int, isinstance, max, options, self, str, title
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\scope.py: bool, float, indent_guides, int, item, key, locals, max_length, max_string, scope, sort_keys, sorted, str, title, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\screen.py: application_mode, bool, height, last, line, options, renderables, self, width
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\segment.py: StopIteration, bool, cache, classmethod, cls, control, cuts, dict, filter, height, include_new_lines, int, iter, len, length, list, max, new_lines, next, pad, post_style, property, segment, segment_style, segments, self, split_segments, str, sum, tuple, type, width
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\spinner.py: KeyError, float, int, isinstance, len, list, name, options, repr, self, sorted, speed, spinner_name, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\status.py: BaseException, float, property, refresh_per_second, self, speed, spinner_style, status, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\style.py: NotImplemented, ValueError, bit, bit_no, bool, bytes, classmethod, cls, color_system, css, default_style, dict, error, handlers, hash, int, isinstance, iter, key, legacy_windows, list, new_style, next, obj, original_word, other, property, range, self, sgr, str, style_definition, styles, sum, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\styled.py: options, renderable, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\syntax.py: ANSI_DARK, ANSI_LIGHT, KeyError, NotImplementedError, StopIteration, any, blend, bool, classmethod, cls, dedent, dict, encoding, end_line, enumerate, ext, first, float, highlight_lines, indent_guides, int, isinstance, iter, justify, left, len, line, line_end, line_number, line_numbers, line_range, line_start, line_token, list, match, max, min, name, next, obj, options, pad_left, pad_right, path, position, property, right, self, set, start_line, str, style_before, style_map, stylized_range, syntax_line, tab_size, token_type, tuple, type, word_wrap, wrapped_line
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\table.py: allow_wrap, any, bool, caption, caption_justify, caption_style, cell, classmethod, cls, col, column_index, dict, enumerate, first, first_row, footer, getattr, headers, index, int, isinstance, iter, justify, last, last_cell, last_row, len, line_no, list, max, max_widths, min, min_width, min_widths, next, no_wrap, options, overflow, pad, pad_right, property, range, ratio, raw_cells, renderable, renderables, rendered_cell, row_cell, row_cells, row_styles, safe_box, self, str, sum, title, title_justify, title_style, tuple, type, wrapable, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\terminal_theme.py: background, bright, foreground, int, list, normal, self, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\text.py: DEFAULT_JUSTIFY, DEFAULT_OVERFLOW, NotImplemented, TypeError, ValueError, allow_blank, amount, bool, callable, case_sensitive, character, classmethod, closing, cls, dict, divmod, emoji_variant, enumerate, full_indents, handlers, include_separator, indent_size, index, int, isinstance, key, last, leaving, len, line, line_end, line_no, line_start, list, max, max_width, min, name, new_length, next_offset, object, options, other, output, part, property, range, remaining_space, self, separator, size, slice, sorted, span, span_end, span_start, span_style, stack, step, stop, str, style_cache, style_id, style_prefix, suffix, tokens, tuple, value, width, word, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\theme.py: Exception, bool, classmethod, cls, config_file, dict, encoding, inherit, isinstance, len, list, name, open, path, print, property, self, sorted, source, str, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\traceback.py: BaseException, BaseExceptionGroup, Exception, ExceptionGroup, IndexError, SyntaxError, ValueError, a, any, args, bool, classmethod, cls, code_width, dict, end, end_column, end_line, enumerate, exception, extra_lines, frame_index, frame_summary, get_ipython, getattr, group_exception, group_last, group_no, group_stack, grouped_exceptions, indent_guides, int, is_syntax, isinstance, iter_locals, key, kwargs, last, len, line1, line2, line_no, list, locals_hide_dunder, locals_max_length, locals_max_string, max, max_frames, min, next, note, notes, object, print, range, reversed, self, set, show_locals, stacks, start, start_column, start_line, str, suppress, suppress_entity, syntax_error, tuple, type, type_, value, width, word_wrap
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\tree.py: CONTINUE, END, FORK, SPACE, StopIteration, bool, expanded, first, hide_root, highlight, index, int, iter, label, last, len, levels, list, max, max_measure, min_measure, next, options, range, self, stack, str, sum, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py: KeyError, default_variant, emoji_code, emoji_name, match, str, text, variant
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_fileno.py: Exception, file_like, fileno, getattr, int, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_inspect.py: Exception, OSError, TypeError, ValueError, all, attr_name, bool, callable, dir, error, fully_qualified_types_names, getattr, hasattr, help, item, key, len, name, object, object_, paragraph, repr, self, sort, str, title, tuple, type, type_, type_name, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_log_render.py: bool, callable, int, len, level, level_width, line_no, link_path, list, omit_repeated_times, path, renderables, row, self, show_level, show_path, show_time, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_loop.py: StopIteration, bool, iter, next, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_null_file.py: BaseException, bool, int, iter, list, self, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_pick.py: bool, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_ratio.py: distributed_total, divmod, edge, edges, enumerate, index, int, len, list, max, maximum, maximums, min, minimum, minimums, print, ratio, result, round, size, sum, total, value, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_stack.py: item, list, property, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_timer.py: print, str, subject
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_win32_console.py: Exception, ImportError, attributes, bool, char, classmethod, column, coord, coords, file, int, len, length, new_position, print, property, row, self, std_handle, str, text, title, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_windows.py: AttributeError, ImportError, ValueError, bool, repr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py: buffer, column, control, control_code, control_codes, int, mode, str, style, term, text, title, tuple, x, y
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\_wrap.py: bool, break_positions, end, fold, int, last, len, line, list, print, start, str, text, tuple, width
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\__init__.py: FileNotFoundError, all, allow_nan, args, bool, check_circular, data, default, docs, dunder, end, ensure_ascii, file, help, highlight, indent, int, json, kwargs, methods, obj, objects, private, sep, skip_keys, sort, sort_keys, str, title, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\rich\__main__.py: b1, b2, g1, g2, options, r1, r2, range, renderable1, renderable2, round, x, y
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\tomli\_parser.py: ASCII_CTRL, AttributeError, BARE_KEY_CHARS, BASIC_STR_ESCAPE_REPLACEMENTS, DeprecationWarning, HEXDIGIT_CHARS, ILLEGAL_BASIC_STR_CHARS, ILLEGAL_COMMENT_CHARS, ILLEGAL_LITERAL_STR_CHARS, ILLEGAL_MULTILINE_BASIC_STR_CHARS, ILLEGAL_MULTILINE_LITERAL_STR_CHARS, IndexError, KEY_INITIAL_CHARS, KeyError, MAX_INLINE_NESTING, RecursionError, TOML_WS, TOML_WS_AND_NEWLINE, TypeError, ValueError, access_lists, array, bool, bytes, chars, chr, codepoint, cont_key, dict, doc, e, error_on_eof, expect, flag, float, float_str, frozenset, header, hex_len, i, int, isinstance, k, key, key_parent, key_part, len, list, literal, msg, multiline, nest_lvl, parsed_escape, range, recursive, self, str, tuple, type, val, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\tomli\_re.py: day, day_str, hour, hour_str, int, match, micros_str, minute, minute_str, month, month_str, offset_hour_str, offset_minute_str, offset_sign_str, parse_float, sec, sec_str, sign_str, str, year, year_str, zulu_time
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\tomli\_types.py: int, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\tomli_w\_writer.py: IndexError, TypeError, ValueError, all, allow_multiline, bool, bytes, chr, chunk, dict, float, fp, frozenset, hex, i, id, in_aot, indent, inside_aot, int, isinstance, item, k, len, list, multiline_strings, name, nest_level, obj, object, ord, part, range, self, str, t, table, tables, tuple, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\truststore\_api.py: AttributeError, Exception, ImportError, NotImplementedError, alpn_protocols, bool, bytes, cadata, cafile, capath, cert, certfile, dict, do_handshake_on_connect, getattr, hasattr, incoming, int, isinstance, keyfile, list, npn_protocols, outgoing, password, property, purpose, self, server_hostname, server_side, session, sock, sock_or_sslobj, str, super, suppress_ragged_eofs, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\truststore\_macos.py: AttributeError, ImportError, MemoryError, NotImplementedError, OSError, TypeError, ValueError, args, bytes, cert_chain, cert_data, cf_string_ref, ctx, ctx_ca_certs_der, e, int, len, list, macos10_16_path, map, name, sec_trust_ref, server_hostname, ssl_context, str, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\truststore\_openssl.py: bool, bytes, cafile, capath, ctx, list, name, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\truststore\_ssl_constants.py: object, ssl_context, super, type, verify_mode
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\truststore\_windows.py: args, bool, bytes, cert_bytes, cert_chain, ctx, custom_ca_certs, e, int, len, list, pPeerCertContext, result, server_hostname, ssl_context, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\truststore\__init__.py: AttributeError, ImportError, hasattr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\connection.py: AttributeError, BaseException, DeprecationWarning, Exception, ImportError, NameError, OSError, TimeoutError, ValueError, any, args, assert_hostname, bytearray, bytes, cert_file, e, getattr, hasattr, header, hex, isinstance, k, key_file, key_password, kw, kwargs, len, map, method, port, property, self, set, sorted, str, strict, super, timeout, url, v, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py: AttributeError, BaseException, OSError, TypeError, assert_fingerprint, assert_hostname, assert_same_host, block, bool, ca_cert_dir, ca_certs, cert_file, cert_reqs, chunked, conn_kw, getattr, hasattr, hpe, httplib_request_kw, isinstance, key_file, key_password, kw, maxsize, object, old_pool, path, pool_timeout, redirect, response_kw, self, ssl_error, ssl_version, str, strict, super, timeout_value, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\exceptions.py: AssertionError, Exception, ValueError, Warning, args, defects, error, expected, length, location, partial, pool, reason, response, retries, self, super, unparsed_data, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\fields.py: UnicodeDecodeError, UnicodeEncodeError, any, cc, ch, classmethod, cls, content_disposition, content_location, default, dict, fieldname, header_formatter, header_name, header_parts, header_value, headers, isinstance, len, match, name, needle, needles_and_replacements, range, self, sort_key, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\filepost.py: dict, field, int, isinstance, iter, k, str, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py: KeyError, connection_pool_kw, field, frozenset, header, isinstance, key, key_class, kw, list, num_pools, override, parsed_url, pool_kwargs, proxy_headers, proxy_ssl_context, redirect, self, super, tuple, url, url_scheme, use_forwarding_for_https, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\request.py: NotImplementedError, TypeError, body, content_type, encode_multipart, fields, multipart_boundary, self, url, urlopen_kw
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\response.py: DeprecationWarning, IOError, OSError, ResponseCls, TimeoutError, ValueError, amt, auto_close, b, body, bytearray, bytes, classmethod, d, default, e, enc, enforce_content_length, getattr, hasattr, int, isinstance, len, m, min, mode, modes, msg, name, original_response, pool, preload_content, property, r, reason, request_method, request_url, response_kw, retries, reversed, self, set, str, val, version, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\_collections.py: ImportError, KeyError, NotImplementedError, TypeError, args, classmethod, cls, default, dict, dispose_func, hasattr, header, isinstance, k, key, kwargs, len, line, list, maxsize, message, object, self, super, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\__init__.py: DeprecationWarning, ImportError, category, level
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\appengine.py: ImportError, body, bool, e, headers, isinstance, redirect, response_kw, self, str, timeout, url, urlfetch_resp, urlfetch_retries, validate_certificate
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\ntlmpool.py: DeprecationWarning, Exception, NegotiateFlags, ServerChallenge, args, assert_same_host, authurl, body, dict, kwargs, method, pw, redirect, retries, s, self, super, url, user
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py: DeprecationWarning, Exception, ImportError, OSError, TimeoutError, UnicodeError, args, binary_form, bufsize, cadata, certfile, connection, dict, e, err_no, getattr, hasattr, isinstance, k, keyfile, kwargs, len, map, mode, p, peer_cert, prefix, property, protocol, self, sock, str, suppress_ragged_eofs, timeout, v, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\securetransport.py: Exception, ImportError, NotImplementedError, OSError, TimeoutError, ValueError, alpn_protocols, args, binary_form, bufsiz, bufsize, bytes, cadata, cafile, capath, certfile, client_cert, client_key, connection_id, data_length_pointer, do_handshake_on_connect, e, exception, f, hasattr, id, isinstance, keyfile, kwargs, len, max_version, min_version, mode, open, p, password, property, protocols, self, server_side, sock, suppress_ragged_eofs, value, verify
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py: ImportError, OSError, TimeoutError, ValueError, args, connection_pool_kw, e, headers, isinstance, kwargs, len, num_pools, password, proxy_url, self, super, username
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\bindings.py: AttributeError, ImportError, OSError, int, macos10_16_path, map, name, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\low_level.py: BaseException, Exception, MemoryError, OSError, bytestring, der_bytes, e, error, f, file_path, index, len, lst, match, new_certs, new_identities, obj, open, path, py_bstr, range, t, tuples, value, ver_maj, ver_min, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\packages\six.py: AttributeError, ImportError, KeyError, NameError, OverflowError, TypeError, ValueError, any, arg, args, assigned, attr, bases, basestring, bs, buf, bytes, chr, classmethod, cls, d, delattr, doc, encoding, enumerate, file, fullname, fullnames, func, getattr, globals, hasattr, i, importer, int, isinstance, it, iter, klass, kw, kwargs, len, long, meta, move, name, obj, object, old, old_mod, ord, s, self, setattr, six_module_name, slots_var, spec, str, super, tp, type, unbound, unicode, updated, wrapped
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\packages\backports\makefile.py: ValueError, encoding, errors, mode, newline, self, set
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\packages\backports\weakref_finalize.py: Exception, args, bool, classmethod, cls, func, i, id, item, kwargs, next, property, self, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\connection.py: Exception, OSError, UnicodeError, address, af, conn, e, getattr, opt, options, port, proto, res, sa, socket_options, socktype, source_address, timeout
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py: ca_cert_data, ca_cert_dir, ca_certs, cert_reqs, destination_scheme, hasattr, proxy_config, proxy_url, ssl_version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\queue.py: item, len, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\request.py: OSError, ValueError, basic_auth, body, body_pos, disable_cache, frozenset, getattr, isinstance, keep_alive, list, object, proxy_basic_auth, str, type, user_agent
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\response.py: AttributeError, TypeError, ValueError, bytes, defect, getattr, headers, int, isinstance, obj, response, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\retry.py: AttributeError, DeprecationWarning, ValueError, backoff_factor, bool, classmethod, cls, default, dict, error, filter, frozenset, getattr, h, has_retry_after, int, isinstance, item, kw, len, list, method, method_whitelist, min, object, property, raise_on_status, respect_retry_after_header, response, reversed, self, set, status_code, status_forcelist, super, tuple, type, url, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py: ValueError, args, binary_form, byte_view, data, e, encoding, errors, flags, func, hasattr, len, memoryview, mode, newline, self, server_hostname, set, ssl_context, staticmethod, suppress_ragged_eofs, value, view
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py: ImportError, NotImplementedError, OSError, a, abs, algorithm, b, bool, bytearray, bytes, ca_cert_data, ca_cert_dir, ca_certs, cadata, cafile, candidate, capath, cert, certfile, cipher_suite, ciphers, e, f, getattr, hasattr, isinstance, key_file, key_password, keyfile, left, len, length, line, open, protocol_version, right, self, server_hostname, server_side, sock, socket, ssl_context, str, tls_in_tls, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py: AttributeError, ImportError, UnicodeError, ValueError, cert, dn, frag, hostname, ipname, isinstance, key, len, map, max_wildcards, repr, str, sub, unicode, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py: TypeError, ValueError, bool, classmethod, cls, connect, float, getattr, isinstance, max, min, name, object, property, read, self, timeout, total, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\url.py: AttributeError, ImportError, ValueError, allowed_chars, any, authority, bytearray, cls, d, delims, encoding, end, hex, host_port, i, int, isinstance, label, len, name, ord, percent_encodings, property, range, s, segment, self, set, start, str, super, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pip\_vendor\urllib3\util\wait.py: AttributeError, Exception, ImportError, OSError, RuntimeError, args, bool, e, float, hasattr, kwargs, read, rready, sock, t, wready, write, xready
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\__init__.py: AssertionError, AttributeError, DeprecationWarning, Exception, ImportError, KeyError, NameError, NotADirectoryError, NotImplementedError, OSError, PermissionError, RuntimeError, RuntimeWarning, SyntaxError, TypeError, UnicodeDecodeError, UserWarning, ValueError, Warning, any, archive_name, attr, base, basename, by_key, callback, callbacks, child, classes, classmethod, compile, dep, dict, dir, dist_spec, distribution_finder, e, e_k_b_n_c, enumerate, exc, existing, ext, extra, extras_spec, f, fallback, fid, file_path, filter, float, frozenset, full_env, getattr, globals, hasattr, hash, importer_type, insert, installer, int, isinstance, iter, k, kw, kwargs, len, list, loader_type, locals, location, map, modname, moduleOrReq, module_name, namespace, namespace_handler, new_requirement, next, normalized_to_canonical_keys, ob, object, only, open, orig_path, other, outf, package, packageName, package_name, package_or_requirement, part, pkg, plugin_env, precedence, project, property, provided, provider_factory, py_version, python, r, ref, registry, replace, replace_conflicting, repr, req_spec, required, requirement, requirement_string, resource_name, script_name, self, set, setattr, sorted, src, staticmethod, str, stream, strs, subitem, super, t, tempname, text, tmpnam, tuple, type, v, val, vars, vartype, zfile, zip_stat
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\extern\__init__.py: ImportError, any, fullname, locals, map, prefix, property, root, root_name, self, set, spec, target, vendor_pkg, vendored_names
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\appdirs.py: ImportError, UnicodeError, c, csidl_name, getattr, map, multipath, opinion, ord, print, prop, property, roaming, self, str, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\zipp.py: AttributeError, FileNotFoundError, IsADirectoryError, ValueError, args, at, classmethod, dict, filter, isinstance, kwargs, list, map, minuend, mode, other, p, property, pwd, root, self, set, source, staticmethod, str, strm, subtrahend, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\abc.py: FileNotFoundError, bool, child, encoding, item, path, resource, self, str, strm
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\readers.py: FileNotFoundError, KeyError, NotADirectoryError, ValueError, all, child, exc, file, iter, list, loader, map, module, namespace_path, path, property, resource, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\simple.py: IsADirectoryError, RuntimeError, args, kwargs, map, mode, next, parent, property, reader, self, traversable
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_adapters.py: AttributeError, FileNotFoundError, ValueError, adapter, args, attr, file, getattr, hasattr, iter, kwargs, len, mode, other, package, path, path_parts, property, self, spec
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_common.py: FileNotFoundError, TypeError, cand, fd, getattr, isinstance, package, path, raw_path, str, suffix
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_compat.py: AttributeError, ImportError, TypeError, ValueError, cls, hasattr, package, property, self, spec
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_itertools.py: element, iterable, key, seen, set
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_legacy.py: DeprecationWarning, ValueError, any, args, bool, bytes, encoding, errors, file_name, fp, func, kwargs, name, package, parent, str, traversable
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\jaraco\context.py: Exception, args, bool, branch, dest_ctx, dict, dir, exceptions, func, issubclass, kwargs, open, property, quiet, remover, repo_dir, self, trap, url, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\jaraco\functools.py: TypeError, action, args, ast, bound_method, cache_wrapper, cleanup, exceptions, f, f1, f2, f_args, f_kwargs, float, func1, func2, funcs, getattr, hasattr, isinstance, k, kwargs, map, max_rate, method, method_name, more_itertools, namespace, obj, object, param, print, r_args, r_kwargs, range, replace, retries, self, setattr, target, transform, trap, use, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py: ImportError, StopIteration, UnicodeDecodeError, args, bytes, classmethod, cls, filter, hash, identifier, isinstance, iter, iterable, len, line, map, match, maxsplit, min, new, next, old, other, para, part, prefix_lines, rest, reversed, s, s1, s2, self, slice, splitter, staticmethod, str, string, sub, subject, suffix, super, text, tuple, value, word
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\more_itertools\more.py: A, BaseException, DeprecationWarning, IndexError, M, N, RuntimeError, StopIteration, TypeError, ValueError, after, any, args, base_type, before, bool, bytes, callback_kwd, child, chunk, chunk_size, combo, context_manager, cur_idx, d, default, delta, delta_primary, deltas_secondary, details, divmod, e, elem, enumerate, exception, exceptions, f, fillvalue, filter, func, func_else, function, g, getattr, group_tuple, hasattr, hash, i1, i2, initial, int, isinstance, iter, iter_primary, iterable_or_value, iterable_positions, iters_secondary, keep_separator, keyfunc, kwargs, len, levels, limit_seconds, list, longest, map, max, maxlen, maxsplit, min, next, next_item, next_multiple, node, obj, object, objects, offsets, ordering, other, others, p, pred, predicate, property, range, reducefunc, repr, result_index, reverse, reversed, s, scalar_positions, scalar_types, scalars, self, set, sizes, slice, smallest_weight_key, sorted, staticmethod, str, strict, sum, super, tail, target, tmp, tuple, type, val, validator, value_list, w, wait_seconds, weight, window_size, wrapping_args, wrapping_func, wrapping_kwargs, x, x_key, y, y_key, zip, zipped_items
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\more_itertools\recipes.py: DeprecationWarning, ImportError, IndexError, StopIteration, TypeError, ValueError, a, b, bool, cond, default, elem, element, exception, fillvalue, filter, first, func, function, i, index, int, isinstance, iter, iterable, iterables, iterator, key, len, list, listOfLists, map, min, next, predicate, range, set, signal, sorted, start, sum, t1, t2, times, tuple, value, vec1, vec2, x, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\markers.py: NotImplementedError, ValueError, all, any, bool, dict, e, environment, first, groups, i, info, isinstance, item, len, lhs, list, m, marker, markers, name, op, oper, results, rhs, self, str, t, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\requirements.py: ValueError, e, list, parts, requirement_string, s, self, set, sorted, str, t
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\specifiers.py: DeprecationWarning, NotImplemented, ValueError, all, any, bool, dict, filtered, fn, frozenset, getattr, hash, int, isinstance, iter, left, left_split, len, list, max, object, op, operator_callable, padded_prospective, padded_spec, parsed, property, result, right, right_split, s, segment, self, set, sorted, spec_str, specifiers, str, super, tuple, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\tags.py: INTERPRETER_SHORT_NAMES, NotImplemented, ValueError, bool, cpu_arch, dict, explicit_abi, frozenset, hasattr, hash, id, int, interpreters, is_32bit, isinstance, len, list, major_version, map, minor, minor_version, object, other, platform_, property, range, self, set, str, string, tag, tuple, version_str, warn
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\utils.py: ValueError, frozenset, int, isinstance, len, sep, str, tuple, version_part, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\version.py: DeprecationWarning, NotImplemented, ValueError, bool, bytes, hash, i, int, isinstance, len, list, object, other, property, reversed, s, self, str, tuple, version, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\_manylinux.py: AssertionError, AttributeError, ImportError, OSError, RuntimeWarning, TypeError, ValueError, arch, bool, bytes, dict, f, file, fmt, glibc_major, glibc_max, hasattr, int, isinstance, linux, open, range, self, str, tuple, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\_musllinux.py: KeyError, OSError, arch, bytes, e_fmt, e_phentsize, e_phnum, e_phoff, executable, fmt, i, int, len, minor, n, open, output, p_filesz, p_fmt, p_idx, p_offset, p_type, print, range, stack, str, t, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\packaging\_structures.py: bool, hash, int, isinstance, object, other, repr, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\actions.py: args, attrName, attrValue, attr_dict, classname, k, l, locn, method_call, n, namespace, object, repl_str, s, self, strg, t, tokens, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\common.py: Combine, FollowedBy, LineEnd, Literal, OneOrMore, Opt, ParseException, ParseResults, ParserElement, Regex, ValueError, White, Word, float, fmt, hexnums, identbodychars, identchars, int, isinstance, l, ll, nums, printables, quoted_string, s, ss, staticmethod, str, sum, t, token_map, tokens, tt, v, vars, ve
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\core.py: AttributeError, Ellipsis, Exception, HIT, ImportError, IndexError, KeyError, MISS, NotImplementedError, ParseBaseException, ParseException, ParseFatalException, ParseSyntaxException, RecursiveGrammarException, RuntimeError, TypeError, UserWarning, ValueError, adjacent, all, any, args, as_group_list, as_keyword, as_match, asdict, aslist, body_chars, bool, break_flag, bytes, c, cache_hit, cache_size_limit, callPreParse, callable, caseless, chars, charset, chr, classmethod, cls, cmd_line_warn_options, col, colno, convert_whitespace_escapes, copy_defaults, cur_, debug, default, diag_enum, diag_file, dict, doActions, e, encoding, end_quote_char, endloc, enumerate, err, esc_char, esc_quote, exact, exception_action, exclude_chars, expr1, exprs_arg, exprtokens, fail_on, failure_tests, file_or_filename, flag, flags, fns, force, frm, full_dump, func, getattr, grouped, hasattr, hex, i, id, ident_chars, ie, include, include_separators, init_chars, instance, int, isinstance, issubclass, item, iter, join_string, k, kwargs, l, len, line, lineno, list, list_all_matches, loc1, loc_, locals, mat, matchString, max, max_limit, max_matches, max_mismatches, maxsplit, message, min, minElements, multiline, n, new_loc, new_peek, next, nextLoc, notChars, not_chars, o, offset, open, optElements, ord, output_html, overlap, p, paArgs, parseElementList, parse_action_exc, parse_all, part, pattern, pbe, pe, pfe, post_parse, prev, prev_loc, prev_peek, prev_result, print, print_results, property, quoteChar, raise_fatal, range, recursive, ref_col, repl, replace_with, repr, resultlist, reversed, s_m, savelist, self, set, setattr, show_groups, show_results_names, skipto_arg, slice, sorted, src, start_action, staticmethod, stop_on, str, str_type, success_action, sum, super, te, test_line, test_string, tmptokens, tok, tokenlist, tokn, toks, tuple, type, unquote_results, v, var, vars, vertical, w_action, w_category, w_message, w_module, warn_env_var, warn_opt, warning_type, with_line_numbers, word_chars, ws, wschar, wslit, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\exceptions.py: Exception, classmethod, cls, elem, enumerate, exc, ff, id, int, isinstance, len, loc, marker_string, msg, parseElementList, pe, property, pstr, self, set, staticmethod, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\helpers.py: And, CaselessKeyword, CaselessLiteral, CharsNotIn, Combine, Diagnostics, Dict, Empty, Enum, FollowedBy, Forward, Group, Iterable, Keyword, LineEnd, List, Literal, MatchFirst, NoMatch, OneOrMore, Opt, ParseAction, ParseException, ParserElement, Regex, SkipTo, Suppress, TokenConverter, Tuple, TypeError, Union, ValueError, Word, ZeroOrMore, a, all, allow_trailing_delim, alphanums, alphas, any, any_close_tag, any_open_tag, arity, as_keyword, as_string, b, backup_stacks, base_expr, blockStatementExpr, bool, caseless, closer, col, combine, dbl_quoted_string, empty, enumerate, ignore_expr, indent, indentStack, instring, int, int_expr, isinstance, j, k, key, l, len, list, ll, loc, max, min, nums, opExpr1, opExpr2, op_list, opener, operDef, other, pa, printables, quoted_string, re_flags, remove_quotes, rightLeftAssoc, s, self, str, str_type, strs, suppress_GT, suppress_LT, sym, t, tag_str, thisExpr, tt, tuple, use_regex, v, value, vars, warnings, xml
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\results.py: AttributeError, Exception, IndexError, KeyError, TypeError, a, any, bool, bytes, classmethod, cls, default_value, dict, dir, enumerate, full, inAccumNames, include_list, indent, ins_string, int, isinstance, item, itemseq, iter, j, k, key, kwargs, len, list, modal, next, obj, object, occurrences, other, p1, p2, position, range, repr, res, sep, set, slice, sorted, state, str, str_type, tuple, type, value, vlist, vv
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\testing.py: Exception, bool, c, dict, enumerate, exc_type, exp, expand_tabs, expected, expected_parse_results, expr, getattr, i, int, isinstance, issubclass, len, line, list, mark_control, mark_spaces, max, min, msg, name, next, print, range, rpt, run_test_results, run_test_success, run_tests_report, self, staticmethod, str, test_string, type, u, value, verbose, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\unicode.py: any, c, cc, chr, filter, fn, getattr, hasattr, int, list, obj, range, rr, self, set, sorted, str, superclass, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\util.py: KeyError, ValueError, bool, c, capacity, chars, chr, classmethod, cls, dict, dname, getattr, i, int, isinstance, iter, key, len, list, ll, loc, name, next, object, ord, prev, re_escape, self, set, setattr, size, sorted, str, strg
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py: globals, int, nv, property, self, str, type, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py: any, bool, child, classmethod, converted, d, diag, diagram, diagram_kwargs, diagrams, dict, e, element, expr, fn, force, func, id, index, int, isinstance, key, label, len, list, name_hint, number, parent, parent_index, partial, property, self, set, show_groups, show_results_names, sorted, specification, state, str, super, type, value, vertical, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\asgi.py: bool, disable_compression, header, headers, int, name, output, receive, scope, send, status, tuple, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\context_managers.py: BaseException, args, callback_name, counter, exception, f, func, gauge, getattr, isinstance, kw, kwargs, max, metric, self, tuple, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\decorator.py: AttributeError, ImportError, KeyError, NameError, RuntimeError, SyntaxError, TypeError, a, addsource, anc, arg, args, arguments, attrs, body, caller, classmethod, cls, compile, defaults, dict, dispatch_args, enumerate, funcdict, g, getattr, hasattr, i, isinstance, issubclass, j, k, kw, len, line, list, module, msg, n, next, obj, print, ra, range, rest, set, setattr, src_templ, str, t, tuple, type, type_, types_, va, vars, vas, wrong, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\exposition.py: Exception, OSError, accepted, addr, address, base_handler, bool, bytes, cafile, capath, certfile, classmethod, client_auth_required, client_cafile, client_capath, cls, code, content_type, dict, disable_compression, encoder, environ, exc, exception, f, family, float, fp, getattr, header, insecure_skip_verify, int, iter, job, k, keyfile, lines, list, metric, newurl, next, object, om_samples, open, password, path, port, protocol, req, s, samples, self, sockaddr, sorted, start_response, str, suffix, timeout, tuple, type, username, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\gc_collector.py: enumerate, gen, hasattr, self, stat, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\metrics.py: BaseException, Exception, NotImplementedError, RuntimeError, UserWarning, ValueError, amount, any, b, bool, bound, dict, documentation, enumerate, exception, exemplar, f, float, frozenset, i, l, labelkwargs, labelnames, len, list, multiprocess_mode, name, namespace, native_histogram_value, s, sample_labels, self, sorted, source_buckets, states, str, subsystem, suffix, super, timestamp, tuple, type, unit, val, value, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\metrics_core.py: ValueError, b, bool, bucket, buckets, count_value, created, dict, documentation, enabled, float, gsum_value, int, isinstance, len, list, names, native_histogram, object, other, s, self, sorted, state, str, sum_value, timestamp, tuple, unit, value, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\mmap_dict.py: RuntimeError, dict, filename, help_text, infp, k, key, labelnames, labelvalues, len, list, metric_name, name, open, read_mode, self, staticmethod, str, timestamp, ts, v, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\multiprocess.py: DeprecationWarning, IOError, NameError, ValueError, accumulate, bucket, dict, f, float, help_text, key, l, labels, m, metric_name, mode, name, name_, registry, s, self, sorted, staticmethod, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\parser.py: ValueError, bool, candidate_name, charpos, dict, fd, float, int, label_value, labels_string, len, list, match, maxsplit, n, openmetrics, startidx, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\platform_collector.py: data, documentation, java_version, k, major, minor, name, patchlevel, platform, self, staticmethod, vm_name, vm_release, vm_vendor, vminfo
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\process_collector.py: AttributeError, ImportError, OSError, TypeError, ValueError, float, int, len, limits, line, namespace, open, proc, self, stat, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\registry.py: AttributeError, ValueError, auto_describe, bool, collector, dict, float, list, metric, name, registry, s, self, set, str, suffix, target_info
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\samples.py: ValueError, bool, dict, float, int, isinstance, object, other, sec, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\utils.py: float, repr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\validation.py: UnicodeDecodeError, ValueError, bool, cls, exemplar, k, l, len, name, str, tok, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\values.py: DeprecationWarning, amount, exemplar, f, help_text, labelnames, labelvalues, metric_name, multiprocess_mode, name, process_identifier, self, timestamp, typ, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\bridge\graphite.py: OSError, address, bool, float, int, interval, k, metric, prefix, pusher, s, self, sorted, str, super, tags, timeout_seconds, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\openmetrics\exposition.py: Exception, ValueError, exception, k, metric, registry, s, sample, sorted, str, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\openmetrics\parser.py: ValueError, candidate_name, char, charpos, deltas_name, dict, end, fd, float, int, isinstance, iter, k, len, map, match, n, pair, quoted, s, set, sorted, spans_name, start, suffixes, sum, tuple, v, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\prometheus_client\twisted\_exposition.py: registry
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\archive_util.py: LookupError, d, dirs, driver, drivers, dst, e, extract_dir, filename, files, info, open, progress_filter, src, tar_obj, z, zipfile_obj
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\build_meta.py: BaseException, ValueError, a_dir, arg, classmethod, cls, config_settings, dict, directory, dirs, e, extension, f, file, flag, getattr, isinstance, key, len, list, long_and_short, metadata_directory, name, open, opt, parent, requirements, result_extension, sdist_directory, self, setup_command, setup_script, specifiers, str, suffix, super, tmp_dist_dir, wheel_directory
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\depends.py: ImportError, byte_code, compile, default, f, getattr, globals, kind, list, locals, module, name, path, paths, self, str, symbol
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\dep_util.py: ValueError, enumerate, i, len, sources_groups, targets
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\discovery.py: NotImplementedError, all, any, bool, classmethod, cls, detected, dict, dir, dirs, distribution, enumerate, field, file, force, getattr, hasattr, i, include, kind, len, list, module, n, other, p, package_name, package_path, parent_dir, pat, path, patterns, pkg, pkg_dir, property, range, reversed, root, root_pkg, self, sorted, staticmethod, str, tuple, where
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\dist.py: AssertionError, AttributeError, Exception, TypeError, ValueError, args, attr, bool, cls, cmd, command_obj, content, default, dict, e, error, ext, f, field, file, filename, filter, frozenset, getattr, hasattr, hook, ignore_option_errors, inifiles, isinstance, item, k, len, license_file, license_files, list, locals, map, marker, module, neg, nsp, o, open, option, option_order, opts, p, package, packages, parent, path, pattern, pkg, pkgname, platform, pos, project_url, r, reader, req, reqs, requires, section, self, set, setattr, sorted, source, src, staticmethod, str, super, tuple, v, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\errors.py: RuntimeError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\extension.py: Exception, args, kw, list, map, name, self, sources, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\glob.py: OSError, basename, bytes, drive, isinstance, list, name, next, pattern, recursive, x, y
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\installer.py: e, egg_dist, isinstance, link, list, str, tmpdir, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\launch.py: compile, dict, fid, getattr, open
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\logging.py: hasattr, level, record
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\monkey.py: AssertionError, ImportError, attr, candidate, cls, func_name, getattr, hasattr, isinstance, item, mod_name, module, next, replacement, setattr, target_mod, type, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\msvc.py: ImportError, IndexError, KeyError, LookupError, OSError, TypeError, UnicodeDecodeError, ValueError, args, bits, crt_dir, dict, dir_name, exc, exists, filter, float, getattr, hkey, i, int, kwargs, line, list, locals, name, next, plat_spec, platform_info, prefix, property, range, registry_info, reversed, self, set, sorted, spec_path_lists, state_file, staticmethod, subkeys, v, value, vc_dir, vc_min_ver, vt, x64, x86
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\namespaces.py: f, filename, list, locals, map, open, parent, pkg, repr, self, sorted, staticmethod, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\package_index.py: Exception, OSError, UserWarning, ValueError, address, any, arg, args, classmethod, cls, d, delim, develop_ok, dict, e, egg_path, entry, expected, ext, fatal, filter, fn, force_scan, frag, frag2, func, getattr, h2, hash_name, host, hosts, index_url, installer, int, isinstance, item, kw, kwargs, len, line, list, local_index, location, m, map, max, message, metadata, meth, nested, open, opener, p, param2, params, password, path2, platform, precedence, property, pw, py_version, q, query, query2, range, raw_lines, rel, reporter, repository, req, requirement, retrieve, s2, search_path, section, self, server, set, source, staticmethod, status, str, super, tag, template, text, tfp, timeout, tmpdir, urls, user, username, v, vars, warning, win_base
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\py34compat.py: AttributeError, ImportError, spec
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\sandbox.py: Exception, NameError, SystemExit, a, any, args, compile, dict, dir, dist, dst, exc, exception, exceptions, file, filename, filepath, filter, flags, func, getattr, globals, hasattr, kw, list, map, mod_name, module_names, name, operation, pattern, repl, replacement, repr, sandbox, saved_exc, self, setattr, setup_script, source, src, staticmethod, stream, target, tb, type, v, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\unicode_utils.py: UnicodeDecodeError, UnicodeEncodeError, UnicodeError, enc, isinstance, str, string
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\version.py: Exception
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\wheel.py: ValueError, d, destination_eggdir, dict, dirnames, dirpath, dst_dir, entry, enumerate, extra, f, filename, filenames, filter, fp, k, list, map, member, mod, n, name, next, open, req, reversed, self, set, setattr, src_dir, staticmethod, str, t, v, zf
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\windows_support.py: func, path
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_deprecation_warning.py: Warning
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_entry_points.py: ep, eps, group, map, sorted, str, type, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_imp.py: ImportError, hasattr, isinstance, issubclass, list, module, open, paths, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_importlib.py: AttributeError, ImportError, isinstance, item, ob
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_itertools.py: ValueError, element, iterable, key, set, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_path.py: bool, p1, p2, path, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_reqs.py: map, strs
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\__init__.py: Exception, all, attrs, base, cfg, command, default, dir, file, filenames, filter, getattr, isinstance, k, kw, list, map, option, path, pathname, reinit_subcommands, self, set, setattr, str, super, v, vars, what
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\alias.py: arg, c, len, map, name, print, repr, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\bdist_egg.py: OSError, bad, base, base_dir, bdf, bool, cmdname, compress, const, dict, dir, dirname, dirs, dry_run, egg_dir, enumerate, ext, ext_name, files, flag, getattr, isinstance, kw, len, mode, name, names, next, old, open, resource, self, str, stubs, target_dir, tuple, zip_filename
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\bdist_rpm.py: line, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\build.py: bool, cmd, dict, list, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\build_clib.py: build_info, dict, isinstance, lib_name, libraries, list, self, source, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\build_ext.py: ImportError, any, base, bool, build_temp, compile, d, debug, dict, export_symbols, extra_postargs, extra_preargs, fn, fnext, hasattr, isinstance, len, lib, libname, libraries, library_dirs, list, macro, name, objects, old_inplace, open, output_dir, output_file, output_libname, runtime_library_dirs, s, self, sorted, str, suffix, target_lang, tuple, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\build_py.py: KeyError, all, attr, bool, copied, d, df, dict, egg_info, file, filter, fn, getattr, include_bytecode, len, level, link, list, map, module, module_file, open, p, package_dir, parent, path, pattern, preserve_mode, preserve_times, self, set, sorted, spec, staticmethod, str, super, tuple, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\develop.py: egg_base, f, getattr, install_dir, line, name, open, self, staticmethod, strm
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\dist_info.py: bool, component, dir_name, dir_path, dst, opts, requires_bkp, self, src, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\easy_install.py: AttributeError, Exception, ImportError, KeyError, OSError, SyntaxError, SystemExit, TypeError, UnicodeError, UserWarning, ValueError, arg, attr, attrs, base, basename, cache, cfglen, classmethod, cls, compile, counter, d, deps, dev_path, dict, dist_path, download, e, enumerate, ev, exe_filename, filter, fix_zipimporter_caches, force_windows, fp, func, getattr, ignore_errors, info, inputs, int, isinstance, item, k, key, last, len, list, locals, m, map, new, npath, onerror, open, orig_header, orig_script, p, param, path_item, prefix, print, q, range, res, script_name, self, setattr, show_deprecation, staticmethod, str, string, super, tag, text, type, type_, updater, vars, wheel_path, wininst, x, y
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\editable_wheel.py: AttributeError, Exception, NotImplementedError, OSError, UserWarning, ValueError, all, any, base_dir, bool, bytes, category, classmethod, cmd_name, dict, dir_, distribution, editable_name, ex, filename, files, getattr, hasattr, i, installation_dir, iter, k, key, len, lib, link, list, map, mod, module, namespaces_, next, ns, other, other_path, output_mapping, outputs, p, package, parent_path, path1, path2, path_entries, pkg, pkg_path, pkg_roots, pth_prefix, range, relative_output, repr, reversed, self, set, sorted, src, src_file, str, super, tmp, tmp_dir, tuple, type, unpacked, v, value, wheel_obj, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\egg_info.py: KeyError, UnicodeEncodeError, ValueError, action, basename, bool, build_py, c, chunk, cmd, debug_print, dict, dir, dir_pattern, e, enumerate, ep, extra, filename, filter, force, getattr, hasattr, ignore_egg_info_dir, int, isinstance, k, len, lf, line, list, map, match_dir, oldname, oldver, open, paths, pattern, predicate, property, range, reqs, self, sorted, staticmethod, str, stream, super, vars, what
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\install.py: caller, dict, frame, run_frame, self, staticmethod
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\install_egg_info.py: dst, self, skip, src
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\install_lib.py: dst, exclusion_path, f, hasattr, infile, ns_pkg, outfile, pkg, pkg_name, preserve_mode, preserve_symlinks, preserve_times, self, set, src, staticmethod
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\install_scripts.py: ImportError, args, contents, getattr, mode, open, script_name, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\py36compat.py: directory, filename, filenames, filter, fn, fspath, hasattr, isinstance, pattern, self, src_dir, staticmethod, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\register.py: self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\rotate.py: ValueError, e, f, int, isinstance, len, p, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\saveopts.py: cmd, opt, self, src, val
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\sdist.py: Exception, TypeError, UnicodeDecodeError, base_dir, c, cmd_name, data_files, dirname, ep, ext, f, file, filenames, fp, getattr, hasattr, item, list, name, open, self, set, src_dir, staticmethod, super, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\setopt.py: ValueError, dry_run, f, filename, kind, len, open, option, options, section, self, settings, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\test.py: dist, fget, file, filter, func, getattr, hasattr, k, len, list, map, module, obj, object, property, self, set, staticmethod, v, val
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\upload.py: self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\upload_docs.py: AssertionError, OSError, body, bool, classmethod, cls, cmd_name, ct, dict, e, f, filename, files, fragments, isinstance, item, key, len, list, map, netloc, open, params, print, query, root, s, schema, self, staticmethod, str, tuple, url
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\command\__init__.py: TypeError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\expand.py: AttributeError, Exception, ModuleNotFoundError, all, any, attr, attr_desc, bytes, callable, char, data_files, dest, dict, distribution, e, f, filepath, filepaths, getattr, hasattr, int, isinstance, iter, k, key, kwargs, len, list, locals, map, namespaces, next, obtain_mapping_value, open, package_data, packages, parent, patterns, property, qualified_class_name, self, sorted, statement, str, target, text, text_source, tuple, v, vars, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\pyprojecttoml.py: Exception, UserWarning, ValueError, any, bool, cfg, classmethod, cls, container, dict, directive, distribution, ensure_discovered, ex, exc_type, exc_value, field, file, fn, group, hasattr, ignore_option_errors, isinstance, k, line, list, open, project_cfg, self, set, setuptools_cfg, specifier, str, super, traceback, tuple, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\setupcfg.py: Exception, KeyError, NotImplementedError, UserWarning, ValueError, args, bool, chunk, classmethod, cls, command_options, config_dict, dict, distribution, ensure_discovered, find_others, func, getattr, handler, ignore_option_errors, isinstance, k, key, kwargs, label, len, line, list, locals, method, name, option, orig_value, other_files, parse_methods, path, property, root_dir, section_options, section_parser_method, sections, self, sep, setattr, str, super, tuple, v, val, values_parser, warning_class
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_apply_pyprojecttoml.py: EMPTY, Exception, PYPROJECT_CORRESPONDENCE, UserWarning, ValueError, acc, attr, callable, classmethod, cls, cmd_class, config, desc, dict, dist, ep, ex, ext, fancy_option, file, filename, getattr, getter, group, hasattr, i, isinstance, k, kind, list, name, next, obj, person, pyproject, set, setattr, str, tuple, type, v, val, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\__init__.py: args, fn, kwargs
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_validate_pyproject\error_reporting.py: all, any, bad, bool, buffer, classmethod, cls, dict, e, enumerate, ex, i, isinstance, jargon, k, len, list, name, p, parent_prefix, parents, path, prefix, property, repl, repr, schemas, self, str, substring, t, term, v, w, word
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_validate_pyproject\extra_validations.py: field, pyproject
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_exceptions.py: ValueError, definition, item, message, name, property, rule, self, super, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_validations.py: all, bool, custom_formats, data, data__authors_item, data__buildsystem__backendpath_item, data__buildsystem__requires_item, data__classifiers_item, data__cmdclass_key, data__cmdclass_val, data__datafiles_key, data__datafiles_val, data__datafiles_val_item, data__dependencies_item, data__dynamic__optionaldependencies_key, data__dynamic__optionaldependencies_val, data__dynamic_item, data__dynamic_key, data__eagerresources_item, data__entrypoints_key, data__entrypoints_val, data__excludepackagedata_key, data__excludepackagedata_val, data__excludepackagedata_val_item, data__file_item, data__find__exclude_item, data__find__include_item, data__find__where_item, data__keywords_item, data__licensefiles_item, data__maintainers_item, data__namespacepackages_item, data__obsoletes_item, data__optionaldependencies_key, data__optionaldependencies_val, data__optionaldependencies_val_item, data__packagedata_key, data__packagedata_val, data__packagedata_val_item, data__packagedir_key, data__packagedir_val, data__packages_item, data__platforms_item, data__provides_item, data__pymodules_item, data__scriptfiles_item, data__urls_key, data__urls_val, data_key, data_val, dict, enumerate, isinstance, len, list, locals, name_prefix, prop, set, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_validate_pyproject\formats.py: Exception, ImportError, all, any, bool, c, e, extras_, i, m, module, name, response, rest, self, set, str, value, version, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py: FORMAT_FUNCTIONS, acc, bool, callable, data, dict, fn, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\extern\__init__.py: ImportError, any, fullname, locals, map, prefix, property, root, root_name, self, set, spec, target, vendor_pkg, vendored_names
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\archive_util.py: DeprecationWarning, ImportError, KeyError, RuntimeError, ValueError, arg, compress, dirnames, dirpath, dry_run, filenames, format, formats, group, name, owner, root_dir, tarinfo, val, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\bcppcompiler.py: DeprecationWarning, KeyError, build, debug, depends, dir, dirs, dry_run, ell, export_symbols, ext, extra_postargs, extra_preargs, file, force, include_dirs, lib, libraries, library_dirs, macros, map, modname, msg, name, output_file, output_libname, print, runtime_library_dirs, self, source, source_filenames, sources, src_name, str, strip_dir, super, sym, tail, target_desc, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\ccompiler.py: ImportError, KeyError, LookupError, NotImplementedError, TypeError, ValueError, args, ast, before, build_temp, class_name, cmd, debug, definitions, defn, depends, dict, dirs, dry_run, dst, enumerate, export_symbols, extra_postargs, extra_preargs, fd, fn, fname, force, func, funcname, getattr, incdirs, incl, isinstance, key, kwargs, len, lib, lib_dir, lib_name, lib_type, libname, libnames, list, macro, mode, name, object, outdir, output_file, output_filename, output_libname, output_progname, pattern, print, property, self, setattr, source, source_filenames, src_name, staticmethod, str, strip_dir, target_lang, tuple, value, vars, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\cmd.py: AttributeError, RuntimeError, TypeError, all, args, attr, base_dir, base_name, cmd, cmd_name, command, create, default, dist, dst, dst_option, error_fmt, format, func, getattr, group, hasattr, infile, isinstance, level, link, list, method, mode, msg, name, option_pairs, outfile, owner, preserve_mode, preserve_symlinks, preserve_times, print, reinit_subcommands, root_dir, search_path, self, setattr, src, src_cmd, src_option, str, tester, tuple, v, what
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\config.py: default, f, key, password, response, self, username
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\core.py: KeyboardInterrupt, OSError, RuntimeError, SystemExit, ValueError, attrs, exc, f, locals, msg, print, script_args, script_name, stop_after, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\cygwinccompiler.py: DeprecationWarning, OSError, ValueError, build_temp, cc, cc_args, debug, details, dll_name, dry_run, exc, export_symbols, ext, extra_postargs, force, int, library_dirs, msg, obj, open, output_dir, output_filename, property, runtime_library_dirs, self, src, src_name, status, strip_dir, super, sym, target_desc, target_lang, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\dep_util.py: ValueError, enumerate, i, len, missing, source, sources, target, targets
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\dir_util.py: OSError, base_dir, cmd, d, dir, directory, drive, dry_run, dst, e, exc, f, file, files, isinstance, mode, n, preserve_mode, preserve_symlinks, preserve_times, set, sorted, src, str, tail, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\dist.py: AttributeError, ImportError, SystemExit, TypeError, ValueError, arg, attr, attrs, base_dir, basename, callable, cmd, cmd_name, cmd_options, command_obj, create, elm, file, frozenset, func, getattr, hasattr, header, help_option, help_tuple, isinstance, issubclass, key, len, level, line, list, locals, name, o, open, option, opts, path, pkg, pkg_info, pkgname, print, reinit_subcommands, repr, section, self, setattr, sorted, source, str, sub, type, v, vars, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\errors.py: Exception
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\extension.py: AssertionError, all, define_macros, depends, export_symbols, extra_compile_args, extra_link_args, extra_objects, filename, id, include_dirs, isinstance, kw, language, len, libraries, library_dirs, list, name, option, optional, repr, runtime_library_dirs, self, sorted, sources, str, swig_opts, undef_macros, v, word
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\fancy_getopt.py: RuntimeError, ValueError, aliases, ch, dict, getattr, header, help, help_string, isinstance, len, line, long_option, msg, negative_alias, negative_opt, option_table, options, opts, ord, print, self, setattr, short_option, str, w, what, width
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\filelist.py: allfiles, anchor, base, classmethod, cls, dirs, end, file, i, is_regex, isinstance, item, len, line, list, map, name, path, pattern, prefix, print, range, self, set, sort_tuple, sorted, start, str, w, walk_item
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\file_util.py: KeyError, OSError, ValueError, buffer_size, contents, dry_run, e, filename, line, link, msg, num, open, preserve_mode, preserve_times, src, verbose
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\log.py: UnicodeEncodeError, ValueError, args, level, self, str, threshold, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\msvc9compiler.py: DeprecationWarning, KeyError, OSError, UnicodeError, ValueError, arch, arg, build, classmethod, cls, debug, depends, dir, dirs, dll_name, dry_run, exe, export_symbols, ext, extra_postargs, extra_preargs, force, getattr, include_dirs, int, len, lib, libraries, library_dirs, list, macro, macros, manifest_file, mffilename, msg, obj, objects, open, output_libname, path, paths, pp_opts, runtime_library_dirs, self, source_filenames, sources, src_name, staticmethod, stderr, str, strip_dir, super, sym, target_desc, v, variable, verbose, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\msvccompiler.py: DeprecationWarning, ImportError, KeyError, UnicodeError, build, debug, depends, dir, dirs, dll_name, dry_run, exe, export_symbols, ext, extra_postargs, extra_preargs, force, getattr, include_dirs, int, len, lib, libraries, library_dirs, macro, macros, msg, obj, objects, output_libname, paths, platform, pp_opts, runtime_library_dirs, self, source_filenames, sources, src_name, str, strip_dir, super, sym, target_desc, v, value, verbose, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\py38compat.py: ImportError, osname, release, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\py39compat.py: vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\spawn.py: AttributeError, OSError, ValueError, dict, dry_run, exc, ext, list, p, search_path
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\sysconfig.py: AttributeError, DeprecationWarning, KeyError, ValueError, any, ar_flags, args, beg, ccshared, compiler, d, dir_a, dir_b, end, fn, getattr, globals, int, isinstance, k, len, list, next, plat_specific, shlib_suffix, spec_prefix, standard_lib, str, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\text_file.py: KeyError, RuntimeError, ValueError, filename, isinstance, list, msg, opt, options, self, setattr, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\unixccompiler.py: TypeError, aix, cc_args, cmd, compiler_cmd, compiler_cxx_ne, debug, dir, dirs, env, extra_postargs, extra_preargs, filter, include_dirs, isinstance, len, lib, lib_name, libraries, library_dirs, linker_cmd, linker_exe_ne, linker_na, linker_ne, macros, map, msg, next, obj, objects, output_dir, output_file, output_libname, root, runtime_library_dirs, self, source, src, staticmethod, str, target_desc, target_lang, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\util.py: DeprecationWarning, ImportError, KeyError, RuntimeError, ValueError, args, base_dir, beg, dict, dry_run, exc, file, force, func, hasattr, header, int, len, local_vars, map, match, n, name, new_root, open, optimize, osname, pathname, prefix, py_files, release, repr, script_fd, script_name, str, value, var, verbose, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\version.py: DeprecationWarning, NotImplemented, ValueError, ctx, enumerate, i, int, isinstance, major, map, minor, obj, patch, prerelease, prerelease_num, self, str, tuple, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\versionpredicate.py: ValueError, aPred, comp, cond, pred, self, verStr, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\_collections.py: KeyError, c, iter, key, len, list, other, reversed, scope, self, set, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\_functools.py: args, func, kwargs, param
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\_macos_compat.py: cmd
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\_msvccompiler.py: ImportError, KeyError, OSError, TypeError, UnicodeDecodeError, ValueError, base, build, classmethod, cls, cmd, debug, depends, dict, dir, dirs, dll_name, dry_run, exc, exe, export_symbols, ext, extra_postargs, extra_preargs, fallback, float, force, i, include_dirs, int, lib, libraries, library_dirs, line, macros, msg, name, obj, objects, output_libname, p, pp_opts, property, runtime_library_dirs, self, sources, staticmethod, str, super, sym, target_desc, tuple, type, v, val, value, vc_dir, verbose, vt
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\__init__.py: ImportError
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\bdist.py: DeprecationWarning, KeyError, dict, enumerate, format, i, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\bdist_dumb.py: KeyError, repr, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\bdist_rpm.py: attr, changelog, d, default, f, field, getattr, isinstance, len, list, open, path, print, readme, repr, rpm_opt, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\build.py: ValueError, cmd_name, hasattr, int, isinstance, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\build_clib.py: build_info, dict, isinstance, len, lib, lib_name, libraries, list, macro, name, self, str, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\build_ext.py: ImportError, UnicodeEncodeError, ValueError, base, build_info, dict, e, enumerate, executor, ext_name, extension, extensions, fut, hasattr, i, int, isinstance, key, len, list, macro, o, self, setattr, sorted, source, str, symbol, tuple, undef, value, vers, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\build_py.py: AssertionError, KeyError, TypeError, ValueError, f, file, fn, include_bytecode, int, isinstance, len, list, name, package_, pattern, self, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\build_scripts.py: OSError, UnicodeEncodeError, ValueError, encoding, file, open, outf, self, staticmethod
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\check.py: AttributeError, ImportError, TypeError, attr, children, debug, e, encoding, error_handler, exc, getattr, globals, halt_level, kwargs, level, message, msg, report_level, self, source, str, stream, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\clean.py: OSError, directory, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\config.py: OSError, call, decl, exe, func, head, header, headers, include_dirs, isinstance, lang, libraries, library, library_dirs, obj, open, other_libraries, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\install.py: AttributeError, Exception, KeyError, attrs, cmd_name, counter, dict, enumerate, exec_prefix, getattr, hasattr, isinstance, key, len, map, msg, name, names, ob, opt, path, print, self, set, setattr, str, value, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\install_data.py: isinstance, out, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\install_egg_info.py: f, name, open, property, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\install_headers.py: header, out, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\install_lib.py: AssertionError, ValueError, cmd_option, file, files, getattr, has_any, int, isinstance, len, output_dir, py_file, py_filenames, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\install_scripts.py: file, self
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\py37compat.py: args, f1, f2, kwargs, list
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\register.py: DeprecationWarning, ValueError, action, cmd_name, code, e, input, key, len, print, self, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\sdist.py: PendingDeprecationWarning, ValueError, cmd_name, directory, filename, filenames, filter, fmt, fn, format, fspath, hasattr, isinstance, manifest, open, pattern, self, src_dir, staticmethod, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\upload.py: AssertionError, OSError, ValueError, command, digest_cons, digest_name, e, filename, fragments, getattr, isinstance, key, len, list, open, params, pyversion, query, schema, self, str, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_distutils\command\_framework_compat.py: dict, locals, name
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\ordered_set.py: ImportError, KeyError, TypeError, ValueError, all, enumerate, hasattr, idx, isinstance, item, iter, iterable, k, key, len, list, map, obj, reversed, self, sequence, set, sets, slice, state, str, subkey, tuple, type, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\typing_extensions.py: AttributeError, C, DeprecationWarning, Ellipsis, ImportError, NotImplemented, TypeError, ValueError, a, all, any, arg, attr, b, base, bool, bound, callable, classmethod, contravariant, covariant, dct, dict, extra, f, frozenset, g, getattr, getitem, globalns, hasattr, hash, include_extras, instance, int, isinstance, issubclass, k, kwds, len, list, localns, map, n, name, namespace, obj, object, orig_bases, other, p, property, repr, scls, set, setattr, slot, str, subclass, super, t, total, tuple, type, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\zipp.py: AttributeError, FileNotFoundError, IsADirectoryError, ValueError, args, at, classmethod, dict, filter, isinstance, kwargs, list, map, minuend, mode, other, p, property, pwd, root, self, set, source, staticmethod, str, strm, subtrahend, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_adapters.py: cls, dict, key, map, orig, property, self, set, super, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_collections.py: classmethod, cls, getattr, key, map, self, str, super, text
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_compat.py: ImportError, cls, filter, finder, getattr, hasattr, staticmethod, val
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_functools.py: args, func, kwargs, method, param, self, setattr
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_itertools.py: TypeError, base_type, bytes, element, isinstance, iter, iterable, key, obj, set, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_meta.py: bool, dict, int, list, property, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\_text.py: hash, maxsplit, other, self, splitter, str, sub, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_metadata\__init__.py: AttributeError, DeprecationWarning, Exception, FileNotFoundError, IsADirectoryError, KeyError, ModuleNotFoundError, NotADirectoryError, OSError, PermissionError, StopIteration, ValueError, all, args, bool, child, classmethod, cls, default, dict, distribution_name, encoding, ep, ext, extra, f, filename, filter, filter_, finder, getattr, group, hash, int, isinstance, item, iter, kwargs, len, line, list, locals, map, method_name, next, param, params, paths, pkg, property, req, resolver, root, sections, self, size_str, sorted, spec, staticmethod, str, stream, super, tuple, value, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\abc.py: FileNotFoundError, bool, child, encoding, item, path, resource, self, str, strm
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\readers.py: FileNotFoundError, KeyError, NotADirectoryError, ValueError, all, child, exc, file, iter, list, loader, map, module, namespace_path, path, property, resource, self, str, super
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\simple.py: IsADirectoryError, RuntimeError, args, kwargs, map, mode, next, parent, property, reader, self, traversable
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\_adapters.py: AttributeError, FileNotFoundError, ValueError, adapter, args, attr, file, getattr, hasattr, iter, kwargs, len, mode, other, package, path, path_parts, property, self, spec
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\_common.py: FileNotFoundError, TypeError, cand, fd, getattr, isinstance, package, path, raw_path, str, suffix
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\_compat.py: AttributeError, ImportError, TypeError, ValueError, cls, hasattr, package, property, self, spec
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\_itertools.py: element, iterable, key, seen, set
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\importlib_resources\_legacy.py: DeprecationWarning, ValueError, any, args, bool, bytes, encoding, errors, file_name, fp, func, kwargs, name, package, parent, str, traversable
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\jaraco\context.py: Exception, args, bool, branch, dest_ctx, dict, dir, exceptions, func, issubclass, kwargs, open, property, quiet, remover, repo_dir, self, trap, url, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\jaraco\functools.py: TypeError, action, args, ast, bound_method, cache_wrapper, cleanup, exceptions, f, f1, f2, f_args, f_kwargs, float, func1, func2, funcs, getattr, hasattr, isinstance, k, kwargs, map, max_rate, method, method_name, more_itertools, namespace, obj, object, param, print, r_args, r_kwargs, range, replace, retries, self, setattr, target, transform, trap, use, vars
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py: ImportError, StopIteration, UnicodeDecodeError, args, bytes, classmethod, cls, filter, hash, identifier, isinstance, iter, iterable, len, line, map, match, maxsplit, min, new, next, old, other, para, part, prefix_lines, rest, reversed, s, s1, s2, self, slice, splitter, staticmethod, str, string, sub, subject, suffix, super, text, tuple, value, word
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\more_itertools\more.py: A, BaseException, DeprecationWarning, IndexError, M, RuntimeError, StopIteration, TypeError, ValueError, after, any, args, base_type, before, bool, bytes, callback_kwd, child, chunk, chunk_size, combo, context_manager, cur_idx, d, default, details, divmod, e, elem, enumerate, exceptions, f, fillvalue, filter, func, function, g, hasattr, hash, i1, i2, initial, int, isinstance, iter, keep_separator, keyfunc, kwargs, len, levels, limit_seconds, list, longest, map, max, maxlen, maxsplit, min, next, next_item, next_multiple, node, obj, object, offsets, ordering, other, p, pred, predicate, property, range, reducefunc, repr, result_index, reverse, reversed, s, self, set, sizes, slice, smallest_weight_key, sorted, staticmethod, str, strict, super, tail, target, tmp, too_long, too_short, tuple, type, val, validator, value_list, w, wait_seconds, weight, window_size, wrapping_args, wrapping_func, wrapping_kwargs, x, y, zip, zipped_items
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\more_itertools\recipes.py: DeprecationWarning, ImportError, IndexError, StopIteration, TypeError, ValueError, a, b, bool, cond, default, element, exception, fillvalue, filter, first, func, function, i, index, int, isinstance, it, iter, iterable, iterables, iterator, key, len, list, listOfLists, map, min, next, range, set, signal, sorted, start, sum, t1, t2, times, tuple, value, vec1, vec2, x, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\markers.py: NotImplementedError, ValueError, all, any, bool, dict, e, environment, first, groups, i, info, isinstance, item, len, lhs, list, m, marker, markers, name, op, oper, results, rhs, self, str, t, tuple, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\requirements.py: ValueError, e, list, parts, requirement_string, s, self, set, sorted, str, t
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py: DeprecationWarning, NotImplemented, ValueError, all, any, bool, dict, filtered, fn, frozenset, getattr, hash, int, isinstance, iter, left, left_split, len, list, max, object, op, operator_callable, padded_prospective, padded_spec, parsed, property, result, right, right_split, s, segment, self, set, sorted, spec_str, specifiers, str, super, tuple, value, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\tags.py: INTERPRETER_SHORT_NAMES, NotImplemented, ValueError, bool, cpu_arch, dict, explicit_abi, frozenset, hasattr, hash, id, int, interpreters, is_32bit, isinstance, len, list, major_version, map, minor, minor_version, object, other, platform_, property, range, self, set, str, string, tag, tuple, version_str, warn
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\utils.py: ValueError, frozenset, int, isinstance, len, sep, str, tuple, version_part, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\version.py: DeprecationWarning, NotImplemented, ValueError, bool, bytes, hash, i, int, isinstance, len, list, object, other, property, reversed, s, self, str, tuple, version, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\_manylinux.py: AssertionError, AttributeError, ImportError, OSError, RuntimeWarning, TypeError, ValueError, arch, bool, bytes, dict, f, file, fmt, glibc_major, glibc_max, hasattr, int, isinstance, linux, open, range, self, str, tuple, version
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\_musllinux.py: KeyError, OSError, arch, bytes, e_fmt, e_phentsize, e_phnum, e_phoff, executable, fmt, i, int, len, minor, n, open, output, p_filesz, p_fmt, p_idx, p_offset, p_type, print, range, stack, str, t, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\packaging\_structures.py: bool, hash, int, isinstance, object, other, repr, self, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\actions.py: args, attrName, attrValue, attr_dict, classname, k, l, locn, method_call, n, namespace, object, repl_str, s, self, strg, t, tokens, v
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\common.py: Combine, FollowedBy, LineEnd, Literal, OneOrMore, Opt, ParseException, ParseResults, ParserElement, Regex, ValueError, White, Word, float, fmt, hexnums, identbodychars, identchars, int, isinstance, l, ll, nums, printables, quoted_string, s, ss, staticmethod, str, sum, t, token_map, tokens, tt, v, vars, ve
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\core.py: AttributeError, Ellipsis, Exception, HIT, ImportError, IndexError, KeyError, MISS, NotImplementedError, ParseBaseException, ParseException, ParseFatalException, ParseSyntaxException, RecursiveGrammarException, RuntimeError, TypeError, UserWarning, ValueError, adjacent, all, any, args, as_group_list, as_keyword, as_match, asdict, aslist, body_chars, bool, break_flag, bytes, c, cache_hit, cache_size_limit, callPreParse, callable, caseless, chars, charset, chr, classmethod, cls, cmd_line_warn_options, col, colno, convert_whitespace_escapes, copy_defaults, cur_, debug, default, diag_enum, diag_file, dict, doActions, e, encoding, end_quote_char, endloc, enumerate, err, esc_char, esc_quote, exact, exception_action, exclude_chars, expr1, exprs_arg, exprtokens, fail_on, failure_tests, file_or_filename, flag, flags, fns, force, frm, full_dump, func, getattr, grouped, hasattr, hex, i, id, ident_chars, ie, include, include_separators, init_chars, instance, int, isinstance, issubclass, item, iter, join_string, k, kwargs, l, len, line, lineno, list, list_all_matches, loc1, loc_, locals, mat, matchString, max, max_limit, max_matches, max_mismatches, maxsplit, message, min, minElements, multiline, n, new_loc, new_peek, next, nextLoc, notChars, not_chars, o, offset, open, optElements, ord, output_html, overlap, p, paArgs, parseElementList, parse_action_exc, parse_all, part, pattern, pbe, pe, pfe, post_parse, prev, prev_loc, prev_peek, prev_result, print, print_results, property, quoteChar, raise_fatal, range, recursive, ref_col, repl, replace_with, repr, resultlist, reversed, s_m, savelist, self, set, setattr, show_groups, show_results_names, skipto_arg, slice, sorted, src, start_action, staticmethod, stop_on, str, str_type, success_action, sum, super, te, test_line, test_string, tmptokens, tok, tokenlist, tokn, toks, tuple, type, unquote_results, v, var, vars, vertical, w_action, w_category, w_message, w_module, warn_env_var, warn_opt, warning_type, with_line_numbers, word_chars, ws, wschar, wslit, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\exceptions.py: Exception, classmethod, cls, elem, enumerate, exc, ff, id, int, isinstance, len, loc, marker_string, msg, parseElementList, pe, property, pstr, self, set, staticmethod, str, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\helpers.py: And, CaselessKeyword, CaselessLiteral, CharsNotIn, Combine, Diagnostics, Dict, Empty, Enum, FollowedBy, Forward, Group, Iterable, Keyword, LineEnd, List, Literal, MatchFirst, NoMatch, OneOrMore, Opt, ParseAction, ParseException, ParserElement, Regex, SkipTo, Suppress, TokenConverter, Tuple, TypeError, Union, ValueError, Word, ZeroOrMore, a, all, allow_trailing_delim, alphanums, alphas, any, any_close_tag, any_open_tag, arity, as_keyword, as_string, b, backup_stacks, base_expr, blockStatementExpr, bool, caseless, closer, col, combine, dbl_quoted_string, empty, enumerate, ignore_expr, indent, indentStack, instring, int, int_expr, isinstance, j, k, key, l, len, list, ll, loc, max, min, nums, opExpr1, opExpr2, op_list, opener, operDef, other, pa, printables, quoted_string, re_flags, remove_quotes, rightLeftAssoc, s, self, str, str_type, strs, suppress_GT, suppress_LT, sym, t, tag_str, thisExpr, tt, tuple, use_regex, v, value, vars, warnings, xml
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\results.py: AttributeError, Exception, IndexError, KeyError, TypeError, a, any, bool, bytes, classmethod, cls, default_value, dict, dir, enumerate, full, inAccumNames, include_list, indent, ins_string, int, isinstance, item, itemseq, iter, j, k, key, kwargs, len, list, modal, next, obj, object, occurrences, other, p1, p2, position, range, repr, res, sep, set, slice, sorted, state, str, str_type, tuple, type, value, vlist, vv
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\testing.py: Exception, bool, c, dict, enumerate, exc_type, exp, expand_tabs, expected, expected_parse_results, expr, getattr, i, int, isinstance, issubclass, len, line, list, mark_control, mark_spaces, max, min, msg, name, next, print, range, rpt, run_test_results, run_test_success, run_tests_report, self, staticmethod, str, test_string, type, u, value, verbose, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\unicode.py: any, c, cc, chr, filter, fn, getattr, hasattr, int, list, obj, range, rr, self, set, sorted, str, superclass, tuple, type
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\util.py: KeyError, ValueError, bool, c, capacity, chars, chr, classmethod, cls, dict, dname, getattr, i, int, isinstance, iter, key, len, list, ll, loc, name, next, object, ord, prev, re_escape, self, set, setattr, size, sorted, str, strg
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py: globals, int, nv, property, self, str, type, zip
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py: any, bool, child, classmethod, converted, d, diag, diagram, diagram_kwargs, diagrams, dict, e, element, expr, fn, force, func, id, index, int, isinstance, key, label, len, list, name_hint, number, parent, parent_index, partial, property, self, set, show_groups, show_results_names, sorted, specification, state, str, super, type, value, vertical, x
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\tomli\_parser.py: AttributeError, IndexError, KeyError, TypeError, ValueError, access_lists, array, bool, chars, chr, codepoint, cont_key, dict, e, error_on_eof, expect, flag, float, float_str, frozenset, header, hex_len, i, int, isinstance, k, key, key_parent, key_part, len, list, literal, msg, multiline, parsed_escape, range, recursive, self, str, tuple, val, value
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\tomli\_re.py: day, day_str, hour, hour_str, int, match, micros_str, minute, minute_str, month, month_str, offset_hour_str, offset_minute_str, offset_sign_str, parse_float, sec, sec_str, sign_str, str, year, year_str, zulu_time
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\setuptools\_vendor\tomli\_types.py: int, str, tuple
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\sniffio\_impl.py: AttributeError, RuntimeError, str
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\sniffio\_tests\test_sniffio.py: old_name
E:\zeta-monorepo\apps\backend\.venv-ollama\Lib\site-packages\_distutils_hack\__init__.py: Exception, ValueError, all, any, classmethod, cls, frame, fullname, getattr, locals, name, pat, path, patterns, self, setattr, staticmethod, string
E:\zeta-monorepo\apps\backend\app\config.py: bool, dict, int, list, str
E:\zeta-monorepo\apps\backend\app\db.py: RuntimeError, session
E:\zeta-monorepo\apps\backend\app\demo_integration_main.py: dict, list, str
E:\zeta-monorepo\apps\backend\app\dependencies.py: ImportError, actor_id, agent_id, credentials, current_user, dict, float, getattr, hash, instance, int, list, plan, request, required_permissions, self, service_name, session, set, str, updates, vo
E:\zeta-monorepo\apps\backend\app\deps.py: session_factory
E:\zeta-monorepo\apps\backend\app\lifespan.py: Exception, ImportError, app, bool, e, getattr, hasattr, key, len, list, name, property, self, status, task
E:\zeta-monorepo\apps\backend\app\logger.py: name, str
E:\zeta-monorepo\apps\backend\app\main_clean.py: Exception, ValueError, call_next, dict, exc, request, str
E:\zeta-monorepo\apps\backend\app\main_production.py: Exception, TimeoutError, disp, e, enumerate, getattr, hasattr, i, int, len, range, self, str, worker_id
E:\zeta-monorepo\apps\backend\app\main_production_clean.py: Exception, ValueError, call_next, dict, exc, request, str
E:\zeta-monorepo\apps\backend\app\worker.py: Exception, RuntimeError, agent_id, bool, c, category, chunk, component, date_range, deployment_config, dict, e, emb, enumerate, exc, exception, file_id, file_path, hasattr, i, int, isinstance, len, list, model, range, report_type, result, retention_days, self, staticmethod, step, str, sum, task, task_id, task_list, text_chunks, training_data, tuple, worker
E:\zeta-monorepo\apps\backend\app\__init__.py: Exception, OSError, RuntimeError, ValueError, dict, e, getattr, list, log_level, str
E:\zeta-monorepo\apps\backend\app\ai\asr_service.py: Exception, bool, dict, getattr, info, model_size, seg, segments, self, str, wav_path
E:\zeta-monorepo\apps\backend\app\ai\config.py: Exception, bool, getattr, str
E:\zeta-monorepo\apps\backend\app\ai\embedder.py: list, model_name, self, str, text, texts
E:\zeta-monorepo\apps\backend\app\ai\llm.py: Exception, base_url, c, client, contexts, ctxs, enumerate, i, model, q, question, self, str
E:\zeta-monorepo\apps\backend\app\ai\ocr_service.py: Exception, bool, lines, page, path, self, str, txt
E:\zeta-monorepo\apps\backend\app\ai\rag_service.py: Exception, buf, chunks, data_dir, float, ids, idx, int, k, len, max_tokens, out, p, parts, query, sc, scores, self, sent, str, t, text, texts, zip
E:\zeta-monorepo\apps\backend\app\api\__init__.py: TypeError, ValueError, bool, data, dict, isinstance, list, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\optimized_schema.py: Exception, bool, dict, e, float, getattr, id, info, input, int, limit, list, offset, owner_id, self, status, str
E:\zeta-monorepo\apps\backend\app\api\graphql\resolvers.py: Exception, ValueError, agent_id, agent_repository, bool, callable, chat_id, chat_repository, current_user_id, dict, e, exc, filters, float, getattr, id, info, input, int, is_active, limit, list, m, memory_repository, memory_type, offset, query, self, set, staticmethod, status, str, u, updated_agent, user_id, user_repository
E:\zeta-monorepo\apps\backend\app\api\graphql\resolvers_simple.py: dict, h, int, list, q, source, str, text, top_k
E:\zeta-monorepo\apps\backend\app\api\graphql\schema.py: NotImplementedError, bool, float, int, list, str
E:\zeta-monorepo\apps\backend\app\api\graphql\subscriptions.py: Exception, KeyError, RuntimeError, agent, agent_id, agent_repository, chat_id, chat_repository, content, dict, e, event_type, event_types, float, getattr, hasattr, list, memory, memory_repository, message_id, metadata, redis_client, role, self, set, str, subscriber_id, subscribers, timestamp
E:\zeta-monorepo\apps\backend\app\api\graphql\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\core\context.py: classmethod, cls, dict, getattr, isinstance, key, len, property, request, self, staticmethod, str, value
E:\zeta-monorepo\apps\backend\app\api\graphql\core\dataloader.py: Exception, agent_repository, batch_load_fn, bool, cache, cache_key_fn, callback, dict, e, entity, float, future, getattr, id_, ids, int, key, kwargs, len, list, loader, max_batch_size, method_name, name, repository, result, self, str, total_stats, value, zip
E:\zeta-monorepo\apps\backend\app\api\graphql\core\middleware.py: ValueError, bool, cache_ttl, cached_result, complexity, dict, enable_caching, error, execution_time, float, hash, info, int, len, list, max_requests, query, schema, self, sorted, str, super, timestamp, tuple, variables, window
E:\zeta-monorepo\apps\backend\app\api\graphql\core\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, int, isinstance, level, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\directives\__init__.py: Any, Exception, PermissionError, ValueError, admin_override, any, arg, args, bool, cached_result, dict, e, float, getattr, hasattr, hash, int, kwargs, len, level, list, max_calls, name, owner_field, resolver, role, roles, self, str, timestamp, ttl, tuple, warn_threshold, window
E:\zeta-monorepo\apps\backend\app\api\graphql\mutations\__init__.py: agent_id, bool, chat_id, config, content, description, dict, float, importance_score, memory_id, memory_type, model_type, name, role, str, title, training_id, updates, user_id
E:\zeta-monorepo\apps\backend\app\api\graphql\queries\__init__.py: agent_id, bool, chat_id, dict, i, int, is_active, limit, list, memory_id, memory_type, min, offset, query, range, status, str, training_id, user_id
E:\zeta-monorepo\apps\backend\app\api\graphql\resolvers\agent_resolvers.py: Exception, PermissionError, ValueError, bool, e, id, info, input, int, len, limit, list, offset, owner_id, status, str
E:\zeta-monorepo\apps\backend\app\api\graphql\resolvers\base_resolvers.py: Exception, PermissionError, ValueError, admin_override, arg, args, bool, callable, check_ownership, dict, e, error, factory, getattr, hasattr, info, input_data, int, isinstance, key, kwargs, operation, resource_id, resource_owner_id, self, str
E:\zeta-monorepo\apps\backend\app\api\graphql\resolvers\optimized_agent_resolvers.py: Exception, RuntimeError, agent_id, arg, args, dict, e, float, func, func_name, hasattr, input, int, kwargs, len, limit, list, offset, operation_name, param_name, permission, required_permissions, schema_class, str, target_ms, ttl, tuple, type
E:\zeta-monorepo\apps\backend\app\api\graphql\resolvers\simple_resolvers.py: dict, h, int, list, q, source, str, text, top_k
E:\zeta-monorepo\apps\backend\app\api\graphql\schema\agent.py: list, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\schema\base.py: NotImplementedError, bool, float, int, list, str
E:\zeta-monorepo\apps\backend\app\api\graphql\schema\memory.py: list, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\schema\training.py: list, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\schema\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, module, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\subscriptions\base_subscriptions.py: list, str
E:\zeta-monorepo\apps\backend\app\api\graphql\subscriptions\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, name, str
E:\zeta-monorepo\apps\backend\app\api\graphql\tests\test_performance.py: Exception, a, agent_data, any, e, error, i, key, kwargs, len, limit, range, self, setattr, skip, str, update_data, value
E:\zeta-monorepo\apps\backend\app\api\middleware\zero_trust.py: Exception, anomaly, any, app, bool, bypass_paths, call_next, dict, e, float, getattr, int, ip, jwt_secret, len, list, locals, method, network, path, print, request, self, set, str, super, threat_detection_config, user_id
E:\zeta-monorepo\apps\backend\app\api\routers\enhanced_core.py: Exception, ValueError, bool, current_user, dict, e, enhancement_request, float, hasattr, int, kg_service, len, node_type, orchestrator, query_request, r, request, request_data, str, task_request, team_id, user_id, websocket
E:\zeta-monorepo\apps\backend\app\api\v1\admin_emergency.py: body, dict, str
E:\zeta-monorepo\apps\backend\app\api\v1\admin_outbox.py: Exception, archived_only, bool, dict, e, event, event_type, int, k, len, list, older_than_days, partitions, repo, request, str, sum, v
E:\zeta-monorepo\apps\backend\app\api\v1\agents_demo.py: agent, agent_data, agent_id, list, service, str
E:\zeta-monorepo\apps\backend\app\api\v1\agents_example.py: a, agent_id, audit_context, current_user, int, limit, list, payload, repo, skip, str, use_case
E:\zeta-monorepo\apps\backend\app\api\v1\agents_simple.py: len, name, service, str
E:\zeta-monorepo\apps\backend\app\api\v1\agents_v2.py: ValueError, a, agent_id, capabilities, e, int, len, limit, list, name_query, offset, owner_user_id, payload, str, svc
E:\zeta-monorepo\apps\backend\app\api\v1\ai.py: current_user, dict, getattr, hasattr, orchestrator, payload, result, str
E:\zeta-monorepo\apps\backend\app\api\v1\ai_trainer.py: Exception, dict, e, ex_data, float, int, len, list, m, min_quality, model, passes_gate, report, request, set, source_type, stage, str, task
E:\zeta-monorepo\apps\backend\app\api\v1\asr.py: Exception, dict, file, str, svc, tmp
E:\zeta-monorepo\apps\backend\app\api\v1\assistants.py: Exception, assistant_id, base_model, bool, capability, current_user, days, dict, e, force, hasattr, int, len, limit, list, offset, request, response, search, sort_by, sort_order, sorted, status_filter, str, svc, user, version, version_id
E:\zeta-monorepo\apps\backend\app\api\v1\assistant_router.py: Exception, bool, claims, dict, e, float, len, request, result, str
E:\zeta-monorepo\apps\backend\app\api\v1\auth_old.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\app\api\v1\automation.py: Exception, bool, bytes, context, description, dict, e, execution_id, factory, float, getattr, int, len, list, plan_id, r, request, s, safety_config, screenshot, service, step, str, type
E:\zeta-monorepo\apps\backend\app\api\v1\core_systems.py: Exception, ValueError, context, dict, e, float, int, len, list, request, service, str
E:\zeta-monorepo\apps\backend\app\api\v1\dashboard.py: Exception, dashboard_service, dict, e, job, stats, str
E:\zeta-monorepo\apps\backend\app\api\v1\datasets.py: categories, category, claims, dict, difficulties, enumerate, i, int, len, limit, list, request, s, sample_id, skip, str, user, user_id
E:\zeta-monorepo\apps\backend\app\api\v1\demo_training.py: ValueError, action, dict, e, int, job_id, limit, list, payload, str
E:\zeta-monorepo\apps\backend\app\api\v1\federated.py: Exception, dict, dt, exc, float, getattr, int, len, list, max, num_updates, payload, rejected, result, round_id, self, session, str, u, updates
E:\zeta-monorepo\apps\backend\app\api\v1\feedback.py: dict, int, len, list, payload, session, session_id, str
E:\zeta-monorepo\apps\backend\app\api\v1\llm.py: AttributeError, dict, result, service, str
E:\zeta-monorepo\apps\backend\app\api\v1\logs.py: LOGS, component, dict, int, job_id, level, limit, list, msg, offset, str
E:\zeta-monorepo\apps\backend\app\api\v1\memory_semantic.py: d, dict, float, i, int, it, list, m, pipe, req, s, str, t
E:\zeta-monorepo\apps\backend\app\api\v1\meta.py: dict, f, meta, path, str, ver
E:\zeta-monorepo\apps\backend\app\api\v1\meta_old.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\app\api\v1\metrics_summary.py: dict, float, int, str
E:\zeta-monorepo\apps\backend\app\api\v1\nlp.py: Exception, ValueError, any, claims, dict, float, int, isinstance, keyword, language, len, llm_result, request, result, str, test_result, text
E:\zeta-monorepo\apps\backend\app\api\v1\observability.py: Exception, bool, e, str, subsystem
E:\zeta-monorepo\apps\backend\app\api\v1\one_click_learning.py: Exception, UnicodeDecodeError, asr_engine, audio, auto_ingest, bool, dict, e, f, file, float, getattr, image, int, language, len, list, ocr_engine, open, preprocess, rag_engine, request, search_query, str, user
E:\zeta-monorepo\apps\backend\app\api\v1\performance.py: Exception, dict, e, endpoint, float, int, list, max, str, window_minutes
E:\zeta-monorepo\apps\backend\app\api\v1\plans_example.py: FileNotFoundError, PermissionError, ValueError, audit, audit_context, current_user, exc, int, limit, list, p, payload, plan_id, repo, skip, status_filter, step_payload, str, use_case
E:\zeta-monorepo\apps\backend\app\api\v1\privacy.py: dict, list, req, str
E:\zeta-monorepo\apps\backend\app\api\v1\profiling.py: Exception, bool, chunks, dict, e, enumerate, float, i, int, k, len, list, min, orch_result, p, range, req, res, str, texts, timings
E:\zeta-monorepo\apps\backend\app\api\v1\rag.py: dict, int, len, list, payload, r, str, x
E:\zeta-monorepo\apps\backend\app\api\v1\rag_router.py: Exception, body, chunk, e, f, files, p, page, payload, s, str, t, tmp, ws
E:\zeta-monorepo\apps\backend\app\api\v1\router.py: Exception, exc, getattr, mod
E:\zeta-monorepo\apps\backend\app\api\v1\router_creators.py: dict, str
E:\zeta-monorepo\apps\backend\app\api\v1\rules.py: RULES, active_only, body, bool, category, dict, list, r, str
E:\zeta-monorepo\apps\backend\app\api\v1\scaffold.py: TypeError, bool, capability, dict, dry_run, getattr, list, s, steps, str
E:\zeta-monorepo\apps\backend\app\api\v1\scaffold_simple.py: bool, capability, dry_run, s, str
E:\zeta-monorepo\apps\backend\app\api\v1\security.py: Exception, bool, current_user, e, int, key, len, list, policy_input, str
E:\zeta-monorepo\apps\backend\app\api\v1\self_improvement.py: Exception, bool, container, dict, e, float, int, len, list, r, result, str, sum, update_request
E:\zeta-monorepo\apps\backend\app\api\v1\settings.py: Exception, e, settings_update
E:\zeta-monorepo\apps\backend\app\api\v1\status.py: Exception, dict, e, f, feature_key, len, list, max, next, round, str
E:\zeta-monorepo\apps\backend\app\api\v1\training.py: Exception, actor_id, allowed_exts, allowed_mimes, artifact_key, bool, current_user, description, dict, e, f, feedback, file, file_svc, files, hasattr, ids, int, isinstance, kb, len, list, rating, request, rlhf, s, set, str, svc, topic, trainer, training_service, tuple
E:\zeta-monorepo\apps\backend\app\api\v1\uploads.py: OSError, content_type, dict, e, extensions, f, file, filename, len, open, str
E:\zeta-monorepo\apps\backend\app\api\v1\users_demo.py: current_user, dict, len, list, operation_data, profile_data, security_ctx, str, user_data, user_id, user_ids
E:\zeta-monorepo\apps\backend\app\api\v1\ws.py: Exception, conns, dict, e, int, job_id, len, notification, notification_connections, payload, set, str, sum, training_connections, websocket, ws
E:\zeta-monorepo\apps\backend\app\api\v1\_schemas.py: bool, dict, float, int, list, str
E:\zeta-monorepo\apps\backend\app\api\v1\agent\router.py: agent, agent_data, agent_id, agent_service, current_user, dict, list
E:\zeta-monorepo\apps\backend\app\api\v1\agent\__init__.py: AttributeError, Exception, RuntimeError, ValueError, bool, config, dict, e, getattr, hasattr, int, isinstance, level, list, module, name, str
E:\zeta-monorepo\apps\backend\app\api\v1\agents\team_router.py: Exception, dict, e, event, len, list, max, pending, queue, str, t, task, team_id, websocket
E:\zeta-monorepo\apps\backend\app\api\v1\auth\router.py: Exception, auth_service, current_user, dict, e, login_data, str, user_data
E:\zeta-monorepo\apps\backend\app\api\v1\chat\router.py: Exception, chat_data, chat_id, chat_service, current_user, list, message_data, msg, websocket
E:\zeta-monorepo\apps\backend\app\api\v1\endpoints\admin_outbox.py: Exception, RuntimeError, bool, dict, e, int, limit, repo, request, str, sum
E:\zeta-monorepo\apps\backend\app\api\v1\endpoints\agents_example.py: ImportError, agent, agent_id, bool, dict, exc, getattr, int, is_active, label, limit, list, offset, payload, search, service, str, user
E:\zeta-monorepo\apps\backend\app\api\v1\endpoints\mentor.py: bytes, dict, float, hasattr, int, len, list, llm, m, payload, str, stream_result, sum, tok
E:\zeta-monorepo\apps\backend\app\api\v1\endpoints\security_demo.py: action, admin_subject, agent_id, deps, dict, file_id, int, list, req, resource, resource_type, str, subject, user_id
E:\zeta-monorepo\apps\backend\app\api\v1\memory\router.py: current_user, dict, list, memory_data, memory_id, memory_service, search_data
E:\zeta-monorepo\apps\backend\app\api\v1\rag\router.py: current_user, dict, doc, document_data, document_id, list, query_data, rag_service, result
E:\zeta-monorepo\apps\backend\app\api\v1\router\factory.py: call_next, dict, float, print, request, self, str, threshold, time_taken
E:\zeta-monorepo\apps\backend\app\api\v1\security\policy_router.py: Exception, body, bool, e, getattr, identity, int, k, list, max, request, str, v
E:\zeta-monorepo\apps\backend\app\api\v1\status\router.py: dict, str, system_service
E:\zeta-monorepo\apps\backend\app\api\v1\ws\progress_router.py: Exception, TimeoutError, run_id, str, websocket
E:\zeta-monorepo\apps\backend\app\api\v1\_common\health.py: Exception, all, bool, dep, dict, e, enumerate, error, float, i, is_healthy, isinstance, k, len, result, round, str, sum, tuple, v
E:\zeta-monorepo\apps\backend\app\api\v1\_common\metrics.py: Exception, ImportError, data, dict, e, len, list, name, str, value
E:\zeta-monorepo\apps\backend\app\api\v2\real_time_collab_optimized.py: Exception, bool, classmethod, cls, connection, cursor_update, dict, e, event_type, initial_content, int, len, list, min, op, op1, op2, operation_request, request, role, self, session, sessions, set, since_version, staticmethod, str, sum, tuple, user, user_cursors, user_id, websocket
E:\zeta-monorepo\apps\backend\app\api\v2\security_ai.py: Exception, agent, dict, event, exc, float, getattr, hasattr, payload, str, svc
E:\zeta-monorepo\apps\backend\app\api\v2\__init__.py: TypeError, ValueError, bool, data, dict, isinstance, list, name, str
E:\zeta-monorepo\apps\backend\app\api\websockets\agent_websocket.py: Exception, RuntimeError, str
E:\zeta-monorepo\apps\backend\app\api\websockets\rag_ws.py: Exception, client, data, dict, e, event, event_type, self, set, str, websocket
E:\zeta-monorepo\apps\backend\app\asr\engine.py: Exception, FileNotFoundError, ImportError, RuntimeError, beam_size, bool, chunk_length, compute_type, dict, e, hasattr, info, int, language, len, list, model_size, print, segment, segments, self, str, vad_filter
E:\zeta-monorepo\apps\backend\app\auth\auth_db.py: Exception, bool, e, email, getattr, int, password_hash, self, session, str, user_id, username
E:\zeta-monorepo\apps\backend\app\auth\auth_dependencies.py: Exception, dict, e, getattr, hasattr, permission_name, request, required_role, resource_builder, str, tenant_id_param, tuple, user
E:\zeta-monorepo\apps\backend\app\auth\dependencies.py: Exception, action_name, action_risk, context, dict, e, permission_name, permission_names, request, resource_id, resource_type, str, token, user, user_agent
E:\zeta-monorepo\apps\backend\app\auth\dependencies_fixed.py: Exception, dict, e, getattr, hasattr, permission_name, request, resource_builder, str, tuple, user, user_agent
E:\zeta-monorepo\apps\backend\app\auth\jwt_dependencies.py: Exception, KeyError, config, dict, e, hash, int, refresh_token, request, self, str, token
E:\zeta-monorepo\apps\backend\app\auth\jwt_handler.py: getattr, isinstance, list, staticmethod, str, token, user
E:\zeta-monorepo\apps\backend\app\auth\logging_config.py: action, allowed, bool, dict, duration_ms, error, event_type, float, kwargs, operation, resource, str, success, tenant_id, token_hash, user_id
E:\zeta-monorepo\apps\backend\app\auth\security_middleware.py: Exception, ValueError, bool, call_next, e, enforce_auth, enforce_rbac, event_type, getattr, hasattr, kwargs, list, perm, permissions, request, route_pattern, scheme, self, str, super, token, user
E:\zeta-monorepo\apps\backend\app\auth\tests\test_auth.py: client, exc_info, isinstance, len, str
E:\zeta-monorepo\apps\backend\app\common\error_handlers.py: Exception, dict, exc, getattr, isinstance, public_code, request, status, str, type
E:\zeta-monorepo\apps\backend\app\common\exceptions.py: Exception, code, detail, dict, http_status, int, meta, self, str, super
E:\zeta-monorepo\apps\backend\app\common\schemas.py: dict, str
E:\zeta-monorepo\apps\backend\app\compat\startup_check.py: Exception, ValueError, dict, getattr, int, mod, str
E:\zeta-monorepo\apps\backend\app\controllers\analytics_controller.py: Exception, ValueError, analytics, dict, exc, isinstance, period, self, str
E:\zeta-monorepo\apps\backend\app\controllers\batch_controller.py: Exception, ValueError, batch, cron, dict, exc, isinstance, name, params, self, str
E:\zeta-monorepo\apps\backend\app\controllers\cli_controller.py: Exception, ValueError, cli, command, exc, int, isinstance, list, self, str
E:\zeta-monorepo\apps\backend\app\controllers\desktop_controller.py: Exception, ValueError, action, all, button, bytes, desktop, dict, exc, int, isinstance, k, len, list, self, str, user_id, x, y
E:\zeta-monorepo\apps\backend\app\controllers\mobile_controller.py: Exception, ValueError, all, arg, args, body, data, device_id, device_token, dict, exc, isinstance, platform, push, self, str, title, user_id
E:\zeta-monorepo\apps\backend\app\controllers\monitoring_controller.py: Exception, ValueError, dict, evt, exc, int, isinstance, len, list, monitoring, n, name, self, str
E:\zeta-monorepo\apps\backend\app\controllers\stream_controller.py: Exception, ValueError, bus, dict, exc, isinstance, msg, payload, self, str, topic
E:\zeta-monorepo\apps\backend\app\controllers\system_controller.py: Exception, dict, exc, self, str, system
E:\zeta-monorepo\apps\backend\app\controllers\voice_controller.py: Exception, ValueError, bytes, dict, exc, float, isinstance, language, self, speed, str, text, voice
E:\zeta-monorepo\apps\backend\app\controllers\webhook_controller.py: Exception, ValueError, bool, bytes, data, dict, event, exc, headers, isinstance, payload, provider, self, str, webhook
E:\zeta-monorepo\apps\backend\app\controllers\web_controller.py: Exception, ValueError, context, dict, exc, isinstance, name, self, str, template
E:\zeta-monorepo\apps\backend\app\controllers\__init__.py: AttributeError, Exception, ImportError, RuntimeError, bool, dict, e, globals, module_name, name, str
E:\zeta-monorepo\apps\backend\app\dependencies\cache.py: getattr, request
E:\zeta-monorepo\apps\backend\app\dependencies\event_dependencies.py: session_factory
E:\zeta-monorepo\apps\backend\app\dependencies\memory.py: Exception, RuntimeError, batch_size, bool, d, deleted, dict, embedding_model, filters, flt, hard, i, ids, int, len, list, m, namespace, r, records, s, self, str, t, target_model, top_k
E:\zeta-monorepo\apps\backend\app\dependencies\__init__.py: Exception, ValueError, config, dict, exc, isinstance, key, settings, str, type
E:\zeta-monorepo\apps\backend\app\deps\auth.py: Exception, any, authorization, bool, credentials, current_user, data, details, dict, e, event_type, exc, getattr, i, isinstance, len, list, range, refresh_token, request, required_scope, resource, resource_owner_id, s, scheme, self, set, str, suggestions, user
E:\zeta-monorepo\apps\backend\app\deps\database.py: session
E:\zeta-monorepo\apps\backend\app\deps\security.py: action, environment, getattr, hasattr, int, min_level, request, required_role, resource_builder, str, subject, tuple
E:\zeta-monorepo\apps\backend\app\deps\__init__.py: ValueError, bool, isinstance, list, logger, permission, self, str
E:\zeta-monorepo\apps\backend\app\exceptions\api_exceptions.py: Exception, code, ctx, details, dict, e, exc, field_errors, getattr, hint, http_status, identifier, int, isinstance, list, message, request, resource, self, service, str, super, tuple, x
E:\zeta-monorepo\apps\backend\app\exceptions\custom_handlers.py: Exception
E:\zeta-monorepo\apps\backend\app\handlers\domain_event_handlers.py: Exception, METRICS, chunking_port, chunking_service, dict, e, embedding_port, embedding_service, event, event_bus, float, getattr, hasattr, i, ids, int, len, list, range, s, self, session_getter, str, text, vector_store, vector_store_port
E:\zeta-monorepo\apps\backend\app\handlers\domain_event_handlers_hardened.py: Exception, chunking_service, dict, e, embedding_service, event, event_bus, float, getattr, hasattr, i, len, list, range, self, session_getter, str, text, vector_store
E:\zeta-monorepo\apps\backend\app\handlers\idempotency.py: Exception, attr, dict, e, event, fn, getattr, handler_name, hasattr, isinstance, key, result, session, session_getter, str
E:\zeta-monorepo\apps\backend\app\infrastructure\__init__.py: list, str
E:\zeta-monorepo\apps\backend\app\middleware\api_version.py: API_VERSION, call_next, request, str
E:\zeta-monorepo\apps\backend\app\middleware\auth_jwt.py: Exception, algorithm, any, app, auto_error, bool, call_next, dict, e, excluded_paths, expires_in, float, int, last_activity, list, path, request, secret_key, self, str, super
E:\zeta-monorepo\apps\backend\app\middleware\auth_middleware.py: Exception, admin_path, algorithm, any, bool, current_user, dict, e, exc, expires_delta, frozenset, getattr, hasattr, int, list, message, permissions, prefix, receive, scope, secret_key, self, send, str, tuple
E:\zeta-monorepo\apps\backend\app\middleware\compression_middleware.py: Exception, any, app, bool, bytes, call_next, chunk, compression_level, dict, e, exclude_path, exclude_paths, gz_file, hasattr, int, isinstance, len, list, max, memoryview, min, minimum_size, path, request, round, self, set, str, stream, super
E:\zeta-monorepo\apps\backend\app\middleware\cors_middleware.py: allow_headers, allow_methods, allow_origin_regex, allow_origins, allowed_origins, app, bool, call_next, dict, expose_headers, getattr, h, header, int, list, max_age, request, self, staticmethod, str, super
E:\zeta-monorepo\apps\backend\app\middleware\ids_loader.py: Exception, app, dict, fh, isinstance, str
E:\zeta-monorepo\apps\backend\app\middleware\jwt.py: Exception, algorithm, any, app, autonomous_path, autonomous_paths, autonomous_rate_limit, bool, call_next, dict, e, event_type, excluded_path, excluded_paths, hasattr, header, int, k, kwargs, metadata, path, rate_limit_per_minute, request, secret_key, self, set, str, super, v, value
E:\zeta-monorepo\apps\backend\app\middleware\jwt_middleware.py: Exception, algorithm, any, app, auto_error, bool, call_next, dict, e, excluded_paths, expires_in, float, int, last_activity, list, path, request, secret_key, self, str, super
E:\zeta-monorepo\apps\backend\app\middleware\logging.py: call_next, request, str
E:\zeta-monorepo\apps\backend\app\middleware\logging_production.py: any, app, data, dict, event_dict, getattr, header, isinstance, item, k, key, len, list, logger_name, message, name, next, pattern, receive, record, round, scope, self, send, sensitive, str, text, v, value
E:\zeta-monorepo\apps\backend\app\middleware\metrics_http.py: Exception, call_next, e, request, self, str
E:\zeta-monorepo\apps\backend\app\middleware\metrics_middleware.py: Exception, app, bool, call_next, dict, e, enable_response_size, float, hasattr, int, len, max, metrics_port, request, self, str, super
E:\zeta-monorepo\apps\backend\app\middleware\performance.py: Exception, ImportError, alert_thresholds, app, bool, call_next, dict, e, endpoint, float, getattr, globals, hasattr, hash, hit, int, key, len, list, m, max, min, operation, operation_name, query, request, row_count, self, sorted, str, sum, super, times, window_minutes
E:\zeta-monorepo\apps\backend\app\middleware\performance_middleware.py: Exception, ImportError, any, app, bool, burst_allowed, burst_info, burst_limit, call_next, compression_level, content_length, content_type, ct, data, default_rate_limit, dict, e, enable_metrics, endpoint, float, getattr, hasattr, int, len, limit, list, max, min, minimum_size, minute_limit, percentile, print, rate_info, redis_url, request, self, slow_request_threshold, sorted, str, sum, super, times, tuple, window
E:\zeta-monorepo\apps\backend\app\middleware\rate_limiting.py: app, call_next, dict, float, hasattr, int, len, list, max, req_time, request, requests_per_minute, self, str, super
E:\zeta-monorepo\apps\backend\app\middleware\request_id.py: call_next, request, str
E:\zeta-monorepo\apps\backend\app\middleware\security_consolidated.py: app, bool, call_next, enable_content_type_sniffing, enable_csrf, enable_hsts, enable_rate_limit_headers, enable_xss_protection, hasattr, int, kwargs, max_request_size, request, self, str, super, user_agent
E:\zeta-monorepo\apps\backend\app\middleware\simple_performance_middleware.py: Exception, app, bool, burst_allowed, burst_info, burst_limit, call_next, dict, e, endpoint, float, getattr, hasattr, int, len, limit, list, max, min, percentile, print, rate_info, req_time, request, requests_per_minute, self, slow_request_threshold, sorted, sorted_data, str, sum, super, times, tuple, window_seconds
E:\zeta-monorepo\apps\backend\app\middleware\security\__init__.py: list, str
E:\zeta-monorepo\apps\backend\app\minimal_rag\core.py: Exception, a, b, cache, dict, embedder, float, i, int, len, list, metadata, question, r, range, redis, reranker, result, retriever, self, sorted, str, sum, text, top_k, ttl_seconds, x, zip
E:\zeta-monorepo\apps\backend\app\minimal_rag\__init__.py: Exception, OSError, RuntimeError, ValueError, dict, e, getattr, list, log_level, str
E:\zeta-monorepo\apps\backend\app\monitoring\metrics.py: Exception, ImportError, args, batch_size, bool, dict, duration_seconds, e, error_type, event_type, float, func, int, kwargs, labels, len, list, max, metric_name, min, name, port, production, result, self, staticmethod, str, sum, value
E:\zeta-monorepo\apps\backend\app\monitoring\__init__.py: Exception, RuntimeError, ValueError, bool, config, dict, e, enable_prometheus, isinstance, key, str
E:\zeta-monorepo\apps\backend\app\observability\custom_metrics.py: Exception, dict, getattr, metrics, str
E:\zeta-monorepo\apps\backend\app\observability\logging.py: Exception, level, str
E:\zeta-monorepo\apps\backend\app\observability\metrics.py: Exception, dict, e, family, len, list, registry, sample, self, str
E:\zeta-monorepo\apps\backend\app\observability\metrics_agent.py: Exception, agent_id, count, dict, e, endpoint, entities_count, error_type, float, int, len, list, max, max_hops, min, relations_count, self, status, str, sum, team_id, teams_by_status, workflow, workflow_type
E:\zeta-monorepo\apps\backend\app\observability\metrics_collector.py: Exception, ImportError, ValueError, bool, collection_interval, collector, collector_func, description, dict, e, enable_detailed_timing, entry, float, format_type, history_deque, hours, int, isinstance, k, len, list, max, max_histogram_buckets, metric_name, metric_type, min, name, rate_deque, result, retention_hours, self, sorted, str, sum, t, tags, timestamp, tuple, unit, v, value, window_seconds
E:\zeta-monorepo\apps\backend\app\observability\metrics_registry.py: Exception, getattr
E:\zeta-monorepo\apps\backend\app\observability\shared_metrics.py: Exception, collector, doc, getattr, list, name, names, self, str
E:\zeta-monorepo\apps\backend\app\observability\tracing.py: Exception, ImportError, app, args, attributes, bool, e, enabled, engine, func, jaeger_endpoint, kwargs, name, self, service_name, str
E:\zeta-monorepo\apps\backend\app\observability\__init__.py: Exception, RuntimeError, ValueError, bool, config, dict, e, enable_metrics, enable_tracing, hasattr, isinstance, key, str
E:\zeta-monorepo\apps\backend\app\ocr\engine.py: Exception, FileNotFoundError, ImportError, RuntimeError, ValueError, bool, box, conf, confidence, dict, e, enumerate, i, int, language, line, preprocess, print, self, str, use_gpu
E:\zeta-monorepo\apps\backend\app\rag\engine.py: Exception, ImportError, ValueError, batch_size, bool, dict, e, enumerate, float, i, idx, int, k, len, list, meta, model_name, normalize, print, query, result, score, score_threshold, self, str, text, texts, tuple, zip
E:\zeta-monorepo\apps\backend\app\realtime\__init__.py: Exception, RuntimeError, ValueError, bool, config, dict, e, enable_websockets, hasattr, isinstance, key, str
E:\zeta-monorepo\apps\backend\app\schemas\agent.py: agent, bool, classmethod, cls, dict, float, int, str
E:\zeta-monorepo\apps\backend\app\schemas\chat.py: bool, chat, classmethod, cls, dict, message, str
E:\zeta-monorepo\apps\backend\app\schemas\memory.py: classmethod, cls, dict, float, int, list, memory, str
E:\zeta-monorepo\apps\backend\app\schemas\rag.py: bool, classmethod, cls, dict, document, float, int, list, str
E:\zeta-monorepo\apps\backend\app\schemas\__init__.py: Exception, TypeError, ValueError, bool, data, dict, e, isinstance, key, list, name, str
E:\zeta-monorepo\apps\backend\app\security\jwks_cache.py: Exception, ValueError, client, dict, e, int, len, max_retries, retry_backoff, self, str, token, ttl, url
E:\zeta-monorepo\apps\backend\app\security\jwt.py: bool, data, dict, e, email, expires_delta, field, hashed_password, int, is_active, list, password, plain_password, role, str, token, user_id, username
E:\zeta-monorepo\apps\backend\app\security\jwt_dependency.py: Exception, any, bool, e, int, isinstance, level, list, method, r, request, required_level, role, self, set, str
E:\zeta-monorepo\apps\backend\app\security\oidc.py: Exception, RuntimeError, audience, client, dict, e, int, issuer, k, list, request, self, str
E:\zeta-monorepo\apps\backend\app\security\opa_client.py: Exception, bool, client, e, input_data, int, list, reason, self, str, timeout, url
E:\zeta-monorepo\apps\backend\app\security\production.py: any, bool, c, data, dict, expires_delta, float, hashed_password, int, key, len, limit, list, mask_char, max, password, plain_password, req, req_time, request_headers, requests, role, self, staticmethod, str, subject, token, tuple, window
E:\zeta-monorepo\apps\backend\app\security\rbac.py: action, all, any, bool, isinstance, len, list, request, require_all, require_all_scopes, required_scope, resource, scope, set, str, token, user_role, user_scopes
E:\zeta-monorepo\apps\backend\app\serializers\admin.py: bool, dict, float, int, list, set, str
E:\zeta-monorepo\apps\backend\app\serializers\agent.py: bool, classmethod, cls, dict, entity, float, getattr, int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\agent_serializers_v2.py: agent, classmethod, cls, dict, int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\analytics_serializers.py: dict, float, int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\assistant_serializers.py: ValueError, bool, dict, float, int, len, list, str, v
E:\zeta-monorepo\apps\backend\app\serializers\auth.py: str
E:\zeta-monorepo\apps\backend\app\serializers\automation.py: bool, dict, float, int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\base_serializers.py: default, str, v
E:\zeta-monorepo\apps\backend\app\serializers\chat_serializers.py: classmethod, cls, dict, ent, getattr, int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\common.py: ValueError, action, bool, classmethod, cls, cursor, data, details, dict, field_errors, float, has_next, has_prev, identifier, int, limit, list, message, meta_kwargs, request_id, resource, str, total_count, v
E:\zeta-monorepo\apps\backend\app\serializers\dashboard_serializers.py: float, int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\memory_serializers.py: dict, float, int, str
E:\zeta-monorepo\apps\backend\app\serializers\plans.py: ValueError, bool, classmethod, cls, data, dict, entity, float, getattr, goal, int, len, list, self, step, str, tag, v
E:\zeta-monorepo\apps\backend\app\serializers\rag.py: ValueError, classmethod, float, int, list, str, v
E:\zeta-monorepo\apps\backend\app\serializers\settings_serializers.py: bool, int
E:\zeta-monorepo\apps\backend\app\serializers\training_serializers.py: int, list, str
E:\zeta-monorepo\apps\backend\app\serializers\user.py: dict, str
E:\zeta-monorepo\apps\backend\app\serializers\ws.py: dict, exported_names, isinstance, k, lines, list, model, name, output_dir, output_file, prop, props, repr, required, schema, str, tuple, v, written
E:\zeta-monorepo\apps\backend\app\serializers\_alias.py: camel, p, s, snake, str
E:\zeta-monorepo\apps\backend\app\services\federated_orchestrator.py: accepted, accepted_mimes, apply_clip, apply_dp, artifact_uri, bool, capabilities, client_id, client_pk, content_type, deadline, dict, duration, float, getattr, ids, int, len, list, max_bytes, meta, metrics, model_version, payload_sha256, payload_size_bytes, payload_uri, plan, r, reg_token_hash, rejected, result, round_id, round_name, sample_size, self, session, sha256, signature, signature_required, str, target_clients, tuple, updates, version
E:\zeta-monorepo\apps\backend\app\services\gemini_service.py: Exception, bool, client_provider, dict, exc, self, settings, str
E:\zeta-monorepo\apps\backend\app\services\llm_adapter.py: Exception, bool, dict, e, float, isinstance, result, return_scores, rules, str, temperature, text
E:\zeta-monorepo\apps\backend\app\startup\authorization.py: Exception, RuntimeError, bool, e, use_mock_jit
E:\zeta-monorepo\apps\backend\app\startup\observability.py: Exception, ImportError, bool, dict, e, enable_metrics, enable_tracing, print, str
E:\zeta-monorepo\apps\backend\app\status\feature_registry.py: Exception, TimeoutError, bool, callable, checker_path, details, dict, e, enumerate, f, feature, feature_config, float, func_name, getattr, i, int, isinstance, key, len, list, module_path, next, open, result, round, status, str, sum, tuple, use_cache
E:\zeta-monorepo\apps\backend\app\status\__init__.py: TypeError, ValueError, bool, data, dict, isinstance, list, name, str
E:\zeta-monorepo\apps\backend\app\status\checks\database.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\dataset.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\gpu.py: Exception, FileNotFoundError, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\inference.py: ConnectionError, Exception, TimeoutError, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\rag.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\redis.py: ConnectionError, Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\storage.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\training.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\vector_db.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\status\checks\websocket.py: Exception, e, str, tuple
E:\zeta-monorepo\apps\backend\app\utils\k8s_client.py: bool, dict, image, int, kubeconfig, list, name, namespace, repo, self, str, timeout_seconds
E:\zeta-monorepo\apps\backend\app\utils\mapper.py: dict, i, isinstance, k, list, m, name, obj, out, str, v
E:\zeta-monorepo\apps\backend\app\validators\assistant_validators.py: ValueError, assistant_data, assistants, bool, config, current_depth, dict, e, enumerate, float, i, int, isinstance, item, key, len, list, max, metadata, name, obj, operation_data, params, permissions, required_perm, set, sorted, str, tool_id, tools, type, user_permissions, v, value
E:\zeta-monorepo\apps\backend\app\validators\business_validators.py: all, bool, isinstance, list, staticmethod, str, t, tags
E:\zeta-monorepo\apps\backend\app\validators\file_validators.py: allowed, bool, path, set, staticmethod, str
E:\zeta-monorepo\apps\backend\app\validators\request_validators.py: dict, payload, staticmethod, str
E:\zeta-monorepo\apps\backend\app\validators\security_validators.py: bool, count, int, limit, required, set, staticmethod, str, user_scopes
E:\zeta-monorepo\apps\backend\app\validators\training_validators.py: ValueError, any, bool, char, chunk, chunk_index, content, data_chunks, dict, enumerate, i, indicator, input_type, int, isinstance, key, len, list, metadata, pattern, str, value
E:\zeta-monorepo\apps\backend\app\websockets\agent_websocket.py: Exception, RuntimeError, str
E:\zeta-monorepo\apps\backend\app\websockets\broadcast.py: Exception, dict, list, msg, str, ws
E:\zeta-monorepo\apps\backend\app\websockets\chat.py: Exception, dict, e, len, list, rag_engine, result, self, str, user, websocket
E:\zeta-monorepo\apps\backend\app\websockets\chat_websocket.py: Exception, ValueError, agent_id, bool, cid, conversation_id, dead, dict, e, exclude_connection, hasattr, index, int, key, keys_to_delete, len, list, message, notification, self, str, svc, ws
E:\zeta-monorepo\apps\backend\app\websockets\export_ws_schema.py: print
E:\zeta-monorepo\apps\backend\app\websockets\get_ws_router.py: dict, str
E:\zeta-monorepo\apps\backend\app\websockets\optimized_connection_manager.py: Exception, bool, compress, connection, dict, e, enable_compression, exclude, int, isinstance, len, list, print, result, round, self, set, str, user_id, websocket, zip
E:\zeta-monorepo\apps\backend\app\websockets\rag_websocket.py: Exception, dict, doc, e, enumerate, i, int, len, list, range, self, str, user_id, websocket
E:\zeta-monorepo\apps\backend\app\websockets\schemas.py: Exception, bool, dict, int, list, m, model, models, out, str, type
E:\zeta-monorepo\apps\backend\app\websockets\security.py: Exception, action_name, allowed, bool, dict, e, getattr, hash, permission, reason, resource_id, resource_type, self, str, user_agent, websocket
E:\zeta-monorepo\apps\backend\app\websockets\training_ws.py: Exception, ValueError, active_connections, dict, e, int, job_id, list, message, progress, stage, str, websocket
E:\zeta-monorepo\apps\backend\app\websockets\router\__init__.py: list, str
E:\zeta-monorepo\apps\backend\cli\dlq_replay.py: Exception, KeyboardInterrupt, ValueError, archived_only, bool, dict, dry_run, e, event, event_type, i, input, int, len, limit, list, min, older_than_days, partition, print, range, result, self, str
E:\zeta-monorepo\apps\backend\cli\maintenance.py: Exception, ImportError, any, bool, conn, description, dry_run, e, error, f, info, issue, len, manifest, message, open, pkg, print, rec, result, scan_only, signature, str, success, var, vuln
E:\zeta-monorepo\apps\backend\config\api_config.py: bool, dict, int, isinstance, list, origin, range, str, v, version
E:\zeta-monorepo\apps\backend\config\auth_config.py: bool, int, str
E:\zeta-monorepo\apps\backend\config\cache.py: Exception, TypeError, UnicodeDecodeError, ValueError, bool, bytes, classmethod, dict, e, float, int, isinstance, k, key, len, list, namespace, node, property, self, stats, str, v
E:\zeta-monorepo\apps\backend\config\cache_config.py: agent_id, bool, bytes, chat_id, dict, file_id, float, identifier, int, message_id, property, self, staticmethod, str, user_id, value
E:\zeta-monorepo\apps\backend\config\celery_config.py: Exception, bool, content, dict, int, isinstance, list, str, v
E:\zeta-monorepo\apps\backend\config\database.py: Exception, alembic_cfg_path, autogenerate, backup_dir, bool, connection, dict, e, hasattr, list, message, result, revision, self, session, sorted, str, x
E:\zeta-monorepo\apps\backend\config\logging.py: ImportError, adapter, bool, console_logging, details, dict, dsn, duration, event_type, file_logging, float, func_name, hasattr, int, kwargs, log_entry, log_level, log_to_console, log_to_file, name, record, self, str, super, user_id
E:\zeta-monorepo\apps\backend\config\ml_config.py: AttributeError, bool, dict, float, getattr, int, isinstance, list, metric, name, pattern, self, str, v
E:\zeta-monorepo\apps\backend\config\models.py: ValueError, bool, dict, float, int, len, list, overrides, property, self, str, v
E:\zeta-monorepo\apps\backend\config\redis.py: bool, host, int, isinstance, list, node, str, v
E:\zeta-monorepo\apps\backend\config\security.py: bool, float, int, list, str
E:\zeta-monorepo\apps\backend\config\settings.py: bool, int, list, str
E:\zeta-monorepo\apps\backend\config\storage_config.py: bool, ext, int, isinstance, list, size, str, v
E:\zeta-monorepo\apps\backend\config\unified_settings.py: ValueError, bool, float, int, list, property, self, str, v
E:\zeta-monorepo\apps\backend\config\settings\base.py: AttributeError, ValueError, bool, classmethod, cls, dict, getattr, int, list, name, self, str, v
E:\zeta-monorepo\apps\backend\config\settings\development.py: bool, list, str
E:\zeta-monorepo\apps\backend\config\settings\loader.py: ENV_VAR, PROFILE_IMPL, TypeError, class_name, dict, getattr, isinstance, issubclass, module_name, str, type, value
E:\zeta-monorepo\apps\backend\config\settings\production.py: bool, float, int, list, str
E:\zeta-monorepo\apps\backend\config\settings\staging.py: bool, int, list, str
E:\zeta-monorepo\apps\backend\config\settings\testing.py: bool, int, list, str
E:\zeta-monorepo\apps\backend\core\base.py: Exception, NotImplementedError, ValueError, aggregate_id, bool, candidate, correlation_id, created_at, created_by, details, e, event_type, hash, id, int, isinstance, left, metadata, other, repository, right, rule_name, self, service, spec, str, super, type, updated_at, updated_by, user_id, version
E:\zeta-monorepo\apps\backend\core\chunking.py: Exception, ValueError, chunk_size, e, int, len, next_sentence, overlap, p, para, s, sentence, str, target, text
E:\zeta-monorepo\apps\backend\core\container.py: Exception, RuntimeError, all, bool, dict, e, factory, isinstance, k, len, name, self, status, str, sum, v, validation_results
E:\zeta-monorepo\apps\backend\core\pipeline.py: ValueError, dict, event, int, isinstance, len, list, maxsize, q, run_id, str
E:\zeta-monorepo\apps\backend\core\types.py: ValueError, bool, classmethod, cls, data, e, error, float, int, isinstance, page, property, self, size, sort_by, sort_order, str, success, total
E:\zeta-monorepo\apps\backend\core\__init__.py: Exception, ImportError, RuntimeError, ValueError, config_override, dict, e, isinstance, logger, str
E:\zeta-monorepo\apps\backend\core\adapters\inmemory_alerts.py: ValueError, context, dict, int, isinstance, len, level, message, self, str, sum
E:\zeta-monorepo\apps\backend\core\adapters\__init__.py: AttributeError, dict, name, str
E:\zeta-monorepo\apps\backend\core\adapters\tests\test_inmemory_alerts.py: AttributeError, ValueError, len, level, str
E:\zeta-monorepo\apps\backend\core\agents\orchestrator.py: Exception, ValueError, agents, all, bool, dict, e, enumerate, float, i, int, isinstance, len, list, name, orchestrator, outbox_service, print, property, r, self, str, sum, t, task, task_type, team_id
E:\zeta-monorepo\apps\backend\core\application\event_bus.py: Exception, TypeError, ValueError, callable, dict, e, enumerate, event, events, handler, i, int, isinstance, len, list, result, self, str
E:\zeta-monorepo\apps\backend\core\application\outbox_hardened.py: Exception, TimeoutError, ValueError, base_backoff, batch_size, callable, concurrency, dict, e, error, event_bus, events, float, getattr, hasattr, int, interval_sec, isinstance, jitter, key, limit, list, lock_timeout_minutes, max_attempts, message_id, min, row, self, session, session_factory, shard, stale_time, str, worker_id
E:\zeta-monorepo\apps\backend\core\application\upcaster.py: Exception, dict, e, event_type, evt_type, fn, from_version, int, len, list, max, payload, result, str, tuple, version, versions
E:\zeta-monorepo\apps\backend\core\application\outbox\batch_processor.py: BaseException, Exception, TimeoutError, batch_size, bool, circuit_failure_threshold, circuit_recovery_timeout, dict, e, enable_circuit_breaker, enable_metrics, float, flush_interval, hash, int, item, kwargs, len, list, max_concurrent_batches, p, partition_count, partition_items, partitioned_items, pid, processing_time, processor_fn, range, self, set, str, t, type
E:\zeta-monorepo\apps\backend\core\application\outbox\config.py: ValueError, bool, classmethod, cls, config_key, data, dict, env_var, float, int, k, prefix, self, str, v
E:\zeta-monorepo\apps\backend\core\application\outbox\integration.py: Exception, RuntimeError, app_event, app_repo, app_row, attempt, bool, core_event, core_repo, dict, e, error, event_bus, hasattr, int, isinstance, limit, list, message_id, repository, row, self, shard, staticmethod, str, use_app_for_writes, use_core_for_reads, worker_count, worker_id
E:\zeta-monorepo\apps\backend\core\application\outbox\manager.py: Exception, RuntimeError, TimeoutError, d, dict, dispatcher_config, e, event, event_bus, events, hasattr, i, len, list, outbox_config, partitions, range, repository, self, str, sum
E:\zeta-monorepo\apps\backend\core\application\outbox\publisher.py: BaseException, Exception, batch_size, dict, e, event, event_bus, events, field, float, flush_interval, getattr, hasattr, hash, int, isinstance, len, list, outbox_repo, self, serializer, str, type
E:\zeta-monorepo\apps\backend\core\application\outbox\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\async_templates\async_service.py: dict, item, list, self
E:\zeta-monorepo\apps\backend\core\auth\base.py: DeprecationWarning, Exception, algorithm, attempt, bool, cache, client_id, client_secret, config, credentials, dict, e, int, key, len, list, max_attempts, permission, provider, role, secret_key, self, session_timeout, str, super, token, window_seconds
E:\zeta-monorepo\apps\backend\core\caching\decorators.py: args, func, int, kwargs, result, str
E:\zeta-monorepo\apps\backend\core\common\base_classes.py: Exception, RuntimeError, ValueError, bool, default, dependencies, e, getattr, isinstance, list, name, property, self, str, type
E:\zeta-monorepo\apps\backend\core\common\exceptions.py: Exception, ValueError, code, details, int, isinstance, level, message, self, str, super
E:\zeta-monorepo\apps\backend\core\cost\guard.py: ValueError, api, api_costs, bool, bucket_size, cost, default_bucket_size, default_refill_rate, dict, enforce_min_interval, float, int, isinstance, last_ts, len, min, min_interval, refill_rate, self, str, sum, tok, user
E:\zeta-monorepo\apps\backend\core\cost\__init__.py: Exception, ValueError, api, e, float, isinstance, str, user
E:\zeta-monorepo\apps\backend\core\distillation\enhanced_service.py: Exception, auto_train, bool, confidence_marker, config, cycle_interval, data_item, data_items, datapoints, dict, dp, e, enumerate, float, i, input_text, inputs, int, isinstance, item, len, line, list, marker, model_spec, reasoning_marker, response_marker, result, safety_level, self, str, task_context, teacher_response, training_result, tuple
E:\zeta-monorepo\apps\backend\core\domain\domain_events.py: aggregate, aggregate_id, classmethod, cls, data, dict, event_type, int, list, payload, print, str, super, type
E:\zeta-monorepo\apps\backend\core\domain\events.py: EVENT_TYPE_REGISTRY, ValueError, bool, dict, event_type, float, int, list, str, type
E:\zeta-monorepo\apps\backend\core\domain\mixins.py: bool, int, list, self, set, str, tag, tags, user_id
E:\zeta-monorepo\apps\backend\core\domain\shared_value_objects.py: ValueError, self, str, v
E:\zeta-monorepo\apps\backend\core\domain\value_objects.py: Exception, ValueError, classmethod, cls, code, field, iso_string, message, rule, self, str, super, v
E:\zeta-monorepo\apps\backend\core\domain\_base_model.py: ValueError, int, self, str
E:\zeta-monorepo\apps\backend\core\domain\agents\team.py: dict, str
E:\zeta-monorepo\apps\backend\core\domain\aggregates\agent_aggregate.py: cap, config_updates, dataset_id, dict, getattr, list, params, reason, self, str
E:\zeta-monorepo\apps\backend\core\domain\aggregates\agent_example.py: ValueError, agent_id, classmethod, cls, list, name, self, str, tag, tags
E:\zeta-monorepo\apps\backend\core\domain\aggregates\base.py: ValueError, bool, condition, event, int, list, message, self, str
E:\zeta-monorepo\apps\backend\core\domain\aggregates\chat_aggregate.py: agent_id, content, dict, getattr, len, list, m, memory_ids, messages, meta, reason, self, set, str, user_id
E:\zeta-monorepo\apps\backend\core\domain\aggregates\collab_room_aggregate.py: bool, dict, getattr, owner_user_id, participants, role, self, str, title, user_id
E:\zeta-monorepo\apps\backend\core\domain\aggregates\federated_round_aggregate.py: artifact_ref, client_id, dict, getattr, len, list, metrics, participants, round_id, self, str, strategy, subs
E:\zeta-monorepo\apps\backend\core\domain\aggregates\memory_aggregate.py: chat_id, content, dict, f, getattr, len, list, metadata, metadata_updates, model_name, namespace, reason, self, str
E:\zeta-monorepo\apps\backend\core\domain\aggregates\model_aggregate.py: dict, float, getattr, list, metrics, name, reason, registry_uri, self, stage, str, to_version, version
E:\zeta-monorepo\apps\backend\core\domain\aggregates\workflow_aggregate.py: ValueError, all, context, dict, getattr, list, metadata, name, outputs, reason, s, self, step_id, str
E:\zeta-monorepo\apps\backend\core\domain\entities\agent.py: ValueError, bool, cap, capabilities, capability, caps, classmethod, config, dict, int, reason, self, set, sorted, str, tag, tags, tuple, update_data, v
E:\zeta-monorepo\apps\backend\core\domain\entities\agent_v2.py: ValueError, bool, cap, capabilities, capability, caps, classmethod, config, dict, int, isinstance, reason, self, set, sorted, str, tag, tags, tuple, update_data, user_id, v
E:\zeta-monorepo\apps\backend\core\domain\entities\audit.py: dict, str
E:\zeta-monorepo\apps\backend\core\domain\entities\base.py: bool, entity_id, hash, int, isinstance, object, other, property, self, str
E:\zeta-monorepo\apps\backend\core\domain\entities\business_rule.py: Exception, action_expression, ast, bool, classmethod, cls, condition_expression, context, description, dict, float, list, name, priority, property, rule_type, self, str, tags
E:\zeta-monorepo\apps\backend\core\domain\entities\chat.py: dict, int, str
E:\zeta-monorepo\apps\backend\core\domain\entities\chunk.py: TypeError, ValueError, dict, float, id, int, isinstance, len, max_chars, object, property, self, str, super
E:\zeta-monorepo\apps\backend\core\domain\entities\config.py: ValueError, classmethod, dict, self, str, v
E:\zeta-monorepo\apps\backend\core\domain\entities\dataset_item.py: ValueError, dict, self, str
E:\zeta-monorepo\apps\backend\core\domain\entities\Document.py: bool, dict, float, int, list, self, str
E:\zeta-monorepo\apps\backend\core\domain\entities\document_clean.py: ValueError, bool, chunks, classmethod, content, data, dict, embeddings, file_size, file_type, float, int, len, list, self, staticmethod, str, super, title, v
E:\zeta-monorepo\apps\backend\core\domain\entities\file.py: ValueError, classmethod, int, self, str, v
E:\zeta-monorepo\apps\backend\core\domain\entities\learning.py: ValueError, classmethod, float, info, str, t, v
E:\zeta-monorepo\apps\backend\core\domain\entities\memory.py: ValueError, bool, case_sensitive, category, classmethod, clear_embedding, default, dict, embedding, enumerate, float, i, importance, int, isinstance, key, len, metadata, self, sorted, str, text, threshold, tuple, v, val, value
E:\zeta-monorepo\apps\backend\core\domain\entities\memory_entry.py: ValueError, classmethod, dict, isinstance, list, new_content, new_tags, self, set, str, tag, v
E:\zeta-monorepo\apps\backend\core\domain\entities\metrics.py: ValueError, classmethod, dict, float, str, v
E:\zeta-monorepo\apps\backend\core\domain\entities\notification.py: self, str
E:\zeta-monorepo\apps\backend\core\domain\entities\permission.py: action, actions, bool, classmethod, cls, condition_key, condition_value, conditions, context, description, dict, name, parent_roles, permission_id, permissions, resource_type, role_id, self, set, str
E:\zeta-monorepo\apps\backend\core\domain\entities\plan.py: ValueError, bool, classmethod, dict, enumerate, float, i, index, int, len, list, range, reason, s, self, set, sorted, step, str, sum, tuple, v
E:\zeta-monorepo\apps\backend\core\domain\entities\session.py: ValueError, bool, classmethod, dict, hours, int, new_context, self, str, v
E:\zeta-monorepo\apps\backend\core\domain\entities\training_job.py: ValueError, float, message, new_progress, self, str
E:\zeta-monorepo\apps\backend\core\domain\entities\user.py: any, bool, list, role, self, str, x
E:\zeta-monorepo\apps\backend\core\domain\entities\vector_document.py: classmethod, cls, content, dict, embeddings, float, int, len, metadata, other_vector, property, self, str, vector_embeddings
E:\zeta-monorepo\apps\backend\core\domain\entities\workflow.py: ValueError, dict, e, graph, int, len, list, n, nid, order, self, str, v
E:\zeta-monorepo\apps\backend\core\domain\entities\Agent\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\domain\entities\Chat\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\domain\entities\Memory\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\domain\entities\Plan\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\domain\entities\User\user.py: bool, property, self, str
E:\zeta-monorepo\apps\backend\core\domain\events\agent_events.py: agent_id, list, name, str, tags
E:\zeta-monorepo\apps\backend\core\domain\events\base.py: KeyError, TypeError, ValueError, causation_id, cls, correlation_id, dict, ev, hasattr, int, isinstance, obj, producer, str, tenant_id, type, version
E:\zeta-monorepo\apps\backend\core\domain\events\chat_events.py: dict, str
E:\zeta-monorepo\apps\backend\core\domain\events\learning_events.py: bool, dict, float, int, str
E:\zeta-monorepo\apps\backend\core\domain\events\memory_events.py: dict, float, list, str
E:\zeta-monorepo\apps\backend\core\domain\events\rule_events.py: Exception, bool, context, dict, error, execution_time_ms, float, input_data, result, rule_id, str, type
E:\zeta-monorepo\apps\backend\core\domain\events\rule_events_old.py: Exception, bool, context, dict, error, execution_time_ms, float, input_data, result, rule_id, staticmethod, str, type
E:\zeta-monorepo\apps\backend\core\domain\events\system_events.py: dict, float, str
E:\zeta-monorepo\apps\backend\core\domain\events\types.py: dict, int, list, str
E:\zeta-monorepo\apps\backend\core\domain\ports\asr.py: bytes, float, list, str
E:\zeta-monorepo\apps\backend\core\domain\ports\event_store.py: aggregate_id, dict, event_id, event_type, int, list, payload, self, str, timestamp
E:\zeta-monorepo\apps\backend\core\domain\ports\external_services.py: dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\domain\ports\repositories.py: Exception, actual_version, entity_id, expected_version, int, self, str, super
E:\zeta-monorepo\apps\backend\core\domain\services\advanced_memory.py: Exception, chunk, chunker, dict, e, embedder, enumerate, filter_metadata, getattr, hasattr, i, int, len, list, memory, model, query_text, range, str, top_k, vectorstore
E:\zeta-monorepo\apps\backend\core\domain\specifications\agent_specifications.py: agent, bool, list, object, required_capabilities, self, status, str
E:\zeta-monorepo\apps\backend\core\domain\specifications\memory_specifications.py: allow_permanent, bool, candidate, field, float, getattr, hasattr, int, isinstance, len, list, max_access_frequency, max_length, max_score, max_size_bytes, min_length, min_score, self, set, str, valid_types
E:\zeta-monorepo\apps\backend\core\domain\specifications\security_specifications.py: all, allowed_ips, any, bool, c, callable, candidate, dt, getattr, hasattr, int, isinstance, len, list, max_requests, max_session_age, max_token_age, min_length, p, perm, req, require_digits, require_lowercase, require_special, require_uppercase, required_permissions, self, str, time_window
E:\zeta-monorepo\apps\backend\core\domain\value_objects\automation.py: ValueError, action, all, bbox_hint, bool, classmethod, cls, confidence, confidence_threshold, context, coords, created_at, description, dict, error_details, estimated_duration, estimated_duration_seconds, execution_time_ms, float, globals, goal, id, int, len, list, max, message, object, parameters, plan, plan_id, point, property, r, recommended_action, result, safety_level, safety_mode, self, session_id, sleep_ms, staticmethod, step, step_id, steps, str, sum, target, target_image, target_text, text, tuple, violations, warnings
E:\zeta-monorepo\apps\backend\core\domain\value_objects\file_metadata.py: ValueError, bool, int, len, property, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\identity.py: hash, int, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\learning.py: bool, float, int, max, property, self, str, threshold
E:\zeta-monorepo\apps\backend\core\domain\value_objects\performance_metrics.py: ValueError, dict, float, latency_ms, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\plan_step.py: ValueError, all, bool, classmethod, cls, completed_step_ids, data, dep_id, dict, error, float, int, kwargs, list, object, reason, result, self, set, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\security_context.py: ValueError, any, bool, default, dict, key, s, scope, self, str, tuple
E:\zeta-monorepo\apps\backend\core\domain\value_objects\training_types.py: str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\vector_query.py: ValueError, bool, dict, float, int, len, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\workflow_node.py: ValueError, bool, dict, int, len, list, outputs, self, status, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\__init__.py: ImportError
E:\zeta-monorepo\apps\backend\core\domain\value_objects\agent\agent_config.py: ValueError, dict, float, frequency_penalty, int, max_tokens, model, presence_penalty, self, str, temperature, top_p
E:\zeta-monorepo\apps\backend\core\domain\value_objects\agent\agent_lifecycle.py: float, int, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\agent\agent_lifecycle_status.py: bool, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\agent\agent_status.py: float, int, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\memory\conversation_context.py: bool, default, dict, key, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\memory\memory_context.py: bool, default, dict, key, self, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\memory\memory_embedding.py: ValueError, a, abs, b, bool, classmethod, cls, data, dict, enumerate, float, i, int, isinstance, len, list, metadata, model, object, other, self, str, sum, tolerance, tuple, val, vector, x, zip
E:\zeta-monorepo\apps\backend\core\domain\value_objects\user\auth.py: int, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\user\permissions.py: ROLE_PERMISSIONS, ROLE_QUOTAS, all, any, bool, current_agents, current_chats_today, current_files_today, current_messages, current_storage_mb, dict, file_size_mb, float, int, message_length, p, permission, permissions, role, self, set, str
E:\zeta-monorepo\apps\backend\core\domain\value_objects\user\user_preferences.py: bool, default, dict, float, getattr, hasattr, int, key, notification_type, self, setattr, str, value
E:\zeta-monorepo\apps\backend\core\exceptions\auth_exceptions.py: Exception, action, dict, error_code, int, kwargs, limit, metadata, resource, self, str, super, user_id, window
E:\zeta-monorepo\apps\backend\core\exceptions\business_exceptions.py: Exception, agent_id, context, current, details, dict, entity, error_code, field, identifier, int, job_id, kwargs, limit, list, message_id, model_name, operation, plan_id, reason, resource, rule, self, service, session_id, severity, step, str, suggestions, super, value, workflow_id
E:\zeta-monorepo\apps\backend\core\exceptions\context.py: Exception, context_data, dict, exc, hasattr, isinstance, list, metadata, operation, self, str
E:\zeta-monorepo\apps\backend\core\exceptions\handlers.py: Exception, app, exc, getattr, handler, isinstance, request, self, user_agent
E:\zeta-monorepo\apps\backend\core\exceptions\repository_exceptions.py: Exception, actual, bool, cache_type, column, constraint, database, details, dict, entity, error_code, expected, field, identifier, int, key, kwargs, operation, parameters, pool_size, query, reason, retryable, self, str, super, table, timeout, value, version
E:\zeta-monorepo\apps\backend\core\exceptions\retry.py: RuntimeError, args, bool, exc, expected_exception, failure_threshold, float, func, getattr, int, kwargs, min, recovery_timeout, result, self, str, type
E:\zeta-monorepo\apps\backend\core\exceptions\telemetry.py: Exception, bool, callable, context, dict, exc, getattr, hasattr, result, self, span, str, type
E:\zeta-monorepo\apps\backend\core\implementations\mock_notification.py: Exception, bool, delivery_id, dict, email, f, getattr, int, list, message_id, phone, recipients, str, url, webhook_id
E:\zeta-monorepo\apps\backend\core\infrastructure\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\infrastructure\db\models.py: dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\infrastructure\db\sqlalchemy_base.py: db_url, str
E:\zeta-monorepo\apps\backend\core\infrastructure\db\__init__.py: Exception, RuntimeError, ValueError, config, dict, e, getattr, int, isinstance, level, name, str
E:\zeta-monorepo\apps\backend\core\infrastructure\events\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\infrastructure\llm_providers\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\infrastructure\messaging\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\infrastructure\repositories\uow_sql.py: exc, self, session_factory
E:\zeta-monorepo\apps\backend\core\infrastructure\search\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\infrastructure\storage\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\ingest\safety_filters.py: Exception, bool, c, category, content, dict, e, enabled, enumerate, error_result, f, filter_instance, filter_name, float, i, int, keywords, kw, len, list, max, max_length, min, min_length, name, pattern, patterns, pii_type, result, safety_level, self, set, str, sum, super, tuple, vuln_type
E:\zeta-monorepo\apps\backend\core\ingest\__init__.py: Exception, RuntimeError, ValueError, config, dict, e, getattr, int, isinstance, level, name, str
E:\zeta-monorepo\apps\backend\core\interfaces\advanced_alerts.py: list, str
E:\zeta-monorepo\apps\backend\core\interfaces\alerts.py: str
E:\zeta-monorepo\apps\backend\core\interfaces\analytics_interfaces.py: bool, dict, float, int, list, str, tuple
E:\zeta-monorepo\apps\backend\core\interfaces\automation.py: bool, str
E:\zeta-monorepo\apps\backend\core\interfaces\backup.py: str
E:\zeta-monorepo\apps\backend\core\interfaces\cache.py: bool, int, str
E:\zeta-monorepo\apps\backend\core\interfaces\documentation.py: dict, str
E:\zeta-monorepo\apps\backend\core\interfaces\external_services.py: bool, dict, float, int, list, str, tuple
E:\zeta-monorepo\apps\backend\core\interfaces\feature_toggles.py: bool, str
E:\zeta-monorepo\apps\backend\core\interfaces\federated.py: float, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\input_control.py: bool, float, int, str
E:\zeta-monorepo\apps\backend\core\interfaces\llm_provider.py: dict, float, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\memory.py: bool, dict, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\memory_backend.py: ValueError, bool, classmethod, count, data, dict, enumerate, error, i, int, isinstance, len, list, metadata, namespace, operation, record, records, status, str, v
E:\zeta-monorepo\apps\backend\core\interfaces\metrics.py: dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\mlops.py: dict, str
E:\zeta-monorepo\apps\backend\core\interfaces\ml_interfaces.py: bool, dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\notification_interfaces.py: bool, dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\observability.py: float, int, str
E:\zeta-monorepo\apps\backend\core\interfaces\perception.py: dict, float, int, list, str, tuple
E:\zeta-monorepo\apps\backend\core\interfaces\security.py: dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\security_ai.py: bytes, dict, float, str
E:\zeta-monorepo\apps\backend\core\interfaces\security_interfaces.py: bool, bytes, dict, float, int, list, str, tuple
E:\zeta-monorepo\apps\backend\core\interfaces\services.py: dict, float, int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\storage_interfaces.py: bool, bytes, dict, float, int, list, str, tuple
E:\zeta-monorepo\apps\backend\core\interfaces\testing.py: dict, list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\agent.py: bool, list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\agent_repository.py: list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\analytics_repository.py: dict, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\chat.py: bool, int, list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\chat_repository.py: list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\document_repository.py: int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\memory.py: bool, list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\memory_repository.py: int, list, str
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\message_repository.py: list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\plan.py: list, str
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\training.py: bool, float, list
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\user.py: bool, str
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\user_repository.py: bool, str
E:\zeta-monorepo\apps\backend\core\interfaces\repositories\vector_repository.py: bool, dict, int, list
E:\zeta-monorepo\apps\backend\core\interfaces\services\ai_service.py: dict, str
E:\zeta-monorepo\apps\backend\core\interfaces\services\notification.py: str
E:\zeta-monorepo\apps\backend\core\knowledge\graph_service.py: ValueError, any, bool, boost, concept, context, cost, current_id, dict, distance, e, edge, edge_types, end_id, entity_id, event, float, i, int, key, len, max_depth, max_distance, min, neighbor, neighbor_id, node_id, path, range, self, set, sorted, source, start_id, str, target, temporal_window_hours, term, v, value, x
E:\zeta-monorepo\apps\backend\core\kpis\cost_targets.py: int
E:\zeta-monorepo\apps\backend\core\kpis\__init__.py: Exception, RuntimeError, ValueError, config, dict, e, getattr, int, isinstance, level, name, str
E:\zeta-monorepo\apps\backend\core\learning\ml_integration.py: Exception, bool, dict, e, model_family, preset_eval, self, str
E:\zeta-monorepo\apps\backend\core\memory\advanced_service.py: Exception, NotImplementedError, access_freq, data_size_mb, dict, e, float, hash, int, k, key, len, list, max, namespace, p, round, self, str, strategy, sum
E:\zeta-monorepo\apps\backend\core\memory\cached_memory_service.py: backend, batch_size, bool, cache_size, cache_ttl, cached_result, dict, embedding_model, filters, getattr, hard, hasattr, ids, int, key, len, list, max_concurrent, namespace, records, self, str, target_model, top_k
E:\zeta-monorepo\apps\backend\core\memory\container.py: bool, classmethod, cls, dep, dict, int, len, self, str, sum, valid
E:\zeta-monorepo\apps\backend\core\memory\encrypted_memory_backend.py: Exception, a, b, bytes, conn, data, db, db_path, dict, e, embedding_dim, embedding_model, enc_content, enc_embedding, enc_metadata, encrypted_data, encryption_key, float, ids, int, len, list, namespace, range, record, record_id, records, row, self, str, sum, super, target_model, text, top_k, vec1, vec2, x, zip
E:\zeta-monorepo\apps\backend\core\memory\optimized_memory_system.py: ValueError, backend_type, batch_size, bool, cache_dir, db_config, dict, embedding_dim, encryption_key, filters, hasattr, ids, int, isinstance, len, list, namespace, records, request, self, str, target_model, top_k, use_bulk, use_cache, use_caching, use_encryption, use_streaming
E:\zeta-monorepo\apps\backend\core\memory\streaming_memory_handler.py: Exception, backend, batch_size, dict, e, filters, generator, i, ids, int, len, list, min, namespace, query, range, records, result_item, self, str, target_model, top_k
E:\zeta-monorepo\apps\backend\core\mlops\feature_service.py: chunks, embedder, float, list, self, str
E:\zeta-monorepo\apps\backend\core\mlops\manager_service.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\core\mlops\mlflow_adapter.py: Exception, RuntimeError, name, object, str, tags, tracking_uri, uri
E:\zeta-monorepo\apps\backend\core\mlops\model_registry.py: KeyError, dict, float, m, metadata, name, self, sorted, str, uri
E:\zeta-monorepo\apps\backend\core\mlops\rollback_service.py: bool, candidate_version, metrics_ok, name, previous_version, registry, self, str
E:\zeta-monorepo\apps\backend\core\mlops\service.py: dict, family, self, str
E:\zeta-monorepo\apps\backend\core\model_management\router.py: Exception, bool, data_sensitivity, dict, e, f, float, input_tokens, int, kwargs, len, list, m, max, model_config, model_id, model_spec, open, output_tokens, provider, s, self, str, task_type, tuple, x
E:\zeta-monorepo\apps\backend\core\model_management\router_guard.py: Exception, ValueError, dict, float, ip, req, self, str, subject, ua
E:\zeta-monorepo\apps\backend\core\multimodal\asr.py: ImportError, audio_path, model_size, result, self, str
E:\zeta-monorepo\apps\backend\core\multimodal\ocr.py: ImportError, conf, confidence_threshold, float, image_path, len, line, page, result, self, str, text
E:\zeta-monorepo\apps\backend\core\observability\logging.py: name, str
E:\zeta-monorepo\apps\backend\core\observability\metrics.py: Exception, self
E:\zeta-monorepo\apps\backend\core\observability\production_monitoring.py: Exception, ImportError, KeyError, TypeError, ValueError, alert_config, alert_name, app, attributes, bool, call_next, channel, channels, cpu, dict, disk, e, error, event_type, float, getattr, hasattr, int, isinstance, key, kwargs, list, logger, memory, message, metric, metric_path, metrics_collector, model, name, object, operation, port, print, rate, request, round, self, service_name, str, super, tokens, tracer, user_id
E:\zeta-monorepo\apps\backend\core\observability\tracing.py: Exception, str
E:\zeta-monorepo\apps\backend\core\optimization\fix_undefined_variables.py: Exception, SyntaxError, alias, arg, bool, dict, e, enumerate, error, file, file_path, func_node, hasattr, i, int, isinstance, item, len, list, node, print, root_path, self, set, sorted, str, subnode, target, undefined, var
E:\zeta-monorepo\apps\backend\core\optimization\memory_manager.py: Exception, ImportError, attr_name, bool, cache_obj, cache_object, dict, dir, e, factory_fn, float, generation, getattr, hasattr, int, len, list, name, operation_name, range, reason, round, self, str, sum
E:\zeta-monorepo\apps\backend\core\orchestrator\capability_resolver.py: Exception, any, auto_install, bool, dict, h, payload, str
E:\zeta-monorepo\apps\backend\core\outbox\handlers.py: Exception, dict, e, event, evt, handlers, job_result, len, print, result, store, str, type
E:\zeta-monorepo\apps\backend\core\outbox\idempotency.py: Exception, RuntimeError, ValueError, args, bool, callable, cfg, dict, e, event, fn, kwargs, message, result, self, store, str
E:\zeta-monorepo\apps\backend\core\outbox\metrics.py: active, age_seconds, attempt, bool, component, dict, dlq_sizes, duration, error_type, event_type, failure_reason, float, from_version, handler, healthy, idle, int, operation, partition, partitions, queue_sizes, size, str, to_version, waiting, worker_index
E:\zeta-monorepo\apps\backend\core\outbox\outbox_hardened.py: Exception, ImportError, NotImplementedError, ValueError, bool, config_overrides, dict, e, error, event, final_payload, final_version, float, handlers, i, int, list, min, num_workers, print, range, repo, self, sig, str, type
E:\zeta-monorepo\apps\backend\core\outbox\processed_store_redis.py: ImportError, bool, handler, int, key, self, str, ttl_sec, url
E:\zeta-monorepo\apps\backend\core\outbox\upcaster.py: Exception, ValueError, bool, current_version, default_value, dict, e, et, event_type, field, fn, from_version, int, len, list, new_field, new_version, old_field, payload, self, str, to_version, transform_fn, tuple
E:\zeta-monorepo\apps\backend\core\performance\advanced_caching.py: data_type, self, str
E:\zeta-monorepo\apps\backend\core\performance\dashboard_config.py: color, dict, enumerate, float, group_name, i, int, len, list, metric_groups, metric_name, panel, self, set, severity, str, threshold, thresholds, zip
E:\zeta-monorepo\apps\backend\core\performance\instrumentation.py: Exception, args, e, func, kwargs, metric_base, metrics, result, span, str, tracer
E:\zeta-monorepo\apps\backend\core\performance\optimizer.py: current_metrics, dict, list, name, self, str, strat
E:\zeta-monorepo\apps\backend\core\performance\smart_cache.py: Exception, ImportError, RuntimeError, args, dict, e, func, func_name, int, key, kwargs, len, list, result, self, sorted, str, sum, tuple
E:\zeta-monorepo\apps\backend\core\plugins\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\policies\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\ports\llm_port.py: bool, loaded, model_name, self, str
E:\zeta-monorepo\apps\backend\core\quality\auto_testing.py: Exception, dict, e, historical_results, int, len, list, max, max_iterations, min, r, result, round, self, str, sum
E:\zeta-monorepo\apps\backend\core\reasoning\engine.py: Exception, context, dict, e, float, goal, len, list, llm_client, result, s, self, step, str, tools
E:\zeta-monorepo\apps\backend\core\registry\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\resilience\patterns.py: Exception, TimeoutError, attempt, base_url, bool, cache_ttl, circuit_config, client, config, default_ttl, dict, e, float, func, int, key, method, name, result, self, str, tuple, url, use_cache, value
E:\zeta-monorepo\apps\backend\core\security\advanced_monitoring.py: acted, b, behavior, dict, float, int, list, min, self, str, window_sec
E:\zeta-monorepo\apps\backend\core\security\ai_permissions.py: AI_LEARNING_PERMISSIONS, ENHANCED_ROLE_PERMISSIONS, bool, dict, inherited_role, list, name, new_perms, perm, perm_name, permission, role, set, str
E:\zeta-monorepo\apps\backend\core\security\audit.py: allowed, audit_data, bool, context, created_by, dict, expires_at, grant_id, logger_name, permission_name, policy_name, reason, resource_id, self, str, user_id, violation_details
E:\zeta-monorepo\apps\backend\core\security\audit_policy.py: dict, str
E:\zeta-monorepo\apps\backend\core\security\content_safety.py: bool, len, list, p, patterns, reasons, self, str, text
E:\zeta-monorepo\apps\backend\core\security\context.py: bool, dict, int, list, self, str
E:\zeta-monorepo\apps\backend\core\security\decorators.py: Exception, action, action_name, any, args, bool, call_history, call_time, capture_args, capture_result, dict, e, float, int, isinstance, key, kwargs, len, list, max_calls, per_user, resource_id, resource_type, result, safe_result, sensitive, sensitivity, service_role, str, tenant_id, time_window, tuple, type, value
E:\zeta-monorepo\apps\backend\core\security\disaster_recovery.py: self, snapshot_id, str
E:\zeta-monorepo\apps\backend\core\security\filters.py: action, context, self, str, text
E:\zeta-monorepo\apps\backend\core\security\jwt_adapter.py: Exception, algorithms, any, audience, bool, client_ip, device_id, e, headers, int, issuer, jwt_secret, list, max, mfa_verified, p, r, role, self, set, str, ttl_hours, user_id
E:\zeta-monorepo\apps\backend\core\security\opa_adapter.py: BaseException, Exception, abac_ok, bool, client, ctx, dict, e, float, input_data, jit_ok, rbac_ok, result, self, str, timeout, type, url
E:\zeta-monorepo\apps\backend\core\security\permissions.py: DEFAULT_ROLE_PERMISSIONS, PERMISSIONS, action, bool, description, dict, domain, list, name, perm, permission_name, required_permission, requires_mfa, risk, risk_level, role_name, self, str, user_permissions
E:\zeta-monorepo\apps\backend\core\security\permission_manager.py: Exception, allowed, audit_enabled, bool, context, dict, e, getattr, jit_repo, permission_name, role, self, set, str, tuple
E:\zeta-monorepo\apps\backend\core\security\permission_service.py: Exception, PermissionError, acm, action, allowed, bool, dict, hasattr, pid, resource, scope, self, str, user
E:\zeta-monorepo\apps\backend\core\security\policy_engine.py: abac_result, any, bool, ctx, dict, int, jit_repo, list, permission, rate_limit_result, rbac_result, reason, requires_mfa, resource_id, risk_result, role, roles, safety_result, self, set, str, tuple, user_id, user_permissions
E:\zeta-monorepo\apps\backend\core\security\security_monitor.py: Exception, bandit_result, bool, code, dep, dict, e, float, int, isinstance, issue, len, list, output, pip_audit_result, pkg, print, result, set, str, sum, target_path, timeout, tool_name, tuple, v, vuln
E:\zeta-monorepo\apps\backend\core\security\threat_detection.py: abs, bool, dict, e, event, fail_threshold, float, int, ip, len, list, max_requests_per_minute, min, rate_limit_window, self, set, str, sum, ts, user_id, window_size
E:\zeta-monorepo\apps\backend\core\security\zero_trust_middleware.py: Exception, any, app, bool, call_next, dict, e, float, getattr, header, int, jwt_secret, kwargs, list, path, pattern, request, requests_per_window, self, str, super, window_seconds
E:\zeta-monorepo\apps\backend\core\security\authentication\bootstrap.py: Exception, ImportError, all, code, device_trust, e, email_manager, len, mfa_manager, print, range, set, sms_manager
E:\zeta-monorepo\apps\backend\core\security\authentication\device_trust_manager.py: ImportError, any, bool, config, device, dict, fingerprint, int, len, list, provided_fingerprint, reason, self, stored_hmac, str, sum, token, ttl
E:\zeta-monorepo\apps\backend\core\security\authentication\email_manager.py: ImportError, base_url, bool, email, is_token, isinstance, mailer, self, str, value
E:\zeta-monorepo\apps\backend\core\security\authentication\factory.py: ImportError, ValueError, backend, body, bool, enable_metrics, enable_tracing, print, redis_kwargs, redis_url, storage_backend, str, subject, to, tuple
E:\zeta-monorepo\apps\backend\core\security\authentication\fastapi_example.py: Exception, ValueError, auth_system, auth_token, background_tasks, bool, call_next, credentials, device, device_trust, dict, e, email_manager, exc, int, len, request, sms_manager, str, user_id
E:\zeta-monorepo\apps\backend\core\security\authentication\memory_storage.py: ImportError, RuntimeError, device, int, key, len, list, self, str, token, value
E:\zeta-monorepo\apps\backend\core\security\authentication\metrics.py: ImportError, args, bool, count, dict, enable_prometheus, enable_tracing, endpoint, event_type, float, func, hasattr, int, k, kwargs, latency, len, limiter_type, list, method, operation, self, severity, span, status, status_code, str, v, verification_type
E:\zeta-monorepo\apps\backend\core\security\authentication\mfa.py: Exception, additional_data, bool, bytes, config, d, device_fingerprint, device_name, dict, e, int, ip_address, key, kwargs, len, list, method, phone_number, provided_code, range, require_mfa_for_admin, self, sorted, stored_code, stored_hash, str, token, totp_issuer, tuple, user_agent, user_email, user_id, user_roles, value
E:\zeta-monorepo\apps\backend\core\security\authentication\mfa_config.py: ValueError, bool, int, len, self, str
E:\zeta-monorepo\apps\backend\core\security\authentication\mfa_manager.py: Exception, ImportError, attempt, bool, config, device_fingerprint, device_trust, dict, e, int, len, list, phone, rate_store, self, span, str, sum, user_id
E:\zeta-monorepo\apps\backend\core\security\authentication\rate_limiter.py: Exception, ImportError, bool, dict, hasattr, identifier, int, max_requests, old_count, pipe, redis, self, store, str, ttl, tuple, window_seconds
E:\zeta-monorepo\apps\backend\core\security\authentication\redis_storage.py: device, dict, int, isinstance, redis, self, str, token, value
E:\zeta-monorepo\apps\backend\core\security\authentication\security_audit.py: Exception, SyntaxError, any, auth_directory, bool, code, description, directory, e, enumerate, filename, func, getattr, hasattr, i, int, isinstance, issue, keyword, len, line, node, pattern, py_file, secret_word, self, str, target
E:\zeta-monorepo\apps\backend\core\security\authentication\sms_manager.py: ImportError, bool, isinstance, phone_number, self, staticmethod, str, submitted
E:\zeta-monorepo\apps\backend\core\security\authentication\storage.py: int, str
E:\zeta-monorepo\apps\backend\core\security\authentication\test_authentication.py: ValueError, all, device_trust, email_manager, hasattr, int, len, mfa_manager, n, range, set, sms1, sms2, sms_manager
E:\zeta-monorepo\apps\backend\core\security\authorization\rbac.py: action, assigned_by, assignment, bool, conditions, d, description, dict, display_name, end_time, enumerate, expires_at, include_expired, kwargs, len, list, name, organization_id, p, parent_role_id, permission_id, permission_manager, project_id, resource_id, resource_owner_id, resource_type, role_id, scope, self, set, start_time, str, user_id
E:\zeta-monorepo\apps\backend\core\security\compliance\compliance_service.py: ValueError, a, affected_systems, assessor, bool, category, category_findings_list, control_id, description, dict, due_date, evidence, f, finding_id, finding_text, findings, float, format_type, framework, generated_by, int, kwargs, len, list, owner, period_end, period_start, remediation_plan, report_type, requirements, resolution_notes, resolved_by, risk_description, round, score, self, severity, status, str, sum, title
E:\zeta-monorepo\apps\backend\core\security\encryption\field_encryption.py: Exception, ValueError, algorithm, bool, bytes, config, data, data_b64, data_dict, dict, e, encrypted_fields, end_time, error_message, field_name, int, isinstance, key_info, key_rotation_enabled, kwargs, list, locals, master_key, new_purpose, operation_type, password, purpose, result, self, start_time, str, success, tuple, user_id
E:\zeta-monorepo\apps\backend\core\security\hardening\input_validation.py: Exception, TypeError, ValueError, any, bool, code, dict, e, err, expiry, field, field_name, float, i, int, isinstance, kwargs, len, list, message, raw_input, required, result, sanitization_type, sanitization_types, secret_key, self, session_id, severity, start_time, str, super, threat_type, threat_types, validation_type
E:\zeta-monorepo\apps\backend\core\security\monitoring\security_monitor.py: Exception, a, abs, alert_id, bool, counter, description, dict, e, end_time, float, handler, int, isinstance, kwargs, len, limit, list, m, max_metrics_history, metric_name, name, print, r, rule, rule_id, self, severity, source, start_time, str, tags, threat_type, threshold_type, timestamp, title, unresolved_only, user_id, value
E:\zeta-monorepo\apps\backend\core\security\policies\base.py: bool, dict, str
E:\zeta-monorepo\apps\backend\core\security\policies\content_safety.py: bool, bytes, content, dict, domain, enabled, enumerate, f, filter_name, float, i, isinstance, len, list, min, name, pattern, profanity_words, self, severity_threshold, str, sum, super, tld, tuple, violation, word
E:\zeta-monorepo\apps\backend\core\security\policies\tool_policies.py: Exception, allowed_domains, allowed_extensions, allowed_models, allowed_paths, allowed_tables, any, bool, dict, enumerate, float, forbidden, forbidden_domains, forbidden_operations, forbidden_paths, i, int, len, list, max_file_size, max_request_size, max_requests_per_hour, max_results, name, other, p, policy, policy_name, priority, request, require_content_filter, require_https, require_review_above, require_where_clause, result, risk_thresholds, self, str, super, t, table, tuple
E:\zeta-monorepo\apps\backend\core\security\privacy\privacy_engine.py: Exception, any, blacklist_fields, data, dict, f, field, field_encryptor, isinstance, key, list, p, protected, self, set, sorted, str, value, whitelist_fields
E:\zeta-monorepo\apps\backend\core\security\session\session_service.py: any, attr1, attr2, bool, bot, config, current_device_data, device_data, dict, exclude_session, extend_lifetime, float, fp1, fp2, int, ip_address, isinstance, kwargs, len, list, min, mobile, reason, remember_me, secret_key, self, session, set, stored_fingerprint, str, tablet, user_agent, user_id, weight, x
E:\zeta-monorepo\apps\backend\core\security\zero_trust\policy.py: action, bool, env, float, int, len, list, max, min, path, reasons, required_actions, resource, str, subject
E:\zeta-monorepo\apps\backend\core\security\zero_trust\risk.py: additional_signals, anomaly, bool, decay_hours, device_trust, float, hasattr, int, isinstance, kwargs, list, mfa, min, name, s, self, setattr, signal_name, stale, str, sum, timestamp, ts, tuple, user_id, val, value
E:\zeta-monorepo\apps\backend\core\self_awareness\health_monitor.py: Exception, TimeoutError, bool, coro, default, dict, e, float, int, interval_seconds, len, limit, list, metrics_health, print, r, repo_health, restart_callback, self, str, sum, thresholds, timeout, ws_health
E:\zeta-monorepo\apps\backend\core\self_improvement\auto_optimizer.py: Exception, apply_callback, dict, e, float, initial_knobs, int, interval_s, limit, list, max, metrics_adapter, min, print, result, self, str, tuple
E:\zeta-monorepo\apps\backend\core\self_improvement\auto_updater.py: Exception, FileNotFoundError, TimeoutError, ValueError, bool, ch, changes, cmd, content, dict, diffs, dst, e, e2, env, float, gates, int, list, message, patch, path, qg, repo, root, runner, self, snapshot, src, staticmethod, stderr_b, stdout_b, str, timeout_s
E:\zeta-monorepo\apps\backend\core\self_improvement\auto_updater_v2.py: ValueError, any, bool, ch, dict, g, generator, goal, history_path, i, int, iterations, len, list, max_iters, msgs, p, pat, policy, range, self, set, str, tuple, updater, w
E:\zeta-monorepo\apps\backend\core\self_improvement\feature_rollout.py: bool, ctx, d, dict, engine, env, f, float, int, name, now, org_id, s, self, set, str, user_id, user_key
E:\zeta-monorepo\apps\backend\core\self_improvement\secure_updater.py: Exception, ImportError, RuntimeError, any, bool, bytes, channel, cmd, dict, e, len, list, manifest_json, note, post_commands, req, requirements, sig_b64, signature_b64, str, version
E:\zeta-monorepo\apps\backend\core\services\agent_orchestrator.py: RuntimeError
E:\zeta-monorepo\apps\backend\core\services\agent_query_service.py: Exception, a, agent_repo, bool, dict, generic_repo, hasattr, int, len, limit, max, name, page_num, seen, self, st, staticmethod, str, total
E:\zeta-monorepo\apps\backend\core\services\agent_service_v2.py: agent_id, capabilities, configuration, dict, int, limit, name, name_query, new_caps, offset, owner_user_id, repo, repo_factory, self, set, str, tags, tuple, uow, uow_factory
E:\zeta-monorepo\apps\backend\core\services\ai_assistant.py: ValueError, bool, capabilities, context, dict, len, list, message, name, role, self, str, updates, user_id
E:\zeta-monorepo\apps\backend\core\services\analytics_service.py: Exception, activities, activity, agent_counts, agent_id, count, counts, created_by, daily_counts, dashboard_id, date, dict, dt, durations, e, end_date, end_time, ev, event_counts, float, groups, ingested, int, isinstance, item, k, kv, last_jobs, len, limit, list, m, max, metadata, offset, order, q, result, self, sorted, start_date, start_time, str, sum, tuple, type_counts, user_counts, user_id, v, x, zip
E:\zeta-monorepo\apps\backend\core\services\assistants_service.py: a, bool, change_summary, created_by, data, days, dict, int, isinstance, key, len, list, next, search_params, self, soft_delete, sorted, str, v, version, version_id
E:\zeta-monorepo\apps\backend\core\services\audit_service.py: Exception, ValueError, a, action_counts, actions, bool, details, dict, e, enable_real_time_alerts, end_time, entry, event, filtered_events, filtered_logs, float, format_type, int, ip_address, len, level, levels, limit, list, log, login_times, lvl, max, max_log_size_mb, offset, resource_id, retention_days, self, severity, standard, start_time, str, t, user_agent, user_id, x
E:\zeta-monorepo\apps\backend\core\services\automation_service.py: Exception, RuntimeError, bool, config, e, executor, id, input_controller, len, ocr_engine, planner, safety_engine, safety_result, screen_perception, screenshot_context, self, step, str, task_description
E:\zeta-monorepo\apps\backend\core\services\automation_steps.py: Exception, bool, dict, e, enumerate, execution_id, f, float, idx, int, k, len, list, min, r, rec, records, results, self, status, step, steps, str, sum, traj_records, trajectory_dir, v
E:\zeta-monorepo\apps\backend\core\services\backup_service.py: Exception, RuntimeError, b, backup, backup_directory, backup_file, backup_schedule_hours, backup_type, bool, compression_enabled, description, dict, e, f, hasattr, int, len, limit, list, max, max_concurrent_backups, open, retention_days, self, set, sorted, str, t, target_name, targets, x
E:\zeta-monorepo\apps\backend\core\services\caching_service.py: Exception, bool, bytes, cache_level, compressed_value, default, default_ttl, dict, disk_cache_size_mb, e, enable_compression, enable_distributed, fetch_function, float, frequency, int, isinstance, key, len, limit, list, memory_cache_size, oldest_key, promote_to_memory, round, self, str, t, x
E:\zeta-monorepo\apps\backend\core\services\chat_runtime.py: Exception, args, chunk, impl, kwargs, metrics, object, self, str
E:\zeta-monorepo\apps\backend\core\services\chunking.py: Exception, chunks, encoding_name, int, len, list, max, max_tokens, name, overlap, self, str, text
E:\zeta-monorepo\apps\backend\core\services\config.py: bool, classmethod, cls, float, int, str
E:\zeta-monorepo\apps\backend\core\services\context_planner.py: a, b, dict, float, int, len, list, max, p, per_doc, picked, r, rows, set, sorted, str
E:\zeta-monorepo\apps\backend\core\services\di.py: KeyError, bool, callable, dict, name, provider_func, self, str
E:\zeta-monorepo\apps\backend\core\services\enhanced_asr_service.py: Exception, ImportError, RuntimeError, audio_chunks, audio_file, audio_paths, bool, bytes, chunk, config, correct, dict, e, enumerate, float, getattr, i, info, int, isinstance, len, list, max_concurrent, model_path, open, openai_api_key, path, result, s, segment, segments, self, str, tmp_file, use_local, wrong
E:\zeta-monorepo\apps\backend\core\services\enhanced_event_bus_service.py: Exception, ImportError, ValueError, bool, callback, correlation_id, data, details, dict, e, end_time, error, event_type, event_types, expected_value, fields, float, handler, hasattr, int, key, len, limit, list, max, max_stream_length, metadata, metric_name, model_id, redis_url, self, session_id, source, str, stream_name, sum, tags, task_type, tuple, unit, user_id, value, websocket, ws
E:\zeta-monorepo\apps\backend\core\services\enhanced_knowledge_graph_service.py: Exception, ImportError, ValueError, a, any, b, bool, cached_result, confidence, dict, document_id, e, embedding_service, entity, entity_extractor, float, hash, int, isinstance, key, len, limit, list, max, max_hops, n, name, neighbor_id, nid, nt, query, query_text, range, redis_url, relation_types, result, rt, seed_node_ids, self, set, source_id, source_type, str, sum, target_id, text, tuple, value, vec1, vec2, weight, x, zip
E:\zeta-monorepo\apps\backend\core\services\enhanced_model_router.py: attempt, bool, cost, dict, float, int, latency_ms, len, list, m, max, max_retries, range, requirements, selection, self, sorted, str, success, tokens_processed, x
E:\zeta-monorepo\apps\backend\core\services\errors.py: Exception, code, details, dict, message, self, str, super
E:\zeta-monorepo\apps\backend\core\services\federated_service.py: Exception, abs, accepted_mimes, aggregator, apply_clip, apply_dp, bool, cleaned, clip_norm, content_type, dp_seed, enumerate, float, getattr, i, int, len, list, map, max, max_bytes, metrics_hook, min, payload_size_bytes, plan, privacy, sample_size, seed, self, sigma, signature, signature_required, str, sum, tuple, upd, updates, val, vector, x
E:\zeta-monorepo\apps\backend\core\services\final_init_report_service.py: Exception, bool, dict, int, len, list, pkg, print, str
E:\zeta-monorepo\apps\backend\core\services\health_monitor.py: Exception, bool, dict, e, float, int, max, min, once, round, self, str
E:\zeta-monorepo\apps\backend\core\services\learning_coordinator.py: Exception, agent, agent_id, agent_repository, any, bool, data, dict, e, enabled, experience_type, feedback, float, hasattr, int, len, list, memories, memory, memory_repository, metric_name, metrics, min, name, optimization_type, outcomes, p, priority, recommendation, self, session, session_type, setattr, start_time, str, strategy, strategy_type, sum, value
E:\zeta-monorepo\apps\backend\core\services\llm_service.py: Exception, RuntimeError, ValueError, code, e, hasattr, llm_port, model, self, str
E:\zeta-monorepo\apps\backend\core\services\memory_manager_service.py: Exception, ValueError, agent_id, bool, cl, clusters, config, content, dict, exc, float, hasattr, highlights, int, isinstance, len, limit, list, m, max, memory_id, memory_repository, memory_type, metadata, min, mm, out, points, query, s, selection, self, sorted, str, text, updates, ws, x
E:\zeta-monorepo\apps\backend\core\services\middleware.py: Exception, args, attempt, backoff, bool, cached_result, call_times, calls, dict, e, expected_exception, exponential, failure_threshold, float, fn, hasattr, hash, int, key_func, kwargs, labels, len, list, metric_counter, metric_histogram, name, period, range, result, seconds, self, sorted, str, t, timeout, times, ttl, type
E:\zeta-monorepo\apps\backend\core\services\moe_router.py: allowed, bool, context_len, dict, fast_ok, float, int, risk, set, str, strat, task
E:\zeta-monorepo\apps\backend\core\services\notification_service.py: Exception, RuntimeError, action_text, action_url, bool, channel, channels, dict, e, image_url, list, memory_repository, message, metadata, notification_type, priority, recipient_id, recipient_type, self, str, summary, title
E:\zeta-monorepo\apps\backend\core\services\outbox_worker.py: Exception, NotImplementedError, batch_size, bool, dict, e, event, float, handler, int, len, list, max_concurrent_events, min, poll_interval, self, set, status, str, sum
E:\zeta-monorepo\apps\backend\core\services\performance_optimizer.py: Exception, abs, agent, agent_id, agent_repository, any, applied, auto_optimize, b, background_collect_interval, bool, bottlenecks, changes, curr, current, dict, dry_run, e, enabled, float, force, getattr, history_limit, int, interval, interval_sec, isinstance, len, limit, list, max, memory_repository, min, name, old, plan_only, planned, prev, provider, r, rec, recommendation, recs, result, rule, self, sorted, str, sum, tuple, x
E:\zeta-monorepo\apps\backend\core\services\planner_llm.py: Exception, ValueError, any, classmethod, cls, config_overrides, data, dict, e, enumerate, error_reason, executor, feedback, float, goal, i, int, isinstance, list, next, self, skill_registry, step, str, super, word
E:\zeta-monorepo\apps\backend\core\services\prompt_injection_guard.py: bool, extras, float, list, max, pat, self, str, t, text, threshold
E:\zeta-monorepo\apps\backend\core\services\prompt_library.py: dict, list, query, str
E:\zeta-monorepo\apps\backend\core\services\rag_budgeter.py: int, list, max, max_tokens, per_chunk_overhead, self, t, token_estimates
E:\zeta-monorepo\apps\backend\core\services\rag_chunker.py: by, ch, chunk_size, int, len, list, max, min, overlap, parts, res, self, sent, str, text
E:\zeta-monorepo\apps\backend\core\services\rag_service.py: Exception, c, chunk_size, dict, float, guard, hasattr, int, isinstance, k, len, max, max_tokens, object, overlap, per_chunk_overhead, router, s, self, str, sum, text, token_estimator
E:\zeta-monorepo\apps\backend\core\services\registry.py: Exception, KeyError, ValueError, bool, dict, e, hasattr, len, list, name, print, reversed, self, service, str
E:\zeta-monorepo\apps\backend\core\services\retrieval_service.py: a, b, dict, doc, f, float, int, k, k1, len, list, max, q, query, self, str, sum, t, text, v
E:\zeta-monorepo\apps\backend\core\services\reward_functions.py: bool, citations_ok, coverage, float, guard_risk, len, max, pred, ref, runtime_regression, set, str, test_pass_rate, x
E:\zeta-monorepo\apps\backend\core\services\rlhf_store.py: NotImplementedError, actor_id, artifact_key, bool, dict, feedback, int, list, meta, rating, self, str
E:\zeta-monorepo\apps\backend\core\services\rule_engine.py: Exception, ValueError, any, bool, dict, list, msg, ok, p, r, rule, self, step, str, tuple, v, violations
E:\zeta-monorepo\apps\backend\core\services\scaffold_service.py: Exception, FileNotFoundError, KeyError, bool, cap_id, capability, dep, dict, dry_run, dst, e, entries, f, fh, group, hook, k, list, requirement, s, self, steps, str, template_rel, v
E:\zeta-monorepo\apps\backend\core\services\scheduler.py: Exception, coro, int, interval_sec, self
E:\zeta-monorepo\apps\backend\core\services\security_ai_agent.py: callable, dict, event, float, getattr, kind, max, min, self, str, v
E:\zeta-monorepo\apps\backend\core\services\security_ai_service.py: dict, event, self, str, text, url
E:\zeta-monorepo\apps\backend\core\services\security_service.py: AttributeError, Exception, ImportError, ValueError, any, attempt, bool, bytes, c, details, dict, e, email, enable_encryption, encrypted_data, events, expires_days, float, int, ip_address, isinstance, jwt_secret_key, key, len, length, list, max_login_attempts, metadata, name, p, password_min_length, perm, permissions, required_permission, self, session, session_timeout_minutes, set, stored_hash, str, sum, tuple, user, user_agent, username
E:\zeta-monorepo\apps\backend\core\services\self_learning_service.py: context_len, dict, float, int, max, min, model, provider, reward, risk, self, str, task
E:\zeta-monorepo\apps\backend\core\services\semantic_memory.py: a, any, b, ch, chunks, dict, doc_id, filters, float, int, k, len, list, max, max_tokens, metadata, query, scored, self, staticmethod, str, sum, t, text, top_k, tuple, v, vec, words, x
E:\zeta-monorepo\apps\backend\core\services\simple_training_service.py: Exception, ValueError, action, bool, callback, channel, dict, e, epoch, int, j, limit, list, min, payload, range, req, self, step, str
E:\zeta-monorepo\apps\backend\core\services\system_service.py: dict, self, str
E:\zeta-monorepo\apps\backend\core\services\telemetry.py: Exception, amount, bool, dict, float, hook, int, k, key, max, ms, self, str, v
E:\zeta-monorepo\apps\backend\core\services\training_service.py: ValueError, chunk, data_chunks, dataset_item_repository, dict, enumerate, error_message, float, i, input_type, int, job, len, list, metadata, progress, self, stats, status, str, training_job_repository, user_id
E:\zeta-monorepo\apps\backend\core\services\types.py: bool, classmethod, cls, code, dict, error, float, int, list, object, self, str, value
E:\zeta-monorepo\apps\backend\core\services\workflow_engine.py: Exception, agent, agent_repository, all, ast, bool, condition_result, config, context, dep_id, dependencies, dict, e, enumerate, error_message, execution_id, float, hist_execution, i, int, iteration_result, len, limit, list, memory_repository, name, range, reason, result, self, step, str, subtask, subtask_result, t, task_type, var_name, var_value, variables, workflow_id
E:\zeta-monorepo\apps\backend\core\services\_base.py: Exception, bool, context, ctx, dict, error, operation, property, self, str, type
E:\zeta-monorepo\apps\backend\core\services\__init__.py: ImportError
E:\zeta-monorepo\apps\backend\core\services\agent\create_agent_service.py: a, agent, analytics, getattr, int, kwargs, list, max_agents_per_owner, orchestrator, owner_id, self, str, tool_resolver
E:\zeta-monorepo\apps\backend\core\services\agent\orchestrator_impl.py: Exception, TimeoutError, ValueError, a, agent, bool, budget, cap, capabilities, config_overrides, configuration, d, description, dict, e, enumerate, estimate, failures, float, i, int, isinstance, len, limit, list, max, max_concurrency, max_concurrent_tasks, model_name, name, norm, norm_results, offset, parent_task, query, r, result, self, st, staticmethod, status, str, sub, subtask, successes, task_timeout, temperature, tid, token_budget
E:\zeta-monorepo\apps\backend\core\services\agent\service.py: NotImplementedError, bool, str
E:\zeta-monorepo\apps\backend\core\services\ai\demo_setup.py: Exception, doc, e, enumerate, i, isinstance, j, key, len, print, query_text, req_data, service, service_name, service_status, source, value
E:\zeta-monorepo\apps\backend\core\services\ai\orchestrator.py: Exception, TimeoutError, ValueError, bool, cap, capabilities, capability, dict, e, float, i, int, list, property, range, self, services, str, super, svc, task, worker_id
E:\zeta-monorepo\apps\backend\core\services\ai\registry.py: Exception, ValueError, any, available_only, bool, c, dep, dependencies, description, dict, e, event_type, float, handler, health_check_interval, include_description, include_tags, item, len, list, max, metadata, name, property, query, self, service_name, status, str, sum, tag, tags, version
E:\zeta-monorepo\apps\backend\core\services\ai\agents\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\services\ai\analytics\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\services\ai\chat\service.py: Exception, ValueError, bool, conv_id, dict, e, float, include_context, int, intent_name, keyword, keywords, len, limit, list, max, message, metadata, msg, num, offset, property, request, self, str, sum, super, tenant_id, user_id, word, x
E:\zeta-monorepo\apps\backend\core\services\ai\chat\service_simple.py: h, prompt, str
E:\zeta-monorepo\apps\backend\core\services\ai\multimodal\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\services\ai\rag\backends.py: ImportError, ValueError, config, dict, e, enumerate, f, float, i, idx, indices, int, list, match, metadata, min, open, score, scores, self, str, texts, top_k, tuple, vector, vectors, zip
E:\zeta-monorepo\apps\backend\core\services\ai\rag\chunking.py: ValueError, chunk_id, chunk_size, content, dict, end_index, enumerate, i, int, kwargs, len, list, max, max_chars, max_paragraphs, max_sentences, metadata, min, overlap, p, paragraph, part, range, s, self, sentence, separator_index, source_id, start_index, str, strategy, text
E:\zeta-monorepo\apps\backend\core\services\ai\rag\cross_encoder_reranker.py: Exception, ImportError, e, int, len, list, model_name, query, result, results, self, set, str, text, token, top_k, x
E:\zeta-monorepo\apps\backend\core\services\ai\rag\embed_interfaces.py: Exception, bool, details, dict, float, int, list, message, property, self, str, super
E:\zeta-monorepo\apps\backend\core\services\ai\rag\enhanced_cache.py: Exception, ImportError, bool, bytes, capacity, data, deserializer, dict, e, enable_redis, float, int, isinstance, k, key, key_prefix, len, obj, print, property, redis_url, result, self, serializer, str, ttl_seconds, v
E:\zeta-monorepo\apps\backend\core\services\ai\rag\enhanced_rag_service.py: Exception, ValueError, bool, bypass_cache, cached_result, config, dict, doc, documents, e, embedder, enumerate, float, i, int, len, list, print, property, r, result, self, str, sum, vector_index
E:\zeta-monorepo\apps\backend\core\services\ai\rag\hybrid_retriever.py: ValueError, alpha, chunk, chunk_idx_str, chunks, combined_score, combined_scores, dict, doc_id, embedder, float, h, hit, index, int, len, lexical_index, lexical_scores, list, max, max_val, meta, min, min_val, norm_score, query, result, results, score, self, sorted, str, text, val, vector_scores, x, zip
E:\zeta-monorepo\apps\backend\core\services\ai\rag\lexical_index.py: dict, doc_key, float, int, key, len, list, max, meta, query, scores, self, sorted, str, text, tf_local, tf_map, token, top_k, tuple, word, x
E:\zeta-monorepo\apps\backend\core\services\ai\rag\pipeline.py: Exception, NotImplementedError, all_passages, bool, callable, component, confidence, content, context, default_config, details, dict, doc, document_id, document_ids, documents, e, embedding_provider, enumerate, float, getattr, hasattr, hash, health, i, int, len, list, m, max, message, metadata, min, n, p, passage, pipeline_type, primary_passages, primary_retriever, query, range, reranked_passages, reranker, result, retriever, retriever_weights, s, secondary_passages, secondary_retrievers, seen, self, set, smax, smin, staticmethod, str, sum, super, unique, value, vars, w, zip
E:\zeta-monorepo\apps\backend\core\services\ai\rag\pipeline_unified.py: ValueError, c, chunk, chunker, confidence, dict, embedder, float, i, int, kwargs, len, list, metadata, min, question, range, retriever, self, sources, str, strategy, text
E:\zeta-monorepo\apps\backend\core\services\ai\rag\production_service.py: Exception, ValueError, any, bool, chunk, chunking_service, dict, document, e, embedding_adapter, enumerate, float, i, int, len, list, min, property, request, result, results, self, set, sorted, source, str, super, tuple, vector_store, word, x
E:\zeta-monorepo\apps\backend\core\services\ai\rag\rag_cache.py: Exception, bool, dict, extras, int, obj, query, scope, self, str, ttl, value
E:\zeta-monorepo\apps\backend\core\services\ai\rag\reranker.py: Exception, bool, details, dict, float, int, list, message, reranker_name, self, str, super
E:\zeta-monorepo\apps\backend\core\services\ai\rag\retriever.py: Exception, bool, details, dict, float, int, list, message, retriever_name, self, str, super
E:\zeta-monorepo\apps\backend\core\services\ai\rag\types.py: bool, c, dict, float, int, len, list, property, self, str
E:\zeta-monorepo\apps\backend\core\services\analytics\dashboards.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\core\services\analytics\service.py: Exception, ctx, db_session, dict, e, int, limit, list, metrics_adapter, self, str, super
E:\zeta-monorepo\apps\backend\core\services\chat\service.py: Exception, ImportError, chunk, context, conversation_id, ctx, dict, doc, e, hasattr, int, limit, list, llm_router, memory_service, rule_engine, self, str, super, token, user_message
E:\zeta-monorepo\apps\backend\core\services\chat\_impl.py: Exception, agent_id, aid, ascending, bool, c, chat_id, chat_ids, chat_repo, chat_type, cid, content, content_filter, dict, filters, float, for_update, getattr, hard, include_archived, int, isinstance, len, limit, list, m, max, message_repo, metadata, min, new_title, participants, pid, query, role, round, self, since, str, sum, super, title, uid_agent, uid_user, uow, uow_factory, user_id
E:\zeta-monorepo\apps\backend\core\services\learning\gpt4o_trainer.py: bool, config, context, dict, fetcher, float, int, it, limit, list, llm, messages, min, query, rules, self, situation, str
E:\zeta-monorepo\apps\backend\core\services\memory\service.py: Exception, ImportError, bool, conversation_id, ctx, dict, doc, e, float, hasattr, int, kv_store, len, list, metadata, namespace, query, self, str, super, text, threshold, top_k, vector_store
E:\zeta-monorepo\apps\backend\core\services\memory\_helpers.py: IMPORTANCE_WEIGHTS, a, b, dict, float, len, max, recency_days, similarity, source_quality, str, x, y, zip
E:\zeta-monorepo\apps\backend\core\services\memory\_impl.py: DeprecationWarning, Exception, IMPORTANCE_LEVELS, LABEL_IMPORTANCE_WEIGHTS, ValueError, a, abs, age_days, b, bool, content, context, dict, enumerate, exc, float, i, importance, importance_threshold, int, isinstance, len, limit, list, m, m1, m2, max, mid, min, next, offset, query, round, self, set, str, sum, type_counts, unique_candidates
E:\zeta-monorepo\apps\backend\core\services\memory\_manager_core.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\core\services\performance\profiler.py: args, bool, cc, ct, dict, enable_io_tracking, enable_memory_tracking, filename, float, func, func_name, function_breakdown, getattr, int, kwargs, len, line, list, max, memory_delta, name, nc, peak, r, recommendation, recs, result, results, self, sorted, str, sum, tt, x
E:\zeta-monorepo\apps\backend\core\shared\cache.py: agent_id, args, bool, cache_service, cache_storage, cached_result, conversation_data, conversation_id, dict, endpoint, func, input_data, int, key_prefix, kwargs, model, output_data, params_hash, query_hash, result, self, session_data, sorted, staticmethod, str, ttl, user_id
E:\zeta-monorepo\apps\backend\core\shared\config.py: bool, str
E:\zeta-monorepo\apps\backend\core\shared\constants.py: str
E:\zeta-monorepo\apps\backend\core\shared\idempotency.py: p, parts, str
E:\zeta-monorepo\apps\backend\core\shared\retry.py: Exception, fn
E:\zeta-monorepo\apps\backend\core\testing\ai_tester.py: dict, generator, len, metrics, reporter, runner, self, str
E:\zeta-monorepo\apps\backend\core\triage\data_triage.py: Exception, any, bool, c, dict, e, enabled, enumerate, float, i, int, k, len, list, max, min, name, rule, rule_name, safety_level, safety_results, self, set, str, super, threshold, tuple
E:\zeta-monorepo\apps\backend\core\triage\safety_filters.py: content, content_type, dict, float, len, list, pattern, str
E:\zeta-monorepo\apps\backend\core\use_cases\ai_use_cases.py: Exception, RuntimeError, ValueError, auto_vectorize, bool, config, content, dataset_path, dict, e, enumerate, float, hash, i, include_metadata, include_scores, int, len, limit, list, max, metadata, model_config, model_info, progress, query, response_time_ms, result, self, source, str, text, threshold, training_params, vector_store
E:\zeta-monorepo\apps\backend\core\use_cases\__init__.py: ImportError
E:\zeta-monorepo\apps\backend\core\use_cases\agent\agent_orchestrator_use_case.py: agent_id, dict, orchestrator, payload, result, self, str, task_type
E:\zeta-monorepo\apps\backend\core\use_cases\agent\create_agent.py: Exception, a, agent, agent_repository, analytics, any, dict, e, idempotency_key, int, isinstance, kind, len, list, max_agents_per_owner, name, owner_id, policies, prompt, self, str, t, tid, tool_resolver, tools
E:\zeta-monorepo\apps\backend\core\use_cases\agent\delete_agent.py: Exception, actor_id, agent, agent_id, agent_repository, bool, dict, force, hasattr, self, str, task_repository
E:\zeta-monorepo\apps\backend\core\use_cases\agent\deploy_agent.py: Exception, RuntimeError, ValueError, agent, agent_id, agent_repository, auto_activate, bool, deployment_config, dict, e, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\agent\get_agent.py: agent, agent_id, agent_repository, getattr, self, str, viewer_id
E:\zeta-monorepo\apps\backend\core\use_cases\agent\list_agents.py: Exception, a, agent_repository, any, c, dict, filtered, getattr, int, k, kinds, len, list, owner_id, page, page_size, self, set, sort, sorted, st, status, str
E:\zeta-monorepo\apps\backend\core\use_cases\agent\monitor_agent.py: Exception, RuntimeError, ValueError, agent, agent_id, agent_repository, bool, dict, e, float, list, max, metric_name, min, self, status, str, value
E:\zeta-monorepo\apps\backend\core\use_cases\agent\scale_agent.py: Exception, RuntimeError, ValueError, agent, agent_id, agent_repository, cpu_threshold, dict, e, float, int, max, memory_threshold, min, monitoring_service, reason, result, scaling_result, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\agent\train_agent.py: Exception, RuntimeError, ValueError, agent, agent_id, agent_repository, bool, dict, e, error_message, performance_metrics, self, str, training_config, training_data, training_results
E:\zeta-monorepo\apps\backend\core\use_cases\agent\update_agent.py: Exception, agent, agent_id, agent_repository, dict, editor_id, getattr, isinstance, len, list, patch, self, str, t
E:\zeta-monorepo\apps\backend\core\use_cases\agent\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\use_cases\agent\create_agent\use_case.py: NotImplementedError, str
E:\zeta-monorepo\apps\backend\core\use_cases\analytics\collect_metrics.py: ValueError, agent_id, dict, float, int, report_type, round, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\auth\authenticate_user.py: BaseException, Exception, JWTError, JWTExpiredSignatureError, TypeError, ValueError, bool, bytearray, bytes, callable, err, existing_user, getattr, hashed_password, isinstance, jwt, password, plain_password, request, self, str, token, tuple, type, user, user_repo
E:\zeta-monorepo\apps\backend\core\use_cases\auth\auth_use_cases.py: bool, existing_user, hashed_password, password, plain_password, request, self, str, user, user_repo
E:\zeta-monorepo\apps\backend\core\use_cases\chat\analyze_sentiment.py: Exception, RuntimeError, ValueError, chat_id, chat_repository, content, dict, e, len, max, min, s, self, sentiment_result, str, sum, w, word
E:\zeta-monorepo\apps\backend\core\use_cases\chat\end_conversation.py: Exception, RuntimeError, ValueError, archive, bool, chat_id, chat_ids, chat_repository, dict, e, len, list, reason, self, str, summary
E:\zeta-monorepo\apps\backend\core\use_cases\chat\generate_summary.py: Exception, RuntimeError, ValueError, ai_service, chat_repository, conversation, conversation_id, date, dict, e, getattr, hasattr, int, len, limit, list, m, max_length, memory_id, memory_ids, memory_repository, message, round, self, str, summary, topic, user_id
E:\zeta-monorepo\apps\backend\core\use_cases\chat\get_conversation.py: ValueError, chat_id, chat_repository, int, limit, list, message_repository, offset, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\chat\send_message.py: ValueError, agent_id, chat_repository, content, self, str, user_id
E:\zeta-monorepo\apps\backend\core\use_cases\chat\start_conversation.py: ValueError, agent_id, chat_repository, chat_type, self, str, user_id
E:\zeta-monorepo\apps\backend\core\use_cases\chat\start_chat\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\use_cases\collaboration\orchestrate_team.py: Exception, agent_id, bool, dict, e, len, list, req, self, store, str, team_id
E:\zeta-monorepo\apps\backend\core\use_cases\memory\backup_memory.py: Exception, RuntimeError, ValueError, b, base_backup_id, bool, compress, compression_service, dict, e, hasattr, include_metadata, len, max, memory, memory_repository, overwrite_existing, r, record, self, storage_result, storage_service, str, sum, target_user_id, user_id, x
E:\zeta-monorepo\apps\backend\core\use_cases\memory\compress_memory.py: Exception, RuntimeError, ValueError, ai_service, compressed_memory_id, compression_result, compression_service, content, content_list, days_threshold, dict, e, enumerate, float, getattr, i, int, len, list, m, max_group_size, max_memories_per_group, memory_id, memory_repository, min, min_length, other_memory, range, round, self, set, similarity_threshold, str, sum, threshold, user_id
E:\zeta-monorepo\apps\backend\core\use_cases\memory\delete_memory.py: Exception, RuntimeError, TypeError, ValueError, any, batch_size, bool, dict, e, hard_delete, i, importance_below, importance_threshold, int, len, list, m, max, memory_id, memory_repository, min, older_than_days, owner_id, range, self, str, tag, tags
E:\zeta-monorepo\apps\backend\core\use_cases\memory\delete_memory_simple.py: bool, dict, input, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\memory\query_memory.py: dict, input, int, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\memory\rebuild_embeddings.py: dict, input, int, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\memory\retrieve_memory.py: Exception, RuntimeError, agent_id, all, bool, days, dict, e, importance, int, len, limit, list, m, match_all, memory_id, memory_repository, memory_type, offset, result, self, status, str, tag, tags, user_id
E:\zeta-monorepo\apps\backend\core\use_cases\memory\search_memory.py: Exception, RuntimeError, any, content_query, date_from, date_to, dict, e, end_date, float, importance, int, len, limit, list, m, max, memory, memory_id, memory_repository, memory_type, offset, query, round, self, start_date, str, sum, tag, tags, user_id, vector
E:\zeta-monorepo\apps\backend\core\use_cases\memory\store_memory.py: AttributeError, Exception, TypeError, ValueError, agent_id, bool, cluster_tops, clusters, content, context, dict, exc, float, getattr, hasattr, importance, int, isinstance, k, kwargs, len, limit, list, m, max, max_tag_length, max_tags, memory_count, memory_id, memory_repo, memory_type, old_memories, out, query, seen, selection, self, set, setattr, str, summary_memory, t, tags, text, threshold, tuple, updated, updates, val, x
E:\zeta-monorepo\apps\backend\core\use_cases\memory\update_memory.py: Exception, RuntimeError, ValueError, batch_size, bool, context_updates, days, dict, dimension, e, field, float, i, importance, int, isinstance, len, link_id, linked_memory_id, list, memory_repository, merge, model, new_content, operation, range, result, self, set, status, str, tag, tags, update_data, updates, value, vector
E:\zeta-monorepo\apps\backend\core\use_cases\memory\upsert_memory.py: dict, input, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\memory\store_memory\__init__.py: list, str
E:\zeta-monorepo\apps\backend\core\use_cases\planning\create_plan.py: ValueError, agent_id, description, dict, enumerate, i, list, plan_id, plan_repo, result, self, step_data, steps_data, str, title, user_id
E:\zeta-monorepo\apps\backend\core\use_cases\planning\execute_plan.py: Exception, dict, e, execution_context, int, list, plan_id, range, self, step_index, step_result, str
E:\zeta-monorepo\apps\backend\core\use_cases\planning\modify_plan.py: Exception, dict, e, float, int, isinstance, len, list, modification_index, modifier_id, parameter_updates, plan_id, position, self, set, step_definition, step_index, str, validation_result
E:\zeta-monorepo\apps\backend\core\use_cases\planning\optimize_plan.py: Exception, current_metrics, dict, e, float, int, isinstance, list, metric, min, optimization_criteria, original_value, plan_id, round, self, str
E:\zeta-monorepo\apps\backend\core\use_cases\planning\validate_plan.py: Exception, any, bool, dep, dict, e, enumerate, field, float, i, int, isinstance, keyword, len, list, max, min, neighbor, new_rules, node, plan_data, result, self, set, step, step_data, step_index, str, validation_level, validation_result
E:\zeta-monorepo\apps\backend\core\use_cases\rag\one_click_learning.py: Exception, RuntimeError, ValueError, bool, chunking_service, e, embedding_service, float, int, len, list, locals, request, self, str, vector_store_service
E:\zeta-monorepo\apps\backend\core\use_cases\rag\use_case.py: alpha, beta, chunks, dict, enumerate, float, int, it, j, list, max, max_tokens, overlap, piece, priors, query, r, reranked, self, store, str, top_k, x
E:\zeta-monorepo\apps\backend\core\utils\async_utils.py: callable, getattr, value
E:\zeta-monorepo\apps\backend\core\utils\configuration_manager.py: Exception, OSError, bool, config_dir, config_name, default, dict, e, env_var, f, file_path, float, int, key, l, len, list, listener, name, open, self, str, sum, v, validator
E:\zeta-monorepo\apps\backend\core\utils\deprecation.py: DeprecationWarning, alternative, args, func, kwargs, list, message_parts, name, reason, removal_version, str
E:\zeta-monorepo\apps\backend\core\utils\ensure_dependencies.py: ImportError, RuntimeError, bool, dict, e, len, list, min_ver, min_version, module_name, package_name, required_packages, str
E:\zeta-monorepo\apps\backend\core\utils\error_handler.py: Exception, action, args, bool, callable, code, details, dict, e, error, exc, field, func, func_name, hasattr, int, kwargs, max, message, operation, resource, resource_id, resource_type, self, service_name, str, sum, super, type, user_id, value, x
E:\zeta-monorepo\apps\backend\core\utils\lazy_loader.py: AttributeError, Exception, attr_name, dict, e, getattr, len, list, max, module_path, name, names, self, str
E:\zeta-monorepo\apps\backend\core\utils\performance_monitor.py: Exception, args, bool, component, dict, error, float, func, int, kwargs, len, list, max, metric, metric_name, min, self, str, threshold, value
E:\zeta-monorepo\apps\backend\core\utils\validation_helpers.py: Exception, data, dict, exc, int, isinstance, model_cls, name, p, str, type, value
E:\zeta-monorepo\apps\backend\core\value_objects\permissions.py: ROLE_DEFAULT_SCOPES, bool, cleaned, dict, list, requested, required, role, s, set, sorted, str, valid
E:\zeta-monorepo\apps\backend\data\database_async.py: Exception, RuntimeError, ValueError, bool, database_url, e, echo, float, int, isinstance, max_overflow, pool_size, pool_timeout, self, str
E:\zeta-monorepo\apps\backend\data\database_init.py: Exception, ModuleNotFoundError, bool, conn, dict, e, e2, echo, init_result, int, isinstance, key, len, print, recreate, result, seed_data, seed_test_data_flag, seed_test_data_option, self, session, str, sum, table, table_counts, value, verify
E:\zeta-monorepo\apps\backend\data\migrations.py: Exception, FileNotFoundError, RuntimeError, alembic_cfg_path, backup_path, bool, conn, dict, e, engine, getattr, int, len, list, object, pending, result, rev, self, staticmethod, str, sync_conn, t, target
E:\zeta-monorepo\apps\backend\data\models.py: CASCADE_DELETE, FK_USERS_ID, MAX_AGENT_NAME_LEN, MAX_CHAT_TITLE_LEN, MAX_DOCUMENT_FILENAME_LEN, MAX_EMAIL_LEN, MAX_FULL_NAME_LEN, MAX_MESSAGE_TYPE_LEN, MAX_ROLE_LEN, MAX_STATUS_LEN, MAX_TRAINING_JOB_NAME_LEN, MAX_USERNAME_LEN, ValueError, bool, dict, float, int, max_size, self, str, version_id
E:\zeta-monorepo\apps\backend\data\adapters\file_knowledge_store.py: Exception, base_dir, dict, float, key, list, matches, query, self, str, threshold, x
E:\zeta-monorepo\apps\backend\data\adapters\inmemory_alerts.py: dict, list, message, self, service, str, title
E:\zeta-monorepo\apps\backend\data\adapters\inmemory_metrics.py: dict, float, int, list, ms, name, self, str, tags, value
E:\zeta-monorepo\apps\backend\data\adapters\asr\local_asr_adapter.py: audio_chunk, audio_data, audio_stream, bytes, float, len, list, model_path, self, str
E:\zeta-monorepo\apps\backend\data\adapters\asr\whisper_adapter.py: Exception, ImportError, api_key, audio_chunk, audio_data, audio_stream, base_url, bytearray, bytes, dict, e, float, format, hasattr, isinstance, language, len, list, message, model, original_error, self, str, super, timeout, transcription_id
E:\zeta-monorepo\apps\backend\data\adapters\llm\anthropic_adapter\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\adapters\llm\openai_adapter\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\adapters\vector\chunking_service.py: Exception, any, default_chunk_size, default_overlap, default_strategy, dict, enumerate, i, int, keyword, len, list, max, min, opts, original_text, range, self, separator, str, sub_chunk, text
E:\zeta-monorepo\apps\backend\data\adapters\vector\enhanced_memory_store.py: ImportError, a, b, bool, dict, dim, doc_data, doc_id, docs, enable_hybrid_search, f, filepath, filter_criteria, float, i, int, isinstance, k, key, len, list, metadata, metadata_filter, open, query, range, result, self, str, sum, super, text, tuple, use_hybrid, value, vec1, vec2, x, zip
E:\zeta-monorepo\apps\backend\data\adapters\vector\hybrid_search.py: bm25_score, config, count, data, dict, doc_id, doc_scores, documents, float, fused_scores, int, len, list, max, query, result, self, str, term, text, tf, vector_results, x
E:\zeta-monorepo\apps\backend\data\adapters\vector\memory_vector_store.py: ImportError, a, b, bool, dict, dim, doc_data, doc_id, docs, enable_hybrid_search, f, filepath, filter_criteria, float, i, id, int, isinstance, k, key, len, list, metadata, metadata_filter, open, property, query, range, result, self, str, sum, text, tuple, value, vec1, vec2, x, zip
E:\zeta-monorepo\apps\backend\data\adapters\vector\openai_embeddings.py: Exception, ImportError, api_key, base_url, bool, dict, dim, documents, e, float, i, int, item, len, list, max_batch_size, message, original_error, query, range, self, str, super, test_result, text, texts, timeout, use_fallback
E:\zeta-monorepo\apps\backend\data\adapters\vector\semantic_chunking.py: ValueError, bool, char_end, char_start, chunk_size, default_strategy, dict, documents, float, int, keyword, len, list, max, max_chunk_size, min, min_chunk_size, name, overlap_size, para_start, prefer_paragraphs, respect_sentences, self, str, strategy, strategy_kwargs, sum, text, tuple, zip
E:\zeta-monorepo\apps\backend\data\clients\openai_adapter.py: Exception, api_key, base_url, chunk, dict, exc, float, getattr, int, kwargs, line, list, messages, min, model, path, payload, self, str, stream_any, temperature, timeout, tok, tools
E:\zeta-monorepo\apps\backend\data\clients\s3_blob_adapter.py: Exception, RuntimeError, StopAsyncIteration, byte_range, bytearray, bytes, cfg, chunk, chunk_size, content_type, dict, done, expires_in, extra, int, it, key, kw, len, list, max_concurrency, metadata, method, n, no, part_size, parts, s3, self, session, set, staticmethod, str, t, tasks, tuple, x
E:\zeta-monorepo\apps\backend\data\clients\vector_store_client.py: ch, chunks, dict, enumerate, float, i, int, list, max, query, r, s, scored, self, str, top_k
E:\zeta-monorepo\apps\backend\data\config\database_config.py: Exception, dict, e, hasattr, int, print, result, self, session, str
E:\zeta-monorepo\apps\backend\data\config\optimized_database_config.py: Exception, connect_args, dict, e, engine_config, int, max, pool_config, print, result, round, self, session, str
E:\zeta-monorepo\apps\backend\data\database\session.py: Exception, session
E:\zeta-monorepo\apps\backend\data\dto\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\dtos\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\external\advanced_alerts_adapters.py: float, list, message, metrics, print, res, severity, str, title
E:\zeta-monorepo\apps\backend\data\external\anthropic_client.py: Exception, analysis_type, api_key, block, chunk, config_overrides, context, dict, e, float, instructions, int, language, len, list, msg, problem, reasoning_type, self, str, style, sum, text
E:\zeta-monorepo\apps\backend\data\external\backup_adapters.py: base_dir, self, str
E:\zeta-monorepo\apps\backend\data\external\database_client.py: Exception, ValueError, bool, count, database_url, dict, e, len, list, output_file, params, result, self, session, str, sum, table
E:\zeta-monorepo\apps\backend\data\external\documentation_adapters.py: dict, openapi, self, str
E:\zeta-monorepo\apps\backend\data\external\elasticsearch_client.py: Exception, ImportError, bool, dict, doc, doc_id, document, documents, e, fields, from_, getattr, hasattr, hit, host, index_name, int, list, mapping, password, port, query_string, result, self, size, str, updates, username
E:\zeta-monorepo\apps\backend\data\external\feature_toggle_adapters.py: bool, dict, feature_name, self, str
E:\zeta-monorepo\apps\backend\data\external\gcp_client.py: Exception, all, blob_name, bool, bucket_name, bytes, chunk, collection, config_overrides, content_type, data, destination_blob_name, dict, e, float, i, int, len, limit, list, min, pred, prefix, project_id, prompt, range, self, source_data, status, str, text, texts, tuple
E:\zeta-monorepo\apps\backend\data\external\huggingface_client.py: Exception, RuntimeError, all, api_token, base_url, batch_size, bool, client, context, dict, do_sample, e, exc, float, getattr, i, image_url, inp, int, isinstance, item, len, limit, list, max_length, min_length, model_id, num_return_sequences, options, params, prompt, question, range, result, search, self, str, task, temperature, text, timeout, v, x
E:\zeta-monorepo\apps\backend\data\external\monitoring_client.py: Exception, RuntimeError, alert_name, api_key, attempt, base_url, condition, dashboard_name, dict, e, end_time, event_type, float, int, labels, len, list, max_retries, message, metadata, metric, metric_name, metrics, notification_channels, query, range, response, self, severity, start_time, str, threshold, value
E:\zeta-monorepo\apps\backend\data\external\observability_adapters.py: dict, float, int, ms, name, self, str, value
E:\zeta-monorepo\apps\backend\data\external\openai_client.py: api_key, c, dict, float, int, list, m, messages, model, ord, self, str, sum, text
E:\zeta-monorepo\apps\backend\data\external\pinecone_client.py: Exception, ImportError, ValueError, api_key, batch_size, bool, delete_all, dict, dimension, e, environment, filter_conditions, float, i, ids, include_metadata, include_values, int, len, list, metadata, metadata_config, metric, namespace, range, replicas, self, set_metadata, shards, str, timeout, top_k, tuple, vector, vector_id, vectors
E:\zeta-monorepo\apps\backend\data\external\postgres_client.py: Exception, RuntimeError, ValueError, analyze, arg, args, bool, col, command, commands, conn, data, database, dict, e, enumerate, host, i, int, len, list, max_pool_size, n, name, names, password, pool_size, port, r, range, result, results, self, set_clauses, str, table, tuple, unique, username, val, where_args, where_clause
E:\zeta-monorepo\apps\backend\data\external\redis_client.py: bool, count, decode_responses, dict, e, encoding, ex, float, int, isinstance, key, list, max_connections, name, nx, px, seconds, self, str, url, xx
E:\zeta-monorepo\apps\backend\data\external\s3_client.py: Exception, ImportError, RuntimeError, access_key, bool, bucket_name, bytes, content_type, dest_key, dict, e, endpoint_url, expiration, file_path, getattr, http_method, int, isinstance, key, len, list, max_keys, metadata, obj, prefix, region, secret_key, self, source_key, str
E:\zeta-monorepo\apps\backend\data\external\services.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\data\external\services_client.py: BaseException, Exception, api_key, base_url, body, bool, client, connection_string, dict, e, endpoint, float, from_email, getattr, host, html_body, int, isinstance, key, len, list, max_tokens, messages, method, model, name, openai_api_key, params, password, port, postgresql_connection, redis_host, redis_password, redis_port, result, secret, self, service, smtp_host, smtp_password, smtp_port, smtp_username, str, subject, sum, super, temperature, text, timeout, to_email, type, username, zip
E:\zeta-monorepo\apps\backend\data\external\webhook_client.py: Exception, TimeoutError, base_url, bool, config, dict, e, event_id, event_type, events, int, isinstance, list, max_retries, metadata, name, result, retry_count, self, session, str, webhook, webhook_config
E:\zeta-monorepo\apps\backend\data\external\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\external\events\event_bus.py: Exception, dict, exc, handler, list, payload, self, str, topic
E:\zeta-monorepo\apps\backend\data\external\events\event_bus_new.py: BaseException, Exception, base_delay, bool, concurrency, dict, e, etype, event_type, float, h, handler, handlers, i, int, isinstance, list, logger, m, max_queue, middlewares, outbox, priority, range, repr, retries, s, self, spec, specs, str, t, type, workers
E:\zeta-monorepo\apps\backend\data\external\events\event_dispatcher.py: RuntimeError
E:\zeta-monorepo\apps\backend\data\external\llm\enhanced_openai_client.py: Exception, api_key, audio_data, audio_size_bytes, base_url, bool, bytes, chunk, dict, e, embedding, filename, float, func, getattr, hasattr, image, image_url, int, isinstance, key, kwargs, language, len, list, max_tokens, msg, organization, prompt, request, request_params, requested_model, required_tokens, result, s, self, str, stream, usage
E:\zeta-monorepo\apps\backend\data\external\llm\gemini_client.py: Exception, RuntimeError, api_endpoint, api_key, dict, exc, int, request_timeout, self, str
E:\zeta-monorepo\apps\backend\data\external\llm\openai_async_adapter.py: Exception, chunk, classmethod, client, cls, dict, estimated_prompt_tokens, float, functions, getattr, int, isinstance, kwargs, list, max_tokens, messages, model, opts, self, str, temperature, tools
E:\zeta-monorepo\apps\backend\data\external\outbox\sqlalchemy_outbox_repository.py: Exception, attempts, backoff_sec, batch_size, bool, dict, e, error, event_id, event_type, float, int, len, list, lock_timeout, next_run_at, owner, partition_key, partition_mod, payload, result, row_id, schema_version, self, session, str, worker_ix
E:\zeta-monorepo\apps\backend\data\external\repositories\jit_grant_repo.py: NotImplementedError, bool, dict, duration_minutes, hasattr, int, permission, resource_id, self, str, user_id
E:\zeta-monorepo\apps\backend\data\external\worker\celery_app.py: getattr
E:\zeta-monorepo\apps\backend\data\external\worker\self_upgrade.py: Exception, SystemExit, all, bool, dep, dict, dry_run, exc, fh, isinstance, len, metadata, open, print, r, str
E:\zeta-monorepo\apps\backend\data\external\worker\tasks\auto_updater.py: Exception, apply, bool, dict, e, str
E:\zeta-monorepo\apps\backend\data\external\worker\tasks\federated_rounds.py: Exception, dict, dt, float, func, int, len, list, map, num_updates, rejected, str, u, updates
E:\zeta-monorepo\apps\backend\data\external\worker\tasks\training_tasks.py: Exception, bool, chunk_size, dict, e, file, file_ids, file_type, float, has_file, i, int, len, link, list, message, overlap, progress, range, stage, str, tags, text, text_chunks, url
E:\zeta-monorepo\apps\backend\data\factories\automation_factory.py: dict, float, guard, learner, list, max, min, moe_canary_ratio, ocr_languages, openai_api_key, openai_model, self, str
E:\zeta-monorepo\apps\backend\data\implementations\automation_executor_impl.py: Exception, ValueError, bool, default_timeout, e, enumerate, float, height, i, input_controller, int, isinstance, len, plan, point_key, result, screen_perception, self, step, step_result, str, width
E:\zeta-monorepo\apps\backend\data\implementations\automation_planner_impl.py: Exception, KeyError, RuntimeError, ValueError, api_key, dict, e, enumerate, error_msg, float, guard, hasattr, i, int, isinstance, learner, len, max, max_steps, min, model, moe_canary_ratio, original_plan, response_content, screenshot_path, self, step_data, str, success_msg, task_description, tuple
E:\zeta-monorepo\apps\backend\data\implementations\input_control_impl.py: Exception, RuntimeError, ValueError, bool, button, clicks, direction, double, duration, e, end, float, int, interval, k, key, position, self, start, str, text, x, y
E:\zeta-monorepo\apps\backend\data\implementations\perception_impl.py: Exception, FileNotFoundError, RuntimeError, ValueError, confidence, detection, dict, e, float, h, image, int, languages, len, list, max, max_loc, max_val, min, offset_x, offset_y, point, region, result, save_path, self, str, target_text, template_path, text, threshold, tuple, w
E:\zeta-monorepo\apps\backend\data\implementations\safety_engine_impl.py: Exception, action_type, area, bool, config, e, isinstance, key, pattern, self, step, str, target, value, x, y, zone
E:\zeta-monorepo\apps\backend\data\implementations\security_ai\phishing_impl.py: cnt, dict, feats, float, len, max, min, p, s, self, str, sum, threshold, url, value
E:\zeta-monorepo\apps\backend\data\implementations\security_ai\river_ueba_impl.py: dict, e, event, float, int, max, min, seed, self, str, threshold, value
E:\zeta-monorepo\apps\backend\data\instrumentation\db_query_counter.py: bool, ch, engine, kw, len, route_hint, sql, statement, str
E:\zeta-monorepo\apps\backend\data\knowledge\fetcher.py: dict, int, limit, list, query, self, str
E:\zeta-monorepo\apps\backend\data\knowledge\http_fetcher.py: Exception, bool, dict, e, float, int, it, len, limit, list, max, max_len, min, out, query, self, str, timeout, use_arxiv, use_wikipedia
E:\zeta-monorepo\apps\backend\data\mappers\repository_mappers.py: Exception, ValueError, dict, domain_data, entity_id, entity_type, error, float, staticmethod, str
E:\zeta-monorepo\apps\backend\data\models\agent_model.py: TypeError, ValueError, bool, capability, conversations_delta, dict, float, int, kb_id, list, max, messages_delta, min, response_time, round, self, state_update, str, tool_config, user_id
E:\zeta-monorepo\apps\backend\data\models\analytics_model.py: self, str
E:\zeta-monorepo\apps\backend\data\models\audit_model.py: action, bool, dict, flag, float, int, key, kwargs, list, operation, resource_type, self, status, str, super, tag, value
E:\zeta-monorepo\apps\backend\data\models\authz_models.py: bool, dict, self, str
E:\zeta-monorepo\apps\backend\data\models\base.py: Exception, NAMING_CONVENTION, bool, c, ch, classmethod, col, conn, data, dialect, dict, drop, enumerate, force, getattr, globals, i, isinstance, k, list, out, self, session, set, setattr, str, v, value
E:\zeta-monorepo\apps\backend\data\models\base_model.py: TypeError, ValueError, action, bool, classmethod, cls, column, data, details, dict, getattr, hasattr, int, isinstance, key, len, list, property, restored_by, result, self, setattr, str, tag, user_id
E:\zeta-monorepo\apps\backend\data\models\cache_model.py: self, str
E:\zeta-monorepo\apps\backend\data\models\chat_model.py: bool, content, content_type, conversation_id, conversation_type, created_by, default, dict, emoji, file_size, filename, float, int, key, kwargs, len, list, max, message_id, original_filename, parent_message_id, role, self, sender_id, sender_type, storage_path, str, super, title, user_id, value
E:\zeta-monorepo\apps\backend\data\models\conversation_model.py: TypeError, ValueError, attachments, bool, context, context_update, dict, feedback, float, int, isinstance, len, list, metadata, rating, raw_s, self, settings, str
E:\zeta-monorepo\apps\backend\data\models\deepseek_model.py: Exception, RuntimeError, e, len, model_name, model_path, prompt, self, str, super
E:\zeta-monorepo\apps\backend\data\models\document_model.py: classmethod, cls, dict, document, self
E:\zeta-monorepo\apps\backend\data\models\file_model.py: bool, content_type, created_by, default, dict, error_message, expires_at, file_hash, file_id, file_path, file_size, filename, float, include_sensitive, int, key, kwargs, list, original_filename, processor, result, self, str, super, tag, unit, uploaded_by, value, version_number
E:\zeta-monorepo\apps\backend\data\models\fl_client.py: dict, str
E:\zeta-monorepo\apps\backend\data\models\fl_model.py: dict, str
E:\zeta-monorepo\apps\backend\data\models\fl_round.py: dict, int, str
E:\zeta-monorepo\apps\backend\data\models\fl_update.py: float, int, str
E:\zeta-monorepo\apps\backend\data\models\knowledge_base_model.py: TypeError, ValueError, bool, delta, dict, float, int, len, list, max, max_length, metadata, self, settings, size_delta, str, user_id, vector
E:\zeta-monorepo\apps\backend\data\models\logs_model.py: self, str
E:\zeta-monorepo\apps\backend\data\models\memory_model.py: ValueError, a, agent_id, association_type, b, bool, content, content_hash, default, dict, embedding_type, embedding_vector, float, importance_score, include_content, include_sensitive, include_vector, int, k, key, keyword, kwargs, len, list, max, max_length, memory_id, memory_type, min, model_name, new_score, other_vector, parent_memory_id, result, self, sensitive, source_memory_id, str, strength, strength_boost, strength_reduction, sum, super, tag, target_memory_id, value, verified, x, zip
E:\zeta-monorepo\apps\backend\data\models\message_model.py: classmethod, cls, dict, message, self
E:\zeta-monorepo\apps\backend\data\models\monitoring_model.py: self, str
E:\zeta-monorepo\apps\backend\data\models\outbox_model.py: dict, int, str
E:\zeta-monorepo\apps\backend\data\models\plan_model.py: abs, agent_id, all, bool, completed_task_ids, criterion, default, dep_id, description, dict, event_data, event_type, float, include_logs, include_tasks, int, key, kwargs, len, list, max, min, name, objective, parent_plan_id, percentage, plan_id, plan_type, reason, result, self, sorted, str, success, sum, super, t, tag, task_id, task_type, template_id, time, tool, value
E:\zeta-monorepo\apps\backend\data\models\release_model.py: str
E:\zeta-monorepo\apps\backend\data\models\security_model.py: self, str
E:\zeta-monorepo\apps\backend\data\models\session_model.py: self, str
E:\zeta-monorepo\apps\backend\data\models\training_models.py: dict, getattr, int, kwargs, list, self, str, super
E:\zeta-monorepo\apps\backend\data\models\user_model.py: TypeError, ValueError, bool, dict, int, list, permission, preference_updates, preferences, self, str, threshold_minutes
E:\zeta-monorepo\apps\backend\data\models\_fixed\agent_model.py: TypeError, bool, capabilities, capability, conversations_delta, dict, float, int, isinstance, kb_id, kb_ids, len, list, max, messages_delta, min, new_state, response_time, round, self, str, tools, user_id
E:\zeta-monorepo\apps\backend\data\models\_fixed\cache_model.py: bool, dict, float, int, self, str
E:\zeta-monorepo\apps\backend\data\models\_fixed\conversation_model.py: TypeError, attachments, context, dict, feedback, float, int, isinstance, list, metadata, rating, self, settings, str
E:\zeta-monorepo\apps\backend\data\models\_fixed\knowledge_base_model.py: TypeError, bool, dict, exclude_fields, float, int, len, list, max_length, self, str, super, value, vector
E:\zeta-monorepo\apps\backend\data\models\_fixed\knowledge_base_model_v2.py: TypeError, all, bool, float, int, isinstance, len, list, max_length, self, str, value, vector, x
E:\zeta-monorepo\apps\backend\data\repositories\agent_repository_impl.py: ValueError, agent, agent_id, list, result, self, session, user_id
E:\zeta-monorepo\apps\backend\data\repositories\base_repository.py: bool, dict, e, entity, entity_id, int, limit, offset, property, result, self, session, str, type, updates
E:\zeta-monorepo\apps\backend\data\repositories\chat_repository_impl.py: bool, chat, dict, list, message, msg_id, self, str, x
E:\zeta-monorepo\apps\backend\data\repositories\complete_repository_system.py: Exception, action, agent_id, bool, category, chat_id, config_key, dict, e, email, entity_id, entity_type, file_hash, filters, getattr, hasattr, int, key, kwargs, limit, list, metadata, model_class, new_values, offset, old_values, order_by, owner_id, plan_id, query, result, self, session, str, super, type, user_id, username, value
E:\zeta-monorepo\apps\backend\data\repositories\document_repository_impl.py: ValueError, document, document_id, int, limit, list, query, result, self, session, str, user_id
E:\zeta-monorepo\apps\backend\data\repositories\factory.py: Exception, NotImplementedError, dict, exc_type, manager, self, session, str
E:\zeta-monorepo\apps\backend\data\repositories\federated_repository.py: artifact_uri, capabilities, client_id, client_pk, deadline, dict, ids, int, list, meta, metrics, model_version, payload_sha256, payload_uri, reg_token_hash, round_id, round_name, sample_size, self, session, sha256, signature, status, str, target_clients, version
E:\zeta-monorepo\apps\backend\data\repositories\federated_round_repository.py: bool, dict, float, int, list, result, round_id, self, str
E:\zeta-monorepo\apps\backend\data\repositories\inmemory_audit_repository.py: client_id, dict, e, kind, payload, round_id, self, str
E:\zeta-monorepo\apps\backend\data\repositories\inmemory_base.py: bool, dict, entity, int, key_fn, limit, list, offset, prefix, self, str, tuple
E:\zeta-monorepo\apps\backend\data\repositories\memory_repository_impl.py: ValueError, int, limit, list, memory, memory_id, query, result, self, session, str, user_id
E:\zeta-monorepo\apps\backend\data\repositories\message_repository_impl.py: chat_id, list, message, message_id, result, self, session
E:\zeta-monorepo\apps\backend\data\repositories\metrics_repository.py: Exception, dict, e, float, metric_name, metric_type, metric_value, self, session, str, tags, timestamp
E:\zeta-monorepo\apps\backend\data\repositories\outbox_repository.py: bool, dict, int, list, str
E:\zeta-monorepo\apps\backend\data\repositories\outbox_repo_impl.py: Exception, RuntimeError, attempts, backoff_sec, batch_size, bool, classmethod, cls, conn, dict, error, event_id, event_type, handler, int, item, key, limit, list, lock_timeout_sec, next_run_at, partition_key, partition_mod, payload, pk, result, row_id, schema_version, self, session, str, worker_ix
E:\zeta-monorepo\apps\backend\data\repositories\outbox_row.py: dict, int, str
E:\zeta-monorepo\apps\backend\data\repositories\simple_training_repository.py: TypeError, bool, float, int, job_id, limit, list, progress, result, self, session, status, str, training_job, user_id
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_agent_repository.py: Exception, agent, bool, capability, dict, e, entity, entity_id, filters, int, k, len, limit, list, m, offset, owner_id, result, self, session, str, user_id, v
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_agent_repository_bridge.py: DeprecationWarning
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_analytics_repository.py: dict, list, self, session, str
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_audit_repository.py: dict, self, session, str
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_backup_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_blob_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_cache_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_chat_repository.py: bool, int, list, message, self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_config_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_dataset_item_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_feedback_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_file_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_memory_repository.py: Exception, bool, dict, e, entity, entity_id, filters, hours, int, isinstance, k, len, limit, list, offset, query, result, self, session, str, total_result, v
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_notification_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_plan_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_security_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_session_repository.py: self, session
E:\zeta-monorepo\apps\backend\data\repositories\sqlalchemy_user_repository.py: bool, email, int, limit, list, offset, query, self, session, str, user, user_id, username
E:\zeta-monorepo\apps\backend\data\repositories\training_job_repository.py: dict, getattr, hasattr, int, j, list, self, session, status, str, tuple
E:\zeta-monorepo\apps\backend\data\repositories\user_repository_impl.py: ValueError, email, result, self, session, str, user, user_id
E:\zeta-monorepo\apps\backend\data\repositories\vector_repository_impl.py: Exception, bool, dict, doc, doc_id, document_id, documents, e, filter_dict, float, int, key, len, list, metadata, query, self, str, v, value, vec1, vec2, vector, x
E:\zeta-monorepo\apps\backend\data\repositories\models\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\seeds\initial_data.py: Exception, dict, e, session, str
E:\zeta-monorepo\apps\backend\data\seeds\seed_authz_data.py: Exception, dict, e, len, list, next, perm_data, perm_name, print, result, role_info, role_name, str
E:\zeta-monorepo\apps\backend\data\seeds\test_data.py: Exception, dict, e, list, session, str
E:\zeta-monorepo\apps\backend\data\services\bulk_memory_adapter.py: Exception, backend, batch, batch_size, bool, dict, e, embedding_model, enable_retry, filters, flt, hard, hasattr, i, ids, int, isinstance, kwargs, len, list, max_workers, namespace, range, records, self, str, super, top_k
E:\zeta-monorepo\apps\backend\data\services\content_safety.py: api_key, bool, len, self, str, text
E:\zeta-monorepo\apps\backend\data\services\database_service.py: Exception, RuntimeError, args, bool, conn, e, kwargs, operation, property, self, session
E:\zeta-monorepo\apps\backend\data\services\file_service.py: Exception, bool, bytes, cand, chunk, content_length, dict, e, end, f, file, int, len, list, manager, max, open, path, s, self, size, start, staticmethod, storage_root, str
E:\zeta-monorepo\apps\backend\data\services\memory_adapter.py: backend, batch_size, bool, dict, embedding_model, filters, flt, hard, ids, int, list, namespace, records, self, str, target_model, top_k
E:\zeta-monorepo\apps\backend\data\services\memory_legacy.py: DeprecationWarning, args, backend, dict, kwargs, object, self, str
E:\zeta-monorepo\apps\backend\data\shared\redis_cache.py: Exception, UnicodeDecodeError, agent_id, amount, args, bool, bytes, cache_manager, cached_result, conversation_id, default, default_ttl, dict, e, endpoint, field, float, func, hits, input_hash, int, isinstance, key, key_prefix, kwargs, list, mapping, max_connections, misses, model, params_hash, pattern, query_hash, redis_client, redis_url, result, self, sorted, staticmethod, str, tuple, user_id
E:\zeta-monorepo\apps\backend\data\utils\__init__.py: list, str
E:\zeta-monorepo\apps\backend\data\vector_stores\faiss_store.py: Exception, RuntimeError, ValueError, bool, content, dict, dimension, distance, distances, doc, e, enable_gpu, enumerate, f, float, hasattr, hash, i, idx, index_type, indices, int, key, len, limit, list, logger, max, max_memory_mb, metric_name, min, model_name, new_value, open, query_vector, search_mode, self, storage_path, str, text, thread_pool_size, threshold, tuple, zip
E:\zeta-monorepo\apps\backend\deployment\rollout.py: Exception, ValueError, bool, config, deployment_result, dict, e, f, int, model_path, open, reason, str, target_percentage
E:\zeta-monorepo\apps\backend\docs\examples\agent_creation.py: Exception, agent, agent_id, analysis_agent, api_key, base_url, basic_agent, bool, code_agent, creative_agent, description, detailed_agent, e, execution_agent, float, int, len, list, name, planning_agent, print, research_agent, self, str, updated_agent, updates
E:\zeta-monorepo\apps\backend\evaluators\verifier_gpt5.py: BENCHMARKS, BENCHMARK_WEIGHT, BENCHMARK_WEIGHTS, DOMAIN_SCORES, Exception, FileNotFoundError, GPT5_WEIGHT, PASS_THRESHOLD, ValueError, abs, all, e, float, isinstance, k, len, list, model_path, model_paths, p, r, str, sum
E:\zeta-monorepo\apps\backend\examples\profiler_demo_impl.py: i, list, print, range, result, sum, x
E:\zeta-monorepo\apps\backend\examples\simple_app_impl.py: bool, dict, getattr, isinstance, len, object, str
E:\zeta-monorepo\apps\backend\infra\embedding.py: Exception, ImportError, RuntimeError, ValueError, config, dict, e, float, getattr, len, list, self, str, text, texts
E:\zeta-monorepo\apps\backend\infra\vector_backends\base.py: NotImplementedError, float, int, list, tuple
E:\zeta-monorepo\apps\backend\infra\vector_backends\pgvector_pool_backend.py: Exception, RuntimeError, batch_size, bool, conn, conn_timeout, cur, dict, dsn, e, embedding_dim, embedding_model, filters, float, hasattr, ids, int, key, len, list, map, max_conn, min_conn, namespace, range, record, record_id, records, row, self, str, super, target_model, top_k, value
E:\zeta-monorepo\apps\backend\infra\vector_backends\pgvector_store.py: NotImplementedError, dim, float, int, list, self, session_factory, tuple
E:\zeta-monorepo\apps\backend\infrastructure\__init__.py: config, dict, self, str
E:\zeta-monorepo\apps\backend\infrastructure\scripts\safe\generate_phase3_work_orders.py: dict, f, isinstance, open, order, print, str
E:\zeta-monorepo\apps\backend\infrastructure\_scaffold\health_check.py: Exception, TimeoutError, any, bool, check_results, connection_factory, dict, e, enumerate, float, hasattr, i, int, isinstance, len, list, migration_checker, property, self, str, sum, super, timeout_seconds, type
E:\zeta-monorepo\apps\backend\infrastructure\_scaffold\repository_base.py: Exception, ValueError, bool, entity_id, entity_type, int, isinstance, list, self, str, super, type
E:\zeta-monorepo\apps\backend\infrastructure\_scaffold\unit_of_work.py: BaseException, Exception, bool, dict, exc_type, property, repo_type, self, super, type
E:\zeta-monorepo\apps\backend\ingest\__init__.py: list, str
E:\zeta-monorepo\apps\backend\integration\__init__.py: config, dict, self, str
E:\zeta-monorepo\apps\backend\integration\api_clients\base_client.py: Exception, ImportError, TimeoutError, ValueError, api_key, attempt, base_url, data, dict, e, endpoint, headers, int, max_retries, method, params, range, rate_limit, self, str, timeout
E:\zeta-monorepo\apps\backend\integration\api_clients\github_client.py: Exception, ImportError, RuntimeError, ValueError, attempt, base, base_url, body, client, dict, e, endpoint, float, head, int, isinstance, json_data, labels, list, max_retries, method, owner, range, repo, self, state, str, timeout, title, token
E:\zeta-monorepo\apps\backend\integration\api_clients\openai_client.py: Exception, api_key, base_url, bool, cat, dict, dimensions, e, flag, float, function_call, functions, int, kwargs, len, list, max_tokens, messages, model, organization, self, str, stream, super, temperature, text
E:\zeta-monorepo\apps\backend\integration\data_fetchers\base_fetcher.py: Exception, attempt, bool, cache_ttl, callable, concurrency, dict, e, enable_cache, float, int, isinstance, len, list, max_retries, min, name, param_generator, param_list, params, progress_callback, r, range, rate_limit, req_time, retry_delay, self, sorted, str, use_cache
E:\zeta-monorepo\apps\backend\integration\security\api_key_manager.py: Exception, action, auto_create_config, bool, char, chr, config_path, dict, e, encryption_key, enumerate, i, int, key, len, limit, list, metadata, new_key, ord, self, service, str, success, use_cache, use_environment
E:\zeta-monorepo\apps\backend\observability\alert_router.py: pagerduty_key, self, severity, slack_webhook, str, text, title
E:\zeta-monorepo\apps\backend\observability\otel_init.py: Exception, ImportError, app, bool, e, enable_db_instrumentation, enable_logging_instrumentation, environment, float, int, kwargs, name, otlp_endpoint, prometheus_port, sample_rate, self, service_name, service_version, str, tuple
E:\zeta-monorepo\apps\backend\observability\sla_slo_dashboard.py: float, max, slo, str, uptime
E:\zeta-monorepo\apps\backend\ollama\client.py: BaseException, Exception, ImportError, attempt, bool, config, data_any, dict, e, endpoint, exc, float, int, isinstance, json_data, kwargs, len, list, messages, method, model, model_count, ok_t, ok_v, options, payload, prompt, property, range, sc_t, sc_v, self, str, stream, tuple, type
E:\zeta-monorepo\apps\backend\ollama\monitoring.py: Exception, ImportError, app, args, bool, check_interval, count, dict, e, enabled, exc, float, health_data, health_response, int, isinstance, kwargs, len, method, ollama_client, raw_count, self, str, success, super, token_count
E:\zeta-monorepo\apps\backend\ollama\smoke_test.py: Exception, dict, e, int, isinstance, print, str
E:\zeta-monorepo\apps\backend\perf\admin.py: Exception, any, bool, check, dict, enabled, exc, float, int, label_key, label_value, len, list, metric_family, metric_name, p95_ms, p99_ms, round, sample, str, sum, tracing_enabled, x_admin_token
E:\zeta-monorepo\apps\backend\perf\config.py: bool, float, int, str
E:\zeta-monorepo\apps\backend\perf\enhanced_instrumentation.py: Exception, ImportError, TypeError, ValueError, active, app, c, call_next, current, duration_seconds, enumerate, exc, float, gen, generation, hasattr, idle, int, last, len, list, locals, query_type, request, str, task, user_agent, zip
E:\zeta-monorepo\apps\backend\perf\instrumentation.py: Exception, ImportError, app, call_next, exc, hasattr, len, request, str
E:\zeta-monorepo\apps\backend\perf\integration_manager.py: Exception, ImportError, abs, any, app, background_tasks, bool, dict, exc, float, imp, int, len, request, str, sum
E:\zeta-monorepo\apps\backend\perf\ml_optimization.py: abs, alert, anomaly_threshold, baseline, bool, cooldown_minutes, current_data, data_point, dict, dp, float, getattr, hasattr, int, len, list, max, metric_name, min, min_data_points, prediction_window_minutes, property, range, self, str, sum, trend, window_size, x, y, zip
E:\zeta-monorepo\apps\backend\perf\production_config.py: bool, dict, enabled, feature_name, float, getattr, hasattr, int, self, setattr, str
E:\zeta-monorepo\apps\backend\perf\smoke.py: Exception, bool, cli, client, code, config, dict, endpoint, error, errors, exc, f, float, i, int, isinstance, latencies, len, list, max, min, open, out, p, print, q, range, result, round, sorted, status_code, status_codes, str, sum, t, tuple
E:\zeta-monorepo\apps\backend\perf\success_metrics.py: Exception, ValueError, abs, all, automation_percent, baseline, baseline_alerts, baseline_cost, baseline_hours, baseline_minutes, bool, current, current_alerts, current_cost, current_hours, current_minutes, dict, engineering_hours, exc, f, float, imp, int, investment_details, len, list, lower_is_better, m, max, measurement_data, metric_name, metrics, open, progress, property, self, storage_path, str, sum
E:\zeta-monorepo\apps\backend\perf\tracing.py: Exception, ImportError, app, app_name, args, bool, exc, func, kwargs, name, object, operation_name, result, self, span, str
E:\zeta-monorepo\apps\backend\scripts\__init__.py: list, str
E:\zeta-monorepo\apps\backend\scripts\seed\seed_ai_roles.py: Exception, any, d, e, inherits, issue, len, name, p, perm, perm_name, perms, print, required_perms, role, role_name, service_role, set, sorted
E:\zeta-monorepo\apps\backend\storage\archive_storage.py: Exception, all, archive_dir, auto_cleanup, bool, chunk, classmethod, cls, compression_level, created_at, date_from, date_to, default_policy, dict, dir_path, e, f, f_in, f_out, file_path, int, iter, k, len, list, m, max_age_days, max_size_mb, metadata_file, open, original_path, query, restore_path, self, str, sum, tag, tags, tar, v, x
E:\zeta-monorepo\apps\backend\storage\backup_storage.py: Exception, all, backup, backup_dir, backup_name, backup_path, backup_type, backups, bool, chunk, classmethod, cls, compress, compressed, config_dir, created_at, db_url, dict, e, enumerate, exclude_patterns, f, file_path, i, int, iter, k, len, limit, line, list, m, max_backups, open, overwrite, pattern, restore_path, result, retention_days, self, str, sum, tag, tags, tar, tarinfo, v, verify_backups, x
E:\zeta-monorepo\apps\backend\storage\blob_storage.py: Exception, access_key, bool, bucket_name, byte_range, bytearray, bytes, chunk, chunk_size, content, content_length, content_type, dest_key, dict, endpoint_url, expires_in, fields, int, key, len, list, max, max_concurrency, max_content_length, max_keys, metadata, method, min, part_number, part_size, parts, prefix, rb, re, region, retry_attempts, secret_key, self, source_key, str, stream, tuple
E:\zeta-monorepo\apps\backend\storage\cache_storage.py: Exception, additional_seconds, bool, cache_entry, default_ttl, dict, int, isinstance, k, key, len, list, max, max_size, min, pattern, self, serialize, str, sum, tuple
E:\zeta-monorepo\apps\backend\storage\document_storage.py: any, author, bool, bytes, checksum, content, content_type, created_at, description, dict, doc, doc_id, document_id, filename, id, int, language, len, list, query, self, size, str, sum, tag, tags, title, updated_at
E:\zeta-monorepo\apps\backend\storage\file_service.py: Exception, OSError, allowed_extensions, bool, bytes, dict, dir_path, directory, expires_in, file_path, int, len, list, max_age_hours, max_file_size, metadata, new_filename, new_path, s3_bucket, self, source_metadata, str, use_s3
E:\zeta-monorepo\apps\backend\storage\local_storage.py: Exception, base_path, base_url, bool, bytes, content, dest_path, dict, directory, e, f, file_path, int, list, open, path, pattern, recursive, relative_path, self, source_path, str
E:\zeta-monorepo\apps\backend\storage\log_storage.py: Exception, ValueError, backup_count, bool, classmethod, cls, compress_rotated, dict, e, end_time, extra_data, f, f_in, f_out, function, hours, i, int, json_format, kwargs, len, level, limit, line_number, list, log_type, log_type_dir, logger_name, max_file_size, message, message_pattern, module, open, query, range, request_id, retention_days, reverse, self, str, user_id, x
E:\zeta-monorepo\apps\backend\storage\media_storage.py: Exception, ImportError, allowed_extensions, bool, chunk, classmethod, cls, created_at, custom_id, data, dict, e, error_msg, extensions, extract_metadata, f, generate_thumbnails, int, is_valid, iter, len, limit, list, m, max_file_size, offset, open, self, storage_dir, str, sum, tag_id, thumbnail_size, tuple, value, x
E:\zeta-monorepo\apps\backend\storage\s3_storage.py: Exception, ImportError, ValueError, access_key, bool, dest_key, dict, e, endpoint_url, etag, expiration, f, http_method, int, k, key, last_modified, len, list, max_age_days, max_concurrency, max_keys, metadata, multipart_chunksize, multipart_threshold, obj, open, page, prefix, region, secret_key, self, size, source_key, storage_class, str, sum, tag, tuple, upload_args, use_ssl, v
E:\zeta-monorepo\apps\backend\storage\session_storage.py: bool, created_at, data, default_ttl, dict, extend_ttl, i, int, key, last_accessed, len, list, max_sessions_per_user, range, self, session, session_id_length, str, sum, user_id, value, x
E:\zeta-monorepo\apps\backend\storage\temp_storage.py: Exception, OSError, auto_cleanup, base_dir, bool, bytes, cleanup_interval_minutes, content, dict, e, encoding, f, fd, float, int, isinstance, item, item_type, len, list, max_age_minutes, max_size_mb, metadata, property, purpose, self, str, suffix, x
E:\zeta-monorepo\apps\backend\storage\vector_storage.py: Exception, ValueError, batch_size, bool, classmethod, cls, created_at, dict, e, f, float, idx, include_vectors, index_type, int, key, len, limit, list, max_vectors, metadata_filter, offset, open, property, record_data, result, score, self, similarity_metric, storage_dir, str, top_k, tuple, value, vector, vector_dim, vid, x
E:\zeta-monorepo\apps\backend\storage\uploads\__init__.py: list, str
E:\zeta-monorepo\apps\backend\stubs\openai.py: staticmethod
E:\zeta-monorepo\apps\backend\tests\conftest.py: Exception, ImportError, ac, args, bool, chat_data, chat_id, chat_repository, conn, content, dict, getattr, int, kwargs, limit, list, message_repository, message_type, mock_client, self, session, str, super, title, user_id, user_repository
E:\zeta-monorepo\apps\backend\tests\test_agent_orchestrator_parallel.py: dict, isinstance, result, str
E:\zeta-monorepo\apps\backend\tests\test_agent_self_improvement.py: isinstance, str
E:\zeta-monorepo\apps\backend\tests\test_ai_runner_fix.py: FileNotFoundError, TimeoutError, cmd_list, len, mock_exec, mock_shell, mock_subprocess, self, str
E:\zeta-monorepo\apps\backend\tests\test_auto_updater.py: isinstance, list
E:\zeta-monorepo\apps\backend\tests\test_basic_structure.py: agent, print
E:\zeta-monorepo\apps\backend\tests\test_chat.py: ImportError, ValueError, abs, i, len, range
E:\zeta-monorepo\apps\backend\tests\test_check_duplicates.py: monkeypatch, str, tmp_path
E:\zeta-monorepo\apps\backend\tests\test_domain_event_aliases.py: any, e, user
E:\zeta-monorepo\apps\backend\tests\test_event_bus_fix.py: data, event, hasattr, len, str, super
E:\zeta-monorepo\apps\backend\tests\test_feedback_api.py: dict, str
E:\zeta-monorepo\apps\backend\tests\test_learning_api.py: body2, dict, i, len, range, str
E:\zeta-monorepo\apps\backend\tests\test_memory_normalization.py: agent, expected, imp, mt_in, str, t
E:\zeta-monorepo\apps\backend\tests\test_no_duplicate_concepts.py: AssertionError, f, list, str
E:\zeta-monorepo\apps\backend\tests\test_performance_advanced_caching.py: range, result
E:\zeta-monorepo\apps\backend\tests\test_plan_isolated.py: len, print, result, str
E:\zeta-monorepo\apps\backend\tests\test_scale_agent_use_case.py: ValueError
E:\zeta-monorepo\apps\backend\tests\test_security_basic.py: len, str
E:\zeta-monorepo\apps\backend\tests\test_security_system.py: ImportError, ValueError, all, event, len, user
E:\zeta-monorepo\apps\backend\tests\test_smoke.py: ImportError, agent, len, print
E:\zeta-monorepo\apps\backend\tests\test_start_all_tools.py: Exception, dict, isinstance, len, mock_popen, print, type
E:\zeta-monorepo\apps\backend\tests\api\test_federated_api.py: async_session, bind, conn, list, session, tables
E:\zeta-monorepo\apps\backend\tests\api\test_training_feedback.py: actor_id, artifact_key, feedback, int, rating, self, str
E:\zeta-monorepo\apps\backend\tests\config\test_settings_loader.py: env, expected_cls_name, str
E:\zeta-monorepo\apps\backend\tests\core\test_advanced_integration.py: all, i, isinstance, len, list, pattern, range, result, s, self
E:\zeta-monorepo\apps\backend\tests\core\test_autonomy_planner.py: Exception, ImportError, action, any, description, dict, isinstance, len, mock_llm_class, name, result
E:\zeta-monorepo\apps\backend\tests\core\test_memory_adapter_and_usecases.py: batch_size, bool, dict, embedding_model, filters, flt, hard, ids, int, len, list, namespace, records, self, str, target_model, top_k
E:\zeta-monorepo\apps\backend\tests\core\test_memory_service.py: int, isinstance, m, str
E:\zeta-monorepo\apps\backend\tests\core\test_memory_simple.py: abs, len
E:\zeta-monorepo\apps\backend\tests\core\test_self_improvement_v2.py: ValueError, abs, enabled, f, i, len, range, result, self, sum
E:\zeta-monorepo\apps\backend\tests\core\domain\aggregates\test_agent_aggregate_events.py: abs, any, evt, float, isinstance, len, str
E:\zeta-monorepo\apps\backend\tests\core\domain\aggregates\test_chat_aggregate_basic.py: any, evt
E:\zeta-monorepo\apps\backend\tests\core\domain\events\test_base_event.py: ValueError, str
E:\zeta-monorepo\apps\backend\tests\core\domain\events\test_rule_events_old.py: AttributeError, ValueError, abs, isinstance, str
E:\zeta-monorepo\apps\backend\tests\core\performance\test_optimization.py: abs, isinstance, len, mock_cpu_percent, mock_virtual_memory, result
E:\zeta-monorepo\apps\backend\tests\core\services\test_caching_decorators.py: ConnectionError, Exception, RuntimeError, ValueError, bool, data, delay, dict, float, hasattr, int, key, len, list, optional, range, self, should_error, size, str, sum, value, x, y
E:\zeta-monorepo\apps\backend\tests\core\services\test_cost_guard.py: Exception, ValueError, abs, all, dict, float, hasattr, i, int, isinstance, len, mock_config, mock_logger, r, range, self
E:\zeta-monorepo\apps\backend\tests\core\services\test_distillation_service.py: Exception, all, c, content, data, dict, float, hasattr, i, int, isinstance, len, list, message, mock_filters_class, mock_logger, mock_router, mock_router_class, mock_triage_class, model_name, pair, progress, range, self, str, student, task_id, teacher
E:\zeta-monorepo\apps\backend\tests\core\services\test_health_monitor.py: RuntimeError, ValueError, abs, i, isinstance, len, mock_gauge, mock_heal, mock_httpx, range, result
E:\zeta-monorepo\apps\backend\tests\core\services\test_performance_optimizer.py: Exception, str
E:\zeta-monorepo\apps\backend\tests\db\test_federated_repositories.py: async_session, bind, conn, isinstance, len, list, session, str, tables
E:\zeta-monorepo\apps\backend\tests\e2e\test_agent_lifecycle.py: Exception, ValueError, ac, agent, all, bool, content, dict, e, i, len, list, msg, next, range, role, self, set, str, title, turn, updated_agent, user
E:\zeta-monorepo\apps\backend\tests\e2e\test_chat_flow.py: Exception, agent, client, e, enumerate, i, len, msg, print, range, result, updated_agent, websocket
E:\zeta-monorepo\apps\backend\tests\e2e\test_full_conversation.py: Exception, ValueError, a, all, auth_result, conversation_result, created_agent, enumerate, i, isinstance, len, message, message_content, msg, q, result, str, user_msg
E:\zeta-monorepo\apps\backend\tests\e2e\test_integration_complete.py: hasattr, isinstance, mock_decode
E:\zeta-monorepo\apps\backend\tests\e2e\test_memory_operations.py: Exception, ValueError, all, any, cleanup_result, enumerate, i, isinstance, len, list, m, mem, range, result, scenario, second_agent, set
E:\zeta-monorepo\apps\backend\tests\e2e\test_minio_s3_adapter.py: Exception, b, bytes, c, ch, len, raw, session, sum
E:\zeta-monorepo\apps\backend\tests\e2e\test_performance.py: agent, all, delay, dict, email, float, i, int, isinstance, kwargs, len, list, max, min, print, query, r, range, request_id, result, self, size, str, sum, task_id
E:\zeta-monorepo\apps\backend\tests\e2e\test_user_workflows.py: ValueError, ac, bool, credentials, current_user, data, dict, e, email, expires_in_hours, field, hashed, int, k, new_password, old_password, password, result, self, str, token, u, updated_user, user, username, v, value
E:\zeta-monorepo\apps\backend\tests\e2e\test_ws_stress.py: Exception, any, bool, e, enumerate, float, i, int, isinstance, len, max, message, num_clients, print, property, r, range, self, size, str, sum, team_id, websocket
E:\zeta-monorepo\apps\backend\tests\entities\test_agent.py: abs
E:\zeta-monorepo\apps\backend\tests\fixtures\sample_data.py: dict, range, str
E:\zeta-monorepo\apps\backend\tests\infrastructure\test_cache.py: all, r, range, result
E:\zeta-monorepo\apps\backend\tests\infrastructure\_scaffold\conftest.py: Exception, bool, dict, exc, str, tmp_path
E:\zeta-monorepo\apps\backend\tests\integration\test_agents_basic.py: len
E:\zeta-monorepo\apps\backend\tests\integration\test_analytics.py: ValueError, abs, days, dict, e, ended_session, i, int, len, list, max, min, p, range, report_type, s, self, session, set, sorted, str, sum, user_event_list, x
E:\zeta-monorepo\apps\backend\tests\integration\test_api_endpoints.py: ac, agent, dict, isinstance, len, list
E:\zeta-monorepo\apps\backend\tests\integration\test_assistants_api.py: client, isinstance, len, list
E:\zeta-monorepo\apps\backend\tests\integration\test_auth_flow.py: ValueError, ac, current_user, dict, e, email, invalid_token, len, password, self, str, user
E:\zeta-monorepo\apps\backend\tests\integration\test_auth_scopes_sync.py: dict, isinstance, list, set, str, token, user
E:\zeta-monorepo\apps\backend\tests\integration\test_automation_api.py: Exception, client, len, mock_factory_class, safety_result
E:\zeta-monorepo\apps\backend\tests\integration\test_database.py: Exception, async_session, conn, i, int, isinstance, len, range, result, session, session_id
E:\zeta-monorepo\apps\backend\tests\integration\test_external_services.py: Exception, FileNotFoundError, ValueError, any, bool, bucket, bytes, d, dict, download_result, e, embedding_result, enumerate, event_type, f, float, hash, i, int, isinstance, len, limit, list, max, model, path, payload, prefix, r, range, result, self, set, sorted, storage_result, str, sum, upload_result, url, value, word, x
E:\zeta-monorepo\apps\backend\tests\integration\test_federated_api_routes.py: hasattr, isinstance, list
E:\zeta-monorepo\apps\backend\tests\integration\test_federated_minimal.py: abs, float, int, isinstance, len, list, n, rej, rid, str, tuple, vec
E:\zeta-monorepo\apps\backend\tests\integration\test_files_streaming.py: bool, bytearray, bytes, chunk, client, content_length, dict, end, file, file_id, getattr, int, len, min, n, object, self, start, str
E:\zeta-monorepo\apps\backend\tests\integration\test_file_operations.py: Exception, FileNotFoundError, ac, all, bool, bytes, dict, e, expected_type, file, filename, i, isinstance, len, range, self, str
E:\zeta-monorepo\apps\backend\tests\integration\test_meta_and_health.py: ac, int, isinstance, str
E:\zeta-monorepo\apps\backend\tests\integration\test_system_integration.py: ValueError, agent, agent_result, component, dict, enumerate, file_result, i, initial_message, int, j, len, message_content, range, self, session, set, str, sum, user, user_session, zip
E:\zeta-monorepo\apps\backend\tests\integration\test_websockets.py: ConnectionError, all, bool, conn_ids, content, dict, enumerate, exclude_connection, i, int, len, list, msg, offline_user, ping_result, pong_result, range, reason, room_connections, self, sender_name, sent_msg, str, sum, user
E:\zeta-monorepo\apps\backend\tests\knowledge\test_graph_service.py: entity, i, len, path, range, self, set
E:\zeta-monorepo\apps\backend\tests\llm\test_openai_async_adapter.py: RuntimeError, delta, dict, list, opts, part, self, str, stream, tuple
E:\zeta-monorepo\apps\backend\tests\memory\test_memory_manager_summarization.py: any, c, content, i, isinstance, list, m, mem, range, s, self, str, ts
E:\zeta-monorepo\apps\backend\tests\memory\test_search_diverse_selection.py: any, content, importance, len, m, str, v
E:\zeta-monorepo\apps\backend\tests\mocks\mock_agent_repository.py: agent, agent_id, bool, capability, dict, int, len, limit, name, offset, self, status, str
E:\zeta-monorepo\apps\backend\tests\performance\test_load.py: Exception, dict, e, error, float, i, int, len, print, property, range, result, self, session, str, sum, user_id
E:\zeta-monorepo\apps\backend\tests\performance\test_performance.py: Exception, ValueError, all, base_url, bool, dict, e, float, i, int, isinstance, len, list, load_result, max, min, print, r, range, request_id, response, response_time, result, self, session, sorted, str, tuple
E:\zeta-monorepo\apps\backend\tests\performance\test_stress.py: Exception, TimeoutError, agent, auth_result, base_delay, chat_result, dict, e, email, float, hasattr, i, int, isinstance, kwargs, len, max, mem_id, memory_id, memory_result, msg_id, op_id, print, r, range, request_id, result, self, set, str, sum, user, workflow_id
E:\zeta-monorepo\apps\backend\tests\rag\__init__.py: list, str
E:\zeta-monorepo\apps\backend\tests\smoke\test_simple_server.py: Exception, RuntimeError, e, endpoint, tuple
E:\zeta-monorepo\apps\backend\tests\standalone\__init__.py: list, str
E:\zeta-monorepo\apps\backend\tests\tools\test_conformance.py: Exception, RuntimeError, any, bool, cls, data, dict, int, isinstance, issue, len, list, protocol, str, x, y
E:\zeta-monorepo\apps\backend\tests\tools\test_missing_code_audit.py: any, content, i, isinstance, len, list, name, str, tmp_path
E:\zeta-monorepo\apps\backend\tests\unit\test_agents.py: ValueError, agent, isinstance, len
E:\zeta-monorepo\apps\backend\tests\unit\test_agent_orchestrator_parallel.py: agent, agent_id, dict, len, payload, r, result, str, task_type
E:\zeta-monorepo\apps\backend\tests\unit\test_auth_suggestions.py: str, suggest_actions_for_user, user
E:\zeta-monorepo\apps\backend\tests\unit\test_automation_basic.py: isinstance, len, result
E:\zeta-monorepo\apps\backend\tests\unit\test_blob_storage_multipart.py: bytes, calls, clen, content, int, len, list, min, monkeypatch, p, part_number, range, sorted, str, sum, tuple
E:\zeta-monorepo\apps\backend\tests\unit\test_config_entity.py: ValueError, abs, isinstance, len, namespace, str
E:\zeta-monorepo\apps\backend\tests\unit\test_entities.py: content, isinstance, len, relevance_score, self, str, timestamp
E:\zeta-monorepo\apps\backend\tests\unit\test_entities_isolated.py: Exception, ImportError, agent, e, e2, isinstance, print, str, user
E:\zeta-monorepo\apps\backend\tests\unit\test_events.py: AttributeError, TypeError, abs, all, e, i, isinstance, len, range, sorted, str
E:\zeta-monorepo\apps\backend\tests\unit\test_event_bus.py: Exception, RuntimeError, data, dict, event_type, i, range, self, str, super
E:\zeta-monorepo\apps\backend\tests\unit\test_federated_orchestrator.py: async_session, bind, conn, list, session, tables
E:\zeta-monorepo\apps\backend\tests\unit\test_federated_privacy_and_validation.py: abs, kwargs, type
E:\zeta-monorepo\apps\backend\tests\unit\test_federated_repositories.py: conn, isinstance, len, session, str, test_db_session
E:\zeta-monorepo\apps\backend\tests\unit\test_gpt4o_trainer.py: has, int, self, str
E:\zeta-monorepo\apps\backend\tests\unit\test_inmemory_audit_repository.py: len
E:\zeta-monorepo\apps\backend\tests\unit\test_inmemory_base_repository.py: created_id, id_, int, len, self, str, value, x
E:\zeta-monorepo\apps\backend\tests\unit\test_learning.py: session
E:\zeta-monorepo\apps\backend\tests\unit\test_memory.py: i, isinstance, len, range, str
E:\zeta-monorepo\apps\backend\tests\unit\test_orchestrator_rule_permission.py: monkeypatch, user
E:\zeta-monorepo\apps\backend\tests\unit\test_permissions_vo.py: p, set
E:\zeta-monorepo\apps\backend\tests\unit\test_plan.py: ValueError, e, isinstance, len, s, set, sorted, str
E:\zeta-monorepo\apps\backend\tests\unit\test_planning.py: len, result, str
E:\zeta-monorepo\apps\backend\tests\unit\test_privacy_engine.py: isinstance, str
E:\zeta-monorepo\apps\backend\tests\unit\test_rag_chunker_sentences.py: all, c, len
E:\zeta-monorepo\apps\backend\tests\unit\test_rag_services.py: c, float, int, len, s, str
E:\zeta-monorepo\apps\backend\tests\unit\test_repositories.py: Exception, agent, bool, data, dict, found_user, hasattr, id, int, isinstance, key, kwargs, len, limit, list, min, range, result, self, session, setattr, str, updated_user, user, value
E:\zeta-monorepo\apps\backend\tests\unit\test_rule_engine.py: ValueError, any, dict, ok, step, str, v, violations
E:\zeta-monorepo\apps\backend\tests\unit\test_rule_engine_service.py: len
E:\zeta-monorepo\apps\backend\tests\unit\test_sanitize_dependency.py: blacklist, data, dict, list, req, str, whitelist
E:\zeta-monorepo\apps\backend\tests\unit\test_scaffold_asr.py: any, isinstance, list, s
E:\zeta-monorepo\apps\backend\tests\unit\test_services.py: ValueError, agent, agent_repo, chat_repo, dict, len, self, str, user, user_repo
E:\zeta-monorepo\apps\backend\tests\unit\test_session_entity.py: ValueError, isinstance, len, str
E:\zeta-monorepo\apps\backend\tests\unit\test_specifications.py: active_agent, admin_user, all, bad_agent, created_at, empty_agent, good_agent, hasattr, heavy_user, i, inactive_agent, inactive_session, is_active, limit_user, limited_user, long_agent, normal_user, old_session, permissions, range, read_user, recent_session, request_count, reserved_agent, self, short_agent, valid_agent
E:\zeta-monorepo\apps\backend\tests\unit\test_training_models.py: dict, isinstance
E:\zeta-monorepo\apps\backend\tests\unit\test_upcaster.py: ValueError, new_payload, new_version, payload, sorted
E:\zeta-monorepo\apps\backend\tests\unit\test_user_entity.py: ValueError, e, isinstance, len, list
E:\zeta-monorepo\apps\backend\tests\unit\test_use_cases.py: Exception, ValueError, all, bool, callable, dict, expected_agent, hasattr, isinstance, len, list, original_agent, step, str
E:\zeta-monorepo\apps\backend\tests\unit\test_value_objects.py: ValueError, abs, bool, isinstance
E:\zeta-monorepo\apps\backend\tests\unit\test_vector_search_service.py: len
E:\zeta-monorepo\apps\backend\tests\unit\test_websockets.py: Exception, client
E:\zeta-monorepo\apps\backend\tests\unit\test_websocket_schemas.py: dict, isinstance, list, model
E:\zeta-monorepo\apps\backend\tests\unit\test_workflow_entity.py: ValueError, a_id, b_id, c_id, d_id, isinstance, len, name, type
E:\zeta-monorepo\apps\backend\tests\unit\test_workflow_node_vo.py: AttributeError, ValueError, node_type
E:\zeta-monorepo\apps\backend\tests\unit\test_zero_trust_middleware.py: body, bool, dict, require_sig, str
E:\zeta-monorepo\apps\backend\tests\unit\agents\test_agent_aggregate.py: ValueError, isinstance, len, str
E:\zeta-monorepo\apps\backend\tests\unit\agents\test_agent_management.py: ValueError, activated_agent, deactivated_agent, existing_agent, len, result, updated_agent
E:\zeta-monorepo\apps\backend\tests\unit\auth\test_auth_use_cases.py: result, user
E:\zeta-monorepo\apps\backend\tests\unit\core\test_observability_logger.py: list, record, self, super
E:\zeta-monorepo\apps\backend\tests\unit\core\test_validation_helpers.py: dict, int, str
E:\zeta-monorepo\apps\backend\tests\unit\core\async_templates\test_async_service.py: AssertionError, Exception, RuntimeError, data, e, int, isinstance, str
E:\zeta-monorepo\apps\backend\tests\unit\core\domain\test_aggregate_base.py: AssertionError, Exception, bool, e, isinstance, self, str, super
E:\zeta-monorepo\apps\backend\tests\unit\core\domain\test_chat_aggregate.py: AssertionError, Exception, e, isinstance, len
E:\zeta-monorepo\apps\backend\tests\unit\core\utils\test_configuration_manager.py: AssertionError, ValueError, conf, data, dict, str, tmp_path
E:\zeta-monorepo\apps\backend\tests\unit\core\utils\test_performance_monitor.py: dict, int, isinstance
E:\zeta-monorepo\apps\backend\tests\unit\domain\aggregates\test_agent_aggregate.py: ValueError, abs, len, mock_get_logger, str
E:\zeta-monorepo\apps\backend\tests\unit\domain\aggregates\test_workflow_aggregate.py: len, str, valid_status
E:\zeta-monorepo\apps\backend\tests\unit\infrastructure\test_async_redis_cache_skeleton.py: all, dict, isinstance, r, range, str
E:\zeta-monorepo\apps\backend\tests\unit\memory\test_memory_use_cases.py: ValueError, len, result
E:\zeta-monorepo\apps\backend\tests\unit\planning\test_planning_use_cases.py: ValueError, len, result
E:\zeta-monorepo\apps\backend\tests\use_cases\test_orchestrate_team.py: Exception, StopAsyncIteration, ValueError, agent, any, e, event, len, range, self, set, str
E:\zeta-monorepo\apps\backend\tests\utils\test_helpers.py: ValueError, args, bytes, client, conn, content, coro, datetime_string, dict, expected_fields, expected_status, expected_value, field, filename, getattr, int, kwargs, model_instance, response, return_value, self, session, str, tuple, uuid_string
E:\zeta-monorepo\apps\backend\tools\implements.py: cls, impl, impl_cls, list, module, proto, proto_cls, protocol, str, tuple, type
E:\zeta-monorepo\apps\backend\tools\ports_tools.py: Exception, UTC, any, asdict, bool, c_names, cls, cm, cur_keys, current, dict, diffs, filepath, get_type_hints, getattr, hash, int, isinstance, issues, k, len, list, member, methods, mi, n, name, node, o_names, obj, old_keys, om, p, package, path, protos, reversed, seg, set, snapshot_data, sorted, str, tuple, version
E:\zeta-monorepo\apps\backend\tools\scaffold\scaffold_service.py: Exception, RuntimeError, bool, cap_id, dep, dict, dry_run, entries, f, group, hook, list, open, requirement, self, steps, str
E:\zeta-monorepo\apps\backend\trainer\distill_gpt5.py: Exception, ValueError, bool, config, dataset_name, description, dict, e, enumerate, ex, example, examples, float, i, int, isinstance, len, list, marker, max, min, openai_client, prompt, ref, result, self, source_type, str, sum, term, tuple
E:\zeta-monorepo\apps\backend\trainer\finetune_llama4.py: ImportError, ValueError, adapter_path, bool, config, dataset_id, dataset_path, do_sample, enumerate, examples, f, float, getattr, i, int, k, len, list, max_length, open, output_dir, print, prompt, run_name, self, str, temperature, test_prompts, tuple, v, zip
E:\zeta-monorepo\apps\backend\trainer\model_matrix.py: bool, dict, float, input_tokens, int, list, local_only, m, max_cost_tier, max_latency_ms, model_name, name, output_tokens, provider, require_local, role, self, sorted, str, task
E:\zeta-monorepo\apps\backend\trainer\datasets\registry.py: Exception, RuntimeError, ValueError, dataset_data, dataset_id, description, dict, e, f, float, int, len, list, min_quality, name, open, property, quality, registry_path, self, sorted, source_type, source_url, stage, str, sum, training_job_id, x
E:\zeta-monorepo\apps\backend\trainer\datasets\__init__.py: Exception, RuntimeError, ValueError, config, dict, e, getattr, int, isinstance, level, name, str
E:\zeta-monorepo\apps\backend\trainer\deployment\__init__.py: list, str
E:\zeta-monorepo\apps\backend\trainer\evaluators\gpt5_verifier.py: Exception, ImportError, ValueError, any, benchmark_tasks, bool, dict, e, enumerate, float, i, int, issues, len, list, model_name, model_path, name, openai_client, prompt, property, quality_threshold, s, self, str, sum, task_data, task_id, threshold, tuple, verifier_model, word
E:\zeta-monorepo\apps\backend\trainer\ingest\__init__.py: list, str
E:\zeta-monorepo\apps\backend\trainer\triage\__init__.py: list, str
E:\zeta-monorepo\apps\backend\trainer\workflows\trainer_workflow.py: Exception, bool, config_dict, d, dataset_lineage, dict, e, float, int, len, list, max, self, source, str, sum
E:\zeta-monorepo\apps\backend\training\gpt4o_trainer.py: Exception, NotImplementedError, RuntimeError, SYS_CTX, TRAINER_POLICY, TimeoutError, ValueError, attempt, bool, concurrency_semaphore, d, dict, e, e2, exc, fetcher, float, int, isinstance, len, limit, list, llm, llm_text, logger, max, mentor_cfg, prompt_lines, query, r, range, rules, self, store, str, telemetry, tuple, usage_tokens
E:\zeta-monorepo\apps\backend\training\__init__.py: Exception, RuntimeError, ValueError, config, dict, e, getattr, int, isinstance, level, name, str
E:\zeta-monorepo\apps\backend\triage\safety_filters.py: bool, c, data, float, item, keyword, len, list, max, min, pattern, str, sum, text, tuple, x
E:\zeta-monorepo\apps\backend\workflows\trainer_pipeline.py: Exception, ImportError, bool, dict, e, enumerate, i, len, step, str
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\biplist\__init__.py: AttributeError, Exception, NameError, OverflowError, TypeError, ValueError, asReference, as_number, bin, binary, bool, bytes, cls, count, description, dict, e, enumerate, f, field, fileOrStream, float, for_binary, hasattr, id, incr, int, isNew, isinstance, k, klass, len, length, list, objRef, object, objectNumber, open, other, pow, property, repr, self, set, setReferencePosition, sorted, str, stream, super, td, tuple, type
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\dmgbuild\badge.py: CFURLCreateWithFileSystemPath, CGBitmapContextCreate, CGBitmapContextCreateImage, CGColorSpaceCreateWithName, CGImageDestinationAddImage, CGImageDestinationCreateWithURL, CGImageDestinationFinalize, CGImageSourceCopyPropertiesAtIndex, CGImageSourceCreateImageAtIndex, CGImageSourceCreateWithURL, CGImageSourceGetCount, CIContext, CIFilter, CIImage, CIVector, NSAffineTransform, badge_file, float, kCFURLPOSIXPathStyle, kCGColorSpaceGenericRGB, kCGImageAlphaPremultipliedLast, kCIInputAspectRatioKey, kCIInputBackgroundImageKey, kCIInputImageKey, kCIInputScaleKey, kCIOutputImageKey, m, n, output_file, range
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\dmgbuild\colors.py: Exception, KeyError, ValueError, context, float, int, len, min, self, staticmethod
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\dmgbuild\core.py: Alias, AttributeError, Bookmark, DSStore, Exception, ImportError, NameError, column, d, enumerate, float, k, len, str, v, x
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\ds_store\buddy.py: AttributeError, Exception, IndexError, NameError, TypeError, ValueError, allocator, args, bytearray, bytes, classmethod, data_or_format, enumerate, file_or_name, fl, isinstance, k, list, magic1, magic2, max, n, offset2, range, rblk, s, self, size_or_format, str, sum, the_file, whence, x
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\ds_store\store.py: KeyError, NameError, StopIteration, TypeError, ValueError, abs, b, block, block_seek, bmk, bool, bytearray, bytes, bytesData, classmethod, cmp, entry, file_or_name, internal, isinstance, largest, left, len, level, list, m, mode, number, other, p, parent, parent_count, plist, point, print, range, right, rootblk, rp, s, self, split, staticmethod, str, type, x, y, zip
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\mac_alias\alias.py: Exception, NameError, ValueError, appinfo, appleshare_info, attribute_flags, b, bytes, classmethod, cls, crdate_hr, dialup_info, disk_image_alias, disk_type, disktype, extra, folder_name, fs_id, fs_type, fstype, getattr, head, int, isinstance, len, levels_from, levels_to, list, mac_epoch, name, network_mount_info, property, recsize, repr, s, self, server, t, tail, target, user, user_home_prefix_len, version, volattrs, voldate_hr, volfsid, volume, zone
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\mac_alias\bookmark.py: ImportError, KeyError, NameError, ValueError, aoff, baseenc, bytearray, bytedata, bytes, classmethod, cls, default, dict, elt, eltoff, enumerate, eoff, eoffset, filename, float, hdrsize, head, ienc, int, isinstance, item, k, keyoff, len, length, list, magic, n, ndx, nexttoc, o, ord, osx_epoch, path, print, property, range, relenc, reloff, repr, self, size, str, tail, tid, toccount, tocid, tocmagic, tocsize, typecode, v, valoff, value, voffset, x
E:\zeta-monorepo\apps\desktop\node_modules\dmg-builder\vendor\mac_alias\osx.py: AttributeError, KeyError, OSError, POINTER, Structure, Union, ValueError, byref, bytes, c_byte, c_char, c_char_p, c_int, c_long, c_longlong, c_short, c_uint, c_ulong, c_ulonglong, c_ushort, c_void_p, cdll, create_string_buffer, entry, hasattr, isinstance, len, list, options, sizeof, ts, unix_epoch
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\update-gyp.py: Exception, directory, f, in_file, member, members, numeric_owner, open, path, print, tar, tar_ref, target, tmp_dir
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\gyp_main.py: Exception, stdout
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\test_gyp.py: arg, directory, f, files, fmt, formats, len, line, option, p, print, root, self, sorted, str, test, verbose
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\common.py: Exception, KeyError, OSError, args, attrname, default, e, filename, flavor, follow_path_symlink, fully_qualified_target, func, generator_flags, getattr, graph, i, idfun, isinstance, item, iterable, last, len, list, msg, neighbor, next_item, node, nodes, open, other, out_path, p, params, parsed_build_file, parsed_toolset, prev_item, qualified_list, roots, s, self, seq, set, sorted, source_file, str, t, target, target_dicts, target_list, tmp_fd, tool_file, var, var_list, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\common_test.py: argument, expected, node, param, self, tuple
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\easy_xml.py: Exception, OSError, at, attr, child_spec, content, dict, encoding, file, isinstance, level, map, match, open, path, pretty, sorted, specification, str, val, value, win32, x, y
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\easy_xml_test.py: self
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\flock_tool.py: Exception, args, cmd_list, getattr, len, lockfile, name_string, self
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\input_test.py: dependency, dependent, len, node, self, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\mac_tool.py: Exception, app_identifier_prefix, bool, bucket, bundle_identifier, c, cmd_list, copy_headers, dict, e, entitlements, enumerate, error, file, file_name, fp, framework, getattr, i, in_file, info_plist, inputs, isinstance, k, len, line, link, list, lockfile, map, max, module_file, name_string, open, ord, output, output_name, overrides, plist_path, preserve, print, profile, provisioning, provisioning_data, range, self, str, team_id, team_identifier, temp, v, value, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSNew.py: any, build_file, config_platform_overrides, dependencies, entries, fixpath_prefix, g, i, isinstance, list, msbuild_toolset, name, other, path, seed, self, set, sorted, spec, str, subentry, v, variants, version, websiteProperties, writer, x, y
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSProject.py: ValueError, config, config_name, config_type, contents, dict, f, files, guid, isinstance, list, name, path, platform, project_path, self, t, version
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSSettings.py: ValueError, e, error_msg, flag, i, int, isinstance, label_list, len, list, msbuild_base, msbuild_name, msbuild_settings_name, msbuild_tool_name, msvs_name, msvs_setting, msvs_settings, msvs_settings_name, msvs_tool_name, msvs_tool_settings, msvs_value, name, new, old, print, self, setting, setting_type, settings, settings_name, stderr, str, tool, tool_name, validators, value
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSSettings_test.py: expected, line, self, sorted
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSToolFile.py: additional_dependencies, cmd, description, extensions, name, outputs, self, tool_file_path
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSUserFile.py: args, config_name, dict, isinstance, key, name, path, self, sorted, spec, user_file_path, val, version, working_directory
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSUtil.py: config_name, deptype, i, in_dict, int, key, len, number, pos, range, sorted, str, suffix, t, target_dicts, target_list, vars
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\MSVSVersion.py: Exception, ImportError, OSError, ValueError, allow_fallback, args, default_toolset, description, e, enumerate, flat_sln, float, force_express, hkey, index, key, name, project_version, root, sdk_based, self, short_name, solution_version, str, subkey, sysdir, target_arch, tool, uses_vcxproj, v, value, versions_to_check
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\msvs_emulation.py: Exception, a, action, allow_isolation, any, append, base_path, base_to_build, build_dir, call, callable, cflags_c, cflags_cc, command, configname, default, default_variables, dict, e, elem, envvar, envvar_dict, expand_special, expansions, extension, field, filename, filter, flag, float, getattr, gyp_to_build_path, gyp_to_ninja, gyp_to_ninja_path, gyp_to_unique_output, hasattr, hex, i, implicit, include, include_dirs, input, int, intermediate_manifest, is_executable, isinstance, key, len, libraries, line, list, manifest_base_name, manifest_flags, midl_include_dirs, mo, name, new, obj_ext, old, open_out, output_of_set, output_of_where, params, parent, path, path_to_base, pch_source_ext, prefix, required, rule, s, self, setattr, settings, source, sources, str, toplevel_build_dir, tuple, value, var, w, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\ninja_syntax.py: command, depfile, deps, depth, description, dict, filter, generator, i, indent, input, inputs, isinstance, iter, key, len, line, list, map, name, output, path, paths, restat, rspfile, rspfile_content, s, self, string, val, variables, width, word
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\simple_copy.py: Exception, KeyError, a, bool, dict, float, int, key, list, str, type, value, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\win_tool.py: Exception, arch, arg, assert_f, dest, dict, dlldata, embed_manifest, f, filename, flags, fn, getattr, h, idl, iid, intermediate_manifest, item, k, ldcmd, len, line, list, manifest_path, manifests, mt, name_string, open, our_f, outdir, output, path, print, proxy, rc, resname, resource_name, resource_path, rspfile, self, source, str, tlb, use_separate_mspdbsrv, v, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\xcodeproj_file.py: KeyError, NotImplementedError, TypeError, ValueError, a_path, all, any, attributes, chr, component, config, configuration, descendant, dict, do_copy, e, enumerate, file, file_group, filetype, force_outdir, force_prefix, group_func, hashable, hierarchical, id, index, input_path, input_string, int, is_list, is_required, isinstance, item, item_key, item_value, len, line, list, match, object, ord, overwrite, parent_ext, parent_root, phase, properties, property, property_type, range, recurse, recursive, reference, remote_object, rp, s, self, set, settings, sorted, str, symroot, t, tabs, target, tuple, type, variant, x, xche_hashable, y
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\xcode_emulation.py: KeyError, NotImplementedError, arch, archs_including_64_bit, basename, built_products_dir, cmdlist, cond_key, config_name, configuration, dependee, dict, directory, e, expansions, flag_pattern, flags, flavor, format_str, framework, global_dict, gyp_path_to_build_output, gyp_path_to_build_path, gyp_to_build_path, infoitem, int, iphoneos, iphonesimulator, isinstance, k, len, library_path, libtoolflag, line, lst, mac, match, node, obj, objs, output_binary, postbuild, prefix, print, product_dir, quiet, res, resources, reversed, rpath, sdk, self, set, setting, simulator_config_dict, sorted, sources, srcroot, target_dict, target_dicts, test_key, to_replace, v, valid_archs, value, x, xcode_build, xcode_settings, xcode_version, zip
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\xcode_ninja.py: OSError, action, build_file_ext, build_file_root, config, data, e, file, gyp_dict, gyp_name, input_file, int, key, old_qualified_target, old_spec, old_target, open, output_file, params, set, sorted, target, target_dict, target_dicts, target_list
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\xml_fix.py: a_name, addindent, indent, is_attrib, newl, node, self, sorted, writer
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\__init__.py: Exception, ValueError, args, build_file, build_files_arg, check, circular_check, conf, data, depth, e, file, flag, flag_value, flat_list, format, getattr, globals, home_var, index, int, isinstance, item, key, kw, len, locals, message, metadata, mode, name, name_value_list, option, options, predicate, print, range, self, set, sorted, str, targets, val
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\analyzer.py: Exception, OSError, ValueError, action, add_if_no_ancestor, additional_compile_target_names, all_targets, back_dep_target, bool, build_files, created_dep_target, created_target, data, default_variables, dep, dep_target, dict, dirname, e, files, frozenset, include, include_file, isinstance, len, list, mapping, name, names, open, params, possible_targets, print, rule, self, set, str, target_dict, target_dicts, target_list, targets, unused, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\android.py: action, actions, base_name, build_file, cflags, config, configname, copies, data, dep, dict, dirname, dynamic_libs, expansion, ext, f, filter, flag, include_file, included_file, includes_from_cflags, input, int, isinstance, k, ldflags_libs, len, lib, libs, list, local_pathify, map, open, out, output_filename, params, print, qualified_target, quoter, root, rule, rule_source, rule_source_basename, rule_source_dirname, rule_source_root, rules, self, set, sorted, source, static_libs, target_dicts, target_list, template, text, toolset, v, value, write_alias_target, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\cmake.py: KeyboardInterrupt, a, action, actions, any, arglist, build_file, command, config_name, config_to_use, configurations, copies, count, data, default_variables, dep, deps, dir, directory, e, enumerate, ext, extra_dep, extra_source, extra_target_name, filename, gyp_file, gyp_target_name, gyp_target_toolset, include, int, isinstance, key, len, lib, lib_dep, library_dir, modifier, o, open, out, output_index, params, path_to_gyp, prefix, prepend, print, project_target, property_modifier, property_name, qualified_target, rawDep, real_source, rel_path, rule, rule_source, rule_source_basename, rule_source_dirname, rule_source_ext, rule_source_root, rules, self, sep, set, source_name, src, str, target_dicts, target_list, value, var, variable, variable_name, xcode_setting, xcode_value, zip
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\compile_commands_json.py: build_file, configuration, configuration_name, data, default_variables, dict, open, params, qualified_target, s, source, target, target_dicts
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\dump_dependency_json.py: KeyError, default_variables, dep, dirname, key, len, open, params, print, target_dicts, target_list, unused, val
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\eclipse.py: NotImplementedError, action, build_file, cflag, compiler_include, config_name, cpp_line, data, default_variables, define, dirname, input_, kind, lang, len, line, list, open, out, out_name, params, path, paths, set, shared_intermediate_dir, sorted, target_dicts, target_list, target_name, toplevel_dir, unused, value
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\gypd.py: data, input_file, open, params, qualified_target, target_list, v
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\gypsh.py: data, repr, sorted, target_dicts, target_list, v
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\make.py: ac, additional_settings, any, base_name, bf, bool, build_dir, bundle_deps, c, comment, configname, configurations, copies, data, defines, dep, dirname, e, enumerate, expansion, extra_env, filepath, filter, force, gch, getattr, i, include_file, included_file, input, int, k, key, lang, lang_flag, len, library_dir, link_dep, list, map, module_name, o, obj, open, order_only, out, output_filename, p, part_of_all, pch_commands, phony, postbuild, precompiled_header, prefix, print, qualified_target, quote, quoter, r, res, resources, rule, rule_source, rule_source_basename, rule_source_dirname, rule_source_root, rules, self, set, sidedeck, sorted, source, str, target_dicts, target_list, targets, template, text, toolset, v, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\msvs.py: KeyError, TypeError, ValueError, a, actions_dict, all, base_path, bucket, build_file_ext, build_file_root, c, c_data, child, config_data, cpy, cygwin_shell, d, data, default_variables, dependency, dict, do_setup_env, dpart, entry, excluded, extension, filters_path, flat, folder, g, gyp_file_name, has_input_path, ignored_setting, input_file, int, is_msbuild, isinstance, iter, k, key, label, len, list, match, msbuild, msbuild_toolset, name, next, node, o, od, only_if_unset, ord, params, parent, parent_filter_name, paths, print, project, project_file_name, project_path, props, props_file, qualified_target, r, range, reversed, root_dir, rule, self, separator, set, setting, sorted, source_files, source_tree, sources_array, sources_set, src, str, target, target_dicts, target_list, targets_file, tf, tool_name, trigger_file, type, v, ver, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\msvs_test.py: self
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\ninja.py: Exception, KeyboardInterrupt, TypeError, action, actions, additional_settings, any, arg, arg_name, arglist, argument, base_dir, binary, binary_type, bool, bundle_depends, config_name, configurations, copies, data, dep, dirname, e, embed_manifest, f, fallback, filter, flags, gch, getattr, i, int, intermediate_manifest, is_command_start, is_empty, isinstance, item, k, key, lang, lang_flag, ldcmd, len, library_dir, line, list, manifest_files, max, meminfo, message, min, mode, new_dep, ninja_file, o, open, ord, order_only, output_binary, output_file_name, p, params, path_dir, precompiled_header, predepends, print, product_dir, prog, qualified, qualified_target, rel, repr, res, resources, root, rule, rules, self, set, settings_key, short_name, sorted, str, target_list, to_copy, toolset, toplevel_dir, v, var, verb, x
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\ninja_test.py: self
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\xcode.py: Exception, KeyError, OSError, bf_tgt, build_file, build_file_dict, build_file_ext, build_file_root, concrete_output_by_rule_source, concrete_output_index, concrete_outputs, config, config_name, configuration_name, copy_group, data, define, dependency, e, enumerate, expansions, file, frozenset, group, gyp_path, hasattr, header, include_dir, included_file, int, is_public, isinstance, item, key, len, library, match, new_pbxproj_path, open, other_pbxproject, output, output_fd, params, path, pbxtd, postbuild, prerequisite, prerequisite_index, print, resource, resource_extension, rule, rule_source, rule_source_basename, rule_source_dirname, rule_source_ext, rule_source_root, run_test_target, s, self, sorted, source, source_extension, str, target, target_dicts, target_list, to_replace, val, variable, x, xck, xcv, zip
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\pylib\gyp\generator\xcode_test.py: self
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\tools\graphviz.py: build_file, dst, dsts, filename, len, list, open, print, suffix, target_name, targets
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\tools\pretty_gyp.py: brace, brace_diff, char, input, len, matchobj, open, print, zip
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\tools\pretty_sln.py: dep, dep_list, deps, dict, len, line, open, print, project, project_info, solution_file, sorted
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\gyp\tools\pretty_vcproj.py: argv, child2, configuration_node, current_directory, current_vsprops, dict, filenames, i, indent, key, len, new_node, node, node1, node2, print, range, sorted, sub_node, value, value2, vcproj, x, y
E:\zeta-monorepo\apps\desktop\node_modules\node-gyp\test\fixtures\test-charmap.py: AttributeError, NameError, print, reload
E:\zeta-monorepo\docs\examples\agent_creation.py: Exception, agent_id, api_key, base_url, bool, description, e, float, int, len, list, name, print, self, str, updates
E:\zeta-monorepo\docs\examples\python-assistant\turbo_assistant.py: base_url, int, max_tokens, mode, print, prompt, resp, self, str
E:\zeta-monorepo\extension\.vscode-test\vscode-win32-x64-archive-1.103.2\resources\app\node_modules\katex\src\fonts\generate_fonts.py: c, hasattr, int, len, max, min, print, record, table
E:\zeta-monorepo\extension\.vscode-test\vscode-win32-x64-archive-1.103.2\resources\app\node_modules\katex\src\metrics\extract_tfms.py: OSError, RuntimeError, char, char_data, chars, dict, family, float, font_name, int, round
E:\zeta-monorepo\extension\.vscode-test\vscode-win32-x64-archive-1.103.2\resources\app\node_modules\katex\src\metrics\extract_ttfs.py: base_char, char, float, font, len, ord, set, sorted, str, t
E:\zeta-monorepo\extension\.vscode-test\vscode-win32-x64-archive-1.103.2\resources\app\node_modules\katex\src\metrics\format_json.py: font, glyph, int, key, len, sorted, value
E:\zeta-monorepo\extension\.vscode-test\vscode-win32-x64-archive-1.103.2\resources\app\node_modules\katex\src\metrics\parse_tfm.py: RuntimeError, char, char_num, depth, f, file_name, fix_rsfs, float, height, inst_next_char, italic, length, object, open, ord, program, range, self, start, width
E:\zeta-monorepo\node_modules\flatted\python\flatted.py: args, dict, int, isinstance, key, kwargs, len, list, self, str, tuple, val
E:\zeta-monorepo\node_modules\shell-quote\print.py: print
E:\zeta-monorepo\scripts\assert_numpy_runtime.py: ImportError, IndexError, ValueError, bool, faiss_ver, getattr, int, module_name, name, print, str, torch_ver, version
E:\zeta-monorepo\scripts\cleanup_duplicates.py: Exception, NotImplementedError, OSError, PermissionError, SystemExit, ValueError, any, bool, candidates, d, dict, dup, e, f, files, fo, g, int, isinstance, k, len, ln_msg, msg_del, ok_del, ok_hl, ok_ln, out, paths, print, r, repo_root, rows, sorted, src, str, strategy, target, tok, use_git, x
E:\zeta-monorepo\scripts\numpy_compatibility_monitor.py: Exception, cmd, cwd, e, len, print, str
E:\zeta-monorepo\scripts\tests\test_cleanup_duplicates.py: args, cwd, f, list, p, print, str, text, tmpdir
E:\zeta-monorepo\tests\ai-codemod\integration\test_engine_integration.py: RuntimeError, dict, object, range, results, str, temp_dir
E:\zeta-monorepo\tests\ai-codemod\unit\test_markdown_reporter.py: RuntimeError, content, dict, object, range, reporter, results, str, temp_dir
E:\zeta-monorepo\tests\compat\test_numpy_runtime.py: any, line, str
E:\zeta-monorepo\tests\load\websocket_load_chaos_test.py: Exception, bool, chaos_mode, concurrent_connections, connection_id, duration_seconds, e, float, i, int, key, max, message_size_bytes, min, print, range, scenario, self, str, target_url, value, websocket
E:\zeta-monorepo\tests\test_data\python\missing_type_hints.py: param, value
E:\zeta-monorepo\tests\unit\test_turbo_api_client.py: dict, int, mock_post, self, status_code
E:\zeta-monorepo\tools\benchmark_ollama.py: base_url, dict, i, int, iterations, len, list, model, print, prompt, r, range, resp, self, sorted, str, sum
E:\zeta-monorepo\tools\ai-code-optimizer\conftest.py: str
E:\zeta-monorepo\tools\ai-code-optimizer\duplicate_detector.py: Exception, b, block_code, block_type, code, code_blocks, dict, file_path, files, float, len, list, ln, min_similarity, self, str, tuple
E:\zeta-monorepo\tools\ai-code-optimizer\import_optimizer.py: Exception, alias, any, bool, dict, e, f, file_path, getattr, hasattr, import_node, isinstance, list, new_body, node, object, open, self, set, statement, str
E:\zeta-monorepo\tools\ai-code-optimizer\optimizer.py: Exception, any, config_path, dict, enumerate, f, idx, int, isinstance, len, list, out, p, path, print, results, root, seg, self, set, str
E:\zeta-monorepo\tools\ai-code-optimizer\structure_enforcer.py: Exception, bool, config_path, dict, file_path, imports, int, isinstance, list, other_code, rules, self, sorted, statement, stmt, str, tuple, updated_node
E:\zeta-monorepo\tools\ai-code-optimizer\tests\test_optimizer_smoke.py: i, len, p, range, s, str, tmp_path
E:\zeta-monorepo\tools\ai-codemod\detectors\python_detector.py: Exception, all, arg, dict, file_path, findings, getattr, isinstance, list, node, object, self, str
E:\zeta-monorepo\tools\ai-codemod\detectors\typescript_detector.py: dict, file_path, list, object, str
E:\zeta-monorepo\tools\ai-codemod\providers\ollama.py: Exception, RuntimeError, ai_suggestions, config, dict, e, fallback_e, finding, findings, lang_rules, list, model, next, object, r, self, str
E:\zeta-monorepo\tools\ai-codemod\reporters\markdown_reporter.py: dict, f, finding, list, open, output_path, print, report, root_dir, self, str
E:\zeta-monorepo\tools\ai_code_optimizer\__init__.py: ImportError, file_name, mod_name, str
E:\zeta-monorepo\tools\auto_fix\cache.py: Exception, bool, cache, d, f, max, p, str
E:\zeta-monorepo\tools\auto_fix\cli.py: FileNotFoundError, SyntaxError, SystemExit, candidates, cmd, d, deps_to_add, dists, f, int, len, list, m, miss_all, path, plan, print, py_imports, set, sorted, str, sym, ts_imports, tuple
E:\zeta-monorepo\tools\auto_fix\git_changed.py: args, l, list, p, str
E:\zeta-monorepo\tools\auto_fix\main.py: FileNotFoundError, ImportError, OSError, SyntaxError, SystemExit, UnicodeDecodeError, candidates, deps_to_add, dict, e, f, imports_added, int, len, list, missing_all, planned, print, py_imports, py_reqs, reqs_added, set, sorted, str, sym, ts_deps, ts_imports, tuple
E:\zeta-monorepo\tools\auto_fix\report.py: data, dict, len, out_dir
E:\zeta-monorepo\tools\auto_fix\python\analyzer.py: alias, dir, isinstance, miss, node, self, set, src_path, str, t
E:\zeta-monorepo\tools\auto_fix\python\injector.py: file_path, int, l, len, list, range, s, set, str, symbols
E:\zeta-monorepo\tools\auto_fix\python\pyproject_updater.py: changed, d, dists, isinstance, item, list, pyproj, set, str
E:\zeta-monorepo\tools\auto_fix\python\requirements_updater.py: Exception, added, dict, dists, line, list, m, mod, modules, req_path, set, sorted, str
E:\zeta-monorepo\tools\auto_fix\typescript\analyzer.py: from_file, m, nm, out, path, root, set, start_file, str, sym, target, tok, tuple
E:\zeta-monorepo\tools\auto_fix\typescript\injector.py: added, enumerate, file_path, i, imports, line, list, mod, str, sym, tuple
E:\zeta-monorepo\tools\auto_fix\typescript\packagejson_updater.py: FileNotFoundError, added, list, packages, pkg, pkg_path, set, sorted, str
E:\zeta-monorepo\tools\auto_fix\typescript\ts_paths.py: dict, ext, len, list, p, pat, prefix, self, spec, str, suffix, t, target, targets, tsconfig_path
E:\zeta-monorepo\tools\consistency\backend_scanner.py: Exception, dict, doc, e, f, len, list, openapi_doc, path, pattern, print, py_file, set, str
E:\zeta-monorepo\tools\consistency\compare_contracts.py: Exception, backend_scan, dict, f, frontend_scan, issue, len, print, set, sorted, str
E:\zeta-monorepo\tools\consistency\fe_hash.py: Exception, path, str
E:\zeta-monorepo\tools\consistency\frontend_scanner.py: Exception, e, ext, filepath, len, m, print, set, str
E:\zeta-monorepo\tools\consistency\openapi_hash.py: SystemExit, dict, doc, int, path, print, str
E:\zeta-monorepo\tools\consistency\openapi_loader.py: Exception, ImportError, SystemExit, e, filepath, getattr, hasattr, module_path, print, str
E:\zeta-monorepo\tools\consistency\report.py: ImportError, event, issue, len, print, reason, result, route, str
E:\zeta-monorepo\tools\consistency\run_all.py: Exception, e, int, print, str
E:\zeta-monorepo\tools\consistency\utils.py: s, str
E:\zeta-monorepo\tools\load\ws_blast.py: Exception, ImportError, KeyboardInterrupt, bool, client_id, e, error, f, float, i, int, isinstance, k, len, m, max, min, open, print, property, range, self, signum, str, sum, task, websocket
E:\zeta-monorepo\tools\pre_commit\enhanced_pre_commit.py: SystemExit, cmd, description, int, list, print, str
E:\zeta-monorepo\tools\pre_commit\pre_commit_auto_fix.py: SystemExit, int, print
E:\zeta-monorepo\tools\repo_maintenance\cleanup.py: Exception, SystemExit, int, len, p, pat, print, set, sorted, str
E:\zeta-monorepo\tools\scripts\advanced_fix_undefined.py: Exception, SyntaxError, alias, arg, bool, dict, e, enumerate, file_path, func_node, hasattr, int, isinstance, item, len, list, max, node, print, root_path, self, set, sorted, str, target, var
E:\zeta-monorepo\tools\scripts\apply_best_practices.py: Exception, SystemExit, any, bool, dict, env_missing, f, int, k, list, ok_env, ok_py, ok_ts, pkg, print, py_data, py_msg, s, str, ts_msg, tuple
E:\zeta-monorepo\tools\scripts\apply_render_only.py: p, print, s
E:\zeta-monorepo\tools\scripts\auto_fix_comprehensive.py: Exception, SyntaxError, bool, e, f, file_path, import_line, isinstance, line, list, new, node, old, pattern, print, replacement, self, set, sorted, str, target
E:\zeta-monorepo\tools\scripts\auto_update_imports.py: DEFAULT_MAPPING, SyntaxError, SystemExit, alias, bool, d, dict, dirnames, dirpath, dry_run, f, filenames, getattr, int, isinstance, len, list, msg, name, new_lines, node, ok, open, out, path, print, replacements, root, sorted, str, syms, target_groups, tgt_mod, tuple, unmapped, x
E:\zeta-monorepo\tools\scripts\check_dependency_map.py: SystemExit, argv, changed, dict, f, int, k, list, p, pat, print, set, str, v
E:\zeta-monorepo\tools\scripts\check_health.py: BASE_URL, Exception, PATHS, RETRIES, TIMEOUT, attempt, dict, e, float, int, list, object, p, print, range, resp, results, status, str, tuple, url
E:\zeta-monorepo\tools\scripts\check_runtime_imports.py: Exception, SystemExit, any, dict, e, int, mod, print, results, str, type, v
E:\zeta-monorepo\tools\scripts\convert_barrels_to_lazy.py: Exception, bool, e, i, len, line, list, ln, n, p, part, path, print, range, str
E:\zeta-monorepo\tools\scripts\convert_remaining_barrels.py: SystemExit, bool, f, int, len, list, ln, path, print, str
E:\zeta-monorepo\tools\scripts\db_migrate.py: Exception, RuntimeError, SystemExit, bool, conn, dict, exc, int, result, str
E:\zeta-monorepo\tools\scripts\deepseek_start_assistant.py: DEEPSEEK_DIR, FileNotFoundError, print
E:\zeta-monorepo\tools\scripts\demo_one_click_learning.py: Exception, dict, e, event, len, print, query, self, str
E:\zeta-monorepo\tools\scripts\demo_security_production.py: Exception, count, e, feature, len, perm, perm_data, print, reason, role_name, roles, scenario, sorted, str
E:\zeta-monorepo\tools\scripts\dlq_replay.py: Exception, bool, days_old, dict, dry_run, e, enumerate, event_type, i, int, len, limit, list, message_ids, msg, msg_id, print, range, row, self, session, str
E:\zeta-monorepo\tools\scripts\find_unused_deps.py: Exception, c, d, dict, i, im, isinstance, it, item, key, len, n, name, node, path, print, raw, root, set, sorted, str
E:\zeta-monorepo\tools\scripts\fix_all_declarations.py: Exception, SyntaxError, bool, e, file_path, isinstance, list, m, node, print, set, sorted, str, target
E:\zeta-monorepo\tools\scripts\fix_barrels_absolute.py: SystemExit, apply, bool, f, int, len, list, out_lines, p, path, print, str
E:\zeta-monorepo\tools\scripts\fix_f821_simple.py: Exception, bool, e, file_path, new, old, pattern, print, replacement, str, test_file
E:\zeta-monorepo\tools\scripts\fix_imports_ordering.py: Exception, d, dirs, e, enumerate, file, files, i, len, print, py_file, root
E:\zeta-monorepo\tools\scripts\fix_import_syntax.py: Exception, bool, e, enumerate, f, file_path, line, match, open, print, str
E:\zeta-monorepo\tools\scripts\fix_minimal_imports_blocks.py: SystemExit, any, apply, bool, enumerate, f, i, int, j, l, len, list, p, print, range
E:\zeta-monorepo\tools\scripts\fix_mypy_errors.py: Exception, bool, e, enumerate, file, file_path, i, len, line, list, print, self, str
E:\zeta-monorepo\tools\scripts\fix_pytest_simple.py: Exception, e, enumerate, f, file, files, i, line, open, print, root, test_file
E:\zeta-monorepo\tools\scripts\fix_syntax_tools.py: Exception, e, f, filename, open, print
E:\zeta-monorepo\tools\scripts\force_render_asr.py: entry, f, print, str
E:\zeta-monorepo\tools\scripts\generate_8_layer_full.py: STRUCTURE_MAP, base_path, dict, f, file_name, file_path, files, len, list, open, print, root_dir, str
E:\zeta-monorepo\tools\scripts\import_optimization_report.py: cmd, code, desc, description, l, len, list, name, print, status, suggestion
E:\zeta-monorepo\tools\scripts\insert_desktop_route.py: Exception, cand, e, enumerate, i, ln, print, str
E:\zeta-monorepo\tools\scripts\load_test_outbox.py: count, enumerate, failed, i, int, len, num_workers, print, range, row, str, success, sum, tuple, worker_id
E:\zeta-monorepo\tools\scripts\migrate_imports.py: UnicodeDecodeError, changed_files, f, len, list, p, pat, print, rep
E:\zeta-monorepo\tools\scripts\normalize_rendered_files.py: p, print, src, str
E:\zeta-monorepo\tools\scripts\optimize_imports_auto.py: bool, cmd, e, len, print, str
E:\zeta-monorepo\tools\scripts\optimize_init_files.py: any, d, dir_path, dirs, export, f, files, item, len, list, module, print, py_file, root, skip, sorted, str, subdir
E:\zeta-monorepo\tools\scripts\optimize_init_files_fixed.py: LAYER_STRUCTURE, chr, content_lines, d, dict, dir_path, dirs, export, f, file, item, layer, len, list, module, open, print, python_files, root, sorted, str, subdir
E:\zeta-monorepo\tools\scripts\parse_jscpd_report.py: Exception, SystemExit, argv, c, dict, enumerate, exc, f, i, int, isinstance, item, len, list, m, open, p, path, print, sorted, str, top
E:\zeta-monorepo\tools\scripts\qa_pipeline.py: Exception, bool, check_func, coverage, description, e, fix, init_file, len, list, name, print, self, str, verbose
E:\zeta-monorepo\tools\scripts\refactor_rename.py: SystemExit, any, apply, bool, d, dict, dst_rel, f, file_moves, int, k, list, m, moves, mr, msgs, new, new_text, old, open, out, p, part, path, print, r, replacements, results, root, s, src_rel, str, tuple, v
E:\zeta-monorepo\tools\scripts\render_templates_update.py: p, print, s
E:\zeta-monorepo\tools\scripts\run_quality_gates.py: Exception, bool, cmd, cwd, e, error, list, name, output, print, str, title, tuple
E:\zeta-monorepo\tools\scripts\run_scaffold_dry.py: print, s, str
E:\zeta-monorepo\tools\scripts\run_training_models_smoke.py: Exception, session, str
E:\zeta-monorepo\tools\scripts\save_plan_asr.py: print, s
E:\zeta-monorepo\tools\scripts\smart_import_cleaner.py: Exception, bool, e, f, file_content, file_path_str, import_name, l, len, open, print, self, set, sorted, str, unused
E:\zeta-monorepo\tools\scripts\start_all_tools.py: Exception, KeyboardInterrupt, actions, any, attempt, background, base_dir, bool, dict, duration, e, float, int, max_attempts, print, range, resp, self, service, session, set, stderr, stdout, str, timeout, tool_name, url
E:\zeta-monorepo\tools\scripts\ts_alias_migrator.py: Exception, SystemExit, alias, apply, bool, ch, changes, ext, f, file_path, head, int, len, list, m, p, prefix, print, root, spec, str, tail, tuple
E:\zeta-monorepo\tools\scripts\update_project_map.py: EXCLUDES_DEFAULT, OSError, PermissionError, body_lines, bool, bytes_, child, cnt, counts, d, depth, dict, dir_path, enumerate, ext_counts, exts, f, float, idx, int, kv, len, lines, list, max, num_bytes, options, p, path, r, root, s, sections, seen, set, sorted, stack, stat_lines, str, tuple, u
E:\zeta-monorepo\tools\scripts\update_project_paths.py: f, open, print
E:\zeta-monorepo\tools\scripts\update_roadmap.py: ImportError, dict, f, float, int, l, layer, layer_num, len, list, missing_file, print, range, req_file, self, str, tuple
E:\zeta-monorepo\tools\scripts\verify_project_map.py: SystemExit, base, int, m, p, print, root, sorted, str
E:\zeta-monorepo\tools\scripts\verify_project_paths.py: Exception, bool, check_func, e, expected_value, f, key, len, list, message, name, open, passed, path, print, results, str, success, sum, tuple
E:\zeta-monorepo\tools\scripts\vscode_config_optimizer.py: Exception, any, category, dict, e, f, feature, features, filename, files, isinstance, k, key, key1, key2, keyword, len, list, open, progress, round, self, set, setting, setting_key, settings, settings1, settings2, str, task, tasks, v, value
E:\zeta-monorepo\tools\scripts\audit\detect_near_duplicates.py: Exception, any, base, by_hash, dict, dup, enumerate, f, file, file_info, group, i, j, len, line, list, open, p, path_a, path_b, paths, print, range, round, seg, str
E:\zeta-monorepo\tools\scripts\consistency\env_consistency.py: Exception, data, desktop, detail, dict, f, issue, k, len, list, object, p, problems, raw_line, server, str, tuple, v
E:\zeta-monorepo\tools\scripts\consistency\i18n_consistency.py: FileNotFoundError, all_keys, any, d, dict, f, file, isinstance, k, keysets, lang, len, list, object, prefix, r, report, set, sorted, str, v
E:\zeta-monorepo\tools\scripts\consistency\openapi_consistency.py: Exception, FileNotFoundError, RuntimeError, dict, e, endpoints, file, int, len, list, map, openapi_url, ordered, p, s, seen, set, sorted, str
E:\zeta-monorepo\tools\scripts\consistency\run_all.py: cmd, code, dict, int, list, object, print, str, summary, tuple
E:\zeta-monorepo\tools\scripts\consistency\ws_events_consistency.py: annot, desktop, dict, enumerate, events, evt, f, idx, it, k, len, list, m, name, py_file, report, req, required_raw, server, set, sorted, str, ts_file, v, x
E:\zeta-monorepo\tools\scripts\copilot\build_context.py: Exception, dir_name, e, f, item, len, list, name, print, sorted, str
E:\zeta-monorepo\tools\scripts\copilot\hotfix_pydantic.py: Exception, e, fix, print
E:\zeta-monorepo\tools\scripts\copilot\hotfix_pydantic_v2.py: Exception, e, print
E:\zeta-monorepo\tools\scripts\copilot\mypy_checker.py: Exception, bool, e, enumerate, error, i, line, print
E:\zeta-monorepo\tools\scripts\copilot\simple_runner.py: Exception, bool, cmd, desc, description, e, len, print, str
E:\zeta-monorepo\tools\scripts\copilot\ultimate_pydantic_fix.py: Exception, e, print
E:\zeta-monorepo\tools\scripts\fix\demo_fix_env.py: FileNotFoundError, ImportError, e, getattr, print, sp
E:\zeta-monorepo\tools\scripts\fix\repair_env.py: Exception, SystemExit, bool, check, cmd, cwd, e, getattr, int, list, mod, print, sp, str
E:\zeta-monorepo\tools\scripts\fix\test_fix_env.py: Exception, bool, e, len, name, print, sum, test_func
E:\zeta-monorepo\tools\scripts\fix\verify_stack.py: Exception, cmd, dict, e, getattr, int, list, m, pkg, print, report, status, str
E:\zeta-monorepo\tools\scripts\maintenance\autofix_imports.py: Exception, bool, c, dict, dry_run, e, file_path, fix_func, int, len, list, match, max, original_name, print, should_fix, str, target_path
E:\zeta-monorepo\tools\scripts\maintenance\comprehensive_init_fixer.py: Exception, RESULTS, alias, any, dict, e, export, file_path, imp, int, isinstance, len, list, node, part, print, py_file, r, root_path, self, set, sorted, str, target, tool
E:\zeta-monorepo\tools\scripts\migration\migrate_graphql_structure.py: Exception, action, dest, dir_name, domain, e, f, open, print, source, str
E:\zeta-monorepo\tools\scripts\monitoring\system_monitor.py: Exception, KeyboardInterrupt, alert_type, client, config, dict, e, endpoint, f, len, message, metrics, print, self, status, str
E:\zeta-monorepo\tools\scripts\quality\dup_guard.py: Exception, dict, directory, e, f, files, func_name, isinstance, issue, len, line, list, name, node, open, print, py_file, str
E:\zeta-monorepo\tools\scripts\repair\fix_duplicates.py: Exception, all, any, bool, dict, dup, e, f, file_path, isinstance, item, len, line, list, open, placeholder, print, str
E:\zeta-monorepo\tools\scripts\repair\fix_empty_try_blocks.py: f, file_path, len, open, print
E:\zeta-monorepo\tools\scripts\repair\fix_import_conflicts.py: f, import_line, m, open, print
E:\zeta-monorepo\tools\scripts\repair\fix_migration_imports.py: any, i, line, migration_init, pattern, print, range
E:\zeta-monorepo\tools\scripts\repair\fix_service_compatibility.py: attr, f, new_method, old_method, open, print
E:\zeta-monorepo\tools\scripts\repair\fix_syntax_errors.py: f, file_path, line, match, open, print
E:\zeta-monorepo\tools\scripts\repair\fix_undefined_vars.py: file_path, line, list, pattern, print, replacement
E:\zeta-monorepo\tools\scripts\repair\fix_undefined_vars_advanced.py: f, file_path, func_name, len, open, print
E:\zeta-monorepo\tools\scripts\safe\apply_merge_plan.py: a, b, item, key, pairs, print, score
E:\zeta-monorepo\tools\scripts\safe\dedup_index.py: Exception, a, b, bucket, buckets, bytes, ca, cb, code, d, dict, f, fn, group, isinstance, len, list, node, open, p, print, r, round, set, sorted, str
E:\zeta-monorepo\tools\scripts\safe\generate_work_orders.py: Exception, cmd, dict, f, int, item, list, mm, print, rr, set, sorted, str, x
E:\zeta-monorepo\tools\scripts\seed\seed_roles.py: Exception, assignment, dict, e, exit, len, perm_data, perm_name, permission_ids, print, role_data, role_ids, role_name, str
E:\zeta-monorepo\tools\scripts\seed\seed_roles_normalized.py: Exception, description, dict, e, len, name, p, perm, perm_data, perm_name, print, r, risk_level, role_data, role_name, scope, str
E:\zeta-monorepo\tools\scripts\self_upgrade\cli.py: SystemExit, int, list, print, str
E:\zeta-monorepo\tools\scripts\upgrade\ensure_configs.py: Exception, desktop, e, k, len, print, sum, v
E:\zeta-monorepo\tools\scripts\upgrade\upgrade_wrapper.py: FileNotFoundError, int, len, list, print, script_path, str
```

## Python Requirements Added
```
A
AI_LEARNING_PERMISSIONS
ANSI_DARK
ANSI_LIGHT
APIHandler
API_VERSION
ASCII
ASCII2
ASCII_CTRL
ASCII_DOUBLE_HEAD
Alias
AnalyzerCls
And
Any
AssertionError
AttributeError
BARE_KEY_CHARS
BASE_URL
BASIC_STR_ESCAPE_REPLACEMENTS
BENCHMARKS
BENCHMARK_WEIGHT
BENCHMARK_WEIGHTS
BOMS
BZ2_EXTENSIONS
BaseException
BaseExceptionGroup
BlockingIOError
Bookmark
BrokenPipeError
C
CASCADE_DELETE
CFURLCreateWithFileSystemPath
CGBitmapContextCreate
CGBitmapContextCreateImage
CGColorSpaceCreateWithName
CGImageDestinationAddImage
CGImageDestinationCreateWithURL
CGImageDestinationFinalize
CGImageSourceCopyPropertiesAtIndex
CGImageSourceCreateImageAtIndex
CGImageSourceCreateWithURL
CGImageSourceGetCount
CIContext
CIFilter
CIImage
CIVector
CONTINUE
CONTROL_CODES_FORMAT
CONTROL_ESCAPE
CORE_CONTRACTS
CaselessKeyword
CaselessLiteral
CharsNotIn
Combine
ConnectionClosed
ConnectionError
DEEPSEEK_DIR
DEFAULT_EXTS
DEFAULT_JUSTIFY
DEFAULT_MAPPING
DEFAULT_OUT
DEFAULT_OVERFLOW
DEFAULT_ROLE_PERMISSIONS
DEFAULT_ROOTS
DEFAULT_STYLES
DOMAIN_SCORES
DSStore
Data
DatabaseManager
DelimitedList
DeprecationWarning
Diagnostics
Dict
EMPTY
END
ENHANCED_CONTRACTS
ENHANCED_ROLE_PERMISSIONS
ENV_VAR
EOFError
EVENT_TRIGGERED_TRANSITIONS
EVENT_TYPE_REGISTRY
EXCLUDES_DEFAULT
EXCLUDE_DIRS
Ellipsis
Empty
EndOfMessage
Enum
Event
Exception
ExceptionGroup
FILE_PATTERNS
FK_USERS_ID
FORK
FORMAT_FUNCTIONS
FileExistsError
FileNotFoundError
FollowedBy
Forward
GPT5_WEIGHT
Group
HEAVY
HEAVY_EDGE
HEAVY_HEAD
HEXDIGIT_CHARS
HIT
ILLEGAL_BASIC_STR_CHARS
ILLEGAL_COMMENT_CHARS
ILLEGAL_LITERAL_STR_CHARS
ILLEGAL_MULTILINE_BASIC_STR_CHARS
ILLEGAL_MULTILINE_LITERAL_STR_CHARS
IMPLEMENTATION_GUIDES
IMPORTANCE_LEVELS
IMPORTANCE_WEIGHTS
INTERPRETER_SHORT_NAMES
IOError
IPSockAddrType
ImportError
IndexError
InformationalResponse
IsADirectoryError
Iterable
JWTError
JWTExpiredSignatureError
KEY_INITIAL_CHARS
KeyError
KeyboardInterrupt
Keyword
LABEL_IMPORTANCE_WEIGHTS
LAYER_STRUCTURE
LOGS
LineEnd
List
Literal
LookupError
M
MAX_AGENT_NAME_LEN
MAX_CHAT_TITLE_LEN
MAX_DOCUMENT_FILENAME_LEN
MAX_EMAIL_LEN
MAX_FULL_NAME_LEN
MAX_INLINE_NESTING
MAX_MESSAGE_TYPE_LEN
MAX_ROLE_LEN
MAX_STATUS_LEN
MAX_TRAINING_JOB_NAME_LEN
MAX_USERNAME_LEN
METRICS
MINIMAL
MINIMAL_DOUBLE_HEAD
MINIMAL_HEAVY_HEAD
MISS
MatchFirst
MemoryError
ModuleNotFoundError
N
NAMING_CONVENTION
NSAffineTransform
NameError
NegotiateFlags
NoMatch
NotADirectoryError
NotImplemented
NotImplementedError
OSError
OneOrMore
Opt
OverflowError
PACKAGE_CONFIGS
PASS_THRESHOLD
PATHS
PERMISSIONS
POINTER
PROFILE_IMPL
PYPROJECT_CORRESPONDENCE
ParseAction
ParseBaseException
ParseException
ParseFatalException
ParseResults
ParseSyntaxException
ParserElement
PendingDeprecationWarning
PermissionError
ProcessLookupError
RESULTS
RETRIES
ROLE_DEFAULT_SCOPES
ROLE_PERMISSIONS
ROLE_QUOTAS
ROUNDED
RULES
RecursionError
RecursiveGrammarException
ReferenceError
Regex
Request
ResourceWarning
Response
ResponseCls
RuntimeError
RuntimeWarning
SECURE_ORIGINS
SIMPLE
SIMPLE_HEAVY
SKIP_DIR_NAMES
SKIP_PATH_CONTAINS
SPACE
SPINNER_CHARS
SPINS_PER_SECOND
SQUARE
SQUARE_DOUBLE_HEAD
STATE_TRIGGERED_TRANSITIONS
STRIP_CONTROL_CODES
STRUCTURE_MAP
SUPPORTED_OPTIONS
SUPPORTED_OPTIONS_EDITABLE_REQ
SUPPORTED_OPTIONS_REQ
SYS_CTX
ServerChallenge
SkipTo
SockAddrType
StopAsyncIteration
StopIteration
StrOrBytesPath
Structure
Suppress
SyntaxError
SystemError
SystemExit
TAR_EXTENSIONS
TIMEOUT
TOML_WS
TOML_WS_AND_NEWLINE
TRAINER_POLICY
TimeoutError
TokenConverter
Tuple
TypeError
UDPPacketType
UNIXDatagramPacketType
UTC
UnicodeDecodeError
UnicodeEncodeError
UnicodeError
Union
UserWarning
ValueError
Warning
White
Word
XZ_EXTENSIONS
ZIP_EXTENSIONS
ZeroOrMore
a
aPred
a_dir
a_id
a_name
a_path
abac_ok
abac_result
abandon_on_cancel
abi
abis
abs
abs_base
abs_path
absent
absolute
ac
acc
accepted
accepted_mimes
access_freq
access_key
access_lists
accessor
accumulate
acm
act
acted
action
action_counts
action_data
action_expression
action_name
action_results
action_risk
action_text
action_type
action_url
actions
actions_dict
activated_agent
active
active_agent
active_alerts
active_connections
active_only
active_rounds
activities
activity
actor
actor_id
actual
actual_arch
actual_multiarch
actual_version
adapter
adapter_kwargs
adapter_path
add_if_no_ancestor
add_launchers
add_timestamp
add_to_parent
added
addindent
additional_compile_target_names
additional_data
additional_dependencies
additional_seconds
additional_settings
additional_signals
addr
addr_family
address
addsource
adjacent
adjs
adjust
admin_override
admin_path
admin_subject
admin_user
af
affected_systems
after
age_days
age_seconds
agent
agent_counts
agent_data
agent_id
agent_repo
agent_repository
agent_result
agent_service
agent_type
agents
aggregate
aggregate_id
aggregation
aggregation_strategy
aggregator
ai_request
ai_service
ai_suggestions
aid
aix
alembic_cfg_path
alert
alert_config
alert_id
alert_name
alert_thresholds
alert_type
alg
algo
algorithm
algorithms
alias
alias_shim
aliases
all
allResults
all_cmds
all_files
all_issues
all_keys
all_misses
all_passages
all_subdirs
all_targets
allfiles
allocator
allow_all_prereleases
allow_blank
allow_fail
allow_fallback
allow_headers
allow_isolation
allow_keyring
allow_methods
allow_multiline
allow_nan
allow_netrc
allow_origin_regex
allow_origins
allow_permanent
allow_special_forms
allow_trailing_delim
allow_wrap
allow_yanked
allowed
allowed_chars
allowed_domains
allowed_extensions
allowed_exts
allowed_ips
allowed_mimes
allowed_models
allowed_origins
allowed_paths
allowed_tables
alpha
alphanums
alphas
alpn_protocols
already_seen
alternative
amount
amt
analysis_agent
analysis_results
analysis_type
analytics
analyze
anc
ancdata
anchor
anchor_attribs
angular
animation_time
annot
annotation_key
anomaly
anomaly_threshold
ansi_text
any
any_close_tag
any_open_tag
anyio_exc_map
aoff
api
api_costs
api_endpoint
api_key
api_level
api_metrics
api_token
app
app_event
app_file
app_identifier_prefix
app_name
app_repo
app_row
appauthor
append
appends
appinfo
appleshare_info
application_mode
applied
apply
apply_callback
apply_clip
apply_dp
appname
ar_flags
arch
arch_prefix
arch_sep
arch_suffix
archive
archive_dir
archive_filename
archive_name
archive_record_path
archive_source
archived_only
archs
archs_including_64_bit
area
arg
arg_name
arglist
args
args_
args_else
args_str
argument
arguments
argv
arity
around
array
artifact_key
artifact_ref
artifact_uri
asReference
as_group_list
as_keyword
as_match
as_number
as_string
ascending
ascii
asdict
aslist
asr
asr_engine
assert_f
assert_fingerprint
assert_hostname
assert_same_host
assessor
assigned
assigned_by
assignment
assistant_data
assistant_id
assistants
association_type
ast
async_cm
async_session
at
attachments
attempt
attempt_number
attempts
attr
attr1
attr2
attrName
attrValue
attr_desc
attr_dict
attr_name
attribs
attribute
attribute_flags
attributes
attrname
attrs
audience
audio
audio_chunk
audio_chunks
audio_data
audio_file
audio_path
audio_paths
audio_size_bytes
audio_stream
audit
audit_context
audit_data
audit_enabled
auth
auth_directory
auth_header
auth_result
auth_service
auth_system
auth_token
author
authority
pywin32
authurl
auto_activate
auto_cleanup
auto_close
auto_confirm
auto_create_config
auto_describe
auto_error
auto_headers
auto_ingest
auto_install
auto_optimize
auto_refresh
auto_train
auto_vectorize
autodelete
autogenerate
automation_percent
autonomous_path
autonomous_paths
autonomous_rate_limit
autoreset
avail
available_models
available_only
b
b1
b2
b_id
back
back_dep_target
backend
backend_class
backend_module
backend_name
backend_options
backend_path
backend_scan
backend_type
background
background_collect_interval
background_tasks
backoff
backoff_factor
backoff_sec
backslashes
backtrack_causes
backup
backup_count
backup_dir
backup_directory
backup_file
backup_name
backup_path
backup_schedule_hours
backup_stacks
backup_type
backups
bad
bad_agent
badge_file
bandit_result
bar_type
bar_width
base
base_backoff
base_backup_id
base_char
base_delay
base_dir
base_expr
base_file
base_handler
base_headers
base_model
base_model_hash
base_name
base_path
base_requirements
base_to_build
base_type
base_url
baseenc
baseline
baseline_alerts
baseline_cost
baseline_hours
baseline_minutes
basename
bases
basestring
basic_agent
basic_auth
batch
batch_load_fn
batch_size
bbox_hint
bdf
beam_size
before
beg
begin
behavior
benchmark_tasks
best
best_agent
best_pattern
beta
bf
bf_tgt
bg
bgcolor
bgr
llama_cpp_python
binary
binary_form
binary_type
binary_units
bind
bit
bit_no
blacklist
blacklist_fields
blend
blob_name
block
block1
block2
blockStatementExpr
block_code
block_seek
block_type
blocked_cmd
blocked_path
blocked_pattern
blocks
blocksize
blue
blue1
blue2
bm25_score
bmk
body
body2
body_chars
body_file
body_lines
body_pos
bold
bom
bom_encoding
bool
boost
borrower
bot
bottlenecks
bottom
bound
bound_method
boundary
python-box
box_name
brace
brace_diff
branch
break_flag
break_positions
bright
bs
bucket
bucket_name
bucket_size
buckets
budget
budget_ms
budget_seconds
buf
buf_char
buffer
buffer_size
buffering
bufs
bufsiz
bufsize
build
build_backend
build_dir
build_env
build_env_installer
build_failures
build_file
build_file_dict
build_file_ext
build_file_root
build_files
build_files_arg
build_info
build_isolation
build_isolation_installer
build_options
build_py
build_successes
build_temp
build_tracker
built_find_links
built_products_dir
bundle_depends
bundle_deps
bundle_identifier
burst_allowed
burst_info
burst_limit
bus
button
bwf
by
by_file
by_full
by_hash
by_head
by_key
by_name
by_norm
by_size
bypass_cache
bypass_paths
byref
byte
byte_code
byte_content
byte_range
byte_str
byte_view
bytearray
bytedata
bytes
bytesData
bytes_
byteslike
bytestring
c
c_byte
c_char
c_char_p
c_data
c_id
c_int
c_long
c_longlong
c_names
c_short
c_uint
c_ulong
c_ulonglong
c_ushort
c_void_p
ca
ca_cert_data
ca_cert_dir
ca_certs
cache
cache_controller
cache_dir
cache_entry
cache_etags
cache_hit
cache_key_fn
cache_level
cache_link_parsing
cache_manager
cache_obj
cache_object
cache_service
cache_size
cache_size_limit
cache_storage
cache_ttl
cache_type
cache_wrapper
cacheable_methods
cacheable_page
cached_result
cadata
cafile
call
callPreParse
call_history
call_next
call_time
call_times
callable
callback
callback_kwd
callback_name
callbacks
caller
calls
camel
cancel_remaining
cancel_scope
cancellable
cand
cand_iter
candidate
candidate_name
candidate_version
candidates
candidates_from_page
canny_high
canny_low
canonical_file
canonical_name
canonname
cap
cap_id
capabilities
capability
capacity
capath
caps
caption
caption_justify
caption_style
capture
capture_args
capture_result
case_sensitive
casedkey
caseless
cat
cat_name
categories
category
category_findings_list
causation_id
cause
causes
cb
cc
cc_args
cc_directive
ccshared
cdll
cell
cert
cert_bytes
cert_chain
cert_data
cert_file
cert_reqs
certfile
cf
cf_string_ref
cfg
cfg_exc
cfg_path
cfglen
cflag
cflags
cflags_c
cflags_cc
ch
challenge
change
change_summary
changed
changed_files
changelog
changes
channel
channels
chaos_mode
char
char_data
char_end
char_len
char_list
char_num
char_start
character
characters
chardet
charpos
chars
charset
charsets
chat
chat_data
chat_history
chat_id
chat_ids
chat_repo
chat_repository
chat_result
chat_service
chat_type
check
check_build_deps
check_circular
check_func
check_interval
check_ltr
check_name
check_object
check_ownership
check_result
check_results
check_supported_wheels
check_target
check_type_strict
checked_pairs
checker_path
checksum
child
child2
child_and_region
child_height
child_spec
child_width
children
choice
chr
chunck
chunk
chunk_end
chunk_id
chunk_idx_str
chunk_index
chunk_length
chunk_size
chunk_start
chunked
chunker
chunking_port
chunking_service
chunks
cid
cipher_suite
ciphers
circuit_config
circuit_failure_threshold
circuit_recovery_timeout
circular_check
citations_ok
cj
cl
claims
class_
class_kwargs
class_name
class_or_tuple
classes
classifier
classmethod
classname
clean_config
cleaned
cleanup
cleanup_func
cleanup_interval_minutes
cleanup_result
clear_embedding
clen
cli
clicks
client
client_auth_required
client_cafile
client_capath
client_cert
client_data
client_id
client_ids
client_ip
client_key
client_pk
client_provider
client_secret
client_updates
clip_norm
close_brace
close_handle
close_token
closed
closefd
closer
closing
cls
cls_or_fn
cluster_tops
clusters
cm
cmd
cmd_args
cmd_class
cmd_line_warn_options
cmd_list
cmd_name
cmd_option
cmd_options
cmd_opts
cmdlist
cmdname
cmds
cmp
cmsg_data
cmsg_level
cmsg_type
cnt
code
code_agent
code_blocks
code_format
code_prompt
code_width
codepoint
codes
coding_sm
col
col_no
collected
collection
collection_interval
collector
collector_func
colno
color
color1
color2
color_24
color_8
color_bgr
color_key
color_name
color_rgb
color_system
colors
column
column_first
column_index
column_lengths
columns
combine
combined_logs
combined_score
combined_scores
combo
comes_from
command
command_args
command_desc
command_description
command_info
command_obj
command_options
command_output
commandprefix
file-manager
commands_dict
comment
commit
commit_id
comp
comp_file
compact
compat_name
compile
compiler
compiler_cmd
compiler_cxx_ne
compiler_include
complete_style
completed_session
completed_step_ids
completed_task_ids
complex
complexity
component
components
compress
compress_rotated
compressed
compressed_memory_id
compressed_value
compression_enabled
compression_level
compression_result
compression_service
compute_type
con
concept
concrete_output_by_rule_source
concrete_output_index
concrete_outputs
concurrency
concurrency_semaphore
concurrent_connections
cond
cond_key
cond_num
condition
condition_expression
condition_key
condition_result
condition_value
conditions
conf
confidence
confidence_marker
confidence_threshold
config
config_data
config_dict
config_dir
config_file
config_holder
config_key
config_name
config_override
config_overrides
config_path
config_platform_overrides
config_settings
config_to_use
config_type
config_updates
configname
configuration
configuration_name
configuration_node
configurations
conflict_details
conflicting
conflicting_deps
conflicting_reqs
conflicting_with
confname
conformance_exit
confvalue
conn
conn_ids
conn_kw
conn_timeout
connect
connect_args
connectable
connected
connection
connection_factory
connection_id
connection_pool_kw
connection_string
connections
conns
console
console_logging
const
constraint
constraints
cont_key
container
container_type
content
content_data
content_disposition
content_file
content_filter
content_hash
content_length
content_lines
content_list
content_location
content_query
content_type
contents
context
context_data
context_len
context_manager
context_provider
context_update
context_updates
contexts
contours
contract
contravariant
control
control_code
control_codes
control_id
controller
controller_class
conv_id
conversation
conversation_data
conversation_id
conversation_result
conversation_type
conversations_delta
convert
convert_whitespace_escapes
converted
converter
cookie
cookie_dict
cookie_in_jar
cookies
cooldown_minutes
coord
coords
copied
copied_bytes
copied_files
copies
copy_defaults
copy_group
copy_headers
core_event
core_file
core_repo
coro
correct
correlation_id
cost
count
count_value
counter
counts
covariant
coverage
cp
cpp_line
cpu
cpu_arch
cpu_threshold
cpy
crdate_hr
create
create_py
create_string_buffer
create_ts
created
created_agent
created_at
created_by
created_dep_target
created_id
created_target
creationflags
creative_agent
credentials
creds
criterion
criteron
critical
critical_file
cron
crop
cross_fade
crt_dir
csidl_name
css
ct
ctx
ctx_ca_certs_der
ctxs
cur
cur_
cur_idx
cur_keys
curr
current
current_agents
current_alerts
current_chats_today
current_cost
current_data
current_depth
current_device_data
current_directory
current_dist
current_file
current_files_today
current_hours
current_id
current_messages
current_metrics
current_minutes
current_storage_mb
current_time
current_user
current_user_id
current_version
current_vsprops
currentframe
cursor
cursor_update
curval
custom_ca_certs
custom_formats
custom_id
cuts
cwd
cycle_interval
cygwin_shell
d
d_id
daily_counts
dargs
dark
dashboard_id
dashboard_name
dashboard_service
data
data__authors_item
data__buildsystem__backendpath_item
data__buildsystem__requires_item
data__classifiers_item
data__cmdclass_key
data__cmdclass_val
data__datafiles_key
data__datafiles_val
data__datafiles_val_item
data__dependencies_item
data__dynamic__optionaldependencies_key
data__dynamic__optionaldependencies_val
data__dynamic_item
data__dynamic_key
data__eagerresources_item
data__entrypoints_key
data__entrypoints_val
data__excludepackagedata_key
data__excludepackagedata_val
data__excludepackagedata_val_item
data__file_item
data__find__exclude_item
data__find__include_item
data__find__where_item
data__keywords_item
data__licensefiles_item
data__maintainers_item
data__namespacepackages_item
data__obsoletes_item
data__optionaldependencies_key
data__optionaldependencies_val
data__optionaldependencies_val_item
data__packagedata_key
data__packagedata_val
data__packagedata_val_item
data__packagedir_key
data__packagedir_val
data__packages_item
data__platforms_item
data__provides_item
data__pymodules_item
data__scriptfiles_item
data__urls_key
data__urls_val
data_after_shebang
data_any
data_b64
data_chunks
data_dict
data_dir
data_filename
data_files
data_item
data_items
data_key
data_length_pointer
data_or_format
data_point
data_scheme_paths
data_sensitivity
data_size_mb
data_type
data_val
database
database_path
database_service
database_url
datapoints
dataset_data
dataset_id
dataset_item_repository
dataset_lineage
dataset_name
dataset_path
date
date_from
date_range
date_to
datetime_string
datum
day
day_str
days
days_old
days_threshold
db
db_config
db_metrics
db_path
db_session
db_url
dbl_quoted_string
dct
deactivated_agent
dead
deadline
debug
debug_mode
debug_print
decay_hours
decl
decode
decode_responses
decode_unicode
decoders
dedent
default
default_bucket_size
default_chunk_size
default_config
default_encoding
default_filename
default_headers
default_overlap
default_policy
default_rate_limit
default_refill_rate
default_strategy
default_style
default_timeout
default_toolset
default_ttl
default_value
default_variables
default_variant
defaults
defect
defects
define
define_macros
defines
defining_class
definition
definitions
defn
delattr
delay
delete
delete_all
delete_on_close
deleted
deletions
delim
delimiter
delims
delivery_id
delta
delta_primary
deltas_name
deltas_secondary
demo_func
demo_name
dep
dep_graph_json
dep_id
dep_list
dep_name
dep_target
dep_version
dependee
dependencies
dependency
dependency-groups
dependent
depends
depfile
deploy_data
deployment_config
deployment_result
deps
deps_to_add
depth
deptype
der_bytes
desc
descendant
description
deserializer
desktop
dest
dest_ctx
dest_dir
dest_dir_path
dest_key
dest_path
dest_subpath
destfile
destfp
destination
destination_blob_name
destination_dir
destination_eggdir
destination_scheme
detail
detailed_agent
details
detected
detection
dev_path
develop_ok
device
device_data
device_fingerprint
device_id
device_name
device_token
device_trust
df
dfp
diag
diag_enum
diag_file
diagram
diagram_kwargs
diagrams
dialect
dialup_info
dict
dict_class
dict_delitem
dict_setitem
diff
difficulties
diffs
digest
digest_cons
digest_list
digest_name
digests
dim
dimension
dimensions
dir
dir_
dir_a
dir_b
dir_counts
dir_name
dir_path
dir_pattern
dir_scripts
direct_url
direct_url_file
direction
directive
directory
directs
dirfiles
dirmode
dirname
dirnames
dirpath
dirpattern
dirs
dirurl
disable
disable_cache
disable_compression
disable_pip_version_check
discovered_reqs
disk
disk_cache_size_mb
disk_image_alias
disk_type
disktype
disp
dispatch_args
dispatcher_config
display_name
dispose_func
dist
dist_args
dist_dir_name
dist_info_dir
dist_name
dist_path
dist_spec
distance
distances
distpath
distributed_total
distribution
distribution_finder
distribution_name
distributions
distro_infos
distro_release_file
dists
divides
divmod
dkw
dll_name
dlldata
dlq_sizes
dn
dname
doActions
do_actions
do_copy
do_handshake_on_connect
do_sample
do_setup_env
doc
doc_data
doc_dir
doc_id
doc_key
doc_path
doc_scores
docs
document
document_data
document_id
document_ids
documentation
documents
domain
domain_data
done
dotted_path
double
download
download_dir
download_info
download_result
downloaded
dp
dp_seed
dpart
drive
driver
drivers
drop
drop_existing
dry
dry_run
dsn
dst
dst_bytes
dst_dir
dst_files
dst_mod
dst_option
dst_rel
dsts
dt
due_date
dunder
dup
dup_contents
dup_file
dup_hash_groups
dupe
duplicate_file
duration
duration_minutes
duration_ms
duration_seconds
durations
durations_by_model
dx
dy
dynamic_field
dynamic_libs
e
e2
e_fmt
e_k_b_n_c
e_phentsize
e_phnum
e_phoff
echo
edge
edge_types
edges
editable
editable_name
editable_req
editables_only
editor_id
egg_base
egg_dir
egg_dist
egg_info
egg_info_dir
egg_link_name
egg_path
eggs
eh
elapsed_when_finished
elem
element
elements
ell
elm
elt
eltoff
email
email_manager
emb
embed
embed_manifest
embedder
embedding
embedding_adapter
embedding_dim
embedding_model
embedding_port
embedding_provider
embedding_result
embedding_service
embedding_type
embedding_vector
embeddings
emitted_options
emoji
emoji_code
emoji_name
emoji_variant
empty
empty_agent
enable
enable_cache
enable_caching
enable_circuit_breaker
enable_compression
enable_content_type_sniffing
enable_csrf
enable_db_instrumentation
enable_detailed_timing
enable_distributed
enable_encryption
enable_gpu
enable_hsts
enable_hybrid_search
enable_io_tracking
enable_link_path
enable_logging_instrumentation
enable_memory_tracking
enable_metrics
enable_near
enable_prometheus
enable_rate_limit_headers
enable_real_time_alerts
enable_redis
enable_response_size
enable_retry
enable_tracing
enable_websockets
enable_xss_protection
enabled
enc
enc_content
enc_embedding
enc_metadata
encode
encode_multipart
encoder
encoding
encoding_name
encoding_or_label
encrypted_data
encrypted_fields
encryption_key
end
end_column
end_date
end_id
end_index
end_line
end_position
end_quote_char
end_time
ended_session
endloc
endpoint
endpoint_name
endpoint_url
endpoints
endpos
enforce_auth
enforce_content_length
enforce_min_interval
enforce_rbac
engine
engine_config
engineering_hours
enhancement_request
enriched
ensure_ascii
ensure_discovered
ensure_exists
ent
entities_count
entities_serialized
entitlements
entity
entity_extractor
entity_id
entity_type
entries
entry
entry_point
entrypoint
enumerate
env
env_file
env_missing
env_name
env_value
env_var
environ
environment
envvar
envvar_dict
eoff
eoffset
ep
epilog
epoch
eps
epsilon
eq_default
equal
equals
err
err2
err_line
err_no
error
error_code
error_details
error_fmt
error_handler
error_info
error_message
error_msg
error_on_eof
error_prompt
error_reason
error_result
error_status_hint
error_type
errors
errors_of_cls
errs
esc_char
esc_quote
escaped
escapes
estimate
estimated_duration
estimated_duration_seconds
estimated_prompt_tokens
et
etag
etype
ev
eval
eval_str
event
event_bus
event_counts
event_data
event_dict
event_id
event_name
event_streamer
event_type
event_types
events
evidence
evt
evt_type
ex
ex_data
exact
exact_cnt
exact_dup
exact_groups
nvidia-ml-py
examples
exc
exc_class
exc_dir
exc_group
exc_info
exc_map
exc_tb
exc_traceback
exc_type
exc_val
exc_value
exception
exception_action
exception_types
exceptions
excgrp
exchange_rate
exchange_rate_dict
excinfo
exclude
exclude_chars
exclude_connection
exclude_editable
exclude_fields
exclude_path
exclude_paths
exclude_patterns
exclude_session
exclude_set
exclude_tests
excluded
excluded_path
excluded_paths
excludes
exclusion_path
exclusions
exe
exe_filename
exec
exec_prefix
executable
execute
execution
execution_agent
execution_context
execution_id
execution_time
execution_time_ms
executor
exemplar
exename
exist_ok
existing
existing_agent
existing_user
exists
exit
exit_code
exp
exp_base
expand
expand_all
expand_dir
expand_special
expand_tabs
expanded
expansion
expansions
expect
expected
expected_agent
expected_cls_name
expected_exception
expected_fields
expected_parse_results
expected_status
expected_type
expected_value
expected_version
expecteds
experience_type
expiration
expires
expires_at
expires_days
expires_delta
expires_in
expires_in_hours
expiry
explicit_abi
explicit_candidates
exponential
export
export_symbols
exported_names
exports
expose_headers
expr
expr1
exprs_arg
exprtokens
ext
ext_counts
ext_hook
ext_name
extend_lifetime
extend_ttl
extension
extensions
extra
extra_args
extra_compile_args
extra_data
extra_dep
extra_env
extra_environ
extra_groups
extra_index
extra_lines
extra_link_args
extra_objects
extra_ok_returncodes
extra_postargs
extra_preargs
extra_source
extra_target_name
extract_dir
extract_metadata
extras
extras_
extras_override
extras_requested
extras_spec
exts
f
f1
f2
f_args
f_in
f_kwargs
f_out
f_str
f_strs
f_val
fa
factor
factory_boy
factory_fn
fail
fail_if_above
fail_on
fail_threshold
failed
failure_reason
failure_tests
failure_threshold
failures
faiss_ver
fallback
fallback_e
fallback_encoding
fallback_planner
fallback_tilde_path
fallback_to_certifi
false
fam
family
fancy_option
fast_acquire
fast_ok
fatal
fault
fb
fc
fd
feats
feature
feature_config
feature_flag
feature_key
feature_name
features
feedback
fence_starts
fetch_function
fetcher
ff
fg
fget
fh
fi
fid
field
field_encryptor
field_errors
field_name
field_specifiers
fieldname
fields
file
file1
file2
fileOrStream
file_content
file_data
file_descriptor
file_errors
file_findings
file_group
file_handler
file_hash
file_id
file_ids
file_info
file_like
file_logging
file_mod
file_moves
file_name
file_or_filename
file_or_name
file_path
file_path_str
file_ranges
file_rel_path
file_result
file_size
file_size_mb
file_storage_domain
file_svc
file_type
file_url
file_values
filecache
filemode
filename
filenames
fileno
filenos
fileob
fileobj
fileobject
fileop
filepath
filepaths
files
files_checked
files_errors
files_processed
filesafe
filetype
fillvalue
filter
filter_
filter_conditions
filter_criteria
filter_dict
filter_instance
filter_metadata
filter_name
filtered
filtered_events
filtered_logs
filtername
filters
filters_path
final
final_mypy
final_payload
final_ruff
final_status
final_version
find_links
find_others
finder
finding
finding_id
finding_text
findings
fingerprint
finished_style
finished_text
first
first_row
fit
fix
fix_func
fix_rsfs
fix_zipimporter_caches
fixpath_prefix
fixture_func
fixturedef
fixturevalue
fl
flag
flag_pattern
flag_value
flagged
flags
flat
flat_list
flat_sln
flatten
flavor
float
float_str
flt
flush_interval
fmode
fmt
fn
fname
fnext
fns
fo
fold
folder
folder_name
follow_path_symlink
follow_redirects
follow_symlinks
font
font_aspect_ratio
font_dir
font_name
font_size
footer
fopts
for_binary
for_filename
for_req
for_update
forbidden
forbidden_domains
forbidden_operations
forbidden_paths
force
force_all
force_express
force_interactive
force_jupyter
force_outdir
force_prefix
force_reinstall
force_scan
force_teacher
force_terminal
force_windows
fore
foreground
forever
format
format_args
format_control
format_str
format_type
formats
formatter
formatter_name
formattername
forward_ref
found
found_name
found_raw_name
found_user
fp
fp1
fp2
frag
frag2
fragment
fragments
frame
frame_index
frame_summary
framework
framing_type
free
frequency
frequency_penalty
frm
from_
from_agent
from_commit
from_email
from_exc
from_file
from_module
from_version
frontend_scan
frozen_default
frozenset
fs_id
fs_type
fspath
fstype
full
full_distribution_name
full_dump
full_env
full_indents
full_items
full_text
fullname
fullnames
fullpath
fully_qualified_target
fully_qualified_types_names
func
func1
func2
func_else
func_info
func_name
func_node
funcdict
funcname
funcs
function
function_breakdown
function_call
function_info
functions
fused_scores
fut
future
g
g1
g2
gap
gates
gauge
gch
gemini_service
gen
general_options
generate_thumbnails
generated
generated_by
generation
generator
generator_flags
generic_repo
get_config
get_console_width
get_datetime
get_ident
get_infos
get_ipython
get_remote_version
get_time
get_type_hints
getattr
getitem
getter
glibc_major
glibc_max
glist
glob
global_dict
global_options
globally_managed
globalns
globals
globs
glyph
goal
goal_description
goal_repo
gone_in
good_agent
got
gots
gotten_hash
grant_id
graph
green
green1
green2
group
group_exception
group_files
group_func
group_last
group_name
group_no
group_prober
group_stack
group_tuple
grouped
grouped_by_dir
grouped_errors
grouped_exceptions
groupname
groups
gsum_value
guard
guard_risk
gui
guid
gyp_dict
gyp_file
gyp_file_name
gyp_name
gyp_path
gyp_path_to_build_output
gyp_path_to_build_path
gyp_target_name
gyp_target_toolset
gyp_to_build_path
gyp_to_ninja
gyp_to_ninja_path
gyp_to_unique_output
gz_file
h
h2
halt_level
handler
handler_name
handlers
happy_eyeballs_delay
hard
hard_delete
has
has_any
has_backend_arg
has_error
has_exception
has_file
has_input_path
has_next
has_prev
has_request_arg
has_retry_after
hasattr
hash
hash_
hash_name
hash_options
hash_value
hashable
hashed
hashed_invalidation
hashed_password
hashes
hashname
hashval
hdrsize
head
head_bytes
header
header_dict
header_end
header_fields
header_formatter
header_key
header_name
header_part
header_parts
header_validator_index
header_value
headers
heading
health
health_check_interval
health_data
health_path
health_response
healthy
heavy_user
height
help
help_
help_option
help_string
help_text
help_tuple
heuristic
hex
hex_color
hex_digest
hex_len
hexnums
hide_cursor
hide_root
hierarchical
highlight
highlight_lines
highlights
hint
hint_stmt
hints
hist_execution
historical_results
history
history_deque
history_limit
history_path
hit
hits
hkey
home
home_var
hook
hook_name
host
host_port
hostname
hosts
hour
hour_str
hours
hpe
hsv_ranges
html
html_body
http1
http2
http_method
http_status
http_version
httpcore_stream
httplib_request_kw
i
i1
i18n_keys
i2
ican
icon
id
id_
idempotency_key
ident_chars
identbodychars
identchars
identifier
identifiers
identity
idfun
idl
idle
ids
idx
ie
ienc
if_node
ig
ignore_cleanup_errors
ignore_config_files
ignore_dependencies
ignore_egg_info_dir
ignore_errors
ignore_expr
ignore_fn
ignore_installed
ignore_option_errors
ignore_requires_python
ignore_threshold
ignored_setting
iid
im
image
image_path
image_url
imp
impl
impl_cls
implementation
implicit
import_line
import_name
import_node
import_path
import_statement
import_stmt
importance
importance_below
importance_score
importance_threshold
importer
importer_type
importlib
imports
imports_added
inAccumNames
in_aot
in_dict
in_file
inactive_agent
inactive_session
incdirs
incl
include
include_archived
include_bytecode
include_content
include_context
include_description
include_dir
include_dirs
include_editables
include_egg
include_expired
include_extras
include_file
include_hidden
include_list
include_logs
include_lsb
include_metadata
include_new_lines
include_oslevel
include_patterns
include_perception
include_scores
include_sensitive
include_separator
include_separators
include_tags
include_tasks
include_uname
include_values
include_vector
include_vectors
included_file
includes_from_cflags
incoming
incompatibilities
incompatible_ids
incompatible_reqs
inconsistencies
incr
increment
ind
ind_data
indent
indentStack
indent_guides
indent_increment
indent_level
indent_size
index
index_name
index_type
index_url
index_url_user_password
index_urls
indexed
indexed_files
indicator
indices
infer_variance
infile
info
info_dir
info_plist
infoitem
information
infos
infp
ingest_path
ingested
inherit
inherited_role
inherits
inifiles
init_chars
init_dict
init_file
init_node
init_result
initial
initial_content
initial_knobs
initial_message
initial_mypy
initial_progress
initial_ruff
initial_value
inline_styles
inner
inner_line
inp
input
input_
input_control
input_controller
input_data
input_file
input_hash
input_path
input_string
input_text
input_tokens
input_type
inputs
ins_string
insecure_skip_verify
insert
insert_line
inside_aot
inspect
inst
inst_next_char
inst_req
install_dir
install_req
install_requirements
installation
installation_dir
installations
installed
installed_file
installed_path
installed_record_path
installed_rows
installer
installer_file
instance
instream
instring
instruction
instructions
int
int_
int_expr
integration
intel_update
intent_name
intermediate_manifest
internal
interpreters
interval
interval_s
interval_sec
interval_seconds
invalid_exc
invalid_token
investment_details
invite_data
io_dict
ip
ip_address
iphoneos
iphonesimulator
ipname
ireq
ireqs
isNew
is_32bit
is_active
is_attrib
is_branch
is_command_start
is_editable
is_empty
is_executable
is_filename
is_gui
is_healthy
is_list
is_local
is_msbuild
is_online
is_public
is_regex
is_required
is_reversed
is_safe
is_satisfied_by
is_syntax
is_token
is_valid
isatty
isinstance
iso_code
iso_string
isodate
isolated
isolated_mode
issubclass
issue
issue_type
issuer
issues
issues_by_owner
istate
it
it_token
it_value
italic
item
item_key
item_type
item_value
itemseq
iter
iter_locals
iter_primary
iterable
iterable_or_value
iterable_positions
iterables
iteration_result
iterations
iterator
iters_secondary
j
jaeger_endpoint
jar
jargon
java_version
jit_ok
jit_repo
jitter
job
job_config
job_id
job_name
job_result
join_string
json
json_data
json_file
json_format
json_instance
justify
PyJWT
jwt_secret
jwt_secret_key
k
k1
k8s_file
kCFURLPOSIXPathStyle
kCGColorSpaceGenericRGB
kCGImageAlphaPremultipliedLast
kCIInputAspectRatioKey
kCIInputBackgroundImageKey
kCIInputImageKey
kCIInputScaleKey
kCIOutputImageKey
k_ratio
kb
kb_id
kb_ids
keep
keep_alive
keep_count
keep_separator
keepalive_expiry
key
key1
key2
key_class
key_file
key_fn
key_func
key_info
key_parent
key_part
key_password
key_prefix
key_rotation_enabled
keyfile
keyfunc
keyname
keyoff
keyring_provider
keys_to_delete
keysets
keyval
keyword
keywords
kg_service
killed_process
killed_processes
kind
kinds
klass
knowledge_graph
kubeconfig
kv
kv_store
kw
kw_only_default
kwargs
kwargs_
kwds
l
label
label_key
label_list
label_value
labelkwargs
labelnames
labels
labels_string
labelvalues
lang
lang_counts
lang_filter
lang_flag
lang_rules
language
languages
largest
last
last_accessed
last_activity
last_attempt
last_cell
last_jobs
last_modified
last_row
last_ts
latencies
latency
latency_ms
layer
layer_num
layout_height
layout_lines
layout_name
layout_row
layouts
lazy_wheel
ldcmd
ldflags_libs
leading_data
leaf
learner
learning_pipeline
leaving
left
left_split
leftmost
legacy
legacy_resolver
legacy_windows
len
length
letters
level
level_width
levelno
levels
levels_from
levels_to
lexer
lexer_name
lexername
lexers
lexical_index
lexical_scores
lf
lhs
lib
lib_dep
lib_dir
lib_name
lib_type
libname
libnames
libraries
library
library_dir
library_dirs
library_path
libs
libtoolflag
license_file
license_files
light
limit
limit_seconds
limit_user
limited_user
limiter
limiter_type
limits
line
line1
line2
line3
line4
line5
line6
line7
line8
line_end
line_index
line_no
line_num
line_number
line_numbers
line_range
line_source
line_start
line_token
lineno
linenumber
lines
link
link1
link2
link_collector
link_dep
link_id
link_is_in_wheel_cache
link_path
linked_memory_id
linker_cmd
linker_exe_ne
linker_na
linker_ne
links
links_to_fully_download
lint
linux
list
listOfLists
list_
list_all_matches
list_files
list_hook
listener
listeners
literal
literal_ast
live_table
lk
ll
llm
llm_client
llm_planner
llm_port
llm_result
llm_router
llm_text
ln
ln_msg
lname
lnk_lead
lnk_rest
load_config_fn
load_only
load_result
loaded
loaded_backends
loader
loader_type
loc
loc1
loc_
local_address
local_index
local_mode
local_only
local_path
local_pathify
local_port
local_result
local_vars
local_version
localns
localrev
locals
locals_hide_dunder
locals_max_length
locals_max_string
location
locations
locator
locators
lock
lock_timeout
lock_timeout_minutes
lock_timeout_sec
lockfile
locn
log
log_entry
log_failed_cmd
log_file
log_level
log_locals
log_path
log_time
log_time_format
log_to_console
log_to_file
log_type
log_type_dir
logger
logger_name
logical_prober
login_data
login_times
long
long_agent
long_and_short
long_option
longest
lookup_cand
lower
lower_is_better
lowerkey
lslice
lst
lvl
m
m1
m2
m_val
mac
mac_epoch
macos10_16_path
macro
macros
python-magic
magic1
magic2
mailer
major
major_version
make_install_req
maker
manager
manager_file
manifest
manifest_base_name
manifest_file
manifest_files
manifest_flags
manifest_json
manifest_path
manifests
map
map_path
mapping
maps
margin
mark_control
mark_spaces
marker
marker_string
markers
markup
mask
mask_char
master_key
mat
match
matchString
match_all
match_dir
match_parameters
match_type_of
matcher
matches
matchobj
max
max_access_frequency
max_age
max_age_days
max_age_hours
max_age_minutes
max_agents_per_owner
max_attempt_number
max_attempts
max_backups
max_batch_size
max_buffer_size
max_bytes
max_calls
max_chars
max_chunk_size
max_concurrency
max_concurrent
max_concurrent_backups
max_concurrent_batches
max_concurrent_events
max_concurrent_tasks
max_conn
max_connections
max_content_length
max_cost_tier
max_delay
max_depth
max_distance
max_file_size
max_frames
max_group_size
max_help_position
max_histogram_buckets
max_hops
max_incomplete_event_size
max_issues
max_items
max_iterations
max_iters
max_keepalive_connections
max_keys
max_latency_ms
max_len
max_length
max_limit
max_lines
max_loc
max_log_size_mb
max_login_attempts
max_matches
max_measure
max_memories_per_group
max_memory_mb
max_metrics_history
max_mismatches
max_norm_size
max_overflow
max_paragraphs
max_pool_size
max_queue
max_rate
max_redirects
max_request_size
max_requests
max_requests_per_hour
max_requests_per_minute
max_results
max_retries
max_rounds
max_score
max_sentences
max_session_age
max_sessions_per_user
max_size
max_size_bytes
max_size_mb
max_steps
max_stream_length
max_string
max_tag_length
max_tags
max_token_age
max_tokens
max_val
max_vectors
max_version
max_width
max_widths
max_wildcards
max_workers
maxfds
maximum
maximums
maxlen
maxlineno
maxsize
maxsplit
maxval
mcls
mcs
md
me
measure_max
measure_min
measurement_data
mem
mem_id
member
members
meminfo
memories
memory
memory_cache_size
memory_count
memory_data
memory_delta
memory_id
memory_ids
memory_repo
memory_repository
memory_result
memory_service
memory_threshold
memory_type
memoryview
mentor_cfg
merge
message
message_content
message_data
message_id
message_ids
message_length
message_parts
message_pattern
message_repo
message_repository
message_size_bytes
message_type
messages
messages_delta
shtab
meta_kwargs
metadata
metadata_config
metadata_contents
metadata_directory
metadata_file
metadata_filename
metadata_filter
metadata_name
metadata_updates
metadata_version_exc
meth
method
method_call
method_func
method_name
method_whitelist
methods
metric
metric_base
metric_counter
metric_family
metric_groups
metric_histogram
metric_name
metric_path
metric_type
metric_value
metrics
metrics_adapter
metrics_collector
metrics_health
metrics_hook
metrics_ok
metrics_port
mfa
mfa_manager
mfa_verified
mffilename
mgr
mgr_file
mi
micros_str
mid
middlewares
midl_include_dirs
migration_checker
migration_init
mime_type
mimetypes
min
minElements
min_chunk_size
min_conn
min_coverage
min_data_points
min_interval
min_length
min_level
min_line_length
min_lines
min_measure
min_participants
min_quality
min_samples
min_score
min_similarity
min_size
min_tokens
min_update_interval_seconds
min_val
min_ver
min_version
min_width
min_widths
minimal
minimum
minimum_size
minimums
minor
minor_version
minuend
minute
minute_limit
minute_str
minutes
minval
mismatch
miss
miss_all
misses
missing
missing_all
missing_code_exit
missing_deps
missing_file
missing_ok
mm
mo
mobile
mockATW32
mockRegister
mockWin32
mock_client
mock_config
mock_cpu_percent
mock_decode
mock_exec
mock_factory_class
mock_filters_class
mock_gauge
mock_get_logger
mock_heal
mock_httpx
mock_llm_class
mock_logger
mock_popen
mock_post
mock_router
mock_router_class
mock_session
mock_shell
mock_subprocess
mock_triage_class
mock_virtual_memory
mod
mod_name
mod_path
modal
mode
model
model_class
model_cls
model_config
model_count
model_family
model_file
model_groups
model_id
model_info
model_instance
model_name
model_path
model_paths
model_size
model_spec
model_type
model_version
models
modes
modification_index
modified
modifier
modifier_id
modifying_pip
modname
module
moduleOrReq
module_file
module_key
module_map
module_name
module_names
module_path
modulename
modules
moe_canary_ratio
monitor
monitoring
monitoring_service
monkeypatch
month
month_str
more-itertools
more_reqs
morsel
mounts
move
moves
mp
mr
mro_entries
ms
msbuild
msbuild_base
msbuild_name
msbuild_settings_name
msbuild_tool_name
msbuild_toolset
msg
msg_del
msg_id
msglen
msgs
msvs_name
msvs_setting
msvs_settings
msvs_settings_name
msvs_tool_name
msvs_tool_settings
msvs_value
mt
mt_in
multi
multiline
multiline_strings
multipart_boundary
multipart_chunksize
multipart_threshold
multipath
multiplier
multiprocess_mode
must_trigger_pat
mv
mvarfmt
n
n1
n2
name
name1
name2
name_
name_dups
name_hint
name_lead
name_prefix
name_prober
name_query
name_rest
name_string
name_value_list
named
names
namespace
namespace_handler
namespace_path
namespaces
namespaces_
native_ansi
native_histogram
native_histogram_value
nbytes
nc
ndef
ndx
near_cnt
near_dup
need_value
need_wheel
needle
needles_and_replacements
neg
negative_alias
negative_opt
neighbor
neighbor_id
nest_level
nest_limit
nest_lvl
nested
net
netaddr
netloc
netloc_no_user_pass
network
network_backend
network_mount_info
new
new_aliases
new_body
new_caps
new_certs
new_content
new_context
new_dep
new_events
new_extras
new_field
new_file
new_filename
new_identities
new_import
new_index_urls
new_key
new_length
new_line
new_line_start
new_lines
new_loc
new_method
new_mode
new_name
new_node
new_nurseries
new_password
new_path
new_pattern
new_payload
new_pbxproj_path
new_peek
new_perms
new_position
new_progress
new_purpose
new_requirement
new_role
new_root
new_rules
new_scheme
new_score
new_segments
new_size
new_state
new_style
new_summary_text
new_tags
new_text
new_title
new_url
new_value
new_values
new_version
newdigest
newl
newline
newurl
next
nextLoc
next_bytes
next_cursor
next_item
next_line
next_multiple
next_offset
next_run_at
next_sentence
next_word
nexttoc
ng
nid
ninja_file
nm
no
no_auto_all
no_cache
no_color
no_eggs
no_index
no_input
no_python_version_warning
no_user_config
no_wrap
node
node1
node2
node_id
node_type
nodes
nonce_count
norm
norm_dups
norm_results
norm_score
normal
normal_user
normalize
normalized_to_canonical_keys
normcase
normed_name
notChars
not_chars
note
note_stmt
notes
notification
notification_channels
notification_connections
notification_type
now
nparams
npath
npn_protocols
ns
ns_pkg
nsp
nt
num
num_bytes
num_clients
num_pools
num_return_sequences
num_tests
num_updates
num_workers
number
numeric_owner
nums
nursery
nv
nx
o
o_names
o_str
o_strs
ob
obj
objRef
obj_ext
obj_path
object
objectNumber
object_
object_hook
object_pairs_hook
objective
objects
objs
oblique
observation
obtain_mapping_value
occ
occurrences
ocr_engine
ocr_languages
od
off
offline_user
offset
offset2
offset_hour_str
offset_minute_str
offset_sign_str
offset_x
offset_y
offsets
ok
ok_del
ok_env
ok_hl
ok_ln
ok_py
ok_t
ok_ts
ok_v
old
old_count
old_csv_rows
old_field
old_file
old_head
old_import
old_inplace
old_keys
old_memories
old_method
old_mod
old_name
old_password
old_pattern
old_pool
old_qualified_target
old_session
old_spec
old_target
old_tempdir_manager
old_url
old_value
old_values
older_than
older_than_days
oldest_key
oldname
oldver
ollama_client
ollama_running
ollama_url
om
om_samples
omit_repeated_times
on
on_error
on_returncode
on_stderr
once
onerror
only
only_if_unset
op
op1
op2
opExpr1
opExpr2
op_id
op_list
op_name
open
open_brace
open_bracket
open_out
open_paren
open_tag
open_token
openai_api_key
openai_client
openai_model
openapi
openapi_doc
openapi_url
opener
openmetrics
oper
operDef
operation
operation_data
operation_name
operation_request
operation_type
operator
operator_callable
operators
opinion
opinion_value
opt
optElements
opt_str
optimization
optimization_criteria
optimization_type
optimize
option
option_factory
option_order
option_pairs
option_table
optional
options
options_str
optname
opts
optsep
orch_result
orchestrator
ord
order
order_by
order_default
order_only
ordered
ordered_reqs
ordering
org_id
organization
organization_id
orig
orig_bases
orig_enc
orig_header
orig_path
orig_script
orig_stream
orig_value
origin
origin_host
origin_port
original
original_agent
original_content
original_error
original_filename
original_name
original_names
original_path
original_plan
original_response
original_text
original_url
original_value
original_version
original_word
os_release_file
osc
oserrors
osname
osx_epoch
other
other_code
other_files
other_libraries
other_memory
other_path
other_pbxproject
other_scheme_paths
other_vector
others
otlp_endpoint
our_f
our_role
out
out_dir
out_line
out_lines
out_name
out_path
outbox
outbox_config
outbox_repo
outbox_service
outbuf
outcome_holder
outcomes
outdir
outf
outfile
outgoing
output
output_binary
output_data
output_dir
output_fd
output_file
output_file_name
output_filename
output_html
output_index
output_json
output_libname
output_lines
output_mapping
output_name
output_of_set
output_of_where
output_path
output_progname
output_text
output_tokens
outputs
outrows
overflow
overlap
overlap_size
override
overrides
overwrite
overwrite_existing
owner
owner_field
owner_id
owner_issues
owner_user_id
p
p1
p2
p95_ms
p99_ms
pPeerCertContext
p_filesz
p_fmt
p_idx
p_name
p_offset
p_opt
p_type
p_ver
pa
paArgs
package
packageName
package_
package_data
package_detail
package_details
package_dir
package_json
package_name
package_or_requirement
package_path
package_set
packages
packages_ok
packed
pad
pad_left
pad_right
pad_top
padded_prospective
padded_spec
page
page_items
page_num
page_size
page_url
page_validator
pagerduty_key
pagination
pair
pairs
panel
par
para
para_start
paragraph
parallel_builds
param
param2
param_generator
param_key
param_list
param_name
param_value
parameter_updates
parameters
params
params_hash
paramstring
parent
parent_count
parent_dir
parent_ext
parent_filter_name
parent_id
parent_index
parent_memory_id
parent_message_id
parent_path
parent_plan_id
parent_prefix
parent_role_id
parent_roles
parent_root
parent_task
parent_version
parentdir
parents
parseElementList
parse_action_exc
parse_all
parse_float
parse_methods
parsed
parsed_build_file
parsed_escape
parsed_files_stack
parsed_frag
parsed_host
parsed_line
parsed_path
parsed_port
parsed_query
parsed_req
parsed_scheme
parsed_toolset
parsed_url
parsed_userinfo
parser
parsing_probs
part
part_num
part_number
part_of_all
part_size
partial
partially_downloaded_reqs
participants
partition
partition_count
partition_items
partition_key
partition_mod
partitioned_items
partitions
parts
pass_fds
passage
passed
passes_gate
password
password_hash
password_min_length
pat
patch
patchlevel
path
path1
path2
path_a
path_b
path_dir
path_entries
path_filter
path_glob
path_item
path_part
path_parts
path_pattern
path_to_base
path_to_gyp
path_tuple
path_variant
pathname
paths
pathsegments
pattern
pattern_hash
pattern_name
pattern_owners
pattern_text
patterns
payload
payload_ref
payload_sha256
payload_size_bytes
payload_uri
pbe
pbxtd
pch_commands
pch_source_ext
pe
peak
peek
peer_cert
pending
per_chunk_overhead
per_doc
per_user
percent_encodings
percentage
percentile
perception
performance_metrics
period
period_end
period_start
perm
perm_data
perm_name
permission
permission_id
permission_ids
permission_manager
permission_name
permission_names
permissions
permit_editable_wheels
perms
persistent
person
pfe
phase
phase_name
phase_num
phone
phone_number
phony
phrase
picked
pickled_cmd
pid
piece
pii_pattern
pii_type
ping_result
pip_audit_result
pip_runnable
pipe
pipeline_type
pk
pkg
pkg_dir
pkg_info
pkg_name
pkg_path
pkg_roots
pkg_strings
pkgname
pkgs
pkgutil
placeholder
plain_password
plain_text
plan
plan_data
plan_id
plan_only
plan_repo
plan_type
planned
planner
planning_agent
plat
plat_spec
plat_specific
platform
platform_
platform_info
platforms
platlib
plist
plist_path
plugin_env
plugins
pod
point
point_key
points
policies
policy
policy_input
policy_name
poll_interval
pong_result
pool
pool_block
pool_config
pool_connections
pool_kwargs
pool_maxsize
pool_size
pool_timeout
poolmanager
port
portal_
pos
pos_num
position
posno
possible_targets
post
post_commands
post_parse
post_style
postbuild
postgresql_connection
pout
pow
pp_opts
pre
precedence
precision
precompiled_header
pred
predepends
predicate
prediction_window_minutes
prefer_binary
prefer_paragraphs
preference_updates
preferences
prefers_installed
prefix
prefix_as_string
prefix_lines
prefix_path
preload_content
prepared_request
preparer
prepend
preprocess
prerelease
prerelease_num
prereleases
prerequisite
prerequisite_index
presence_data
presence_penalty
preserve
preserve_metadata
preserve_mode
preserve_symlinks
preserve_times
preset_eval
pretty
prev
prev_item
prev_loc
prev_peek
prev_result
previous_version
primary_passages
primary_retriever
print
print_results
printables
priority
priors
privacy
privacy_budgets
private
prober
probers
problem
problems
proc
process
process_identifier
process_to_kill
processing_time
processor
processor_fn
producer
product_dir
production
profanity_words
profile
profile_data
prog
program
progress
progress_bar
progress_callback
progress_filter
proj
project
project_cfg
project_file_name
project_id
project_info
project_name
project_path
project_root
project_target
project_url
project_version
prometheus_port
promote_to_memory
prompt
prompt_lines
prompting
prop
properties
property
property_modifier
property_name
property_type
props
props_file
protected
protected_paths
proto-plus
proto_cls
protocol
protocol_cls
protocol_method
protocol_version
protocols
protos
provided
provided_code
provided_extra
provided_fingerprint
provider
provider_factory
provider_func
provisioning
provisioning_data
proxies
proxy
proxy_auth
proxy_basic_auth
proxy_config
proxy_headers
proxy_ip
proxy_key
proxy_kwargs
proxy_origin
proxy_ssl_context
proxy_url
pstr
pth
pth_prefix
public_code
public_paths
pulse
pulse_style
purelib
purpose
push
pusher
pw
pwd
px
py
py_bstr
py_data
py_file
py_filenames
py_files
py_imports
py_map
py_msg
py_path
py_reqs
py_version
py_version_info
pycompile
pyfile
pyfuncitem
pypi_version
pyproj
pyproject
pyproject_toml
python
python_executable
python_files
python_str
python_version
pyver
pyversion
q
qg
quad
qualified
qualified_class_name
qualified_list
qualified_target
quality
quality_threshold
queries
query
query2
query_data
query_hash
query_name
query_request
query_string
query_text
query_type
query_vector
question
queue
queue_sizes
quick
quiet
quote
quoteChar
quoted
quoted_string
quoter
r
r1
r2
r_args
r_kwargs
ra
rag_engine
rag_service
raise_app_exceptions
raise_errors
raise_fatal
raise_on_status
raise_outofdata
range
range_start
rate
rate_deque
rate_info
rate_limit
rate_limit_per_minute
rate_limit_result
rate_limit_window
rate_store
rating
ratio
raw
rawDep
raw_bytes
raw_cells
raw_count
raw_input
raw_key
raw_license_expression
raw_line
raw_lines
raw_name
raw_output
raw_path
raw_s
raw_socket
raw_stream_bytes
rb
rbac_ok
rbac_result
rblk
rc
re
re_escape
re_flags
re_highlight
read
read_mode
read_size
read_user
reader
pyreadline3
readme
real_source
reason
reason_phrase
reasoning_marker
reasoning_type
reasons
rec
receive
receive_stream
recency_days
recent_session
recipient_id
recipient_type
recipients
recommendation
recommended_action
record
record_data
record_file
record_id
record_path
record_reader
records
recovery_timeout
recreate
recs
recsize
recurse
recursion
recursive
red
red1
red2
redirect
redirect_stderr
redirect_stdout
redis
redis_client
redis_host
redis_kwargs
redis_metrics
redis_password
redis_port
redis_url
reducefunc
redundant
ref
ref_col
ref_name
ref_sha
refactoring_type
reference
referrer
refill_rate
refresh_per_second
refresh_token
reg_token_hash
regex
regexes
region
registration
registry
registry_info
registry_path
registry_uri
reinit_subcommands
rej
rejected
rel
rel_path
related
relation_types
relations_count
relationships
relationships_serialized
relative
relative_output
relative_path
release
release_file
relenc
relevance_score
reload
reloff
relpath
rels
remainder
remaining_space
remediation_plan
remember_me
remote
remote_addr
remote_address
remote_host
remote_object
remote_origin
remote_path
remote_port
remote_url
removal_version
remove_quotes
remover
render_output
renderable
renderable1
renderable2
renderable_width
renderables
rendered_cell
rep
repeat
repl
repl_str
replace
replace_conflicting
replace_with
replacement
replacements
replicas
repo
repo_dir
repo_factory
repo_file
repo_groups
repo_health
repo_root
repo_type
report
report_file
report_level
report_path
report_type
reporter
reporthook
repos
repository
repr
repr_callable
repr_str
req
req_attr
req_data
req_description
req_ext
req_file
req_file_path
req_files
req_info
req_name
req_path
req_set
req_spec
req_str
req_string
req_time
req_to_install
reqs
reqs_added
reqs_to_build
reqt
request
request_body
request_count
request_data
request_desc
request_headers
request_hooks
request_id
request_method
request_params
request_setting
request_timeout
request_url
requested
requested_extras
requested_group
requested_items
requested_model
requested_revision
requests
requests_per_minute
requests_per_window
require_all
require_all_scopes
require_bound
require_connected
require_content_filter
require_digits
require_hashes
require_https
require_local
require_lowercase
require_markers
require_mfa_for_admin
require_review_above
require_sig
require_special
require_uppercase
require_virtualenv
require_where_clause
required
required_actions
required_capabilities
required_file
required_level
required_packages
required_pat
required_perm
required_permission
required_permissions
required_perms
required_raw
required_role
required_scope
required_tokens
requirement
requirement_keys
requirement_or_candidate
requirement_string
requirements
requires
requires_bkp
requires_mfa
requires_python
reranked
reranked_passages
reranker
reranker_name
res
research_agent
reserved
reserved_agent
resname
resolution_notes
resolve_symlinks
resolved
resolved_by
resolver
resolver_variant
resource
resource_builder
resource_extension
resource_id
resource_msg
resource_name
resource_owner_id
resource_path
resource_type
resources
resources_ok
resources_reader
resources_root
resp
respect_retry_after_header
respect_sentences
response
response_content
response_headers
response_kw
response_marker
response_or_ref
response_time
response_time_ms
rest
restart_callback
restat
restore_path
restored_by
result
result_extension
result_index
result_item
result_payload
resultlist
results
resume_retries
retention_days
retention_hours
retries
retrieve
retriever
retriever_name
retriever_weights
retry_attempts
retry_backoff
retry_count
retry_delay
retry_error_callback
retry_error_cls
retry_object
retry_state
retryable
return_scores
return_value
retval
reuse_port
rev
rev_options
reverse
reversed
revision
reward
rewrite_rules
rewritten
rexmatch
rhs
rich_args
rich_renderable
rich_tracebacks
rich_visited_set
rid
right
rightLeftAssoc
right_split
risk
risk_description
risk_level
risk_result
risk_thresholds
rlhf
roaming
role
role_data
role_id
role_ids
role_info
role_name
roles
room_connections
root
root_dir
root_ireqs
root_name
root_package
root_path
root_pkg
root_reqs
root_scheme_paths
rootblk
rootdir
roots
round
round_count
round_data
round_id
round_index
round_name
route
route_hint
route_pattern
router
router_attr
row
row_cell
row_cells
row_count
row_id
row_styles
rows
rp
rpath
rpm_opt
rpt
rr
rready
rslice
rspfile
rspfile_content
rt
rule
rule_engine
rule_id
rule_name
rule_no
rule_planner
rule_source
rule_source_basename
rule_source_dirname
rule_source_ext
rule_source_root
rule_type
rules
run_frame
run_func
run_id
run_name
run_test_results
run_test_success
run_test_target
run_tests_report
runner
runtime_library_dirs
runtime_regression
rx
s
s0
s1
s2
s3
s3_bucket
s_m
sa
safe
safe_box
safe_result
safety_config
safety_engine
safety_level
safety_mode
safety_policy
safety_result
safety_results
same
sample
sample_id
sample_labels
sample_rate
sample_size
samples
sandbox
sanitization_type
sanitization_types
save_path
saved_exc
saved_values
savelist
sc
sc_t
sc_v
scalar_positions
scalar_types
scalars
scaling_result
scan_only
scan_request
scan_result
scan_results
scenario
schema
schema_class
schema_file
schema_version
schemas
scheme
scheme_key
scls
scope
scope1
scope2
scope_id
score
score_tensor
score_threshold
scored
scores
screen_capture
screen_perception
screenshot
screenshot_context
screenshot_path
script
script_args
script_dir
script_fd
script_name
script_path
script_scheme_paths
google-auth
sdist_directory
sdk
sdk_based
search
search_data
search_mode
search_params
search_path
search_query
sec
sec_format
sec_str
sec_trust_ref
second
second_agent
second_char
secondary_passages
secondary_retrievers
seconds
secret
secret_key
secret_name
secret_password
secret_url
secret_word
section
section_items
section_key
section_options
section_parser_method
sections
secure_host
secure_origin
secure_port
secure_protocol
security_ctx
security_events
seed
seed_data
seed_node_ids
seed_test_data_flag
seed_test_data_option
seen
seg
segment
segment_style
segments
selectors
selection_prefs
self
semicolon
send
sender_id
sender_name
sender_type
sensitive
sensitivity
sent
sent_msg
sentence
sentiment_result
sep
sep1
sep2
separator
separator_index
seperator
seq
sequence
sequential
serialize
serializer
server
server_hostname
server_side
server_switch_event
service
service_health
service_name
service_role
service_status
service_version
services
sess
session
session_data
session_factory
session_getter
session_hooks
session_id
session_id_length
session_repo
session_setting
session_timeout
session_timeout_minutes
session_type
sessions
set
setReferencePosition
set_clauses
set_metadata
setattr
sets
setting
setting_key
setting_type
settings
settings1
settings2
settings_key
settings_name
settings_update
setup_command
setup_py
setup_py_path
setup_script
setuptools_cfg
severity
severity_threshold
sgr
sha256
shard
shards
shared_intermediate_dir
shim_paths
shim_pytest
shlib_suffix
short_agent
short_name
short_option
short_paths
shortpath
should_error
should_fix
should_ignore
should_match
should_rename_legacy
show
show_choices
show_default
show_deprecation
show_groups
show_level
show_locals
show_path
show_results_names
show_speed
show_stdout
show_time
sidedeck
sig
sig_b64
sigma
sign
sign_password
sign_str
signal
signal_name
signals
signature
signature_b64
signature_filename
signature_required
signer
signum
similar_plan
similarity
similarity_metric
similarity_threshold
sims
simulator_config_dict
since
since_version
sink
site
site_config_file
sites
situation
six_module_name
size
size_delta
size_or_format
size_str
sizeof
sizes
skill
skill_name
skill_registry
skip
skip_disconnected
skip_keys
skip_missing
skip_reason
skip_unknown
skip_validations
skipto_arg
sl
slack_webhook
sleep
sleep_ms
slfkjsldkfj
slice
slo
slot
slots_var
slow_request_threshold
sm
smallest_weight_key
smax
smin
sms1
sms2
sms_manager
smtp_host
smtp_password
smtp_port
smtp_username
snake
snapshot
snapshot_data
snapshot_id
snippets_map
sock
sock_or_fd
sock_or_sslobj
sock_type
sockaddr
socket
socket_options
socktype
soft_delete
solution_file
solution_version
sort
sort_by
sort_key
sort_keys
sort_order
sort_tuple
sorted
sorted_data
sorted_scripts
source
source_address
source_buckets
source_code
source_data
source_dir
source_extension
source_file
source_filenames
source_files
source_id
source_key
source_memory_id
source_metadata
source_name
source_path
source_quality
source_tree
source_type
source_url
sources
sources_array
sources_groups
sources_set
sp
span
span_end
span_start
span_style
spans
spans_name
spec
spec_path_lists
spec_prefix
spec_str
specialttype
specification
specifications
specifier
specifier_set
specifiers
specs
speed
speed_estimate_period
spin_chars
spinner
spinner_name
spinner_style
split
split_commas
split_segments
splitter
sql
src
src_bytes
src_cmd
src_dir
src_file
src_files
src_mod
src_name
src_option
src_path
src_pattern
src_record_path
src_rel
src_templ
srcfile
srcroot
ss
ssl_context
ssl_error
ssl_version
st
stack
stacklevel
stacks
stage
staged
stale
stale_time
standard
standard_compatible
standard_lib
start
start_action
start_column
start_date
start_file
start_id
start_index
start_line
start_new_session
start_position
start_response
start_time
startidx
startupinfo
stat
stat_lines
state
state_file
state_update
statefile
statement
states
static_libs
staticmethod
stats
status
status_code
status_codes
status_eq
status_filter
status_forcelist
std3_rules
std_handle
stderr
stderr_b
stdin
stdout
stdout_b
stdout_only
stem
step
step_data
step_definition
step_dict
step_dicts
step_duration
step_func
step_id
step_index
step_name
step_payload
step_result
step_results
steps
steps_data
stmt
stop
stop_after
stop_after_delay
stop_on
stops
storage_backend
storage_class
storage_dir
storage_path
storage_result
storage_root
storage_service
store
stored_code
stored_fingerprint
stored_hash
stored_hmac
str
str_type
strat
strategies
strategy
strategy_kwargs
strategy_type
stream
stream_any
stream_contents
stream_id
stream_name
stream_result
strength
strength_boost
strength_reduction
strg
strict
strict_map_key
strict_types
string
string_ip
string_network
strip
strip_dir
strip_trailing_zero
strm
strs
structure
stubs
student
style
style_before
style_cache
style_definition
style_id
style_map
style_name
style_prefix
style_rule
style_stack
stylebegin
styledef
styleend
stylename
styles
stylesheet_rules
stylized_range
sub
sub_check
sub_chunk
sub_id
sub_item
sub_node
sub_result
sub_type
subclass
subdir
subdirectory
subdirs
subentry
subitem
subject
subkey
subkeys
submitted
subnode
subreq
subs
subscriber
subscriber_id
subscribers
substring
subsystem
subtask
subtask_id
subtask_result
subtitle
subtitle_align
subtrahend
succ
success
success_action
success_msg
successes
suffix
suffixes
suggest_actions_for_user
suggester
suggestion
suggestions
sum
sum_value
summary
summary_memory
summary_path
super
superclass
supported
supported_tags
suppress
suppress_GT
suppress_LT
suppress_entity
suppress_logging
suppress_no_index
suppress_ragged_eofs
svc
svc_name
svg_main_code
swig_opts
switch_event
sym
symbol
symbol_name
symbols
symroot
syms
sync_conn
sync_data
syntax_error
syntax_line
sysdir
system
system_service
t
t1
t2
tab_size
table
table_column
table_counts
tables
tablet
tabs
tag
tag_id
tag_str
tag_text
tag_to_priority
tags
tail
tar
tar_obj
tar_ref
target
target_arch
target_clients
target_desc
target_dict
target_dicts
target_dir
target_fps
target_groups
target_id
target_image
target_info
target_is_directory
target_lang
target_layer
target_list
target_memory_id
target_mod
target_model
target_ms
target_name
target_path
target_percentage
target_python
target_text
target_ts
target_url
target_user_id
target_value
targets
targets_file
tarinfo
task-planner
task_context
task_data
task_description
task_group
task_id
task_list
task_repository
task_request
task_status_future
task_timeout
task_type
tasks
tb
td
tdef
te
teacher
teacher_response
team_id
team_identifier
teams_by_status
telemetry
telemetry_service
temp
temp_build_dir
temp_dir
temp_width
tempd
temperature
template
template_id
template_key
template_name
template_path
template_rel
tempname
temporal_window_hours
tenant_id
tenant_id_param
term
terminal_text
grafana-api
test_after
test_data
test_db_session
test_dir
test_exit
test_file
test_func
test_key
test_line
test_name
test_pass_rate
test_prompt
test_prompts
test_result
test_string
test_type
test_url
tester
text
text_backgrounds
text_bg
text_chunks
text_fg
text_format_no_percentage
text_group
text_source
texts
tf
tf_local
tf_map
tfp
tg
tgt
tgt_mod
tgt_set
the_file
thefile
this
thisExpr
thread_pool_size
threat_detection_config
threat_level
threat_type
threat_types
threshold
threshold_minutes
threshold_type
thresholds
thumbnail_size
tid
time
time_taken
time_unit
time_window
timeout
timeout_duration
timeout_s
timeout_seconds
timeout_value
times
timestamp
timings
title
title_align
title_justify
title_style
titles
tlb
tld
tline
tls
tls_in_tls
tls_standard_compatible
tmp
tmp_descriptor
tmp_dir
tmp_dist_dir
tmp_fd
tmp_file
tmp_handler
tmp_name
tmp_path
tmpdir
tmpnam
tmptokens
to
to_clean
to_copy
to_email
to_exc
to_file
to_install
to_replace
to_scan_again
to_version
toccount
tocid
tocmagic
tocsize
tok
token
token_budget
token_count
token_estimates
token_estimator
token_hash
token_map
token_type
tokenizer
tokenlist
tokens
tokens_processed
tokensource
tokn
toks
tol
tolerance
too_long
too_short
tool
tool_config
tool_file
tool_file_path
tool_id
tool_name
tool_resolver
tools
toolset
top
top_down
top_k
top_level_pkg
top_p
topic
toplevel_build_dir
toplevel_dir
torch_ver
total
total_count
total_files
total_length
total_result
total_stats
totp_issuer
tp
trace
traceback
tracebacks_code_width
tracebacks_extra_lines
tracebacks_max_frames
tracebacks_show_locals
tracebacks_suppress
tracebacks_theme
tracebacks_width
tracebacks_word_wrap
tracer
tracing_enabled
track_thread
tracker
tracking_uri
trailing_data
trainer
training_config
training_connections
training_data
training_id
training_job
training_job_id
training_job_repository
training_params
training_result
training_results
training_service
traj_records
trajectory_dir
transcription_id
transform
transform_fn
transform_netloc
transient
transitional
transport_stream
trap
traversable
tree_lines
trend
trigger
trigger_file
trigger_pattern
trim_ratio
trio_exc_map
trust_env
trust_internet
trusted_hosts
try_codegen
ts
ts_deps
ts_file
ts_imports
ts_map
ts_msg
tsconfig
tsconfig_path
tt
ttl
ttl_hours
ttl_sec
ttl_seconds
ttype
tuple
tuples
turn
tvar
txt
typ
type
type_
type_counts
type_name
type_param
type_params
typecode
typed_results
typename
types
types_
typevarlike
typing_is_inline
u
u_string
ua
uds
uid
uid_agent
uid_user
umask
un
unbound
unbuffered_output
undef
undef_macros
undefined
undefined_names
underline
unfiltered
unicode
uniq
unique
unique_candidates
unit
unix_epoch
unix_ns
unix_sec
unmapped
unpacked
unpacked_source_directory
unparsed
unparsed_data
unparsed_key
unprocessed
unquote_results
unresolved_only
unused
unverified_chain
uow
uow_factory
upd
update_data
update_i
update_j
update_request
updated
updated_agent
updated_at
updated_by
updated_node
updated_user
updater
updates
upgrade
upgrade_strategy
upload_args
upload_result
uploaded_by
upper
uptime
uri
url
url1
url2
url_label
url_scheme
url_user_password
url_without_auth
urlfetch_resp
urlfetch_retries
urlopen_kw
urls
usage
usage_tokens
use
use_abspath
use_app_for_writes
use_arxiv
use_ascii
use_bin_type
use_bulk
use_cache
use_caching
use_case
use_core_for_reads
use_datetime
use_deprecated_feature
use_encryption
use_environment
use_fallback
use_forwarding_for_https
use_git
use_gpu
use_hybrid
use_list
use_local
use_mock_jit
use_new_feature
use_pep517
use_regex
use_s3
use_separate_mspdbsrv
use_single_float
use_ssl
use_streaming
use_turbo
use_user_site
use_wikipedia
user
user_agent
user_context
user_counts
user_cursors
user_data
user_email
user_event_list
user_file_path
user_function
user_home_prefix_len
user_id
user_ids
user_input
user_key
user_log_file
user_message
user_msg
user_only
user_pass
user_permissions
user_repo
user_repository
user_requested
user_role
user_roles
user_scopes
user_service
user_session
user_supplied
user_text
username
uses_vcxproj
using_user_site
uts46
uuid_string
v
v2
va
vad_filter
val
valid
valid_agent
valid_archs
valid_status
valid_types
configobj
validate_certificate
validation
validation_func
validation_level
validation_result
validation_results
validation_type
validator
validators
valoff
value
value2
value_list
values_dict
values_parser
var
var_list
var_name
var_value
variable
variable_name
variables
variant
variants
variation
varname
vars
vartype
vas
vc_class
vc_dir
vc_min_ver
vcproj
vcs
vcs_backend
ve
vec
vec1
vec2
vector
vector_dim
vector_embeddings
vector_id
vector_index
vector_results
vector_scores
vector_store
vector_store_port
vector_store_service
vectors
vectorstore
vendor_pkg
vendored_names
ver
verStr
ver_maj
ver_min
verb
verbose
verbosity
verification_type
verified
verifier_model
verify
verify_backups
verify_mode
vers
vertexai
version_control
version_id
version_info
version_number
version_part
version_str
version_string
versions
versions_found
versions_set
versions_to_check
vertical
vertical_overflow
vh
vid
view
viewer_id
violation
violation_details
violations
visible
visited_ids
visual_prober
vk
vks
vlist
vm_name
vm_release
vm_vendor
vminfo
vn
vo
voffset
voice
volattrs
voldate_hr
volfsid
volume
vt
vuln
vuln_type
vv
vw
vx
vy
w
w_action
w_category
w_message
w_module
wait
wait_seconds
waiting
walk_item
walk_up
wantdirs
wanted
warmup
warn
warn_env_var
warn_for
warn_on_hash_mismatch
warn_opt
warn_script_location
warn_threshold
warning
warning_class
warning_type
warnings
wav_path
weak_self
webhook
webhook_config
webhook_id
websiteProperties
websocket-client
weight
weight_max
weight_min
wgts
what
wheel
wheel_cache
wheel_data
wheel_dir
wheel_directory
wheel_hash
wheel_name
wheel_obj
wheel_path
wheel_tags
wheel_zip
whence
where
where_args
where_clause
whitelist
whitelist_fields
whl_zip
width
widths
wiki_start_pages
wildcards
win32
win_base
window
window_minutes
window_sec
window_seconds
window_size
wininst
winterm
with_line_numbers
with_requires
word
word_chars
word_wrap
words
worker
worker_count
worker_id
worker_index
worker_ix
workers
workflow
workflow_id
workflow_type
working_directory
wrap
wrapable
wrapped
wrapped_line
wrapping_args
wrapping_func
wrapping_kwargs
wready
write
write_alias_target
write_file
writer
writer_func
written
wrong
ws
ws_health
wschar
wsgi_errors
wslit
x
x64
x86
x_admin_token
x_key
xche_hashable
xck
xcode_build
xcode_setting
xcode_settings
xcode_value
xcode_version
xcv
xml
xml_file
xready
xs
xx
y
y_key
yaml_file
yanked_versions_set
year
year_str
yes
yield_requests
ys
z
zf
zfile
zinfo
zip
zip_file
zip_filename
zip_stat
zipf
zipfile_obj
zipped_items
zone
zulu_time
```

## TypeScript Imports Added
```
E:\zeta-monorepo\.cleanup_backup\redundant_1757367219\backup_dirs\consolidation_trash\20250907_175850\apps\desktop\src\services\inputController.ts: +1
E:\zeta-monorepo\apps\backend\apiClient.ts: +30
E:\zeta-monorepo\apps\backend\auth.ts: +6
E:\zeta-monorepo\apps\backend\typedClient.ts: +8
E:\zeta-monorepo\apps\backend\wsSchema.ts: +3
E:\zeta-monorepo\apps\desktop\vite.config.ts: +3
E:\zeta-monorepo\apps\desktop\electron\main.ts: +3
E:\zeta-monorepo\apps\desktop\electron\preload.ts: +4
E:\zeta-monorepo\apps\desktop\electron\main\crash-reporter.ts: +6
E:\zeta-monorepo\apps\desktop\electron\main\health.ts: +7
E:\zeta-monorepo\apps\desktop\electron\main\retention.ts: +3
E:\zeta-monorepo\apps\desktop\src\analytics\components\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\analytics\hooks\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\analytics\hooks\useRealtimeMetrics.ts: +5
E:\zeta-monorepo\apps\desktop\src\analytics\__tests__\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\apiClient.ts: +30
E:\zeta-monorepo\apps\desktop\src\api\auth.ts: +6
E:\zeta-monorepo\apps\desktop\src\api\client.ts: +19
E:\zeta-monorepo\apps\desktop\src\api\errorCodes.ts: +110
E:\zeta-monorepo\apps\desktop\src\api\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\typedClient.ts: +8
E:\zeta-monorepo\apps\desktop\src\api\wsSchema.ts: +3
E:\zeta-monorepo\apps\desktop\src\api\generated\client.ts: +7
E:\zeta-monorepo\apps\desktop\src\api\generated\index.ts: +17
E:\zeta-monorepo\apps\desktop\src\api\generated\types.ts: +5
E:\zeta-monorepo\apps\desktop\src\api\generated\core\ApiError.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\generated\core\ApiRequestOptions.ts: +9
E:\zeta-monorepo\apps\desktop\src\api\generated\core\ApiResult.ts: +1
E:\zeta-monorepo\apps\desktop\src\api\generated\core\CancelablePromise.ts: +13
E:\zeta-monorepo\apps\desktop\src\api\generated\core\index.ts: +7
E:\zeta-monorepo\apps\desktop\src\api\generated\core\OpenAPI.ts: +15
E:\zeta-monorepo\apps\desktop\src\api\generated\core\request.ts: +43
E:\zeta-monorepo\apps\desktop\src\api\generated\models\ActionResponse.ts: +1
E:\zeta-monorepo\apps\desktop\src\api\generated\models\HealthStatus.ts: +1
E:\zeta-monorepo\apps\desktop\src\api\generated\models\index.ts: +11
E:\zeta-monorepo\apps\desktop\src\api\generated\models\LogItem.ts: +6
E:\zeta-monorepo\apps\desktop\src\api\generated\models\RuleResponse.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\generated\models\RuleUpsert.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\generated\models\TrainingJob.ts: +8
E:\zeta-monorepo\apps\desktop\src\api\generated\models\TrainingJobCreate.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\generated\models\UploadRequest.ts: +2
E:\zeta-monorepo\apps\desktop\src\api\generated\models\UploadResponse.ts: +1
E:\zeta-monorepo\apps\desktop\src\api\generated\services\DefaultService.ts: +27
E:\zeta-monorepo\apps\desktop\src\api\generated\services\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\automation\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\automation\components\index.ts: +5
E:\zeta-monorepo\apps\desktop\src\automation\hooks\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\automation\hooks\useWorkflowEngine.ts: +34
E:\zeta-monorepo\apps\desktop\src\automation\types\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\automation\types\workflow.ts: +28
E:\zeta-monorepo\apps\desktop\src\automation\__tests__\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\components\index.ts: +21
E:\zeta-monorepo\apps\desktop\src\components\about\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\components\common\index.ts: +4
E:\zeta-monorepo\apps\desktop\src\components\dashboard\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\components\nav\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\components\Settings\index.ts: +4
E:\zeta-monorepo\apps\desktop\src\components\stats\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\components\__tests__\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\constants\index.ts: +86
E:\zeta-monorepo\apps\desktop\src\constants\OPENAPI_HASH.ts: +7
E:\zeta-monorepo\apps\desktop\src\context\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\controllers\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\controllers\inputController.ts: +18
E:\zeta-monorepo\apps\desktop\src\events\bus.ts: +3
E:\zeta-monorepo\apps\desktop\src\events\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\events\types.ts: +13
E:\zeta-monorepo\apps\desktop\src\features\index.ts: +13
E:\zeta-monorepo\apps\desktop\src\features\dashboard\index.ts: +4
E:\zeta-monorepo\apps\desktop\src\features\training\index.ts: +6
E:\zeta-monorepo\apps\desktop\src\features\training\oneClick\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\hooks\index.ts: +4
E:\zeta-monorepo\apps\desktop\src\hooks\useChat.ts: +6
E:\zeta-monorepo\apps\desktop\src\hooks\useHotkey.ts: +4
E:\zeta-monorepo\apps\desktop\src\hooks\useVoice.ts: +3
E:\zeta-monorepo\apps\desktop\src\lib\openapiHashGuard.ts: +11
E:\zeta-monorepo\apps\desktop\src\lib\websocket.ts: +32
E:\zeta-monorepo\apps\desktop\src\lib\ws\rag.ts: +5
E:\zeta-monorepo\apps\desktop\src\memory\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\memory\components\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\memory\hooks\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\memory\hooks\useMemoryAPI.ts: +34
E:\zeta-monorepo\apps\desktop\src\memory\types\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\memory\types\memory.ts: +48
E:\zeta-monorepo\apps\desktop\src\memory\__tests__\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\pages\index.ts: +13
E:\zeta-monorepo\apps\desktop\src\providers\index.ts: +5
E:\zeta-monorepo\apps\desktop\src\router\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\actionPlan.ts: +10
E:\zeta-monorepo\apps\desktop\src\services\actionQueue.testshim.ts: +9
E:\zeta-monorepo\apps\desktop\src\services\actionQueue.ts: +9
E:\zeta-monorepo\apps\desktop\src\services\admin.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\agents.ts: +7
E:\zeta-monorepo\apps\desktop\src\services\analytics.ts: +2
E:\zeta-monorepo\apps\desktop\src\services\apiService.ts: +66
E:\zeta-monorepo\apps\desktop\src\services\assistants.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\auth.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\buildInfo.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\cache.ts: +46
E:\zeta-monorepo\apps\desktop\src\services\cacheManager.ts: +5
E:\zeta-monorepo\apps\desktop\src\services\chat.ts: +11
E:\zeta-monorepo\apps\desktop\src\services\commandHandler.ts: +14
E:\zeta-monorepo\apps\desktop\src\services\config.enterprise.ts: +11
E:\zeta-monorepo\apps\desktop\src\services\config.ts: +17
E:\zeta-monorepo\apps\desktop\src\services\consent.ts: +2
E:\zeta-monorepo\apps\desktop\src\services\contextManager.ts: +2
E:\zeta-monorepo\apps\desktop\src\services\emergency.ts: +1
E:\zeta-monorepo\apps\desktop\src\services\federated.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\feedback.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\feedbackProcessor.ts: +14
E:\zeta-monorepo\apps\desktop\src\services\files.ts: +10
E:\zeta-monorepo\apps\desktop\src\services\health.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\httpMeta.ts: +10
E:\zeta-monorepo\apps\desktop\src\services\index.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\learningRouter.ts: +13
E:\zeta-monorepo\apps\desktop\src\services\llm.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\log.ts: +8
E:\zeta-monorepo\apps\desktop\src\services\memory.ts: +7
E:\zeta-monorepo\apps\desktop\src\services\performance.ts: +2
E:\zeta-monorepo\apps\desktop\src\services\permissionManager.teststub.ts: +1
E:\zeta-monorepo\apps\desktop\src\services\permissionManager.ts: +10
E:\zeta-monorepo\apps\desktop\src\services\planning.ts: +6
E:\zeta-monorepo\apps\desktop\src\services\plugin.manifest.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\plugin.ts: +7
E:\zeta-monorepo\apps\desktop\src\services\privacy.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\rag.ts: +7
E:\zeta-monorepo\apps\desktop\src\services\robotFacade.ts: +1
E:\zeta-monorepo\apps\desktop\src\services\robotIntegration.ts: +14
E:\zeta-monorepo\apps\desktop\src\services\ruleEngine.ts: +14
E:\zeta-monorepo\apps\desktop\src\services\screenCapture.ts: +10
E:\zeta-monorepo\apps\desktop\src\services\security.ts: +24
E:\zeta-monorepo\apps\desktop\src\services\session.ts: +9
E:\zeta-monorepo\apps\desktop\src\services\settings.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\socket.ts: +12
E:\zeta-monorepo\apps\desktop\src\services\streaming.ts: +18
E:\zeta-monorepo\apps\desktop\src\services\system.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\telemetry.enhanced.ts: +8
E:\zeta-monorepo\apps\desktop\src\services\telemetry.safe.ts: +11
E:\zeta-monorepo\apps\desktop\src\services\telemetry.ts: +6
E:\zeta-monorepo\apps\desktop\src\services\training.ts: +6
E:\zeta-monorepo\apps\desktop\src\services\trainingSocket.ts: +12
E:\zeta-monorepo\apps\desktop\src\services\upload.ts: +2
E:\zeta-monorepo\apps\desktop\src\services\voice.ts: +6
E:\zeta-monorepo\apps\desktop\src\services\webhooks.ts: +6
E:\zeta-monorepo\apps\desktop\src\services\websocket.ts: +10
E:\zeta-monorepo\apps\desktop\src\services\ws.ts: +14
E:\zeta-monorepo\apps\desktop\src\services\wsSchema.ts: +47
E:\zeta-monorepo\apps\desktop\src\services\wsSchemaValidators.ts: +4
E:\zeta-monorepo\apps\desktop\src\services\api\auth.ts: +8
E:\zeta-monorepo\apps\desktop\src\services\api\client.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\api\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\cache\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\services\cache\indexedDBCache.ts: +3
E:\zeta-monorepo\apps\desktop\src\services\cache\rendererCache.ts: +8
E:\zeta-monorepo\apps\desktop\src\stores\chatStore.ts: +5
E:\zeta-monorepo\apps\desktop\src\stores\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\stores\searchStore.ts: +2
E:\zeta-monorepo\apps\desktop\src\test\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\test\setup.ts: +8
E:\zeta-monorepo\apps\desktop\src\tests\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\tests\setupElectronESM.ts: +3
E:\zeta-monorepo\apps\desktop\src\tests\setupElectronReset.ts: +1
E:\zeta-monorepo\apps\desktop\src\tests\ws-mock.ts: +21
E:\zeta-monorepo\apps\desktop\src\tests\doubles\better-sqlite3.ts: +1
E:\zeta-monorepo\apps\desktop\src\tests\doubles\electron.ts: +2
E:\zeta-monorepo\apps\desktop\src\tests\doubles\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\tests\doubles\metrics_ref.ts: +2
E:\zeta-monorepo\apps\desktop\src\tests\doubles\node-http.ts: +1
E:\zeta-monorepo\apps\desktop\src\tests\doubles\nut-tree-nut-js.ts: +11
E:\zeta-monorepo\apps\desktop\src\tests\doubles\systeminformation.ts: +3
E:\zeta-monorepo\apps\desktop\src\types\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\types\ws.ts: +14
E:\zeta-monorepo\apps\desktop\src\ui\index.ts: +33
E:\zeta-monorepo\apps\desktop\src\ui\components\index.ts: +10
E:\zeta-monorepo\apps\desktop\src\ui\hooks\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\ui\hooks\useTheme.ts: +23
E:\zeta-monorepo\apps\desktop\src\ui\providers\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\ui\styles\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\ui\styles\themes.ts: +13
E:\zeta-monorepo\apps\desktop\src\ui\styles\tokens.ts: +30
E:\zeta-monorepo\apps\desktop\src\ui\__tests__\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\utils\crypto.ts: +5
E:\zeta-monorepo\apps\desktop\src\utils\fs.ts: +3
E:\zeta-monorepo\apps\desktop\src\utils\index.ts: +2
E:\zeta-monorepo\apps\desktop\src\utils\logger.ts: +1
E:\zeta-monorepo\apps\desktop\src\utils\ocr.ts: +4
E:\zeta-monorepo\apps\desktop\src\utils\rateLimiter.ts: +3
E:\zeta-monorepo\apps\desktop\src\utils\whisper.ts: +4
E:\zeta-monorepo\apps\desktop\src\__tests__\contracts.app-config.test.ts: +4
E:\zeta-monorepo\apps\desktop\src\__tests__\contracts.plugin.manifest.test.ts: +1
E:\zeta-monorepo\apps\desktop\src\__tests__\contracts.ws.training.test.ts: +1
E:\zeta-monorepo\apps\desktop\src\__tests__\feedbackProcessor.test.ts: +3
E:\zeta-monorepo\apps\desktop\src\__tests__\index.ts: +3
E:\zeta-monorepo\apps\desktop\src\__tests__\ipcCache.metrics.server.spec.ts: +4
E:\zeta-monorepo\apps\desktop\src\__tests__\ipcCache.metrics.spec.ts: +7
E:\zeta-monorepo\apps\desktop\src\__tests__\ipcCache.spec.ts: +5
E:\zeta-monorepo\apps\desktop\src\__tests__\learningRouter.test.ts: +5
E:\zeta-monorepo\apps\desktop\src\__tests__\plugin.registry.test.ts: +2
E:\zeta-monorepo\apps\desktop\src\__tests__\socket.test.ts: +11
E:\zeta-monorepo\apps\desktop\src\__tests__\streaming.test.ts: +8
E:\zeta-monorepo\apps\desktop\src\__tests__\trainingSocket.test.ts: +7
E:\zeta-monorepo\apps\desktop\tests\batchReset.test.ts: +3
E:\zeta-monorepo\apps\desktop\tests\setupTests.ts: +29
E:\zeta-monorepo\apps\desktop\tests\test_cache.ts: +1
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\agent.ts: +32
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\cognitive\codeAnalyzer.ts: +74
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\memory\memoryManager.ts: +20
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\planner\actionPlanner.ts: +66
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\planner\reactPlanner.ts: +117
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\planner\toolExecutor.ts: +49
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\agent\reasoner\chainOfThought.ts: +53
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\devops\deploymentStrategies.ts: +62
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\devops\devopsOrchestrator.ts: +43
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\devops\dockerManager.ts: +67
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\devops\kubernetesManager.ts: +69
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\devops\pipelineGenerator.ts: +92
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\devops\terraformGenerator.ts: +100
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\explainability\explainabilityEngine.ts: +171
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\explainability\explainabilityUtils.ts: +94
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\feedback\feedbackUtils.ts: +111
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\feedback\humanFeedbackLoop.ts: +148
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\integration\autonomousAI.ts: +31
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\integration\demo.ts: +85
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\integration\integratedAI.ts: +83
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\learning\metaLearner.ts: +153
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\memory\memoryManager.ts: +67
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\memory\vectorStore.ts: +73
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\observability\observabilitySystem.ts: +113
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\observability\observabilityUtils.ts: +58
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\ollama\client.ts: +25
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\ollama\models.ts: +6
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\ollama\types.ts: +15
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\optimization\autoTuner.ts: +69
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\optimization\performanceMonitor.ts: +72
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\plugins\pluginRegistry.ts: +107
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\plugins\pluginUtils.ts: +75
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\safety\safetyPolicyEngine.ts: +108
E:\zeta-monorepo\apps\zeta-ai-agent\src\core\safety\safetyUtils.ts: +28
E:\zeta-monorepo\apps\zeta-ai-agent\src\extension\extension.ts: +43
E:\zeta-monorepo\apps\zeta-ai-agent\src\extension\providers\chatProvider.ts: +49
E:\zeta-monorepo\apps\zeta-ai-agent\src\extension\providers\codeViewProvider.ts: +62
E:\zeta-monorepo\apps\zeta-ai-agent\src\extension\providers\statusBarProvider.ts: +13
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\masterTestRunner.ts: +109
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\runTests.ts: +62
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\testFramework.ts: +153
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\testRunner.ts: +18
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\integration\agent.test.ts: +32
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\integration\integrationTests.ts: +70
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\performance\performanceBenchmarks.ts: +63
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\safety\safetyValidation.ts: +130
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\scenarios\realWorldScenarios.ts: +120
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\unit\cache.test.ts: +11
E:\zeta-monorepo\apps\zeta-ai-agent\src\tests\unit\validation.test.ts: +12
E:\zeta-monorepo\apps\zeta-ai-agent\src\types\shared.ts: +39
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\batchProcessor.ts: +39
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\cache.ts: +22
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\configManager.ts: +50
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\index.ts: +43
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\performance.ts: +46
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\rateLimiter.ts: +29
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\smartCache.ts: +29
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\telemetry.ts: +61
E:\zeta-monorepo\apps\zeta-ai-agent\src\utils\validation.ts: +42
E:\zeta-monorepo\apps\zeta-ai-agent\tests\integration\comprehensive.test.ts: +33
E:\zeta-monorepo\apps\zeta-ai-agent\tests\mocks\ollamaServer.ts: +37
E:\zeta-monorepo\desktop\src\lib\preview\media.ts: +7
E:\zeta-monorepo\extension\src\extension.ts: +68
E:\zeta-monorepo\extension\src\test\extension.test.ts: +7
E:\zeta-monorepo\packages\ollama\src\index.ts: +7
E:\zeta-monorepo\packages\ollama\src\ollama-manager.ts: +37
E:\zeta-monorepo\packages\ollama\src\ollama-service.ts: +28
E:\zeta-monorepo\packages\shared\src\index.ts: +5
E:\zeta-monorepo\scripts\desktop_api_codegen.ts: +13
E:\zeta-monorepo\src\core\agent\agent.ts: +51
E:\zeta-monorepo\src\core\agent\cognitive\codeAnalyzer.ts: +29
E:\zeta-monorepo\src\core\agent\memory\memoryManager.ts: +12
E:\zeta-monorepo\src\core\agent\planner\actionPlanner.ts: +27
E:\zeta-monorepo\src\core\ollama\client.ts: +8
E:\zeta-monorepo\src\core\ollama\models.ts: +4
E:\zeta-monorepo\src\core\ollama\types.ts: +6
E:\zeta-monorepo\src\core\utils\cache.ts: +9
E:\zeta-monorepo\src\core\utils\monitoring.ts: +16
E:\zeta-monorepo\src\core\utils\rateLimiter.ts: +12
E:\zeta-monorepo\src\core\utils\validation.ts: +27
E:\zeta-monorepo\src\extension\extension.ts: +21
E:\zeta-monorepo\src\types\shared.ts: +28
E:\zeta-monorepo\tests\zeta-agent.test.ts: +8
E:\zeta-monorepo\apps\desktop\src\App.tsx: +9
E:\zeta-monorepo\apps\desktop\src\main-original.tsx: +98
E:\zeta-monorepo\apps\desktop\src\main.tsx: +93
E:\zeta-monorepo\apps\desktop\src\analytics\index.tsx: +5
E:\zeta-monorepo\apps\desktop\src\analytics\components\Dashboard.tsx: +14
E:\zeta-monorepo\apps\desktop\src\analytics\__tests__\dashboard.test.tsx: +15
E:\zeta-monorepo\apps\desktop\src\automation\AutomationPage.tsx: +24
E:\zeta-monorepo\apps\desktop\src\automation\index.tsx: +20
E:\zeta-monorepo\apps\desktop\src\automation\components\NodeLibrary.tsx: +24
E:\zeta-monorepo\apps\desktop\src\automation\components\TriggerPanel.tsx: +72
E:\zeta-monorepo\apps\desktop\src\automation\components\WorkflowEditor.tsx: +30
E:\zeta-monorepo\apps\desktop\src\automation\__tests__\workflow.test.tsx: +28
E:\zeta-monorepo\apps\desktop\src\components\ASRPanel.tsx: +7
E:\zeta-monorepo\apps\desktop\src\components\ChatPanel.tsx: +9
E:\zeta-monorepo\apps\desktop\src\components\ControlPanel.tsx: +54
E:\zeta-monorepo\apps\desktop\src\components\DatasetsPanel.tsx: +14
E:\zeta-monorepo\apps\desktop\src\components\DataUploadModal.tsx: +11
E:\zeta-monorepo\apps\desktop\src\components\EmergencyStop.tsx: +8
E:\zeta-monorepo\apps\desktop\src\components\FeedbackPanel.tsx: +11
E:\zeta-monorepo\apps\desktop\src\components\LanguageToggle.tsx: +4
E:\zeta-monorepo\apps\desktop\src\components\Layout.tsx: +37
E:\zeta-monorepo\apps\desktop\src\components\LearningPanel.tsx: +18
E:\zeta-monorepo\apps\desktop\src\components\LoginForm.tsx: +3
E:\zeta-monorepo\apps\desktop\src\components\MainDashboard.tsx: +20
E:\zeta-monorepo\apps\desktop\src\components\Navigation.tsx: +24
E:\zeta-monorepo\apps\desktop\src\components\PermissionDialog.tsx: +12
E:\zeta-monorepo\apps\desktop\src\components\RateLimitBadge.tsx: +6
E:\zeta-monorepo\apps\desktop\src\components\ResultsPanel.tsx: +9
E:\zeta-monorepo\apps\desktop\src\components\TrainingPanel.tsx: +18
E:\zeta-monorepo\apps\desktop\src\components\UpdateBanner.tsx: +6
E:\zeta-monorepo\apps\desktop\src\components\about\AboutModal.tsx: +11
E:\zeta-monorepo\apps\desktop\src\components\common\ErrorBoundary.tsx: +10
E:\zeta-monorepo\apps\desktop\src\components\common\LoadingFallback.tsx: +4
E:\zeta-monorepo\apps\desktop\src\components\dashboard\HealthBadge.tsx: +5
E:\zeta-monorepo\apps\desktop\src\components\nav\Sidebar.tsx: +10
E:\zeta-monorepo\apps\desktop\src\components\Settings\LoginBox.tsx: +12
E:\zeta-monorepo\apps\desktop\src\components\Settings\SafetySettings.tsx: +8
E:\zeta-monorepo\apps\desktop\src\components\stats\StatsCard.tsx: +2
E:\zeta-monorepo\apps\desktop\src\components\__tests__\LanguageToggle.test.tsx: +2
E:\zeta-monorepo\apps\desktop\src\context\AuthContext.tsx: +11
E:\zeta-monorepo\apps\desktop\src\features\dashboard\Dashboard.tsx: +6
E:\zeta-monorepo\apps\desktop\src\features\training\oneClick\Dropzone.tsx: +39
E:\zeta-monorepo\apps\desktop\src\memory\index.tsx: +11
E:\zeta-monorepo\apps\desktop\src\memory\MemoryPage.tsx: +52
E:\zeta-monorepo\apps\desktop\src\memory\components\KnowledgeExplorer.tsx: +43
E:\zeta-monorepo\apps\desktop\src\memory\__tests__\memory.test.tsx: +47
E:\zeta-monorepo\apps\desktop\src\pages\AssistantPage.tsx: +9
E:\zeta-monorepo\apps\desktop\src\pages\Chat.tsx: +3
E:\zeta-monorepo\apps\desktop\src\pages\ChatUpload.tsx: +63
E:\zeta-monorepo\apps\desktop\src\pages\Control.tsx: +3
E:\zeta-monorepo\apps\desktop\src\pages\Dashboard.tsx: +40
E:\zeta-monorepo\apps\desktop\src\pages\DatasetPage.tsx: +11
E:\zeta-monorepo\apps\desktop\src\pages\Logs.tsx: +45
E:\zeta-monorepo\apps\desktop\src\pages\OneClickLearning.tsx: +10
E:\zeta-monorepo\apps\desktop\src\pages\Settings.tsx: +63
E:\zeta-monorepo\apps\desktop\src\pages\Status.tsx: +3
E:\zeta-monorepo\apps\desktop\src\pages\Training.tsx: +6
E:\zeta-monorepo\apps\desktop\src\pages\TrainingPanel.tsx: +46
E:\zeta-monorepo\apps\desktop\src\providers\AppProviders.tsx: +9
E:\zeta-monorepo\apps\desktop\src\providers\PermissionProvider.tsx: +4
E:\zeta-monorepo\apps\desktop\src\providers\QueryProvider.tsx: +2
E:\zeta-monorepo\apps\desktop\src\router\AppRoutes.tsx: +8
E:\zeta-monorepo\apps\desktop\src\routes\Agents.tsx: +49
E:\zeta-monorepo\apps\desktop\src\ui\components\AccessibilityMenu.tsx: +27
E:\zeta-monorepo\apps\desktop\src\ui\components\AnimationWrapper.tsx: +26
E:\zeta-monorepo\apps\desktop\src\ui\components\ErrorDisplay.tsx: +20
E:\zeta-monorepo\apps\desktop\src\ui\components\LoadingSpinner.tsx: +11
E:\zeta-monorepo\apps\desktop\src\ui\components\Modal.tsx: +20
E:\zeta-monorepo\apps\desktop\src\ui\components\ResponsiveLayout.tsx: +17
E:\zeta-monorepo\apps\desktop\src\ui\components\ThemeToggle.tsx: +25
E:\zeta-monorepo\apps\desktop\src\ui\components\Toast.tsx: +18
E:\zeta-monorepo\apps\desktop\src\ui\providers\ThemeProvider.tsx: +20
E:\zeta-monorepo\apps\desktop\src\ui\__tests__\advanced-components.test.tsx: +31
E:\zeta-monorepo\apps\desktop\src\ui\__tests__\components.test.tsx: +24
E:\zeta-monorepo\apps\desktop\src\ui\__tests__\theme.test.tsx: +23
E:\zeta-monorepo\apps\desktop\src\__tests__\ChatPanel.test.tsx: +1
```

## TypeScript Dependencies Added
```
A
ACCURACY
ACTIONS
ACTIVE
ACTIVE_LEARNING
ADMIN_CONFIG
ADMIN_USERS
ADVANCED
AES
AGENT
AI
AIAgent
AI_DECIDES
AI_MODELS
ALERT
ALL
ANALYSIS
ANSWERED
APIRateLimiter
API_BASE
API_BASE_URL
API_KEY
API_URL_OBJ
APIs
APP_NAME
ARCHIVED
ARRAY
AS
ASR
ASSISTANT
ASSISTANTS
ATTENTION
AUDITOR
AUGMENTED
AUTH_001
AUTH_002
AUTH_003
AUTH_004
AUTH_005
AUTH_006
AUTH_007
AUTH_EXPIRED
AUTH_INVALID
AUTH_LOGIN
AUTH_REFRESH
AUTH_XXX
AUTO
AUTOMATED
AUTONOMOUS
AUTO_OPEN
Abort
AbortController
AbortError
AbortSignal
Aborted
Aborting
Accept
Access
Accessed
Accessibility
AccessibilityMenuProps
Accessible
Account
Achieved
Acting
Action
ActionBatcher
ActionConfig
ActionEvent
ActionNode
ActionPlan
ActionResponse
ActionStep
Actions
Activate
Activating
Active
ActiveLearningQuery
Activity
Adapt
Adaptation
AdaptationType
AdaptiveRateLimiter
Adapts
Add
Additional
Address
Adjust
Admin
Advanced
After
Agent
AgentAction
AgentConfig
AgentContext
AgentCreationError
AgentDeploymentError
AgentInteraction
AgentNotFoundError
AgentProfile
AgentState
AgentTeam
Aggregate
Ajv
Alert
AlertRule
AlertSystem
Algorithm
Alias
All
Allow
Allowed
AllowedIPCChannel
AllowedRegion
Allowlist
Already
Also
Alt
Alternative
AlternativeOption
Always
An
Analysis
AnalysisArgument
AnalysisConfig
AnalysisResult
AnalysisTemplate
AnalyticsPage
Analyze
Analyzed
Analyzing
AnimatePresence
Animated
Animation
AnimationWrapperProps
AnomalyDetection
Answer
Anthropic
Any
ApiCfgCtx
ApiConfig
ApiError
AppBoot
AppConfig
AppErrorBoundary
AppShortcutPayload
Application
Apply
Approach
Approximate
ArXiv
ArXivEntry
Architecture
Are
Area
Argo
Arial
ArrayBuffer
ArrayBufferLike
ArrayBufferView
Article
Artifacturl
Ask
Assess
Assessment
Assistant
AssistantReplyEvent
AssistantRequest
AssistantResponse
Assistants
Async
AsyncGenerator
Atom
AttachFile
Attempt
Attempted
Audience
Audio
AudioFile
Auth
AuthContextType
AuthProvider
Authentication
AuthenticationError
Authorization
AuthorizationError
Auto
Automated
Automatic
Autonomous
AutonomousAIOptions
AutonomousAIService
AutonomousAITestFramework
AutonomousResult
AutonomousTask
Autoscaler
Availability
Available
Average
Avg
Avoid
Azure
B
BACKEND_URL
BASE
BASIC
BATCH_LEARNING
BAYESIAN
BE
BEHAVIORAL
BENCHMARKS
BETWEEN
BIASED
BINARY
BIZ_001
BIZ_002
BIZ_003
BIZ_004
BIZ_005
BIZ_006
BIZ_007
BIZ_008
BIZ_009
BIZ_010
BIZ_011
BIZ_012
BIZ_013
BIZ_014
BIZ_015
BIZ_016
BIZ_XXX
BLOB
BLOCK
BLOCKED
BOOLEAN
BUILD_INFO
BULLET_LIST
Backend
Background
BackgroundVariant
Backoff
BackupError
Backward
Bad
Balance
Balanced
Bao
Bar
Barrel
Base
Based
Basic
Batch
BatchProcessorOptions
BatchRequest
BatchResponse
Bayesian
Bearer
Before
Begin
Behavior
Benchmark
BenchmarkMetrics
BenchmarkResult
Beside
Best
Better
Bias
Binary
BlinkMacSystemFont
Blob
BlobCallback
Blocked
Body
Boot
Border
Boundary
Break
Breaking
Breakpoints
Bridge
Browser
BrowserWindow
Budget
Buffer
Build
BuildId
BuildJob
Builder
Buildx
BurstRateLimiter
Business
BusinessRuleViolationError
Button
Bytes
C
CACHE_TTL
CALCULATION
CANCELLED
CAPABILITY
CARD
CAUSAL_ANALYSIS
CD
CHART
CHAT_CONVERSATIONS
CHAT_MESSAGES
CI
CI_COMMIT_SHA
CI_REGISTRY_IMAGE
CLARITY
CLASSIFICATION
CLEAN
CLOSED
CLOSING
CMD
CODE
CODE_BLOCK
CODE_GENERATION
CODE_REVIEW_PROMPTS
COLLABORATIVE
COMMON_SAFETY_PATTERNS
COMPLETE
COMPLETED
COMPLETENESS
COMPLIANT
COMPREHENSIVE
COMPRESSED
CONCLUSION
CONFIG_KEY
CONGRATULATIONS
CONNECTING
CONSENSUS
CONSISTENCY
CONTAINS
CONTENT
CONTENT_FILTERING
CONTEXTUAL
CONTINUOUS
CONVERSATION
COPY
CORRECTION
CORS
COUNTER
COUNTERFACTUAL
CPU
CREATE
CREATED
CREDENTIALS
CRITICAL
CRITICAL_RESPONSE_TIME
CRITIQUE
CSP_DEV
CSP_PROD
CSS
CSV
CUSTOM_ENDPOINTS
CUSTOM_REASONING
Cache
CacheConfig
CacheConnectionError
CacheEntry
CacheError
CacheManager
CacheMetrics
Caching
Calculate
Call
Calls
Camera
Canary
CanaryStep
Cancel
CancelError
CancelablePromise
Cancellable
Cancellation
CancellationToken
Cannot
Canvas
Capabilities
Capability
Capacity
Capture
CaptureOptions
Cards
Case
Category
Cause
Centralized
Certification
Chain
Challenge
Change
ChangeEvent
ChangeEventHandler
Changes
ChatClient
ChatClientMsg
ChatClientOptions
ChatCompletedEvent
ChatCompletedPayload
ChatErrorEvent
ChatErrorPayload
ChatInterface
ChatMessage
ChatMessageSchema
ChatOptions
ChatPage
ChatReply
ChatResponse
ChatResponseSchema
ChatServerMsg
ChatSessionError
ChatState
ChatTokenEvent
ChatTokenPayload
ChatView
Check
CheckCircle
Checking
Checkout
Checks
Chi
Children
Cho
Circular
Claim
Class
Classification
Classify
Clean
Cleaning
Cleanup
Clear
Click
ClickPayload
Client
Close
CloseEvent
CloudUpload
ClusterIP
CoT
CoTExample
CoTOptions
CoTReasoner
CoTResult
Code
CodeAnalyzer
CodeContext
CodeIssue
CodeOptimization
CodeReview
CodeSuggestion
CodeValidator
Codegen
Collaboration
CollaborationPattern
CollaborationPatternGenerator
Collaborative
Collect
Color
Colors
Combine
Command
Commit
Common
CommonJS
Compare
Compile
Complete
Completed
CompletionContext
CompletionItem
CompletionItemKind
CompletionItemProvider
CompletionSuggestion
Complex
Complexity
ComplexityLevel
Compliance
Component
Comprehensive
Concerns
Concurrency
Concurrent
Condense
Condition
ConditionNode
Conditions
Conduct
Confidence
Confident
Config
ConfigMap
ConfigMaps
ConfigValidationResult
ConfigValidator
Configuration
ConfigurationTarget
Configurations
Configure
Confirm
Connected
Connecting
Connection
ConnectionPoolExhaustedError
ConsentState
Consider
Consistency
Consistent
Consolas
Console
Consolidate
ConsolidationOptions
Constrained
Constraint
Constraints
Consumption
Container
ContainerInfo
Containment
Contains
Content
ContentFilter
ContextItem
ContextWindow
Continue
Continuous
Contract
Contrast
ControlPage
Controls
Convenience
Convenient
Conversation
ConversationContext
ConversationHistoryEvent
Convert
Copy
Core
Cost
Count
Counter
Counterfactual
CounterfactualExplanation
Courier
Crash
Crashpad
Create
CreateDatasetRequest
CreateMemoryRequest
Created
Creates
Creation
Creative
Critical
Cron
Ctrl
Ctx
Cung
Current
Custom
CustomEvent
Cycle
D
DATA
DATABASE_ACCESS
DATA_PRIVACY
DATA_PROCESSING
DB
DB_NAME
DEBUG
DECISION_TREE
DECLINING
DECREASING
DEFAULTS
DEFAULT_API_BASE_URL
DEFAULT_COT_EXAMPLES
DEFAULT_RATE_LIMIT
DEFAULT_WS_URL
DEGRADED
DELETE
DELETED
DEMONSTRATION
DEPENDENCY
DEPLOYMENT
DESKTOP_API_BASE_URL
DETAILED
DETECTED
DEV
DEVELOPER
DEV_ALLOW_WS_NO_TOKEN
DFS
DIAGRAM
DIR
DISABLED
DO
DOCKER
DOCKER_DRIVER
DOCKER_TLS_CERTDIR
DOCTYPE
DOCX
DOMException
DOMParser
DROP
Dangerous
DangerousPattern
Dark
DashboardPage
Data
DataIntegrityError
DataValidator
Database
DatabaseConnectionError
Dataset
DatasetInfo
DatasetStats
Datasets
Days
Deactivate
Deactivating
Deadlock
DeadlockError
Debug
DebugSolution
DebugStep
Debugging
Decision
DecisionContext
DecisionNode
Declining
Decorator
Decrease
Dedicated
Deep
DeepSeek
Default
DefaultModelManager
DefaultService
Defer
Define
Definitions
Delay
DelayNode
Delegate
Delete
Demo
Demonstrate
Demonstrates
Demonstration
Demonstrations
Deny
Dependencies
Deploy
DeployToProduction
Deploying
Deployment
DeploymentPlan
DeploymentResult
DeploymentRisk
DeploymentStatus
DeploymentStep
DeploymentStrategy
Derive
Describe
Description
Design
Desktop
Destroy
Detail
Detailed
Details
Detect
Determine
DevOps
DevOpsCapabilities
DevOpsConfig
Develop
Development
Device
Different
Difficulty
DifficultyLevel
Direction
Directory
Disabled
Disconnected
Discover
Discuss
Display
Disposable
Distribution
Diverse
Do
Docker
DockerConfig
Dockerfile
Document
Documentation
Documents
Domain
Don
Dots
Download
Downloading
Drag
DragEvent
Drop
Dummy
DuplicateRecordError
Duration
Durations
Dynamic
EASY
EDIT
EH
ELECTRON_SECURITY
EMAIL
ENABLE_CV
ENABLE_FEDERATED
ENABLE_TELEMETRY
ENCODE_PATH
END_USER
ENV
EPISODIC
EQ
EQUALS
ERROR
ERROR_MESSAGES
ES6
ESCALATE
ESCALATED
ESM
EVOLUTIONARY
EXAMPLE_BASED
EXAMPLE_SELECTION
EXCELLENCE
EXECUTED
EXECUTING
EXECUTION_ERROR
EXISTS
EXPERT
EXPIRED
EXPLANATION
EXPOSE
EXTERNAL
EXTERNAL_API
Earlier
Early
Easy
Edge
Edit
Education
Effectiveness
Efficiency
Efficiently
Effort
EffortLevel
Electron
Element
Email
Embedding
EmbeddingDimensionError
Embeddings
EmbeddingsRequest
EmbeddingsResponse
Emergency
Emit
Empty
Enable
Enabled
Enables
Encrypt
End
Endpoint
Enforcement
Engine
Enhance
Ensure
Enter
Entity
EntityNotFoundError
Entry
Enums
Env
Environment
Equal
Equals
Error
ErrorBoundaryState
ErrorDisplayProps
Errors
Escape
Estimate
Estimated
Evaluate
Evaluated
Evaluation
Event
EventName
EventPayload
EventPayloadMap
EventTarget
EventsBus
Every
Everything
Evidence
Exact
Example
Examples
Exception
Exclude
Exclusive
Execute
ExecutePlanOptions
Executed
Executing
Execution
ExecutionResult
Executor
Existing
Exit
ExpandLess
ExpandMore
Expect
Expectation
Expected
Expert
Expertise
ExpertiseLevel
Expire
Explain
Explainability
Explanation
ExplanationAudience
ExplanationFormatter
ExplanationHelpers
ExplanationLevel
ExplanationMetrics
ExplanationRequest
ExplanationResult
ExplanationTemplate
ExplanationType
ExplanationValidator
Exploitation
Explore
Exponential
Export
Exported
Exporting
Expose
Exposes
Expression
Extended
Extensibility
Extension
ExtensionConfig
ExtensionContext
ExternalServiceError
Extract
Extremely
F
FAILED
FAILURE
FAIR
FAISS
FATAL
FC
FE
FEATURE_IMPORTANCE
FEDERATED_JOBS
FEDERATED_ROUNDS
FEDERATED_STATUS
FEEDBACK
FEW_SHOT
FILE
FILES_DELETE
FILES_DOWNLOAD
FILES_LIST
FILES_UPLOAD
FILE_OPERATIONS
FILTERED
FINAL_ANSWER
FLAG
FOR
FROM
Facade
Factor
Factors
Factory
Fade
FadeTransition
Failed
Failures
Fair
Fairness
FakeWebSocket
Fallback
Fast
FastAPI
Fatal
Feature
FeatureFlags
FeatureImportance
Federated
Feedback
FeedbackAnalyzer
FeedbackBuilder
FeedbackCollector
FeedbackConfig
FeedbackIn
FeedbackIntegrationResult
FeedbackPayload
FeedbackQuality
FeedbackResult
FeedbackSource
FeedbackTestUtils
FeedbackType
Fetch
Few
File
FileItem
FileList
FileReader
Files
Fill
Filter
Filters
Final
Finalizing
Find
Finish
Finished
Fire
First
Fix
Flow
Flush
Focus
Font
For
Forbidden
Force
ForeignKeyViolationError
Form
FormContent
FormData
FormEvent
Format
Found
Framer
Framework
Frameworks
Free
Frontend
Full
Fullscreen
Function
FunctionDefinition
Functionality
Functions
GAUGE
GB
GEN
GENERATED
GENERATION
GET
GIF
GIT
GITHUB_TOKEN
GLOBAL
GRADIENT
GRADIENT_BASED
GRAPH
GREATER_THAN
GT
GTE
GUIDE
Gateway
Gauge
General
Generate
GenerateRequest
GenerateResponse
Generated
Generating
Generation
Generator
Generic
Get
Getting
Ghi
Giao
Git
GitHub
GitLab
Global
Go
Goal
Good
Grafana
Grant
Graph
Grays
Greater
Grid
Group
Guard
Guide
Guidelines
HANDLED
HARD
HEAD
HEADERS
HEALTH
HEALTHCHECK
HEALTHY
HEALTH_DETAILED
HIGH
HISTOGRAM
HMR
HTML
HTMLDivElement
HTMLElement
HTMLInputElement
HTMLSelectElement
HTMLTextAreaElement
HTTP
HTTPS
HUMAN
HUMAN_DECIDES
HYPOTHESIS
Handle
Handler
Handles
Handling
Hardened
Harmful
Hash
Header
Headers
Health
HealthCheck
HealthCheckUtils
HealthReport
HealthStatus
Heap
Heavy
Hello
Help
Helper
Here
Hi
Hide
High
Higher
Histogram
History
Hit
Hook
Horizontal
HorizontalPodAutoscaler
Hotkey
Hours
How
HttpMetaStore
Human
HumanFeedback
I
IAny
ICache
ID
IDBDatabase
IDs
IF
IM
IMAGE_NAME
IMITATION_LEARNING
IMMEDIATE_UPDATE
IMPROVEMENT_OPPORTUNITY
IMPROVING
INACTIVE
INCREASING
INFERENCE
INFO
INSERT
INTEGER
INTEGRATED
INTEGRATION
INTERMEDIATE
INTO
IP
IPC
IPC_ALLOWLIST
ISO
ISOLATED
ISSUES
Icon
Id
Identification
Identify
If
Ignore
Image
ImageBitmap
ImageCapture
ImageCaptureCtor
ImageScanResult
Images
Immediate
Impact
ImpactLevel
Implement
Implementation
Implements
Import
ImportMeta
Importance
Important
Improve
Improved
Improvements
In
Include
Inconsistent
Increase
IndexedDB
IndexedDBCache
Indicator
Individual
Inferred
Infinity
Info
Information
Infrastructure
InfrastructureResource
Ingest
Ingress
Initial
Initialization
Initialize
Initialized
Initializing
Initially
Initiating
Inject
Input
InputAction
InputProps
InputValidator
InsertDriveFile
Insight
Insights
Install
Instructions
Insufficient
Integrate
IntegratedAIConfig
IntegratedAutonomousAI
Integrates
Integration
IntegrationTestScenario
Intelligent
Intent
Inter
Interaction
InteractionBatchIn
InteractionEvent
InteractionMode
Interactive
Interface
Internal
Interval
Invalid
InvalidCredentialsError
InvalidTokenError
IpcCache
Is
Isolated
Issue
Issues
IstioRoute
It
Item
ItemComponent
Items
JPG
JS
JSDoc
JSONP
JSX
JWT
JWTTokenError
JetBrains
Job
JobStatus
Jobid
Jobs
Just
K
K8s
KB
KEY
KEYWORD
KNOWLEDGE_GAP
Keep
Key
Keyboard
KeyboardEvent
KeyboardVoice
Kick
Knowledge
KnowledgeEdge
KnowledgeExplorerProps
KnowledgeGraph
KnowledgeNode
Kubernetes
KubernetesConfig
KubernetesManifest
LABEL
LEAKED
LEARNING
LEARNING_DATASETS
LEARNING_INGEST_TEXT
LEARNING_INGEST_URLS
LEARNING_INTERACTIONS
LEARNING_JOB
LEARNING_JOBS
LEARNING_JOB_CANCEL
LESS_THAN
LIME
LLM
LLM_CHAT
LLM_COMPLETE
LLM_EMBED
LOADING
LOCAL
LOCAL_SPEC
LOG
LOGGED
LOG_LEVEL
LONG_TERM
LOW
LRU
LRUCache
LS_KEY
LT
LTE
Label
Language
Larger
Last
Latency
Later
LayoutProps
Lazy
Learn
Learner
Learning
LearningEpisode
LearningInsight
LearningJob
LearningSession
LearningSessionUtils
LearningStrategy
LeftAlt
LeftCmd
LeftControl
LeftShift
LeftSuper
Length
Less
Level
Levels
Library
Lifecycle
Light
Lightweight
Limit
Limited
Line
Lines
Lint
List
Listen
Listener
Literal
Live
Load
LoadBalancer
Loaded
Loading
LoadingFallbackProps
LoadingSpinnerProps
Local
LocalHospital
LocalStorage
Locked
Log
LogEntry
LogItem
LogLevel
Logger
Login
LoginPayload
LoginRequest
LoginResponse
Logo
Logout
Long
Look
Looking
Loop
Low
Lower
M12
M21
MALICIOUS_CODE
MANUALLY
MARKDOWN
MASKED
MAX_CONTENT_LENGTH
MAX_CONTEXT_SIZE
MAX_TEXT
MAX_VIOLATIONS_PER_HOUR
MB
MEDIUM
MEMORY_ACCESS
MENTOR_GUIDE
MENTOR_GUIDE_STREAM
META_GRADIENT
METRIC
METRICS
METRICS_PORT
MFA
MFARequiredError
MILESTONE
MINIMAL
MIT
ML
MODE
MODERATE
MODIFY
MODULES
MONITOR
MP3
MP4
MUI
Made
MainContent
MainHealthService
MainProcessHealthStatus
Maintain
Maintainability
Making
Malicious
Manage
ManagedBy
Management
Manager
Manages
Manifest
Manifests
Manual
Map
Mark
Markdown
Master
Math
Max
Maximum
May
Measure
MediaQueryListEvent
MediaStream
Medium
Meeting
MemState
Memories
MemoryBrowser
MemoryCache
MemoryCard
MemoryEntry
MemoryImportance
MemoryItem
MemoryMetrics
MemoryOperationError
MemoryQueryResult
MemorySearchQuery
MemorySearchRequest
MemorySearchResult
MemoryStatus
MemoryType
MemoryUsage
Mentor
Menu
Merge
Message
MessageEvent
MessageProcessingError
Messages
Meta
MetaExample
Metadata
Method
MethodName
Methods
Metric
MetricType
Metrics
MetricsCollector
MetricsRecorder
Migrate
MigrationError
Milliseconds
Min
MiniMap
Minimal
Minimum
Minutes
Mismatch
Missing
Mitigation
Mobile
Mock
MockClass
MockOllamaClient
MockOllamaServer
MockResponse
MockWS
ModalProps
ModalTransition
Model
ModelInfo
ModelListResponse
ModelLoadError
ModelManager
Moderately
Modify
Module
Modules
Monaco
Monitor
Monitoring
Mono
Moon
More
Motion
Mouse
MouseEvent
MoveMousePayload
MuiAutocomplete
MuiButton
MuiCheckbox
MuiDrawer
MuiFormControl
MuiRadio
MuiSelect
MuiSwitch
MuiTextField
Multi
Multiple
Must
My
N
NEEDS
NEGATIVE
NETWORK
NETWORK_ACCESS
NETWORK_ATTACK
NEUTRAL
NEXT
NLP
NLPParseResponse
NO
NODE_ENV
NODE_TYPES
NODE_VERSION
NON
NOT
NOVICE
NO_CHANGE
NUMBER
NUMBERED_LIST
NaN
Name
Names
Namespace
Naming
Natural
NaturalLanguageExplanation
NavigationMenu
Need
Negative
Network
Neutral
Never
New
NewMessageEvent
Next
No
NoSchedule
Node
NodeJS
NodeLibraryProps
NodePort
NodeTool
NodeType
Non
None
Normal
Normalize
Not
NotExpectation
Note
Notes
Notice
Notification
NotificationConfig
Notify
Nucleus
Null
O
OBSERVATION
OCR
OK
OLLAMA_API_KEY
OLLAMA_BASE_URL
OLLAMA_DEFAULT_MODEL
OLLAMA_HOST
OLLAMA_PORT
ON_DEMAND
OPEN
OPENAPI_JSON
OPERATIONAL_SAFETY
OPTIMIZATION
OPTIONS
OR
OS
OUT_DIR
Observability
ObservabilityPatterns
Observation
Offline
Ollama
OllamaChatMessage
OllamaChatRequest
OllamaChatResponse
OllamaClient
OllamaConfig
OllamaError
OllamaGenerateRequest
OllamaGenerateResponse
OllamaManager
OllamaModel
OllamaResponse
OllamaService
OllamaServiceConfig
Omit
OnCancel
One
OneClickDropzone
Only
Opaque
Open
OpenAI
OpenAPI
OpenAPIConfig
OpenTracing
Operation
OperationLogger
OperationRateLimiter
Operations
Operator
Optimistic
Optimization
OptimizationExperiment
OptimizationImprovement
OptimizationMetrics
OptimizationParameters
OptimizationStrategy
Optimize
Optimized
Optimizing
Optional
Optionally
Options
Or
Orchestration
Orchestrator
Ordered
Original
OriginalWS
Other
Outcome
Output
OutputNode
Outputs
Over
Overall
Overlay
Overloads
Override
Overview
P
P50
P95
P99
PARTIAL
PASSED
PASSIVE
PASSWORD
PATCH
PATTERN
PATTERN_DETECTION
PAUSED
PDF
PENDING
PEP
PERFORMANCE
PERFORMANCE_METRICS
PERFORMANCE_PROFILE
PERIODIC
PERMISSIVE
PERMUTATION
PHASE
PII
PLAIN_TEXT
PLANNING
PLANNING_CREATE
PLANNING_EXECUTE
PLANNING_OPTIMIZE
PLANNING_VALIDATE
PLUGIN_EXECUTION
PNG
PORT
POSITIVE
POST
PRECEDENT
PREFERENCE
PREFERENCE_LEARNING
PRIMARY
PRIVACY_POLICIES
PRIVACY_SANITIZE
PRIVATE
PROBABILISTIC
PROCEDURAL
PROCESSED
PROMPT_MODIFICATION
PROTECTED
PUBLIC
PUT
PYTHON_COMMANDS
PYTHON_FILE_PATTERNS
Paddle
PaddleOCR
Page
PageTransition
Palette
Panel
Panic
Parallel
Parallelize
Parameter
Parameters
Parse
ParseRequest
ParseResponse
Partial
PartialHandler
Passed
Path
PathParams
Pattern
Pause
Payload
Peak
Pending
PendingRequest
Per
Percentage
Perform
Performance
PerformanceAlert
PerformanceBaseline
PerformanceBenchmark
PerformanceMetric
PerformanceMetrics
PerformanceMonitor
PerformanceMonitoringUtils
PerformanceSession
PerformanceTracker
PerformanceTrend
Period
Periodic
Permission
PermissionDeniedError
Persist
Persistent
PersistentCache
PersistentVolumeClaim
Phase
Phone
Photoshop
Pick
Ping
PingEvent
PingMessage
PingMessageSchema
Pipeline
PipelineConfig
PipelineTemplate
PipelineTrigger
Pipfile
Placeholder
Plan
PlanFeedback
PlanOut
Planned
PlannedAction
Planner
Planning
PlanningError
Platform
PlayArrow
Please
Plugin
PluginAPI
PluginBuilder
PluginCapability
PluginConfigSchema
PluginConflictType
PluginDependency
PluginDiscoveryResult
PluginEnvironment
PluginExecutionContext
PluginExecutionResult
PluginFactory
PluginHelpers
PluginInfo
PluginMeta
PluginMetadata
PluginMetric
PluginRegistration
PluginSandbox
PluginStatus
Plugins
Pod
PodMetrics
Point
Points
Policy
PolicyType
PongEvent
Pool
Position
Post
Potential
Potentially
Pre
Predefined
Prefer
Preference
PreferenceModel
PreferenceModelUtils
Prefers
Prefix
Prepare
Prerequisites
Preserve
Prev
Prevent
Previous
Primary
Priority
PriorityLevel
Privacy
Private
Problem
Procedural
Procedure
Process
Processing
Processor
Produce
Production
Programming
Progress
Progressing
Project
ProjectContext
ProjectStructure
Prometheus
PromiseFulfilledResult
PromiseLike
Promote
Promoting
Prompt
PromptTemplate
Prompts
Properties
PropertyDescriptor
Props
PropsWithChildren
Protected
Protection
Provide
Provider
Provides
Psychology
Pub
Pull
PullRequest
Push
PushRequest
PyAutoGUI
Python
PythonProjectDetector
PythonWorkflowManager
Q4_0
QUERY_ANSWERED
QUERY_GENERATED
QUESTION_ANSWERING
Quality
Query
QueryExecutionError
QueryGenerator
QueryOmitFields
QueryProviderProps
QueryTimeoutError
Question
Queue
Queued
Quick
RAG
RAG_INDEX
RAG_QUERY
RAG_SEARCH
RAM
RANKING
RATE
RATE_LIMITED
RATE_LIMITING
RATING
READY
REAL
REASONING
REASONING_CHAIN
RECOMMENDATIONS
RECOVERED
REDACTED
REF
REGEX
REGISTERED
REGISTRY
REINFORCEMENT
REINFORCEMENT_LEARNING
REJECTED
RELEVANCE
REPLACE
REPO_001
REPO_002
REPO_003
REPO_004
REPO_005
REPO_006
REPO_007
REPO_008
REPO_009
REPO_010
REPO_011
REPO_012
REPO_013
REPO_014
REPO_015
REPO_016
REPO_017
REPO_XXX
REQUESTED
RESEARCHER
RESOURCE_USAGE
RESTRICTED
RESTful
RESULTS
REVIEW
ROOT
RPC
RULE
RULE_BASED
RUN
RUNNING
Radius
RagQueryRequest
RagResult
Random
Range
Rapid
Rate
RateLimit
RateLimitConfig
RateLimitError
RateLimitExceededError
RateLimitInfo
Rating
Re
ReAct
ReActPlan
ReActStep
ReactElement
ReactFlow
ReactNode
Read
ReadWriteOnce
ReadableStream
ReadableStreamDefaultReader
Readonly
Ready
Real
RealWorldScenarioSuite
Realistic
Reason
Reasoner
Reasoning
ReasoningOutput
ReasoningStep
Receive
Recent
Recommendation
Recommendations
Record
RecordNotFoundError
Recovery
Recreate
Reduce
Refactor
RefactorPattern
Refill
Refine
Refresh
RefreshHandler
Refreshing
RegExp
RegExpExecArray
Region
Register
Registry
Regular
Reject
Rejection
Relationships
Relevance
RelevantContext
Reliability
Remember
RememberMap
Remove
Renderer
Repeated
Repetition
Replace
Replicas
Report
Reporter
Repository
Represents
Request
RequestArgs
RequestInit
RequestRecord
RequestRejecter
RequestResolver
Requests
Requeue
Require
Required
Requirements
Res
Reset
Resilience
Resolve
Resolver
Resource
ResourceLimitExceededError
ResourceLimits
Respond
Response
ResponseCache
Responses
Responsive
ResponsiveLayoutProps
Restart
Result
Results
Resume
Retrieve
Retry
Return
ReturnType
Review
Reviewing
Revise
Revised
Right
Risk
RiskFactor
RiskLevel
RobotCommand
RobotJS
Roboto
Role
Rollback
RollingUpdate
Rollout
Rollouts
Root
Rough
Route
Routine
Rule
RuleContext
RuleResponse
RuleUpsert
Rules
Run
Runner
Running
Runtime
S
SAFE
SAFETY
SAFETY_CHECK
SAFETY_CONSTANTS
SANDBOX
SCENARIOS
SECRET
SECRET_KEYS
SECURITY
SELECT
SEMANTIC
SENSITIVE_DATA
SESSION_ENDED
SESSION_STARTED
SET
SETTINGS_RELOAD
SHA
SHAP
SHELL
SIGTERM
SIMPLE
SLACK_WEBHOOK
SOLUTION
SQL
SQLite
SQLiteCache
SSE
SSN
SSR
STABLE
STANDARD
STARTED
STEPS
STORAGE_KEY
STORE
STRATEGY_CHANGE
STRICT
STRING
STT
SUBMITTED
SUB_KEY
SUCCESS
SUCCESSFUL
SUCCESSFULLY
SUGGESTIONS
SUITE
SUMMARIZATION
SUMMARY
SYNTHETIC
SYSTEM
SYSTEM_ACCESS
SYSTEM_COMMANDS
SYSTEM_INFO
SYSTEM_OPERATION
SYSTEM_VERSION
Safe
Safety
SafetyAssessment
SafetyConfig
SafetyContext
SafetyTestResult
SafetyValidationSuite
SafetyViolation
Sai
Same
Sample
Satisfaction
Save
Saved
Scalability
Scale
Scaling
ScalingDecision
Scan
Scenario
ScenarioMetrics
ScenarioTestResult
Scenarios
Schedule
Schema
Schemas
Science
Score
Screen
Script
Scroll
ScrollPayload
Search
SearchState
Searching
Secondary
Seconds
Secret
SecretStorage
Secrets
Secure
SecureConfig
Security
SecurityConfig
SecurityLevel
SecurityPolicy
SecurityTestMetrics
SecurityValidator
Seek
Segoe
Select
Selected
Selection
Self
Semantic
Send
Sentiment
Seq
Sequential
Server
Service
ServiceAccount
ServiceMonitor
Session
SessionExpiredError
SessionManager
SessionMetrics
SessionState
Set
SetState
SettingsPage
SettingsPanel
Setup
Severity
SeverityLevel
Shadows
Share
Shared
Shell
ShellLayout
Shift
Shortcut
Shorten
Should
ShouldCancel
Show
Shutdown
Shutting
Significant
Similar
Simple
Simplified
Simplify
Simulate
Simulating
Since
Single
Singleton
Sink
Size
Skeleton
Slide
SlideTransition
Small
Smaller
Smart
SmartCacheEntry
Smooth
Smoothing
Snyk
SocketBus
Software
Solution
Solve
Solving
Some
Sorry
Sort
Source
SourceBranch
Sources
Space
Spacing
SpanType
Specialized
Specific
Speech
SpeechRecognition
Speed
Split
SqliteCls
SseOptions
St
Stack
Stage
Stagger
StaggerList
Staging
Stakes
StakesLevel
Standard
Start
Started
Starting
State
Statistics
Stats
StatusBadge
StatusBarAlignment
StatusBarItem
StatusUpdatedEvent
Step
StepResult
Steps
Stop
Stopping
Storage
StorageEvent
Store
Strategies
Strategy
StrategyConfig
StreamEvent
StreamResponse
Strength
Stress
Strict
StrictMode
Strongly
Structured
Style
Sub
Submit
Submitting
Subscribe
Succeeded
Success
Successful
Suggest
Suggestion
Suggestions
Suite
Suites
Summarize
Summary
Sun
Support
Supported
Supports
Suppress
Switch
Symbol
Sync
Synthetic
SyntheticEvent
System
System32
SystemMetric
SystemMetrics
SystemPingPayload
SystemPongPayload
SystemValidationReport
T
TABLE
TASK_EXECUTION
TB
TCP
TECHNICAL
TEXT
THEME_STORAGE_KEY
THROTTLE
THROTTLED
TIMER
TODO
TOKEN
TOOL_CALL
TRAINING_JOB
TRAINING_JOBS
TRAINING_JOB_CANCEL
TRAINING_MODELS
TRAINING_START
TRANSFER
TRANSLATION
TREE
TRUSTED
TResult
TResult1
TResult2
TTL
TXT
Tab
Tag
Tags
Talk
Target
Task
TaskType
Tasks
Team
Teams
Technical
Technology
Telemetry
TelemetryEvent
Temp
Temperature
Template
Temporary
Terraform
TerraformConfig
TerraformModule
TerraformPlan
TestComponent
TestConfig
TestFramework
TestJob
TestResult
TestSuite
TestSuiteResult
TestWrapper
Testing
Text
TextDecoder
TextDocument
TextEncoder
TextFields
Than
The
Theme
ThemeColor
ThemeContext
ThemeName
ThemeProviderProps
ThemeToggleProps
Thin
Think
This
Thought
Threshold
Throughput
Throwing
Thu
Tick
Time
Timed
Timeline
Timeout
Timer
Timestamp
Timestamps
Timing
TimingResult
Tin
Title
ToastBridge
ToastProps
Toggle
Toggles
Token
Tokens
Tolerations
Too
Tool
ToolDefinition
ToolExecutionContext
ToolExecutionResult
Tools
Tooltip
Top
Topic
Total
Totals
Trace
TraceLogger
TraceSpan
Traced
Tracer
Track
Tracker
Tracks
TrafficSplitting
TrainingAny
TrainingCompleted
TrainingCompletedEvent
TrainingCompletedPayload
TrainingError
TrainingErrorEvent
TrainingErrorPayload
TrainingJob
TrainingJobCreate
TrainingPage
TrainingProgress
TrainingProgressEvent
TrainingProgressPayload
TrainingSampleRequest
TrainingSampleResponse
Trang
TransactionError
Transcript
Transition
TransitionComponent
Translate
Transparent
Trend
Trigger
TriggerConfig
TriggerNode
TriggerPanelProps
Triggers
Trivy
Truy
Try
Ts
Tuner
Type
TypeError
TypeScript
TypeTextPayload
Typed
TypedListener
Typing
TypingIndicatorEvent
Typography
UNCERTAIN
UNHEALTHY
UNKNOWN
UNREGISTERED
UNSAFE
UPDATE
URL
URLSearchParams
URLs
USD
USER
USERNAME
USER_INTERACTION
USER_INTERFACE
UTF
Uint8Array
Unauthorized
Unavailable
Unexpected
Unit
Unknown
Unregister
Untitled
Unused
Unusual
Update
UpdateDatasetRequest
Updated
Upload
UploadRequest
UploadResponse
Uploaded
UploadedFile
Uploading
Uploads
Uri
Usability
Usage
UsageMetrics
Use
UseMemoryAPIReturn
UseThemeReturn
Used
User
UserInfo
UserRateLimiter
Using
Utf8
Utilities
Utility
Utilization
V
VALIDATION
VALIDATION_FAILED
VALUES
VECTOR_DB_PATH
VERBOSE
VERSION
VITE_API_BASE
VITE_API_BASE_URL
VITE_API_URL
VITE_APP_ENV
VITE_APP_NAME
VITE_APP_VERSION
VITE_BUILD_TIME
VITE_CHECK_OPENAPI_HASH
VITE_CLIENT_AES_KEY
VITE_DEV_ALLOW_WS_NO_TOKEN
VITE_ENABLE_CV
VITE_ENABLE_FEDERATED
VITE_ENABLE_OPA
VITE_ENABLE_PROMETHEUS
VITE_ENABLE_TELEMETRY
VITE_ENABLE_ZERO_TRUST
VITE_GIT_SHA
VITE_I18N_DEFAULT_LANG
VITE_TELEMETRY
VITE_UNKNOWN_FEATURE
VITE_WEBSOCKET_RETRY_MAX
VITE_WS_URL
VN
VOICE_STT
VOICE_TTS
VS
Validate
ValidateFunction
Validation
ValidationError
ValidationResult
ValidationWarning
Value
Variable
Variables
Vector
VectorDatabaseError
VectorEmbeddingError
VectorStoreMemory
Verify
Version
Very
Vi
Video
VideoFile
Videos
Vietnamese
View
ViewColumn
VisibilityOff
Visual
Vite
Voice
VoiceState
Volume
VotingResult
Vue
Vui
W3C
WARN
WARNING
WAV
WEBHOOK
WHERE
WITH
WITH_CREDENTIALS
WORKDIR
WORKFLOW_AUTOMATION
WORKING
WORLD
WS
WSClient
WSClientOptions
WSCtx
WSEventType
WSHandler
WSOptions
WSProvider
WSState
WSStatus
WSUrl
WS_EVENTS
WS_ORIGIN
WS_PATH
WS_RETRY_MAX
WS_SCHEMAS
WS_URL
Wait
Warning
Watch
Web
WebSocket
WebSocketManager
Webhook
WebhookEvent
Webview
WebviewPanel
WebviewView
WebviewViewProvider
WebviewViewResolveContext
Week
What
Whether
Which
Why
Wiki
WikiResult
Wikipedia
Will
Window
WindowWithElectron
Windows
With
WithLogger
Workflow
WorkflowEdge
WorkflowEditorProps
WorkflowEngineState
WorkflowExecution
WorkflowExecutionError
WorkflowLog
WorkflowNode
WorkflowSpec
WorkflowTemplate
Workflows
Working
Works
Workspace
WorkspaceConfiguration
WorkspaceEdit
World
Would
Wrapper
Write
Writing
WsEventName
WsMessage
X
XML
XSS
Xem
Y
YAML
YES
You
Young
Your
YourComponent
Z
Z0
ZERO_SHOT
ZETA
ZETA_AI
Za
Zeta
ZetaApiClient
ZetaChatProvider
ZetaCodeViewProvider
ZetaCompletionProvider
ZetaStatusBarProvider
ZetaWebSocket
ZetaWsEvent
Zipkin
Zod
ZoomIn
```

