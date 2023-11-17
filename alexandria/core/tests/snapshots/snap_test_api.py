# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_api_create[CategoryViewSet] 1"] = {
    "queries": [],
    "query_count": 0,
    "request": {
        "CONTENT_LENGTH": "646",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/categories",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "color": "#093f87",
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "relationships": {
                "children": {"data": [], "meta": {"count": 0}},
                "parent": {"data": None},
            },
            "type": "categories",
        }
    },
    "response": {
        "errors": [
            {
                "code": "method_not_allowed",
                "detail": 'Method "POST" not allowed.',
                "source": {"pointer": "/data"},
                "status": "405",
            }
        ]
    },
    "status": 405,
}

snapshots["test_api_create[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'note-act-source\' LIMIT 21',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid LIMIT 21',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" WHERE "alexandria_core_mark"."slug" = \'father-should-keep\' LIMIT 21',
        """INSERT INTO "alexandria_core_document" ("created_at", "created_by_user", "created_by_group", "modified_at", "modified_by_user", "modified_by_group", "metainfo", "id", "title", "description", "category_id", "date") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'{}\', \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Michael Edwards\',\'\',\'\']), hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.','','']), 'note-act-source', '1999-11-26'::date)""",
        'SELECT "alexandria_core_tag"."id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'INSERT INTO "alexandria_core_document_tags" ("document_id", "tag_id") VALUES (\'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid) ON CONFLICT DO NOTHING',
        'SELECT "alexandria_core_mark"."slug" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'INSERT INTO "alexandria_core_document_marks" ("document_id", "mark_id") VALUES (\'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, \'father-should-keep\') ON CONFLICT DO NOTHING',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
    ],
    "query_count": 11,
    "request": {
        "CONTENT_LENGTH": "859",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/documents",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "date": "1999-11-26",
                "description": {
                    "de": "",
                    "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "Michael Edwards", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "note-act-source", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "marks": {
                    "data": [{"id": "father-should-keep", "type": "marks"}],
                    "meta": {"count": 1},
                },
                "tags": {
                    "data": [
                        {"id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1", "type": "tags"}
                    ],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "date": "1999-11-26",
                "description": {
                    "de": "",
                    "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "Michael Edwards", "fr": ""},
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "relationships": {
                "category": {"data": {"id": "note-act-source", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "marks": {
                    "data": [{"id": "father-should-keep", "type": "marks"}],
                    "meta": {"count": 1},
                },
                "tags": {
                    "data": [
                        {"id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1", "type": "tags"}
                    ],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "status": 201,
}

snapshots["test_api_create[FileViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21',
        'INSERT INTO "alexandria_core_file" ("created_at", "created_by_user", "created_by_group", "modified_at", "modified_by_user", "modified_by_group", "metainfo", "id", "variant", "original_id", "name", "document_id", "checksum", "upload_status") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'{}\', \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, \'original\', NULL, \'Jason Lopez\', \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, NULL, \'undefined\')',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
    ],
    "query_count": 3,
    "request": {
        "CONTENT_LENGTH": "645",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/files",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "checksum": None,
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Jason Lopez",
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jason Lopez",
                "upload-status": "undefined",
                "upload-url": "",
                "variant": "original",
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "relationships": {
                "document": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "documents",
                    }
                },
                "original": {"data": None},
                "renderings": {"data": [], "meta": {"count": 0}},
            },
            "type": "files",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "checksum": None,
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "download-url": "http://minio/download-url/f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad_Jason Lopez",
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jason Lopez",
                "upload-status": "undefined",
                "upload-url": "http://minio/upload-url",
                "variant": "original",
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "relationships": {
                "document": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "documents",
                    }
                },
                "original": {"data": None},
                "renderings": {"data": [], "meta": {"count": 0}},
            },
            "type": "files",
        }
    },
    "status": 201,
}

snapshots["test_api_create[MarkViewSet] 1"] = {
    "queries": [
        """INSERT INTO "alexandria_core_mark" ("created_at", "created_by_user", "created_by_group", "modified_at", "modified_by_user", "modified_by_group", "metainfo", "slug", "name", "description") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'{}\', \'erin-scott\', hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Erin Scott\',\'\',\'\']), hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.','','']))"""
    ],
    "query_count": 1,
    "request": {
        "CONTENT_LENGTH": "540",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/marks",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "type": "marks",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "erin-scott",
            "type": "marks",
        }
    },
    "status": 201,
}

snapshots["test_api_create[TagViewSet] 1"] = {
    "queries": [
        """INSERT INTO "alexandria_core_tag" ("created_at", "created_by_user", "created_by_group", "modified_at", "modified_by_user", "modified_by_group", "metainfo", "id", "name", "description", "tag_synonym_group_id") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'{}\', \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'Pamela Horton\', hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.','','']), NULL)"""
    ],
    "query_count": 1,
    "request": {
        "CONTENT_LENGTH": "572",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/tags",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Pamela Horton",
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {"tag-synonym-group": {"data": None}},
            "type": "tags",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Pamela Horton",
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "relationships": {"tag-synonym-group": {"data": None}},
            "type": "tags",
        }
    },
    "status": 201,
}

