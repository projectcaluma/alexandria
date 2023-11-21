from collections import defaultdict

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


@pytest.fixture()
def post_migrate_to_current_state(transactional_db):
    """
    Apply all current migrations after test has run.

    In migration-tests, the `transactional_db` fixture seems to fail to apply the
    newest migrations for all apps, leading to flaky tests. This fixture makes sure,
    that all apps are migrated to their most current state.
    """
    try:
        yield
    finally:
        executor = MigrationExecutor(connection)
        migrations_dict = defaultdict(list)
        for app, migration in executor.loader.disk_migrations.keys():
            migrations_dict[app].append(migration)

        migrations_list = [
            (app, max(migrations)) for app, migrations in migrations_dict.items()
        ]
        executor.loader.build_graph()
        executor.migrate(migrations_list)
        executor.loader.build_graph()


def test_0011_file_path(post_migrate_to_current_state):
    executor = MigrationExecutor(connection)
    migrate_from = [("alexandria_core", "0010_mark")]
    migrate_to = [("alexandria_core", "0011_file_content")]
    executor.loader.build_graph()
    executor.migrate(migrate_from)

    old_apps = executor.loader.project_state(migrate_from).apps
    OldFile = old_apps.get_model("alexandria_core", "file")
    OldDocument = old_apps.get_model("alexandria_core", "document")
    doc = OldDocument.objects.create()
    OldFile.objects.create(name="existing_file", document=doc)

    executor.loader.build_graph()
    executor.migrate(migrate_to)
    new_apps = executor.loader.project_state(migrate_to).apps

    NewFile = new_apps.get_model("alexandria_core", "file")
    _file = NewFile.objects.first()
    assert _file.name in _file.content.url
