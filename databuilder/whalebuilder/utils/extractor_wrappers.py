import os

from pyhocon import ConfigFactory
from whalebuilder.extractor.presto_loop_extractor import PrestoLoopExtractor
from whalebuilder.models.connection_config import ConnectionConfigSchema
from whalebuilder.extractor.amundsen_neo4j_metadata_extractor \
    import AmundsenNeo4jMetadataExtractor
from whalebuilder.extractor.bigquery_metadata_extractor \
    import BigQueryMetadataExtractor
from whalebuilder.extractor.snowflake_metadata_extractor \
    import SnowflakeMetadataExtractor
from databuilder.extractor.sql_alchemy_extractor import SQLAlchemyExtractor
from databuilder.extractor.bigquery_watermark_extractor import BigQueryWatermarkExtractor


BUILD_SCRIPT_TEMPLATE = \
    """source {venv_path}/bin/activate \
    && {python_binary} {build_script_path}"""
SQL_ALCHEMY_SCOPE = SQLAlchemyExtractor().get_scope()


def configure_bigquery_extractors(connection: ConnectionConfigSchema):
    extractor = BigQueryMetadataExtractor()
    scope = extractor.get_scope()
    watermark_extractor = BigQueryWatermarkExtractor()
    watermark_scope = watermark_extractor.get_scope()
    conf = ConfigFactory.from_dict({
        '{}.key_path'.format(scope): connection.key_path,
        '{}.project_id'.format(scope): connection.project_id,
        '{}.project_credentials'.format(scope): connection.project_credentials,
        '{}.page_size'.format(scope): connection.page_size,
        '{}.filter_key'.format(scope): connection.filter_key,
        '{}.key_path'.format(watermark_scope): connection.key_path,
        '{}.project_id'.format(watermark_scope): connection.project_id,
        '{}.project_credentials'.format(watermark_scope): connection.project_credentials,
    })

    extractors = [extractor, watermark_extractor]

    return extractors, conf


def configure_presto_extractors(
        connection: ConnectionConfigSchema,
        is_full_extraction_enabled: bool = False):
    extractor = PrestoLoopExtractor()
    scope = extractor.get_scope()
    conn_string_key = '{}.conn_string'.format(scope)

    username_password_placeholder = \
        '{}:{}'.format(connection.username, connection.password) \
        if connection.password is not None else ''

    conn_string = 'presto://{username_password}@{uri}:{port}'.format(
        username_password=username_password_placeholder,
        uri=connection.uri,
        port=connection.port)

    conf = ConfigFactory.from_dict({
        conn_string_key: conn_string,
        '{}.is_table_metadata_enabled'.format(scope): True,
        '{}.is_full_extraction_enabled'.format(scope):
            is_full_extraction_enabled,
        '{}.is_watermark_enabled'.format(scope): False,
        '{}.is_stats_enabled'.format(scope): False,
        '{}.is_analyze_enabled'.format(scope): False,
        '{}.database'.format(scope): connection.name,
        '{}.cluster'.format(scope): connection.cluster,
        '{}.included_schemas'.format(scope): connection.included_schemas,
        '{}.excluded_schemas'.format(scope): connection.excluded_schemas,
    })

    extractors = [extractor]

    return extractors, conf


def configure_neo4j_extractors(connection: ConnectionConfigSchema):
    extractor = AmundsenNeo4jMetadataExtractor()
    scope = extractor.get_scope()
    conn_string = 'bolt://{uri}:{port}'.format(
        uri=connection.uri,
        port=connection.port)
    conf = ConfigFactory.from_dict({
        '{}.graph_url'.format(scope): conn_string,
        '{}.neo4j_auth_user'.format(scope): connection.username,
        '{}.neo4j_auth_pw'.format(scope): connection.password,
        '{}.included_keys'.format(scope): connection.included_keys,
        '{}.excluded_keys'.format(scope): connection.excluded_keys,
        '{}.included_key_regex'.format(scope): connection.included_key_regex,
        '{}.excluded_key_regex'.format(scope): connection.excluded_key_regex,
    })

    extractors = [extractor]

    return extractors, conf


def configure_snowflake_extractors(connection: ConnectionConfigSchema):
    extractor = SnowflakeMetadataExtractor()
    scope = extractor.get_scope()

    conn_string_key = '{}.{}.conn_string'\
        .format(scope, SQL_ALCHEMY_SCOPE)

    username_password_placeholder = \
        '{}:{}'.format(connection.username, connection.password) \
        if connection.password is not None else ''

    conn_string = \
        '{connection_type}://{username_password}@{uri}:{port}'.format(
            connection_type=connection.type,
            username_password=username_password_placeholder,
            uri=connection.uri,
            port=connection.port)

    conf = ConfigFactory.from_dict({
        conn_string_key: conn_string,
        '{}.database'.format(scope): connection.name,
        '{}.cluster'.format(scope): connection.cluster,
    })

    extractors = [extractor]

    return extractors, conf


def run_build_script(connection: ConnectionConfigSchema):
    if not connection.python_binary:
        python_binary = 'python3'
    else:
        python_binary = os.path.expanduser(connection.python_binary)

    venv_path = os.path.expanduser(connection.venv_path)
    build_script_path = os.path.expanduser(connection.build_script_path)

    os.system(BUILD_SCRIPT_TEMPLATE.format(
        venv_path=venv_path,
        python_binary=python_binary,
        build_script_path=build_script_path
    ))