snapshots["test_api_destroy[CategoryViewSet] 1"] = {
    "queries": [],
    "query_count": 0,
    "request": {
        "PATH_INFO": "/api/v1/categories/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 405,
}

snapshots["test_api_destroy[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21',
        'SELECT "alexandria_core_file"."id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
        'DELETE FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "alexandria_core_document_marks" WHERE "alexandria_core_document_marks"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "query_count": 5,
    "request": {
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 204,
}

snapshots["test_api_destroy[FileViewSet] 1"] = {
    "queries": [],
    "query_count": 0,
    "request": {
        "PATH_INFO": "/api/v1/files/9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 405,
}

snapshots["test_api_destroy[MarkViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" WHERE "alexandria_core_mark"."slug" = \'note-act-source\' LIMIT 21',
        'DELETE FROM "alexandria_core_document_marks" WHERE "alexandria_core_document_marks"."mark_id" IN (\'note-act-source\')',
        'DELETE FROM "alexandria_core_mark" WHERE "alexandria_core_mark"."slug" IN (\'note-act-source\')',
    ],
    "query_count": 3,
    "request": {
        "PATH_INFO": "/api/v1/marks/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 204,
}

snapshots["test_api_destroy[TagViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21',
        'DELETE FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."tag_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "query_count": 3,
    "request": {
        "PATH_INFO": "/api/v1/tags/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 204,
}

snapshots["test_api_detail[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id", T2."created_at", T2."created_by_user", T2."created_by_group", T2."modified_at", T2."modified_by_user", T2."modified_by_group", T2."metainfo", T2."slug", T2."name", T2."description", T2."color", T2."parent_id" FROM "alexandria_core_category" LEFT OUTER JOIN "alexandria_core_category" T2 ON ("alexandria_core_category"."parent_id" = T2."slug") WHERE "alexandria_core_category"."slug" = \'note-act-source\' LIMIT 21',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."parent_id" IN (\'note-act-source\')',
    ],
    "query_count": 2,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/categories/note-act-source",
        "QUERY_STRING": "include=parent%2Cchildren",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": {
            "attributes": {
                "color": "#093f87",
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "relationships": {
                "children": {"data": [], "meta": {"count": 0}},
                "parent": {"data": None},
            },
            "type": "categories",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date", "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_document" LEFT OUTER JOIN "alexandria_core_category" ON ("alexandria_core_document"."category_id" = "alexandria_core_category"."slug") WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21',
        'SELECT ("alexandria_core_document_tags"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT ("alexandria_core_document_marks"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."parent_id" = \'note-act-source\'',
    ],
    "query_count": 5,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "include=category%2Ctags%2Cmarks%2Cfiles",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "date": "1999-11-26",
                "description": {
                    "de": "",
                    "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "Michael Edwards", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "note-act-source", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "marks": {
                    "data": [{"id": "father-should-keep", "type": "marks"}],
                    "meta": {"count": 1},
                },
                "tags": {
                    "data": [
                        {"id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1", "type": "tags"}
                    ],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        },
        "included": [
            {
                "attributes": {
                    "color": "#093f87",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Erin Scott", "fr": ""},
                },
                "id": "note-act-source",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Hope star check record well.
With Mr letter eye way society. Move enter them his half long.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Philip Holmes", "fr": ""},
                },
                "id": "father-should-keep",
                "type": "marks",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """History off reason career. Wide even material police. List usually large exactly out.
Difficult make listen unit seven lead effort. Race couple identify.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Miss Ebony Gaines",
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {"tag-synonym-group": {"data": None}},
                "type": "tags",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_detail[FileViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status", T2."created_at", T2."created_by_user", T2."created_by_group", T2."modified_at", T2."modified_by_user", T2."modified_by_group", T2."metainfo", T2."id", T2."variant", T2."original_id", T2."name", T2."document_id", T2."checksum", T2."upload_status", "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date" FROM "alexandria_core_file" LEFT OUTER JOIN "alexandria_core_file" T2 ON ("alexandria_core_file"."original_id" = T2."id") INNER JOIN "alexandria_core_document" ON ("alexandria_core_file"."document_id" = "alexandria_core_document"."id") WHERE "alexandria_core_file"."id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid LIMIT 21',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
    ],
    "query_count": 5,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/files/9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
        "QUERY_STRING": "include=document%2Coriginal%2Crenderings",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": {
            "attributes": {
                "checksum": None,
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Jason Lopez",
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jason Lopez",
                "upload-status": "undefined",
                "upload-url": "",
                "variant": "original",
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "relationships": {
                "document": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "documents",
                    }
                },
                "original": {"data": None},
                "renderings": {"data": [], "meta": {"count": 0}},
            },
            "type": "files",
        },
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "1999-11-26",
                    "description": {
                        "de": "",
                        "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Michael Edwards", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {
                        "data": {"id": "note-act-source", "type": "categories"}
                    },
                    "files": {
                        "data": [
                            {
                                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                                "type": "files",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "marks": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            }
        ],
    },
    "status": 200,
}

snapshots["test_api_detail[MarkViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" WHERE "alexandria_core_mark"."slug" = \'note-act-source\' LIMIT 21'
    ],
    "query_count": 1,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/marks/note-act-source",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "type": "marks",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[TagViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id", "alexandria_core_tagsynonymgroup"."id", "alexandria_core_tagsynonymgroup"."created_at", "alexandria_core_tagsynonymgroup"."created_by_user", "alexandria_core_tagsynonymgroup"."created_by_group", "alexandria_core_tagsynonymgroup"."modified_at", "alexandria_core_tagsynonymgroup"."modified_by_user", "alexandria_core_tagsynonymgroup"."modified_by_group", "alexandria_core_tagsynonymgroup"."metainfo" FROM "alexandria_core_tag" LEFT OUTER JOIN "alexandria_core_tagsynonymgroup" ON ("alexandria_core_tag"."tag_synonym_group_id" = "alexandria_core_tagsynonymgroup"."id") WHERE "alexandria_core_tag"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21'
    ],
    "query_count": 1,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/tags/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "include=tag_synonym_group",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Pamela Horton",
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {"tag-synonym-group": {"data": None}},
            "type": "tags",
        }
    },
    "status": 200,
}

snapshots["test_api_list[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id", T2."created_at", T2."created_by_user", T2."created_by_group", T2."modified_at", T2."modified_by_user", T2."modified_by_group", T2."metainfo", T2."slug", T2."name", T2."description", T2."color", T2."parent_id" FROM "alexandria_core_category" LEFT OUTER JOIN "alexandria_core_category" T2 ON ("alexandria_core_category"."parent_id" = T2."slug")',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."parent_id" IN (\'note-act-source\', \'run-too-successful\', \'story-thing-piece\')',
    ],
    "query_count": 2,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/categories",
        "QUERY_STRING": "include=parent%2Cchildren",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": [
            {
                "attributes": {
                    "color": "#093f87",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Erin Scott", "fr": ""},
                },
                "id": "note-act-source",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#2eba92",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Arm serious live by itself. Project find white continue none president.
Partner area media increase meeting article. Success provide beyond seek officer player.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Timothy Malone", "fr": ""},
                },
                "id": "run-too-successful",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#eda797",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Wide happy air represent. Cup debate medical. Today morning standard effort summer.",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Douglas Keller", "fr": ""},
                },
                "id": "story-thing-piece",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date", "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_document" LEFT OUTER JOIN "alexandria_core_category" ON ("alexandria_core_document"."category_id" = "alexandria_core_category"."slug")',
        'SELECT ("alexandria_core_document_tags"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid)',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT ("alexandria_core_document_marks"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid)',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."parent_id" = \'note-act-source\'',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."parent_id" = \'right-professor\'',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."parent_id" = \'moment-poor\'',
    ],
    "query_count": 7,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/documents",
        "QUERY_STRING": "include=category%2Ctags%2Cmarks%2Cfiles",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "1999-11-26",
                    "description": {
                        "de": "",
                        "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Michael Edwards", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {
                        "data": {"id": "note-act-source", "type": "categories"}
                    },
                    "files": {"data": [], "meta": {"count": 0}},
                    "marks": {
                        "data": [{"id": "father-should-keep", "type": "marks"}],
                        "meta": {"count": 1},
                    },
                    "tags": {
                        "data": [
                            {
                                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                                "type": "tags",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "2005-06-14",
                    "description": {
                        "de": "",
                        "en": """Bank arm serious live by itself. Project find white continue none president. Idea eye plan third program.
Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Rebecca Gonzalez", "fr": ""},
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "category": {
                        "data": {"id": "right-professor", "type": "categories"}
                    },
                    "files": {"data": [], "meta": {"count": 0}},
                    "marks": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "1973-06-29",
                    "description": {
                        "de": "",
                        "en": """Cell series star. Agency season worry take value eye sell.
Human less power relate fine religious. Loss increase firm friend ability. Their office though television return main.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "William Kennedy", "fr": ""},
                },
                "id": "ea416ed0-759d-46a8-de58-f63a59077499",
                "relationships": {
                    "category": {"data": {"id": "moment-poor", "type": "categories"}},
                    "files": {"data": [], "meta": {"count": 0}},
                    "marks": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
        ],
        "included": [
            {
                "attributes": {
                    "color": "#eaf254",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Window relate raise gun. Base hear human high word. Boy per news traditional article.
Pressure dog sell maybe kitchen. Impact wide yourself win reflect purpose important.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Ronnie Mcdonald", "fr": ""},
                },
                "id": "moment-poor",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#093f87",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Erin Scott", "fr": ""},
                },
                "id": "note-act-source",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#1acca5",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Road political heart outside capital. Myself can bed notice range. Minute can second prove every check official.
Culture create risk against capital factor find able. For brother weight upon.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Andre Kennedy", "fr": ""},
                },
                "id": "right-professor",
                "relationships": {
                    "children": {"data": [], "meta": {"count": 0}},
                    "parent": {"data": None},
                },
                "type": "categories",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Hope star check record well.
With Mr letter eye way society. Move enter them his half long.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Philip Holmes", "fr": ""},
                },
                "id": "father-should-keep",
                "type": "marks",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """History off reason career. Wide even material police. List usually large exactly out.
Difficult make listen unit seven lead effort. Race couple identify.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Miss Ebony Gaines",
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {"tag-synonym-group": {"data": None}},
                "type": "tags",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_list[FileViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status", T2."created_at", T2."created_by_user", T2."created_by_group", T2."modified_at", T2."modified_by_user", T2."modified_by_group", T2."metainfo", T2."id", T2."variant", T2."original_id", T2."name", T2."document_id", T2."checksum", T2."upload_status", "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date" FROM "alexandria_core_file" LEFT OUTER JOIN "alexandria_core_file" T2 ON ("alexandria_core_file"."original_id" = T2."id") INNER JOIN "alexandria_core_document" ON ("alexandria_core_file"."document_id" = "alexandria_core_document"."id") ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'dad3a37a-a9d5-0688-b515-7698acfd7aee\'::uuid, \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid',
    ],
    "query_count": 11,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/files",
        "QUERY_STRING": "include=document%2Coriginal%2Crenderings",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": [
            {
                "attributes": {
                    "checksum": None,
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Jason Lopez",
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Jason Lopez",
                    "upload-status": "undefined",
                    "upload-url": "",
                    "variant": "original",
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {
                    "document": {
                        "data": {
                            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                            "type": "documents",
                        }
                    },
                    "original": {"data": None},
                    "renderings": {"data": [], "meta": {"count": 0}},
                },
                "type": "files",
            },
            {
                "attributes": {
                    "checksum": None,
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "download-url": "http://minio/download-url/ea416ed0-759d-46a8-de58-f63a59077499_Rebecca Gonzalez",
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Rebecca Gonzalez",
                    "upload-status": "undefined",
                    "upload-url": "",
                    "variant": "original",
                },
                "id": "ea416ed0-759d-46a8-de58-f63a59077499",
                "relationships": {
                    "document": {
                        "data": {
                            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                            "type": "documents",
                        }
                    },
                    "original": {"data": None},
                    "renderings": {"data": [], "meta": {"count": 0}},
                },
                "type": "files",
            },
            {
                "attributes": {
                    "checksum": None,
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "download-url": "http://minio/download-url/dad3a37a-a9d5-0688-b515-7698acfd7aee_William Kennedy",
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "William Kennedy",
                    "upload-status": "undefined",
                    "upload-url": "",
                    "variant": "original",
                },
                "id": "dad3a37a-a9d5-0688-b515-7698acfd7aee",
                "relationships": {
                    "document": {
                        "data": {
                            "id": "fb0e22c7-9ac7-5679-e988-1e6ba183b354",
                            "type": "documents",
                        }
                    },
                    "original": {"data": None},
                    "renderings": {"data": [], "meta": {"count": 0}},
                },
                "type": "files",
            },
        ],
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "1999-11-26",
                    "description": {
                        "de": "",
                        "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Michael Edwards", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {
                        "data": {"id": "note-act-source", "type": "categories"}
                    },
                    "files": {
                        "data": [
                            {
                                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                                "type": "files",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "marks": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "2005-06-14",
                    "description": {
                        "de": "",
                        "en": """Serious live by. Run then project find white continue.
Effort partner area media increase meeting. Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Olivia Miller", "fr": ""},
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "category": {
                        "data": {"id": "right-professor", "type": "categories"}
                    },
                    "files": {
                        "data": [
                            {
                                "id": "ea416ed0-759d-46a8-de58-f63a59077499",
                                "type": "files",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "marks": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "date": "1977-12-09",
                    "description": {
                        "de": "",
                        "en": """Star Republican agency season. Take value eye sell them he.
Same season natural think Mr course tree. Within never whose five hold food.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Carol Mata", "fr": ""},
                },
                "id": "fb0e22c7-9ac7-5679-e988-1e6ba183b354",
                "relationships": {
                    "category": {
                        "data": {"id": "party-coach-note", "type": "categories"}
                    },
                    "files": {
                        "data": [
                            {
                                "id": "dad3a37a-a9d5-0688-b515-7698acfd7aee",
                                "type": "files",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "marks": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_list[MarkViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark"'
    ],
    "query_count": 1,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/marks",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Arm serious live by itself. Project find white continue none president.
Partner area media increase meeting article. Success provide beyond seek officer player.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Timothy Malone", "fr": ""},
                },
                "id": "run-too-successful",
                "type": "marks",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Erin Scott", "fr": ""},
                },
                "id": "note-act-source",
                "type": "marks",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Process truth assume popular contain commercial with. Detail race high even might.
Thing summer prevent free environment measure role later. Capital direction capital Congress doctor land prevent.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Linda Taylor", "fr": ""},
                },
                "id": "front-her-occur",
                "type": "marks",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[TagViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id", "alexandria_core_tagsynonymgroup"."id", "alexandria_core_tagsynonymgroup"."created_at", "alexandria_core_tagsynonymgroup"."created_by_user", "alexandria_core_tagsynonymgroup"."created_by_group", "alexandria_core_tagsynonymgroup"."modified_at", "alexandria_core_tagsynonymgroup"."modified_by_user", "alexandria_core_tagsynonymgroup"."modified_by_group", "alexandria_core_tagsynonymgroup"."metainfo" FROM "alexandria_core_tag" LEFT OUTER JOIN "alexandria_core_tagsynonymgroup" ON ("alexandria_core_tag"."tag_synonym_group_id" = "alexandria_core_tagsynonymgroup"."id")'
    ],
    "query_count": 1,
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/tags",
        "QUERY_STRING": "include=tag_synonym_group",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Pamela Horton",
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {"tag-synonym-group": {"data": None}},
                "type": "tags",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Bank arm serious live by itself. Project find white continue none president. Idea eye plan third program.
Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Rebecca Gonzalez",
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {"tag-synonym-group": {"data": None}},
                "type": "tags",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Free environment measure role later now over.
Can bed notice range. Minute can second prove every check official. Stay culture create risk.
Daughter single product trade.""",
                        "fr": "",
                    },
                    "metainfo": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Lorraine Reynolds",
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {"tag-synonym-group": {"data": None}},
                "type": "tags",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_patch[CategoryViewSet] 1"] = {
    "queries": [],
    "query_count": 0,
    "request": {
        "CONTENT_LENGTH": "646",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/categories/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "color": "#093f87",
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "relationships": {
                "children": {"data": [], "meta": {"count": 0}},
                "parent": {"data": None},
            },
            "type": "categories",
        }
    },
    "response": {
        "errors": [
            {
                "code": "method_not_allowed",
                "detail": 'Method "PATCH" not allowed.',
                "source": {"pointer": "/data"},
                "status": "405",
            }
        ]
    },
    "status": 405,
}

snapshots["test_api_patch[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."metainfo", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id", "alexandria_core_document"."date" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."metainfo", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color", "alexandria_core_category"."parent_id" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'note-act-source\' LIMIT 21',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid LIMIT 21',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" WHERE "alexandria_core_mark"."slug" = \'father-should-keep\' LIMIT 21',
        """UPDATE "alexandria_core_document" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user" = \'admin\', "created_by_group" = \'admin\', "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_by_user" = \'admin\', "modified_by_group" = \'admin\', "metainfo" = \'{}\', "title" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Michael Edwards\',\'\',\'\']), "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.\',\'\',\'\']), "category_id" = \'note-act-source\', "date" = \'1999-11-26\'::date WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid""",
        'SELECT "alexandria_core_tag"."id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_mark"."slug" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."metainfo", "alexandria_core_file"."id", "alexandria_core_file"."variant", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id", "alexandria_core_file"."checksum", "alexandria_core_file"."upload_status" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" INNER JOIN "alexandria_core_document_marks" ON ("alexandria_core_mark"."slug" = "alexandria_core_document_marks"."mark_id") WHERE "alexandria_core_document_marks"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" LEFT OUTER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."id" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IS NULL',
    ],
    "query_count": 11,
    "request": {
        "CONTENT_LENGTH": "859",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "date": "1999-11-26",
                "description": {
                    "de": "",
                    "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "Michael Edwards", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "note-act-source", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "marks": {
                    "data": [{"id": "father-should-keep", "type": "marks"}],
                    "meta": {"count": 1},
                },
                "tags": {
                    "data": [
                        {"id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1", "type": "tags"}
                    ],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "date": "1999-11-26",
                "description": {
                    "de": "",
                    "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "Michael Edwards", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "note-act-source", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "marks": {
                    "data": [{"id": "father-should-keep", "type": "marks"}],
                    "meta": {"count": 1},
                },
                "tags": {
                    "data": [
                        {"id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1", "type": "tags"}
                    ],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[FileViewSet] 1"] = {
    "queries": [],
    "query_count": 0,
    "request": {
        "CONTENT_LENGTH": "645",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/files/9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "checksum": None,
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Jason Lopez",
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jason Lopez",
                "upload-status": "undefined",
                "upload-url": "",
                "variant": "original",
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "relationships": {
                "document": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "documents",
                    }
                },
                "original": {"data": None},
                "renderings": {"data": [], "meta": {"count": 0}},
            },
            "type": "files",
        }
    },
    "response": {
        "errors": [
            {
                "code": "method_not_allowed",
                "detail": 'Method "PATCH" not allowed.',
                "source": {"pointer": "/data"},
                "status": "405",
            }
        ]
    },
    "status": 405,
}

snapshots["test_api_patch[MarkViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_mark"."created_at", "alexandria_core_mark"."created_by_user", "alexandria_core_mark"."created_by_group", "alexandria_core_mark"."modified_at", "alexandria_core_mark"."modified_by_user", "alexandria_core_mark"."modified_by_group", "alexandria_core_mark"."metainfo", "alexandria_core_mark"."slug", "alexandria_core_mark"."name", "alexandria_core_mark"."description" FROM "alexandria_core_mark" WHERE "alexandria_core_mark"."slug" = \'note-act-source\' LIMIT 21',
        """UPDATE "alexandria_core_mark" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user" = \'admin\', "created_by_group" = \'admin\', "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_by_user" = \'admin\', "modified_by_group" = \'admin\', "metainfo" = \'{}\', "name" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Erin Scott\',\'\',\'\']), "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.\',\'\',\'\']) WHERE "alexandria_core_mark"."slug" = \'note-act-source\'""",
    ],
    "query_count": 2,
    "request": {
        "CONTENT_LENGTH": "540",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/marks/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "type": "marks",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
            },
            "id": "note-act-source",
            "type": "marks",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[TagViewSet] 1"] = {
    "queries": [
        'SELECT DISTINCT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."metainfo", "alexandria_core_tag"."id", "alexandria_core_tag"."name", "alexandria_core_tag"."description", "alexandria_core_tag"."tag_synonym_group_id" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid LIMIT 21',
        """UPDATE "alexandria_core_tag" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user" = \'admin\', "created_by_group" = \'admin\', "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_by_user" = \'admin\', "modified_by_group" = \'admin\', "metainfo" = \'{}\', "name" = \'Pamela Horton\', "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.\',\'\',\'\']), "tag_synonym_group_id" = NULL WHERE "alexandria_core_tag"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid""",
    ],
    "query_count": 2,
    "request": {
        "CONTENT_LENGTH": "572",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/tags/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Pamela Horton",
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {"tag-synonym-group": {"data": None}},
            "type": "tags",
        }
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "metainfo": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Pamela Horton",
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {"tag-synonym-group": {"data": None}},
            "type": "tags",
        }
    },
    "status": 200,
}
