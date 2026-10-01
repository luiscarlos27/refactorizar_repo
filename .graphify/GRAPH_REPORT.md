# Graph Report - .  (2026-09-29)

## Corpus Check
- 234 files · ~194,346 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5445 nodes · 7596 edges · 145 communities detected
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 326 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 2768 · rationale_for: 2406 · calls: 1635 · uses: 326 · MODIFIES: 287 · method: 92 · imports_from: 45 · inherits: 15 · ON_BRANCH: 11 · PARENT_OF: 10 · imports: 1


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 234 · Candidates: 249
- Excluded: 304 untracked · 9186 ignored · 0 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `aa29e6d`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `AppConfig` - 59 edges
2. `Movie` - 52 edges
3. `MovieService` - 43 edges
4. `Cache` - 41 edges
5. `FavoritesRepository` - 40 edges
6. `HistoryRepository` - 39 edges
7. `_simular_input()` - 39 edges
8. `OmdbClient` - 34 edges
9. `Series` - 31 edges
10. `SeriesService` - 30 edges

## Surprising Connections (you probably didn't know these)
- `Cliente HTTP dedicado para la API de OMDB, sin logica de negocio.` --uses--> `AppConfig`  [INFERRED]
  refactorizar/proyecto_refactoring/proyecto_refactoring/api/omdb_client.py → refactorizar/proyecto_refactoring/proyecto_refactoring/config.py
- `Busca una pelicula por titulo.          Returns:             Datos de la pelicul` --uses--> `AppConfig`  [INFERRED]
  refactorizar/proyecto_refactoring/proyecto_refactoring/api/omdb_client.py → refactorizar/proyecto_refactoring/proyecto_refactoring/config.py
- `Busca peliculas de un actor.          Returns:             Lista de resultados d` --uses--> `AppConfig`  [INFERRED]
  refactorizar/proyecto_refactoring/proyecto_refactoring/api/omdb_client.py → refactorizar/proyecto_refactoring/proyecto_refactoring/config.py
- `Llama protegido por el circuit breaker y reintentos.` --uses--> `AppConfig`  [INFERRED]
  refactorizar/proyecto_refactoring/proyecto_refactoring/api/omdb_client.py → refactorizar/proyecto_refactoring/proyecto_refactoring/config.py
