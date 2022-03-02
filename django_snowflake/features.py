from django.db import InterfaceError
from django.db.backends.base.features import BaseDatabaseFeatures
from django.utils.functional import cached_property


class DatabaseFeatures(BaseDatabaseFeatures):
    # Specifying a pk of zero is problematic because of the SELECT MAX(id)
    # approach to getting the last insert id.
    allows_auto_pk_0 = False
    can_clone_databases = True
    can_introspect_json_field = False
    closed_cursor_error_class = InterfaceError
    # This feature is specific to the Django fork used for testing.
    enforces_foreign_key_constraints = False
    # This feature is specific to the Django fork used for testing.
    enforces_unique_constraints = False
    has_case_insensitive_like = False
    has_json_object_function = False
    indexes_foreign_keys = False
    nulls_order_largest = True
    supported_explain_formats = {'JSON', 'TABULAR', 'TEXT'}
    supports_column_check_constraints = False
    supports_table_check_constraints = False
    supports_expression_indexes = False
    supports_ignore_conflicts = False
    # This feature is specific to the Django fork used for testing.
    supports_indexes = False
    supports_index_column_ordering = False
    # Not yet implemented in this backend.
    supports_json_field = False
    supports_over_clause = True
    supports_partial_indexes = False
    # https://docs.snowflake.com/en/sql-reference/functions-regexp.html#backreferences
    supports_regex_backreferencing = False
    supports_sequence_reset = False
    supports_slicing_ordering_in_compound = True
    supports_subqueries_in_group_by = False
    supports_temporal_subtraction = True
    # This really means "supports_nested_transactions". Snowflake supports a
    # single level of transaction, BEGIN + (ROLLBACK|COMMIT). Multiple BEGINS
    # contribute to the current (only) transaction.
    supports_transactions = False
    # This feature is specific to the Django fork used for testing.
    supports_tz_offsets = False
    uses_savepoints = False
    test_collations = {
        'ci': 'en-ci',
        # Snowflake: case-sensitive always returns the lowercase version of a
        # letter before the uppercase version of the same letter which isn't
        # what CollateTests.test_collate_order_by_cs expects.
        'cs': None,
        'non_default': 'en-ci',
        'swedish_ci': 'sv-ci',
    }

    django_test_expected_failures = {
        # Subquery issue to be investigated.
        'lookup.tests.LookupTests.test_exact_exists',
        # In Snowflake "the regex pattern is implicitly anchored at both ends
        # (i.e. '' automatically becomes '^$')." This gives different results
        # than other databases.
        # https://docs.snowflake.com/en/sql-reference/functions-regexp.html#corner-cases
        'lookup.tests.LookupTests.test_regex',
        # "Binding data in type (event) is not supported." To be investigated.
        'model_fields.test_charfield.TestCharField.test_assignment_from_choice_enum',
        # Binding data in type (safestring) is not supported.
        'i18n.tests.TestModels.test_safestr',
        # Invalid argument types for function '+': (INTERVAL, TIMESTAMP_NTZ(9))
        'expressions.tests.FTimeDeltaTests.test_delta_add',
        # DatabaseOperations.format_for_duration_arithmetic() INTERVAL syntax
        # doesn't accept column names.
        'annotations.tests.NonAggregateAnnotationTestCase.test_mixed_type_annotation_date_interval',
        'expressions.tests.FTimeDeltaTests.test_duration_with_datetime',
        'expressions.tests.FTimeDeltaTests.test_durationfield_add',
        # Interval math off by one microsecond for years beyond ~2250:
        # https://github.com/snowflakedb/snowflake-connector-python/issues/926
        'expressions.tests.FTimeDeltaTests.test_duration_with_datetime_microseconds',
        # Interval math off by one hour due to crossing daylight saving time.
        'expressions.tests.FTimeDeltaTests.test_delta_update',
        # Altering Integer PK to AutoField not supported.
        'migrations.test_operations.OperationTests.test_alter_field_pk',
        'schema.tests.SchemaTests.test_alter_int_pk_to_autofield_pk',
        'schema.tests.SchemaTests.test_alter_int_pk_to_bigautofield_pk',
        'schema.tests.SchemaTests.test_alter_smallint_pk_to_smallautofield_pk',
        # Interval math with NULL crashes:
        # https://github.com/cedar-team/django-snowflake/issues/26
        'expressions.tests.FTimeDeltaTests.test_date_subtraction',
        'expressions.tests.FTimeDeltaTests.test_datetime_subtraction',
        'expressions.tests.FTimeDeltaTests.test_time_subtraction',
        # SQL compilation error: <subquery> is not a valid order by expression.
        'ordering.tests.OrderingTests.test_orders_nulls_first_on_filtered_subquery',
    }

    django_test_skips = {
        'Snowflake does not enforce FOREIGN KEY constraints.': {
            'backends.tests.FkConstraintsTests',
            'fixtures_regress.tests.TestFixtures.test_loaddata_raises_error_when_fixture_has_invalid_foreign_key',
            'model_fields.test_uuid.TestAsPrimaryKeyTransactionTests.test_unsaved_fk',
            'transactions.tests.NonAutocommitTests.test_orm_query_after_error_and_rollback',
        },
        'Snowflake does not enforce UNIQUE constraints.': {
            'auth_tests.test_basic.BasicTestCase.test_unicode_username',
            'auth_tests.test_migrations.ProxyModelWithSameAppLabelTests.test_migrate_with_existing_target_permission',
            'constraints.tests.UniqueConstraintTests.test_database_constraint',
            'contenttypes_tests.test_operations.ContentTypeOperationsTests.test_content_type_rename_conflict',
            'contenttypes_tests.test_operations.ContentTypeOperationsTests.test_existing_content_type_rename',
            'custom_pk.tests.CustomPKTests.test_unique_pk',
            'get_or_create.tests.GetOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key',
            'get_or_create.tests.GetOrCreateTestsWithManualPKs.test_savepoint_rollback',
            'get_or_create.tests.GetOrCreateThroughManyToMany.test_something',
            'get_or_create.tests.UpdateOrCreateTests.test_manual_primary_key_test',
            'get_or_create.tests.UpdateOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key',
            'model_fields.test_filefield.FileFieldTests.test_unique_when_same_filename',
            'one_to_one.tests.OneToOneTests.test_multiple_o2o',
        },
        'Snowflake does not support indexes.': {
            'introspection.tests.IntrospectionTests.test_get_constraints_index_types',
            'migrations.test_operations.OperationTests.test_add_index',
            'migrations.test_operations.OperationTests.test_alter_field_with_index',
            'migrations.test_operations.OperationTests.test_alter_index_together',
            'migrations.test_operations.OperationTests.test_remove_index',
            'schema.tests.SchemaTests.test_add_remove_index',
            'schema.tests.SchemaTests.test_alter_field_add_index_to_integerfield',
            'schema.tests.SchemaTests.test_create_index_together',
            'schema.tests.SchemaTests.test_index_together',
            'schema.tests.SchemaTests.test_index_together_with_fk',
            'schema.tests.SchemaTests.test_indexes',
            'schema.tests.SchemaTests.test_order_index',
            'schema.tests.SchemaTests.test_remove_constraints_capital_letters',
            'schema.tests.SchemaTests.test_remove_db_index_doesnt_remove_custom_indexes',
            'schema.tests.SchemaTests.test_remove_field_unique_does_not_remove_meta_constraints',
            'schema.tests.SchemaTests.test_remove_index_together_does_not_remove_meta_indexes',
            'schema.tests.SchemaTests.test_remove_unique_together_does_not_remove_meta_constraints',
            'schema.tests.SchemaTests.test_text_field_with_db_index',
        },
        'Snowflake does not enforce PositiveIntegerField constraint.': {
            'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
        },
        'Snowflake: Unsupported subquery type cannot be evaluated.': {
            'admin_filters.tests.ListFiltersTests.test_emptylistfieldfilter_genericrelation',
            'admin_filters.tests.ListFiltersTests.test_emptylistfieldfilter_reverse_relationships',
            'admin_filters.tests.ListFiltersTests.test_listfilter_genericrelation',
            'admin_filters.tests.ListFiltersTests.test_relatedfieldlistfilter_manytomany',
            'admin_filters.tests.ListFiltersTests.test_relatedfieldlistfilter_reverse_relationships',
            'admin_views.tests.AdminSearchTest.test_exact_matches',
            'admin_views.tests.AdminSearchTest.test_no_total_count',
            'admin_views.tests.AdminSearchTest.test_search_on_sibling_models',
            'admin_views.tests.AdminViewBasicTest.test_relation_spanning_filters',
            'admin_views.tests.LimitChoicesToInAdminTest.test_limit_choices_to_as_callable',
            'aggregation.test_filter_argument.FilteredAggregateTests.test_filtered_aggregate_ref_multiple_subquery_annotation',  # noqa
            'aggregation.test_filter_argument.FilteredAggregateTests.test_filtered_aggregate_ref_subquery_annotation',
            'aggregation.tests.AggregateTestCase.test_aggregation_subquery_annotation',
            'aggregation.tests.AggregateTestCase.test_aggregation_subquery_annotation_values',
            'aggregation.tests.AggregateTestCase.test_aggregation_subquery_annotation_values_collision',
            'aggregation_regress.tests.AggregationTests.test_annotate_and_join',
            'annotations.tests.NonAggregateAnnotationTestCase.test_annotation_exists_aggregate_values_chaining',
            'annotations.tests.NonAggregateAnnotationTestCase.test_annotation_filter_with_subquery',
            'annotations.tests.NonAggregateAnnotationTestCase.test_annotation_subquery_outerref_transform',
            'auth_tests.test_models.UserWithPermTestCase.test_basic',
            'auth_tests.test_models.UserWithPermTestCase.test_nonexistent_permission',
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_subquery_with_parameters',
            'expressions_window.tests.WindowFunctionTests.test_subquery_row_range_rank',
            'lookup.tests.LookupTests.test_nested_outerref_lhs',
            'expressions.tests.BasicExpressionsTests.test_aggregate_subquery_annotation',
            'expressions.tests.BasicExpressionsTests.test_annotation_with_nested_outerref',
            'expressions.tests.BasicExpressionsTests.test_annotation_with_outerref',
            'expressions.tests.BasicExpressionsTests.test_annotations_within_subquery',
            'expressions.tests.BasicExpressionsTests.test_boolean_expression_combined',
            'expressions.tests.BasicExpressionsTests.test_boolean_expression_combined_with_empty_Q',
            'expressions.tests.BasicExpressionsTests.test_case_in_filter_if_boolean_output_field',
            'expressions.tests.BasicExpressionsTests.test_exists_in_filter',
            'expressions.tests.BasicExpressionsTests.test_nested_outerref_with_function',
            'expressions.tests.BasicExpressionsTests.test_nested_subquery',
            'expressions.tests.BasicExpressionsTests.test_nested_subquery_join_outer_ref',
            'expressions.tests.BasicExpressionsTests.test_nested_subquery_outer_ref_2',
            'expressions.tests.BasicExpressionsTests.test_nested_subquery_outer_ref_with_autofield',
            'expressions.tests.BasicExpressionsTests.test_order_by_exists',
            'expressions.tests.BasicExpressionsTests.test_subquery',
            'expressions.tests.BasicExpressionsTests.test_subquery_filter_by_lazy',
            'expressions.tests.BasicExpressionsTests.test_subquery_in_filter',
            'expressions.tests.FTimeDeltaTests.test_date_subquery_subtraction',
            'expressions.tests.FTimeDeltaTests.test_datetime_subquery_subtraction',
            'filtered_relation.tests.FilteredRelationTests.test_with_exclude',
            'generic_relations.tests.GenericRelationsTests.test_queries_content_type_restriction',
            'generic_relations_regress.tests.GenericRelationTests.test_ticket_20378',
            'generic_relations_regress.tests.GenericRelationTests.test_ticket_20564',
            'generic_relations_regress.tests.GenericRelationTests.test_ticket_20564_nullable_fk',
            'many_to_many.tests.ManyToManyTests.test_selects',
            'model_forms.tests.LimitChoicesToTests.test_fields_for_model_applies_limit_choices_to',
            'model_forms.tests.LimitChoicesToTests.test_limit_choices_to_callable_for_fk_rel',
            'model_forms.tests.LimitChoicesToTests.test_limit_choices_to_callable_for_m2m_rel',
            'model_forms.tests.LimitChoicesToTests.test_limit_choices_to_no_duplicates',
            'queries.test_qs_combinators.QuerySetSetOperationTests.test_union_with_values_list_on_annotated_and_unannotated',  # noqa
            'queries.tests.ExcludeTest17600.test_exclude_plain',
            'queries.tests.ExcludeTest17600.test_exclude_plain_distinct',
            'queries.tests.ExcludeTest17600.test_exclude_with_q_is_equal_to_plain_exclude',
            'queries.tests.ExcludeTest17600.test_exclude_with_q_is_equal_to_plain_exclude_variation',
            'queries.tests.ExcludeTest17600.test_exclude_with_q_object_distinct',
            'queries.tests.ExcludeTest17600.test_exclude_with_q_object_no_distinct',
            'queries.tests.ExcludeTests.test_exclude_multivalued_exists',
            'queries.tests.ExcludeTests.test_exclude_subquery',
            'queries.tests.ExcludeTests.test_subquery_exclude_outerref',
            'queries.tests.ExcludeTests.test_ticket14511',
            'queries.tests.ExcludeTests.test_to_field',
            'queries.tests.ForeignKeyToBaseExcludeTests.test_ticket_21787',
            'queries.tests.JoinReuseTest.test_inverted_q_across_relations',
            'queries.tests.ManyToManyExcludeTest.test_exclude_many_to_many',
            'queries.tests.ManyToManyExcludeTest.test_ticket_12823',
            'queries.tests.Queries1Tests.test_double_exclude',
            'queries.tests.Queries1Tests.test_exclude',
            'queries.tests.Queries1Tests.test_exclude_in',
            'queries.tests.Queries1Tests.test_nested_exclude',
            'queries.tests.Queries1Tests.test_ticket7096',
            'queries.tests.Queries1Tests.test_tickets_5324_6704',
            'queries.tests.Queries4Tests.test_ticket24525',
            # invalid identifier '"subquery"."col1"'
            'queries.tests.Queries6Tests.test_distinct_ordered_sliced_subquery_aggregation',
            'queries.tests.Queries6Tests.test_tickets_8921_9188',
            # invalid identifier '"subquery"."dumbcategory_ptr_id"'
            'queries.tests.SubqueryTests.test_distinct_ordered_sliced_subquery',
            'queries.tests.TestTicket24605.test_ticket_24605',
            'queries.tests.Ticket20788Tests.test_ticket_20788',
            'queries.tests.Ticket22429Tests.test_ticket_22429',
            'queries.tests.Ticket23605Tests.test_ticket_23605',
        },
        'Snowflake: Window function type [ROW_NUMBER] requires ORDER BY in '
        'window specification.': {
             'expressions_window.tests.WindowFunctionTests.test_row_number_no_ordering',
        },
        # https://github.com/cedar-team/django-snowflake/issues/40
        'DatabaseOperations.sequence_reset_sql() must be implemented for this test.': {
            'backends.tests.SequenceResetTest.test_generic_relation',
            'backends.base.test_operations.SqlFlushTests.test_execute_sql_flush_statements',
            'servers.tests.LiveServerDatabase.test_database_writes',
        },
        "Snowflake prohibits string truncation when using Cast.": {
            'db_functions.comparison.test_cast.CastTests.test_cast_to_char_field_with_max_length',
        },
        'Snowflake does not support nested transactions.': {
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_add_url_not_allowed',
            'admin_views.tests.AdminViewBasicTest.test_disallowed_to_field',
            'admin_views.tests.AdminViewPermissionsTest.test_add_view',
            'admin_views.tests.AdminViewPermissionsTest.test_change_view',
            'admin_views.tests.AdminViewPermissionsTest.test_change_view_save_as_new',
            'admin_views.tests.AdminViewPermissionsTest.test_delete_view',
            'auth_tests.test_views.ChangelistTests.test_view_user_password_is_readonly',
            'fixtures.tests.FixtureLoadingTests.test_loaddata_app_option',
            'fixtures.tests.FixtureLoadingTests.test_unmatched_identifier_loading',
            'force_insert_update.tests.ForceTests.test_force_update',
            'many_to_one.tests.ManyToOneTests.test_fk_assignment_and_related_object_cache',
            'many_to_many.tests.ManyToManyTests.test_add',
            'model_fields.test_booleanfield.BooleanFieldTests.test_null_default',
            'model_fields.test_floatfield.TestFloatField.test_float_validates_object',
            'multiple_database.tests.QueryTestCase.test_generic_key_cross_database_protection',
            'multiple_database.tests.QueryTestCase.test_m2m_cross_database_protection',
            'transaction_hooks.tests.TestConnectionOnCommit.test_discards_hooks_from_rolled_back_savepoint',
            'transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_rolled_back_with_outer',
            'transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_does_not_affect_outer',
            'transactions.tests.DisableDurabiltityCheckTests',
        },
        'Unused DatabaseIntrospection.get_key_columns() not implemented.': {
            'introspection.tests.IntrospectionTests.test_get_key_columns',
        },
        'Unused DatabaseIntrospection.get_sequences() not implemented.': {
            'introspection.tests.IntrospectionTests.test_sequence_list',
        },
        'snowflake-connector-python returns datetimes with timezone': {
            'timezones.tests.LegacyDatabaseTests.test_cursor_execute_returns_naive_datetime',
        },
        'Snowflake: cannot change column type.': {
            # NUMBER to FLOAT
            'migrations.test_operations.OperationTests.test_alter_field_pk_fk',
            'migrations.test_operations.OperationTests.test_alter_fk_non_fk',
            # NUMBER to VARCHAR
            'migrations.test_executor.ExecutorTests.test_alter_id_type_with_fk',
            'migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_with_to_field_related_name_target_type_change',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_with_to_field_target_type_change',  # noqa
            'schema.tests.SchemaTests.test_alter_auto_field_to_char_field',
            # VARCHAR to DATE
            'schema.tests.SchemaTests.test_alter_text_field_to_date_field',
            # VARCHAR TO TIMESTAMP
            'schema.tests.SchemaTests.test_alter_text_field_to_datetime_field',
            # VARCHAR to TIME
            'schema.tests.SchemaTests.test_alter_text_field_to_time_field',
            # VARCHAR to NUMBER
            'schema.tests.SchemaTests.test_char_field_with_db_index_to_fk',
            'schema.tests.SchemaTests.test_char_field_pk_to_auto_field',
            'schema.tests.SchemaTests.test_text_field_with_db_index_to_fk',
        },
        'Snowflake: reducing the byte-length of a varchar is not supported.': {
            'migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_target_changes',
            'migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_with_to_field_target_changes',  # noqa
            'migrations.test_operations.OperationTests.test_rename_field_reloads_state_on_fk_target_changes',
            'schema.tests.SchemaTests.test_alter_field_type_and_db_collation',
            'schema.tests.SchemaTests.test_alter_textual_field_keep_null_status',
            'schema.tests.SchemaTests.test_m2m_rename_field_in_target_model',
            'schema.tests.SchemaTests.test_rename',
        },
        'Snowflake: cannot change column type because they have incompatible collations.': {
            'schema.tests.SchemaTests.test_alter_field_db_collation',
            'schema.tests.SchemaTests.test_ci_cs_db_collation',
        },
        # https://github.com/cedar-team/django-snowflake/issues/24
        'Database caching is not supported.': {
            'cache.tests.CreateCacheTableForDBCacheTests',
            'cache.tests.DBCacheTests',
            'cache.tests.DBCacheWithTimeZoneTests',
        },
        'assertNumQueries is sometimes off because of the extra queries this '
        'backend uses to fetch an object\'s ID.': {
            'contenttypes_tests.test_models.ContentTypesTests.test_get_for_models_creation',
            'model_formsets_regress.tests.FormsetTests.test_extraneous_query_is_not_run',
            'model_inheritance.tests.ModelInheritanceTests.test_create_child_no_update',
        },
        'It can be problematic if a model instance is manually assigned a pk value.': {
            'contenttypes_tests.test_views.ContentTypesViewsSiteRelTests.test_shortcut_view_with_null_site_fk',
            'contenttypes_tests.test_views.ContentTypesViewsSiteRelTests.test_shortcut_view_with_site_m2m',
        },
        'This test takes on order of an hour due to 2,000 inserts.': {
            'delete.tests.DeletionTests.test_large_delete_related',
        },
    }

    @cached_property
    def introspected_field_types(self):
        return{
            **super().introspected_field_types,
            'DurationField': 'BigIntegerField',
            'GenericIPAddressField': 'CharField',
            'PositiveBigIntegerField': 'BigIntegerField',
            'PositiveIntegerField': 'IntegerField',
            'PositiveSmallIntegerField': 'SmallIntegerField',
        }