- `Realiza la peticion GET a OMDB y devuelve el JSON.` --uses--> `AppConfig`  [INFERRED]
  refactorizar/proyecto_refactoring/proyecto_refactoring/api/omdb_client.py → refactorizar/proyecto_refactoring/proyecto_refactoring/config.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (50): OmdbClient, Movie, Pelicula de OMDB con campos tipados., Valida invariantes basicos del modelo., Serializa la Movie como diccionario para persistencia JSON., _movie_local(), Capa de servicios: casos de uso de peliculas con dependencias inyectadas., Agrega una pelicula a favoritas. (+42 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (38): Encapsula las llamadas REST a OMDB con timeout, retries y breaker.      Args:, Tests de OmdbClient con HTTP mockeado (sin red real)., Cliente OMDB con api_key de prueba., Encapsula las llamadas REST a TVMaze con timeout, retries y breaker.      Args:, Busca series por nombre.          Returns:             Lista de resultados de la, Obtiene los detalles de una serie por id.          Returns:             Dicciona, Llama protegido por el circuit breaker y reintentos., Realiza la peticion GET a TVMaze y devuelve el JSON. (+30 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (50): add_beta_feature(), add_research_area(), add_roadmap_item(), backup_api_cache_future_config(), export_api_cache_future_config(), get_all_api_cache_future_settings(), get_api_cache_future_config_summary(), get_api_cache_future_setting() (+42 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (50): backup_notification_config(), disable_desktop(), disable_email(), disable_notifications(), disable_sound(), enable_desktop(), enable_email(), enable_notifications() (+42 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (49): add_deprecated_feature(), backup_api_cache_legacy_config(), disable_backward_compatibility(), disable_legacy_mode(), disable_migration_required(), enable_backward_compatibility(), enable_legacy_mode(), enable_migration_required() (+41 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (49): backup_search_config(), disable_fuzzy(), disable_popularity_boost(), disable_search_cache(), enable_fuzzy(), enable_popularity_boost(), enable_search_cache(), export_search_config() (+41 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (48): backup_accessibility_config(), disable_high_contrast(), disable_keyboard_navigation(), disable_large_text(), disable_screen_reader(), enable_high_contrast(), enable_keyboard_navigation(), enable_large_text() (+40 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (48): backup_api_cache_analytics_config(), disable_cache_analytics(), disable_generate_reports(), disable_track_performance(), disable_track_usage_patterns(), enable_cache_analytics(), enable_generate_reports(), enable_track_performance() (+40 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (48): backup_api_cache_best_practices_config(), disable_enforce_naming_conventions(), disable_enforce_security_policies(), disable_require_documentation(), disable_validate_configurations(), enable_enforce_naming_conventions(), enable_enforce_security_policies(), enable_require_documentation() (+40 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (48): backup_api_cache_collaboration_config(), disable_cache_collaboration(), disable_collaborative_optimization(), disable_cross_team_caching(), disable_shared_cache(), enable_cache_collaboration(), enable_collaborative_optimization(), enable_cross_team_caching() (+40 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (48): backup_api_cache_debug_config(), disable_cache_debug(), disable_dump_cache_state(), disable_trace_requests(), disable_verbose_logging(), enable_cache_debug(), enable_dump_cache_state(), enable_trace_requests() (+40 more)

### Community 11 - "Community 11"
Cohesion: 0.05
Nodes (48): backup_api_cache_documentation_config(), disable_api_reference(), disable_auto_generate_docs(), disable_cache_documentation(), disable_include_examples(), enable_api_reference(), enable_auto_generate_docs(), enable_cache_documentation() (+40 more)

### Community 12 - "Community 12"
Cohesion: 0.05
Nodes (48): backup_api_cache_failover_config(), disable_auto_recovery(), disable_cache_failover(), disable_fallback_to_disk(), disable_fallback_to_memory(), enable_auto_recovery(), enable_cache_failover(), enable_fallback_to_disk() (+40 more)

### Community 13 - "Community 13"
Cohesion: 0.05
Nodes (48): backup_api_cache_governance_config(), disable_cache_governance(), disable_cache_quotas(), disable_policy_enforcement(), disable_usage_limits(), enable_cache_governance(), enable_cache_quotas(), enable_policy_enforcement() (+40 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (48): backup_api_cache_innovation_config(), disable_cache_innovation(), disable_experimental_features(), disable_innovation_pipeline(), disable_research_mode(), enable_cache_innovation(), enable_experimental_features(), enable_innovation_pipeline() (+40 more)

### Community 15 - "Community 15"
Cohesion: 0.05
Nodes (48): backup_api_cache_intelligence_config(), disable_adaptive_ttl(), disable_cache_intelligence(), disable_machine_learning(), disable_predictive_caching(), enable_adaptive_ttl(), enable_cache_intelligence(), enable_machine_learning() (+40 more)

### Community 16 - "Community 16"
Cohesion: 0.05
Nodes (48): backup_api_cache_mentoring_config(), disable_best_practices_sharing(), disable_cache_mentoring(), disable_code_review(), disable_peer_review(), enable_best_practices_sharing(), enable_cache_mentoring(), enable_code_review() (+40 more)

### Community 17 - "Community 17"
Cohesion: 0.05
Nodes (48): backup_api_cache_metrics_config(), disable_cache_metrics(), disable_track_hit_miss_ratio(), disable_track_latency(), disable_track_size_evictions(), enable_cache_metrics(), enable_track_hit_miss_ratio(), enable_track_latency() (+40 more)

### Community 18 - "Community 18"
Cohesion: 0.05
Nodes (48): backup_api_cache_monitoring_config(), disable_alert_on_high_usage(), disable_cache_monitoring(), disable_track_hit_rate(), disable_track_size(), enable_alert_on_high_usage(), enable_cache_monitoring(), enable_track_hit_rate() (+40 more)

### Community 19 - "Community 19"
Cohesion: 0.05
Nodes (48): backup_api_cache_observability_config(), disable_cache_observability(), disable_distributed_tracing(), disable_health_checks(), disable_metrics_collection(), enable_cache_observability(), enable_distributed_tracing(), enable_health_checks() (+40 more)

### Community 20 - "Community 20"
Cohesion: 0.05
Nodes (48): backup_api_cache_performance_config(), disable_async_operations(), disable_batch_operations(), disable_optimize_for_read(), disable_optimize_for_write(), enable_async_operations(), enable_batch_operations(), enable_optimize_for_read() (+40 more)

### Community 21 - "Community 21"
Cohesion: 0.05
Nodes (48): backup_api_cache_recommendations_config(), disable_auto_optimize(), disable_cache_recommendations(), disable_suggest_cache_size(), disable_suggest_ttl_adjustments(), enable_auto_optimize(), enable_cache_recommendations(), enable_suggest_cache_size() (+40 more)

### Community 22 - "Community 22"
Cohesion: 0.05
Nodes (48): backup_api_cache_resilience_testing_config(), disable_chaos_engineering(), disable_fault_injection(), disable_recovery_scenarios(), disable_resilience_testing(), enable_chaos_engineering(), enable_fault_injection(), enable_recovery_scenarios() (+40 more)

### Community 23 - "Community 23"
Cohesion: 0.05
Nodes (48): backup_api_cache_security_config(), disable_access_control(), disable_encrypt_cache(), disable_secure_deletion(), disable_validate_integrity(), enable_access_control(), enable_encrypt_cache(), enable_secure_deletion() (+40 more)

### Community 24 - "Community 24"
Cohesion: 0.05
Nodes (48): backup_api_cache_security_testing_config(), disable_penetration_testing(), disable_security_audit(), disable_security_testing(), disable_vulnerability_scanning(), enable_penetration_testing(), enable_security_audit(), enable_security_testing() (+40 more)

### Community 25 - "Community 25"
Cohesion: 0.05
Nodes (48): backup_api_cache_training_config(), disable_cache_training(), disable_certification(), disable_interactive_mode(), disable_progress_tracking(), enable_cache_training(), enable_certification(), enable_interactive_mode() (+40 more)

### Community 26 - "Community 26"
Cohesion: 0.05
Nodes (48): backup_api_cache_validation_config(), disable_cache_validation(), disable_strict_validation(), disable_validate_checksum(), disable_validate_on_read(), enable_cache_validation(), enable_strict_validation(), enable_validate_checksum() (+40 more)

### Community 27 - "Community 27"
Cohesion: 0.05
Nodes (48): backup_api_debug_config(), disable_log_api_errors(), disable_log_api_requests(), disable_log_api_responses(), disable_show_api_timing(), enable_log_api_errors(), enable_log_api_requests(), enable_log_api_responses() (+40 more)

### Community 28 - "Community 28"
Cohesion: 0.06
Nodes (48): backup_debug_config(), disable_debug(), disable_log_api_calls(), disable_show_errors(), disable_show_timing(), disable_verbose(), enable_debug(), enable_log_api_calls() (+40 more)

### Community 29 - "Community 29"
Cohesion: 0.06
Nodes (47): backup_api_cache_testing_config(), disable_cache_testing(), disable_mock_cache(), disable_test_isolation(), disable_verbose_output(), enable_cache_testing(), enable_mock_cache(), enable_test_isolation() (+39 more)

### Community 30 - "Community 30"
Cohesion: 0.06
Nodes (46): backup_api_cache_compliance_config(), disable_audit_logging(), disable_data_anonymization(), disable_gdpr_compliance(), enable_audit_logging(), enable_data_anonymization(), enable_gdpr_compliance(), export_api_cache_compliance_config() (+38 more)

### Community 31 - "Community 31"
Cohesion: 0.06
Nodes (46): backup_api_cache_deprecation_config(), disable_auto_remove_expired(), disable_cache_deprecation(), disable_deprecation_warnings(), enable_auto_remove_expired(), enable_cache_deprecation(), enable_deprecation_warnings(), export_api_cache_deprecation_config() (+38 more)

### Community 32 - "Community 32"
Cohesion: 0.06
Nodes (46): add_integration_point(), backup_api_cache_integration_config(), disable_cache_integration(), enable_cache_integration(), export_api_cache_integration_config(), get_all_api_cache_integration_settings(), get_api_cache_integration_config_summary(), get_api_cache_integration_setting() (+38 more)

### Community 33 - "Community 33"
Cohesion: 0.06
Nodes (46): backup_api_cache_invalidation_config(), disable_cache_invalidation(), disable_invalidate_on_error(), disable_invalidate_on_write(), enable_cache_invalidation(), enable_invalidate_on_error(), enable_invalidate_on_write(), export_api_cache_invalidation_config() (+38 more)

### Community 34 - "Community 34"
Cohesion: 0.06
Nodes (46): backup_api_cache_migration_schedule_config(), disable_auto_rollback(), disable_notification_before_migration(), disable_scheduled_migration(), enable_auto_rollback(), enable_notification_before_migration(), enable_scheduled_migration(), export_api_cache_migration_schedule_config() (+38 more)

### Community 35 - "Community 35"
Cohesion: 0.06
Nodes (46): backup_api_error_handling_config(), disable_include_stack_trace(), disable_log_errors(), disable_show_user_errors(), enable_include_stack_trace(), enable_log_errors(), enable_show_user_errors(), export_api_error_handling_config() (+38 more)

### Community 36 - "Community 36"
Cohesion: 0.06
Nodes (46): backup_api_monitoring_config(), disable_api_monitoring(), disable_track_error_rates(), disable_track_response_times(), enable_api_monitoring(), enable_track_error_rates(), enable_track_response_times(), export_api_monitoring_config() (+38 more)

### Community 37 - "Community 37"
Cohesion: 0.06
Nodes (46): backup_api_testing_config(), disable_api_testing(), disable_mock_responses(), disable_verbose_output(), enable_api_testing(), enable_mock_responses(), enable_verbose_output(), export_api_testing_config() (+38 more)

### Community 38 - "Community 38"
Cohesion: 0.06
Nodes (46): backup_security_config(), disable_special_chars(), enable_special_chars(), export_security_config(), get_all_security_settings(), get_lockout_duration(), get_max_login_attempts(), get_password_min_length() (+38 more)

### Community 39 - "Community 39"
Cohesion: 0.06
Nodes (20): _crear_retrier(), Cliente HTTP dedicado para la API de OMDB, sin logica de negocio., Construye el reintentador con los parametros de la configuracion., _crear_retrier(), Cliente HTTP dedicado para la API de TVMaze, sin logica de negocio., Construye el reintentador con los parametros de la configuracion., 0606be4 Cerrar fase 4: manejo de errores, logging y resiliencia (tenacity + pybreaker), _flotante() (+12 more)

### Community 40 - "Community 40"
Cohesion: 0.06
Nodes (45): backup_api_caching_strategy_config(), disable_cache_warming(), disable_invalidate_on_error(), disable_pre_fetch(), enable_cache_warming(), enable_invalidate_on_error(), enable_pre_fetch(), export_api_caching_strategy_config() (+37 more)

### Community 41 - "Community 41"
Cohesion: 0.06
Nodes (45): backup_backup_config(), disable_backup(), disable_compression(), enable_backup(), enable_compression(), export_backup_config(), get_all_backup_settings(), get_backup_config_summary() (+37 more)

### Community 42 - "Community 42"
Cohesion: 0.06
Nodes (45): backup_display_config(), disable_animations(), disable_compact_mode(), disable_icons(), enable_animations(), enable_compact_mode(), enable_icons(), export_display_config() (+37 more)

### Community 43 - "Community 43"
Cohesion: 0.06
Nodes (45): backup_privacy_config(), disable_analytics(), disable_crash_reporting(), disable_personalization(), enable_analytics(), enable_crash_reporting(), enable_personalization(), export_privacy_config() (+37 more)

### Community 44 - "Community 44"
Cohesion: 0.06
Nodes (44): backup_api_cache_config(), disable_api_cache(), disable_cache_responses(), enable_api_cache(), enable_cache_responses(), export_api_cache_config(), get_all_api_cache_settings(), get_api_cache_config_summary() (+36 more)

### Community 45 - "Community 45"
Cohesion: 0.06
Nodes (44): backup_api_cache_deprecation_schedule_config(), disable_auto_deprecate(), disable_auto_remove_after_grace(), enable_auto_deprecate(), enable_auto_remove_after_grace(), export_api_cache_deprecation_schedule_config(), get_all_api_cache_deprecation_schedule_settings(), get_api_cache_deprecation_schedule_config_summary() (+36 more)

### Community 46 - "Community 46"
Cohesion: 0.06
Nodes (44): backup_api_cache_disaster_recovery_config(), disable_disaster_recovery(), disable_geographic_redundancy(), enable_disaster_recovery(), enable_geographic_redundancy(), export_api_cache_disaster_recovery_config(), get_all_api_cache_disaster_recovery_settings(), get_api_cache_disaster_recovery_config_summary() (+36 more)

### Community 47 - "Community 47"
Cohesion: 0.06
Nodes (44): backup_api_cache_migration_config(), disable_cache_migration(), disable_data_validation(), disable_rollback(), enable_cache_migration(), enable_data_validation(), enable_rollback(), export_api_cache_migration_config() (+36 more)

### Community 48 - "Community 48"
Cohesion: 0.06
Nodes (44): backup_api_cache_performance_testing_config(), disable_measure_latency(), disable_performance_testing(), enable_measure_latency(), enable_performance_testing(), export_api_cache_performance_testing_config(), get_all_api_cache_performance_testing_settings(), get_api_cache_performance_testing_config_summary() (+36 more)

### Community 49 - "Community 49"
Cohesion: 0.06
Nodes (44): backup_api_cache_preloading_config(), disable_cache_preloading(), disable_preload_on_startup(), enable_cache_preloading(), enable_preload_on_startup(), export_api_cache_preloading_config(), get_all_api_cache_preloading_settings(), get_api_cache_preloading_config_summary() (+36 more)

### Community 50 - "Community 50"
Cohesion: 0.06
Nodes (44): backup_api_cache_recovery_config(), disable_auto_recovery(), disable_cache_recovery(), enable_auto_recovery(), enable_cache_recovery(), export_api_cache_recovery_config(), get_all_api_cache_recovery_settings(), get_api_cache_recovery_config_summary() (+36 more)

### Community 51 - "Community 51"
Cohesion: 0.06
Nodes (44): backup_api_cache_reporting_config(), disable_cache_reporting(), disable_include_charts(), enable_cache_reporting(), enable_include_charts(), export_api_cache_reporting_config(), get_all_api_cache_reporting_settings(), get_api_cache_reporting_config_summary() (+36 more)

### Community 52 - "Community 52"
Cohesion: 0.06
Nodes (44): backup_api_cache_scalability_config(), disable_auto_scaling(), disable_cache_scalability(), enable_auto_scaling(), enable_cache_scalability(), export_api_cache_scalability_config(), get_all_api_cache_scalability_settings(), get_api_cache_scalability_config_summary() (+36 more)

### Community 53 - "Community 53"
Cohesion: 0.06
Nodes (44): backup_api_cache_stress_testing_config(), disable_monitor_resources(), disable_stress_testing(), enable_monitor_resources(), enable_stress_testing(), export_api_cache_stress_testing_config(), get_all_api_cache_stress_testing_settings(), get_api_cache_stress_testing_config_summary() (+36 more)

### Community 54 - "Community 54"
Cohesion: 0.06
Nodes (44): backup_proxy_config(), disable_proxy(), enable_proxy(), export_proxy_config(), get_all_proxy_settings(), get_proxy_config_summary(), get_proxy_host(), get_proxy_password() (+36 more)

### Community 55 - "Community 55"
Cohesion: 0.06
Nodes (41): add_to_favorites(), add_to_history(), backup_state(), clear_history(), clear_state(), export_state(), get_current_user(), get_session_stats() (+33 more)

### Community 56 - "Community 56"
Cohesion: 0.06
Nodes (44): backup_theme_config(), export_theme_config(), get_all_theme_settings(), get_background_color(), get_primary_color(), get_secondary_color(), get_text_color(), get_theme_config_summary() (+36 more)

### Community 57 - "Community 57"
Cohesion: 0.06
Nodes (43): backup_api_cache_architecture_config(), disable_clustering(), disable_persistence(), enable_clustering(), enable_persistence(), export_api_cache_architecture_config(), get_all_api_cache_architecture_settings(), get_api_cache_architecture_config_summary() (+35 more)

### Community 58 - "Community 58"
Cohesion: 0.06
Nodes (43): backup_api_cache_serialization_config(), disable_include_metadata(), disable_pretty_print(), enable_include_metadata(), enable_pretty_print(), export_api_cache_serialization_config(), get_all_api_cache_serialization_settings(), get_api_cache_serialization_config_summary() (+35 more)

### Community 59 - "Community 59"
Cohesion: 0.06
Nodes (43): backup_api_failover_config(), disable_api_failover(), disable_auto_switch(), enable_api_failover(), enable_auto_switch(), export_api_failover_config(), get_all_api_failover_settings(), get_api_failover_config_summary() (+35 more)

### Community 60 - "Community 60"
Cohesion: 0.06
Nodes (43): backup_email_config(), disable_tls(), enable_tls(), export_email_config(), get_all_email_settings(), get_email_config_summary(), get_email_setting(), get_sender_email() (+35 more)

### Community 61 - "Community 61"
Cohesion: 0.06
Nodes (43): add_feature(), backup_features(), clear_features(), disable_feature(), enable_feature(), export_features(), get_all_features(), get_disabled_features() (+35 more)

### Community 62 - "Community 62"
Cohesion: 0.06
Nodes (43): backup_log_config(), disable_logging(), enable_logging(), export_log_config(), get_all_log_settings(), get_backup_count(), get_log_config_summary(), get_log_file() (+35 more)

### Community 63 - "Community 63"
Cohesion: 0.06
Nodes (42): backup_api_auth_config(), disable_api_auth(), enable_api_auth(), export_api_auth_config(), get_all_api_auth_settings(), get_api_auth_config_summary(), get_api_auth_setting(), get_auth_type() (+34 more)

### Community 64 - "Community 64"
Cohesion: 0.06
Nodes (42): backup_api_cache_alerting_config(), disable_cache_alerting(), enable_cache_alerting(), export_api_cache_alerting_config(), get_alert_cooldown(), get_all_api_cache_alerting_settings(), get_api_cache_alerting_config_summary(), get_api_cache_alerting_setting() (+34 more)

### Community 65 - "Community 65"
Cohesion: 0.06
Nodes (42): backup_api_cache_cleanup_config(), disable_cache_cleanup(), enable_cache_cleanup(), export_api_cache_cleanup_config(), get_all_api_cache_cleanup_settings(), get_api_cache_cleanup_config_summary(), get_api_cache_cleanup_setting(), get_cleanup_interval() (+34 more)

### Community 66 - "Community 66"
Cohesion: 0.06
Nodes (42): backup_api_cache_compression_config(), disable_cache_compression(), enable_cache_compression(), export_api_cache_compression_config(), get_all_api_cache_compression_settings(), get_api_cache_compression_config_summary(), get_api_cache_compression_setting(), get_compression_algorithm() (+34 more)

### Community 67 - "Community 67"
Cohesion: 0.06
Nodes (42): backup_api_cache_distribution_config(), disable_cache_distribution(), enable_cache_distribution(), export_api_cache_distribution_config(), get_all_api_cache_distribution_settings(), get_api_cache_distribution_config_summary(), get_api_cache_distribution_setting(), get_distribution_strategy() (+34 more)

### Community 68 - "Community 68"
Cohesion: 0.06
Nodes (42): backup_api_cache_evolution_config(), disable_compatibility_mode(), enable_compatibility_mode(), export_api_cache_evolution_config(), get_all_api_cache_evolution_settings(), get_api_cache_evolution_config_summary(), get_api_cache_evolution_setting(), get_cache_version() (+34 more)

### Community 69 - "Community 69"
Cohesion: 0.06
Nodes (42): backup_api_cache_lifecycle_config(), disable_cache_lifecycle(), disable_ttl(), enable_cache_lifecycle(), enable_ttl(), export_api_cache_lifecycle_config(), get_all_api_cache_lifecycle_settings(), get_api_cache_lifecycle_config_summary() (+34 more)

### Community 70 - "Community 70"
Cohesion: 0.06
Nodes (42): backup_api_cache_load_testing_config(), disable_load_testing(), enable_load_testing(), export_api_cache_load_testing_config(), get_all_api_cache_load_testing_settings(), get_api_cache_load_testing_config_summary(), get_api_cache_load_testing_setting(), get_max_concurrent_users() (+34 more)

### Community 71 - "Community 71"
Cohesion: 0.06
Nodes (42): backup_api_cache_warming_config(), disable_cache_warming(), enable_cache_warming(), export_api_cache_warming_config(), get_all_api_cache_warming_settings(), get_api_cache_warming_config_summary(), get_api_cache_warming_setting(), get_max_warming_items() (+34 more)

### Community 72 - "Community 72"
Cohesion: 0.06
Nodes (42): backup_api_circuit_breaker_config(), disable_circuit_breaker(), enable_circuit_breaker(), export_api_circuit_breaker_config(), get_all_api_circuit_breaker_settings(), get_api_circuit_breaker_config_summary(), get_api_circuit_breaker_setting(), get_failure_threshold() (+34 more)

### Community 73 - "Community 73"
Cohesion: 0.06
Nodes (42): backup_api_logging_config(), disable_api_logging(), enable_api_logging(), export_api_logging_config(), get_all_api_logging_settings(), get_api_log_file(), get_api_log_level(), get_api_logging_config_summary() (+34 more)

### Community 74 - "Community 74"
Cohesion: 0.06
Nodes (42): backup_api_performance_config(), disable_compression(), disable_keep_alive(), enable_compression(), enable_keep_alive(), export_api_performance_config(), get_all_api_performance_settings(), get_api_performance_config_summary() (+34 more)

### Community 75 - "Community 75"
Cohesion: 0.06
Nodes (42): backup_api_rate_limit_config(), disable_rate_limiting(), enable_rate_limiting(), export_api_rate_limit_config(), get_all_api_rate_limit_settings(), get_api_rate_limit_config_summary(), get_api_rate_limit_setting(), get_omdb_requests_per_minute() (+34 more)

### Community 76 - "Community 76"
Cohesion: 0.06
Nodes (42): backup_api_rate_limiter_config(), disable_rate_limiter(), enable_rate_limiter(), export_api_rate_limiter_config(), get_all_api_rate_limiter_settings(), get_api_rate_limiter_config_summary(), get_api_rate_limiter_setting(), get_bucket_size() (+34 more)

### Community 77 - "Community 77"
Cohesion: 0.06
Nodes (42): backup_api_retry_config(), disable_exponential_backoff(), enable_exponential_backoff(), export_api_retry_config(), get_all_api_retry_settings(), get_api_retry_config_summary(), get_api_retry_setting(), get_max_retries() (+34 more)

### Community 78 - "Community 78"
Cohesion: 0.06
Nodes (41): backup_api_security_config(), disable_allow_redirects(), disable_ssl_verification(), enable_allow_redirects(), enable_ssl_verification(), export_api_security_config(), get_all_api_security_settings(), get_api_security_config_summary() (+33 more)

### Community 79 - "Community 79"
Cohesion: 0.06
Nodes (42): backup_api_timeout_retry_config(), disable_retry_on_timeout(), enable_retry_on_timeout(), export_api_timeout_retry_config(), get_all_api_timeout_retry_settings(), get_api_timeout_retry_config_summary(), get_api_timeout_retry_setting(), get_connect_timeout() (+34 more)

### Community 80 - "Community 80"
Cohesion: 0.06
Nodes (41): backup_network_config(), disable_ssl_verification(), enable_ssl_verification(), export_network_config(), get_all_network_settings(), get_max_retries(), get_network_config_summary(), get_network_setting() (+33 more)

### Community 81 - "Community 81"
Cohesion: 0.06
Nodes (40): add_api(), backup_api_config(), clear_api_configs(), export_api_config(), get_all_api_configs(), get_api_config(), get_api_config_summary(), get_api_key() (+32 more)

### Community 82 - "Community 82"
Cohesion: 0.06
Nodes (41): backup_api_degradation_config(), disable_degradation(), enable_degradation(), export_api_degradation_config(), get_all_api_degradation_settings(), get_api_degradation_config_summary(), get_api_degradation_setting(), get_degrade_after_failures() (+33 more)

### Community 83 - "Community 83"
Cohesion: 0.06
Nodes (41): backup_performance_config(), disable_compression(), enable_compression(), export_performance_config(), get_all_performance_settings(), get_cache_size_mb(), get_connection_pool_size(), get_max_concurrent_requests() (+33 more)

### Community 84 - "Community 84"
Cohesion: 0.09
Nodes (41): _anular_delay(), menu(), _simular_input(), test_buscar_actor_detalles_app_error(), test_buscar_actor_selecciona_volver(), test_buscar_actor_sin_resultados(), test_buscar_actor_ver_detalles(), test_buscar_pelicula_app_error() (+33 more)

### Community 85 - "Community 85"
Cohesion: 0.06
Nodes (40): backup_api_bulkhead_config(), disable_bulkhead(), enable_bulkhead(), export_api_bulkhead_config(), get_all_api_bulkhead_settings(), get_api_bulkhead_config_summary(), get_api_bulkhead_setting(), get_bulkhead_timeout() (+32 more)

### Community 86 - "Community 86"
Cohesion: 0.06
Nodes (40): backup_api_timeout_config(), export_api_timeout_config(), get_all_api_timeout_settings(), get_api_timeout_config_summary(), get_api_timeout_setting(), get_connect_timeout(), get_default_timeout(), get_omdb_timeout() (+32 more)

### Community 87 - "Community 87"
Cohesion: 0.06
Nodes (40): backup_cache_expiry_config(), export_cache_expiry_config(), get_all_cache_expiry_settings(), get_cache_expiry_config_summary(), get_cache_expiry_setting(), get_default_expiry_hours(), get_movie_expiry_hours(), get_search_expiry_hours() (+32 more)

### Community 88 - "Community 88"
Cohesion: 0.08
Nodes (40): add_favorite(), add_movie(), add_series(), add_to_history(), clear_all_data(), clear_history(), create_backup(), delete_data_file() (+32 more)

### Community 89 - "Community 89"
Cohesion: 0.06
Nodes (40): backup_database_config(), disable_backup(), enable_backup(), export_database_config(), get_all_database_settings(), get_database_config_summary(), get_database_path(), get_database_setting() (+32 more)

### Community 90 - "Community 90"
Cohesion: 0.07
Nodes (40): add_language(), backup_language_config(), export_language_config(), get_all_language_settings(), get_available_languages(), get_current_language(), get_fallback_language(), get_language_config_summary() (+32 more)

### Community 91 - "Community 91"
Cohesion: 0.06
Nodes (39): backup_maintenance_config(), disable_maintenance(), enable_maintenance(), export_maintenance_config(), get_all_maintenance_settings(), get_estimated_time(), get_maintenance_config_summary(), get_maintenance_message() (+31 more)

### Community 92 - "Community 92"
Cohesion: 0.06
Nodes (40): backup_storage_config(), export_storage_config(), get_all_storage_settings(), get_backup_dir(), get_cache_dir(), get_data_dir(), get_max_storage_mb(), get_storage_config_summary() (+32 more)

### Community 93 - "Community 93"
Cohesion: 0.07
Nodes (33): _rating_promedio(), Modelo de dominio Series para series de TVMaze., Serie de TVMaze con campos tipados., Construye una Series desde la respuesta de TVMaze.          Acepta tanto los res, Convierte un valor en texto o None si esta vacio., Extrae el promedio del objeto rating de TVMaze., Series, _texto() (+25 more)

### Community 94 - "Community 94"
Cohesion: 0.07
Nodes (36): backup_cache_config(), disable_cache(), enable_cache(), export_cache_config(), get_all_cache_settings(), get_cache_config_summary(), get_cache_setting(), get_expiry_hours() (+28 more)

### Community 95 - "Community 95"
Cohesion: 0.07
Nodes (35): backup_stats(), export_stats(), get_error_stats(), get_favorite_stats(), get_search_stats(), get_session_stats(), get_stats(), get_stats_summary() (+27 more)

### Community 96 - "Community 96"
Cohesion: 0.07
Nodes (35): cache_exists(), cleanup_expired_cache(), clear_cache(), export_cache(), get_cache_entry_info(), get_cache_key(), get_cache_size(), get_cache_stats() (+27 more)

### Community 97 - "Community 97"
Cohesion: 0.08
Nodes (35): backup_ui_config(), export_ui_config(), get_all_ui_settings(), get_items_per_page(), get_language(), get_theme(), get_ui_config_summary(), get_ui_setting() (+27 more)

### Community 98 - "Community 98"
Cohesion: 0.06
Nodes (25): format_list_display(), format_movie_display(), format_series_display(), get_timestamp(), get_user_input(), handle_menu_choice(), init_dirs(), print_header() (+17 more)

### Community 99 - "Community 99"
Cohesion: 0.07
Nodes (31): add_notification(), backup_notifications(), clear_notifications(), export_notifications(), get_all_notifications(), get_notification_stats(), get_notifications_by_type(), get_notifications_summary() (+23 more)

### Community 100 - "Community 100"
Cohesion: 0.07
Nodes (33): backup_audit_log(), clear_audit_log(), export_audit_log(), get_all_audit_entries(), get_audit_entry(), get_audit_stats(), get_audit_summary(), get_entries_by_action() (+25 more)

### Community 101 - "Community 101"
Cohesion: 0.08
Nodes (32): backup_config(), delete_config(), export_config(), get_all_config(), get_config(), get_config_summary(), get_config_value(), import_config() (+24 more)

### Community 102 - "Community 102"
Cohesion: 0.08
Nodes (31): add_search(), backup_history(), clear_history(), delete_search(), export_history(), get_history_size(), get_popular_searches(), get_recent_searches() (+23 more)

### Community 103 - "Community 103"
Cohesion: 0.08
Nodes (30): add_permission(), add_role_permission(), backup_permissions(), clear_permissions(), export_permissions(), get_all_permissions(), get_permission(), get_permission_stats() (+22 more)

### Community 104 - "Community 104"
Cohesion: 0.08
Nodes (29): backup_plugins(), disable_plugin(), enable_plugin(), export_plugins(), get_all_plugins(), get_enabled_plugins(), get_plugin_config(), get_plugin_stats() (+21 more)

### Community 105 - "Community 105"
Cohesion: 0.08
Nodes (30): backup_settings(), delete_setting(), export_settings(), get_all_settings(), get_setting(), get_setting_type(), get_settings_summary(), import_settings() (+22 more)

### Community 106 - "Community 106"
Cohesion: 0.09
Nodes (32): backup_version(), compare_versions(), export_version(), get_current_version(), get_version_history(), get_version_info(), get_version_summary(), import_version() (+24 more)

### Community 107 - "Community 107"
Cohesion: 0.08
Nodes (27): authenticate_user(), backup_users(), create_user(), delete_user(), export_users(), get_all_users(), get_current_user(), get_user() (+19 more)

### Community 108 - "Community 108"
Cohesion: 0.09
Nodes (29): clear_logs(), create_log_entry(), export_logs(), filter_logs_by_date(), filter_logs_by_level(), get_log_content(), get_log_stats(), get_recent_logs() (+21 more)

### Community 109 - "Community 109"
Cohesion: 0.08
Nodes (27): add_event(), backup_schedule(), clear_schedule(), export_schedule(), get_all_events(), get_events_by_date(), get_events_by_type(), get_past_events() (+19 more)

### Community 110 - "Community 110"
Cohesion: 0.07
Nodes (26): copy_export(), create_backup(), delete_export(), export_data_report(), get_export_info(), get_total_export_size(), import_from_csv(), import_from_json() (+18 more)

### Community 111 - "Community 111"
Cohesion: 0.08
Nodes (26): add_favorite(), backup_favorites(), clear_favorites(), export_favorites(), get_favorite(), get_favorites(), get_favorites_count(), get_favorites_stats() (+18 more)

### Community 112 - "Community 112"
Cohesion: 0.09
Nodes (25): backup_errors(), clear_errors(), export_errors(), get_all_errors(), get_error_stats(), get_errors_by_type(), get_errors_summary(), get_resolved_errors() (+17 more)

### Community 113 - "Community 113"
Cohesion: 0.09
Nodes (25): add_tag(), backup_tags(), clear_tags(), export_tags(), get_all_tags(), get_popular_tags(), get_recent_tags(), get_tag_stats() (+17 more)

### Community 114 - "Community 114"
Cohesion: 0.09
Nodes (24): add_metadata(), backup_metadata(), clear_metadata(), export_metadata(), get_all_metadata(), get_metadata_by_pattern(), get_metadata_stats(), get_metadata_summary() (+16 more)

### Community 115 - "Community 115"
Cohesion: 0.10
Nodes (22): backup_reports(), clear_reports(), create_report(), delete_report(), export_reports(), generate_report(), get_all_reports(), get_report_stats() (+14 more)

### Community 116 - "Community 116"
Cohesion: 0.13
Nodes (14): Enum, Alert, AlertLevel, AlertLogger, InMemoryAlertStorage, PressureProcessor, Industrial sensor telemetry and alert system., SensorConfig (+6 more)

### Community 117 - "Community 117"
Cohesion: 0.08
Nodes (22): cache_exists(), cleanup_expired_cache(), export_cache(), get_cache_key(), get_cache_size(), get_cache_stats(), get_from_cache(), import_cache() (+14 more)

### Community 118 - "Community 118"
Cohesion: 0.12
Nodes (23): clear_log(), export_log(), filter_log_by_date(), filter_log_by_level(), format_log_entry(), get_log_lines(), get_log_stats(), log_critical() (+15 more)

### Community 119 - "Community 119"
Cohesion: 0.09
Nodes (7): omdb_client(), Tests de MovieService: delegacion, cache y degradacion., Servicio de peliculas con dependencias inyectadas reales., Cliente OMDB real con api_key de prueba (no se llama a la red)., _respuesta(), service(), test_buscar_por_titulo_exito_guarda_en_cache()

### Community 120 - "Community 120"
Cohesion: 0.24
Nodes (19): buscar_pelicula_omdb(), buscar_peliculas_por_actor(), buscar_series_tvmaze(), clear_screen(), delay(), funcion_buscar_actor(), funcion_buscar_pelicula(), funcion_buscar_series() (+11 more)

### Community 121 - "Community 121"
Cohesion: 0.12
Nodes (18): backup_exists(), cleanup_old_backups(), create_backup(), delete_backup(), export_backup(), get_backup_info(), get_total_backup_size(), import_backup() (+10 more)

### Community 122 - "Community 122"
Cohesion: 0.15
Nodes (9): FilePurchaseRepository, Item, PurchaseCalculator, PurchaseProcessor, PurchaseResult, Purchase processing system with tax calculation and discounts., UserCart, UserType (+1 more)

### Community 123 - "Community 123"
Cohesion: 0.13
Nodes (17): export_config(), get_config(), import_config(), load_config(), print_config(), Carga configuración sin manejo de errores, Obtiene valor de configuración sin validación, Establece valor de configuración (+9 more)

### Community 124 - "Community 124"
Cohesion: 0.18
Nodes (14): Exception, ApiClientError, AppError, ConfigError, MovieNotFoundError, NetworkError, Jerarquia de excepciones del dominio con base comun ``AppError``., Fallo de red o timeout en una llamada HTTP. (+6 more)

### Community 125 - "Community 125"
Cohesion: 0.13
Nodes (1): Tests del modelo Movie: creacion, validacion y conversion.

### Community 126 - "Community 126"
Cohesion: 0.20
Nodes (7): client(), _mock_response(), test_buscar_por_actor_con_resultados(), test_buscar_por_actor_sin_resultados(), test_buscar_por_titulo_encontrada(), test_buscar_por_titulo_no_encontrada(), test_verbose_false_no_logs_debug()

### Community 127 - "Community 127"
Cohesion: 0.24
Nodes (11): Tests de la validacion de entradas de la capa UI (input mockeado)., _simular_input(), test_pedir_entero_en_rango_limites(), test_pedir_entero_en_rango_valido(), test_pedir_entero_enter_cancela(), test_pedir_entero_fuera_de_rango_vuelve_a_pedir(), test_pedir_entero_no_numerico_vuelve_a_pedir(), test_pedir_texto_excede_longitud_vuelve_a_pedir() (+3 more)

### Community 128 - "Community 128"
Cohesion: 0.15
Nodes (3): bf7661e Subir repositorio de refactorizacion: codigo, docs y analisis, SensorManager, Constantes centralizadas de la aplicacion de peliculas y series.

### Community 129 - "Community 129"
Cohesion: 0.21
Nodes (7): client(), _mock_response(), Tests de TvmazeClient con HTTP mockeado (sin red real)., Cliente TVMaze con configuracion por defecto., test_buscar_series_con_resultados(), test_buscar_series_sin_resultados(), test_obtener_detalles()

### Community 130 - "Community 130"
Cohesion: 0.29
Nodes (11): main(), make_dataset(), median_interleaved(), payroll_original(), peak_mem(), print_overhead_ms(), Benchmark final: nomina1.py (actual) vs nomina1_optimized.py (Python puro).  Sin, Replica exacta del algoritmo de nomina1.py (incluye print y escritura). (+3 more)

### Community 131 - "Community 131"
Cohesion: 0.17
Nodes (4): Servicio de series con dependencias inyectadas reales., Cliente TVMaze real (no se llama a la red)., service(), tvmaze_client()

### Community 132 - "Community 132"
Cohesion: 0.18
Nodes (1): Tests del modelo Series: construccion desde TVMaze y conversion.

### Community 133 - "Community 133"
Cohesion: 0.20
Nodes (9): correlation_scope(), _CorrelationFilter, get_logger(), Configuracion centralizada de logging y correlation ID por operacion., Adjunta el correlation ID activo a cada registro., Configura consola y archivo con nivel segun ``config`` (solo una vez)., Devuelve un logger con el nombre del modulo., Genera un correlation ID para una operacion y lo propaga al contexto.      Todos (+1 more)

### Community 136 - "Community 136"
Cohesion: 0.36
Nodes (10): main, 0af61b9 Quitar artefacto .coverage del repositorio, 30541a0 Cerrar fase 3: consolidar specs de separacion de responsabilidades y archivar change, 5bed7d6 Agregar README con descripcion, objetivos, tecnologias y flujo SDD/OpenSpec, 60af690 Documentar skills de opencode instaladas en el proyecto, 66c66df Quitar libreria opencode-skills del repo (referenciada en README en su lugar), a8b0935 Cerrar fases 5 y 6: consolidar specs de seguridad y suite de tests (pytest, cobertura >=90%), aa29e6d Corregir entrada .coverage en .gitignore (se pegó a *.log) (+2 more)

### Community 137 - "Community 137"
Cohesion: 0.22
Nodes (1): Tests del HistoryRepository: registro, listado y persistencia JSON.

### Community 138 - "Community 138"
Cohesion: 0.25
Nodes (4): Busca una pelicula por titulo.          Returns:             Datos de la pelicul, Busca peliculas de un actor.          Returns:             Lista de resultados d, Llama protegido por el circuit breaker y reintentos., Ejecuta la llamada a OMDB (reintenta y degrada).

### Community 139 - "Community 139"
Cohesion: 0.25
Nodes (4): Protocol, PurchaseRepository, AlertStorage, SensorProcessor

### Community 140 - "Community 140"
Cohesion: 0.25
Nodes (7): pedir_entero_en_rango(), pedir_texto(), Validacion de entradas de usuario de la capa UI, reutilizable por el menu., Solicita un texto no vacio y acotado en longitud, re-pidiendo si es invalido., Solicita un numero entero dentro del rango indicado.      Returns:         El nu, Sanitiza un nombre base de archivo, rechazando rutas y caracteres peligrosos., sanitizar_nombre_archivo()

### Community 141 - "Community 141"
Cohesion: 0.38
Nodes (6): main(), payroll(), Calculo de nomina mensual optimizado en Python puro (sin dependencias).  Es mas, Calcula la nomina y devuelve las lineas de salida formateadas.      Las operacio, Escribe todos los registros en una sola operacion de I/O., write_output()

### Community 142 - "Community 142"
Cohesion: 0.29
Nodes (1): Tests del Cache en memoria con TTL.

### Community 143 - "Community 143"
Cohesion: 0.40
Nodes (1): Tests de AppConfig: valores por defecto, tipos e invariantes.

### Community 144 - "Community 144"
Cohesion: 0.40
Nodes (1): Tests de la jerarquia de excepciones de dominio.

### Community 145 - "Community 145"
Cohesion: 0.50
Nodes (3): _Entrada, Valor cacheado con su instante de expiracion., Guarda un valor asociado a una clave con TTL.

### Community 146 - "Community 146"
Cohesion: 1.00
Nodes (1): Realiza la peticion GET a OMDB y devuelve el JSON.

## Knowledge Gaps
- **2304 isolated node(s):** `Benchmark final: nomina1.py (actual) vs nomina1_optimized.py (Python puro).  Sin`, `Replica exacta del algoritmo de nomina1.py (incluye print y escritura).`, `Purchase processing system with tax calculation and discounts.`, `Industrial sensor telemetry and alert system.`, `Calculo de nomina mensual optimizado en Python puro (sin dependencias).  Es mas` (+2299 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 125`** (1 nodes): `Tests del modelo Movie: creacion, validacion y conversion.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 132`** (1 nodes): `Tests del modelo Series: construccion desde TVMaze y conversion.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 137`** (1 nodes): `Tests del HistoryRepository: registro, listado y persistencia JSON.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 142`** (1 nodes): `Tests del Cache en memoria con TTL.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 143`** (1 nodes): `Tests de AppConfig: valores por defecto, tipos e invariantes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 144`** (1 nodes): `Tests de la jerarquia de excepciones de dominio.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `Realiza la peticion GET a OMDB y devuelve el JSON.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AppConfig` connect `Community 1` to `Community 0`, `Community 39`, `Community 138`, `Community 146`, `Community 133`, `Community 143`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `OmdbClient` connect `Community 0` to `Community 39`, `Community 138`, `Community 146`, `Community 1`, `Community 119`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `Punto de entrada de la aplicacion: compone y arranca las dependencias.` connect `Community 1` to `Community 0`, `Community 39`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `AppConfig` (e.g. with `OmdbClient` and `Cliente HTTP dedicado para la API de OMDB, sin logica de negocio.`) actually correct?**
  _`AppConfig` has 56 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `Movie` (e.g. with `Tests del modelo Movie: creacion, validacion y conversion.` and `MovieService`) actually correct?**
  _`Movie` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `MovieService` (e.g. with `Punto de entrada de la aplicacion: compone y arranca las dependencias.` and `Lee la clave de OMDB del entorno cargado desde .env.      Returns:         Valor`) actually correct?**
  _`MovieService` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Benchmark final: nomina1.py (actual) vs nomina1_optimized.py (Python puro).  Sin`, `Replica exacta del algoritmo de nomina1.py (incluye print y escritura).`, `Purchase processing system with tax calculation and discounts.` to the rest of the system?**
  _2304 weakly-connected nodes found - possible documentation gaps or missing edges._