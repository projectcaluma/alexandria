# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_api_list[FileViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'dad3a37a-a9d5-0688-b515-7698acfd7aee\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'dad3a37a-a9d5-0688-b515-7698acfd7aee\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid',
    ],
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
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Devon Cooke",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Devon Cooke",
                    "type": "original",
                    "upload-url": "",
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
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "download-url": "http://minio/download-url/ea416ed0-759d-46a8-de58-f63a59077499_Rebecca Gonzalez",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Rebecca Gonzalez",
                    "type": "original",
                    "upload-url": "",
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
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "download-url": "http://minio/download-url/dad3a37a-a9d5-0688-b515-7698acfd7aee_Michelle Johnson",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Michelle Johnson",
                    "type": "original",
                    "upload-url": "",
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
                    "description": {
                        "de": "",
                        "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "John Fernandez", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {
                        "data": {"id": "mrs-shake-recent", "type": "categories"}
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
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Serious live by. Run then project find white continue.
Effort partner area media increase meeting. Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Olivia Miller", "fr": ""},
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "category": {
                        "data": {"id": "reach-piece-it-all", "type": "categories"}
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
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Them he consumer same season. Fine religious where loss increase firm friend.
Their office though television return main.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Victoria Nash", "fr": ""},
                },
                "id": "fb0e22c7-9ac7-5679-e988-1e6ba183b354",
                "relationships": {
                    "category": {
                        "data": {"id": "material-eight", "type": "categories"}
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
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_create[TagViewSet] 1"] = {
    "queries": [
        "INSERT INTO \"alexandria_core_tag\" (\"created_at\", \"created_by_user\", \"created_by_group\", \"modified_at\", \"modified_by_user\", \"modified_by_group\", \"meta\", \"slug\", \"name\", \"description\") VALUES ('2017-05-21T00:00:00+00:00'::timestamptz, 'admin', 'admin', '2017-05-21T00:00:00+00:00'::timestamptz, 'admin', 'admin', '{}', 'jordan-mccarthy', 'Jordan Mccarthy', hstore(ARRAY['en','de','fr'], ARRAY['Bit among again across environment long line. Team suggest traditional boy above.','','']))"
    ],
    "request": {
        "CONTENT_LENGTH": "400",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
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
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jordan Mccarthy",
            },
            "id": "mrs-shake-recent",
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
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jordan Mccarthy",
            },
            "id": "jordan-mccarthy",
            "type": "tags",
        }
    },
    "status": 201,
}

snapshots["test_api_detail[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'mrs-shake-recent\''
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/categories/mrs-shake-recent",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": {
            "attributes": {
                "color": "#ea8594",
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
            "type": "categories",
        }
    },
    "status": 200,
}

snapshots["test_api_create[CategoryViewSet] 1"] = {
    "queries": [],
    "request": {
        "CONTENT_LENGTH": "447",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/categories",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "color": "#ea8594",
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
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

snapshots["test_api_destroy[FileViewSet] 1"] = {
    "queries": [],
    "request": {
        "PATH_INFO": "/api/v1/files/9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 405,
}

snapshots["test_api_create[FileViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'INSERT INTO "alexandria_core_file" ("created_at", "created_by_user", "created_by_group", "modified_at", "modified_by_user", "modified_by_group", "meta", "id", "type", "original_id", "name", "document_id") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', \'admin\', \'{}\', \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, \'original\', NULL, \'Devon Cooke\', \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
    ],
    "request": {
        "CONTENT_LENGTH": "594",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/files",
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
                "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Devon Cooke",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Devon Cooke",
                "type": "original",
                "upload-url": "",
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
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "download-url": "http://minio/download-url/f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad_Devon Cooke",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Devon Cooke",
                "type": "original",
                "upload-url": "http://minio/upload-url",
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

snapshots["test_api_patch[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'mrs-shake-recent\'',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'fly-even-yourself\'',
        "UPDATE \"alexandria_core_document\" SET \"created_at\" = '2017-05-21T00:00:00+00:00'::timestamptz, \"created_by_user\" = 'admin', \"created_by_group\" = 'admin', \"modified_at\" = '2017-05-21T00:00:00+00:00'::timestamptz, \"modified_by_user\" = 'admin', \"modified_by_group\" = 'admin', \"meta\" = '{}', \"title\" = hstore(ARRAY['en','de','fr'], ARRAY['John Fernandez','','']), \"description\" = hstore(ARRAY['en','de','fr'], ARRAY['Decade wall thing for east later still. Number inside put fire try cell.','','']), \"category_id\" = 'mrs-shake-recent' WHERE \"alexandria_core_document\".\"id\" = '9dd4e461-268c-8034-f5c8-564e155c67a6'::uuid",
        'SELECT "alexandria_core_tag"."slug" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "640",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
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
                "description": {
                    "de": "",
                    "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "John Fernandez", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "mrs-shake-recent", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "tags": {
                    "data": [{"id": "fly-even-yourself", "type": "tags"}],
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
                "description": {
                    "de": "",
                    "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "John Fernandez", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "mrs-shake-recent", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "tags": {
                    "data": [{"id": "fly-even-yourself", "type": "tags"}],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "status": 200,
}

snapshots["test_api_create[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'mrs-shake-recent\'',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'fly-even-yourself\'',
        "INSERT INTO \"alexandria_core_document\" (\"created_at\", \"created_by_user\", \"created_by_group\", \"modified_at\", \"modified_by_user\", \"modified_by_group\", \"meta\", \"id\", \"title\", \"description\", \"category_id\") VALUES ('2017-05-21T00:00:00+00:00'::timestamptz, 'admin', 'admin', '2017-05-21T00:00:00+00:00'::timestamptz, 'admin', 'admin', '{}', '9336ebf2-5087-d91c-818e-e6e9ec29f8c1'::uuid, hstore(ARRAY['en','de','fr'], ARRAY['John Fernandez','','']), hstore(ARRAY['en','de','fr'], ARRAY['Decade wall thing for east later still. Number inside put fire try cell.','','']), 'mrs-shake-recent')",
        'SELECT "alexandria_core_tag"."slug" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
        'SELECT "alexandria_core_document_tags"."tag_id" FROM "alexandria_core_document_tags" WHERE ("alexandria_core_document_tags"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid AND "alexandria_core_document_tags"."tag_id" IN (\'fly-even-yourself\'))',
        'INSERT INTO "alexandria_core_document_tags" ("document_id", "tag_id") VALUES (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'fly-even-yourself\') RETURNING "alexandria_core_document_tags"."id"',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "640",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
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
                "description": {
                    "de": "",
                    "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "John Fernandez", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "mrs-shake-recent", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "tags": {
                    "data": [{"id": "fly-even-yourself", "type": "tags"}],
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
                "description": {
                    "de": "",
                    "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "John Fernandez", "fr": ""},
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "relationships": {
                "category": {"data": {"id": "mrs-shake-recent", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "tags": {
                    "data": [{"id": "fly-even-yourself", "type": "tags"}],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "status": 201,
}

snapshots["test_api_patch[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'mrs-shake-recent\'',
        "UPDATE \"alexandria_core_tag\" SET \"created_at\" = '2017-05-21T00:00:00+00:00'::timestamptz, \"created_by_user\" = 'admin', \"created_by_group\" = 'admin', \"modified_at\" = '2017-05-21T00:00:00+00:00'::timestamptz, \"modified_by_user\" = 'admin', \"modified_by_group\" = 'admin', \"meta\" = '{}', \"name\" = 'Jordan Mccarthy', \"description\" = hstore(ARRAY['en','de','fr'], ARRAY['Bit among again across environment long line. Team suggest traditional boy above.','','']) WHERE \"alexandria_core_tag\".\"slug\" = 'mrs-shake-recent'",
    ],
    "request": {
        "CONTENT_LENGTH": "400",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/tags/mrs-shake-recent",
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
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jordan Mccarthy",
            },
            "id": "mrs-shake-recent",
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
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jordan Mccarthy",
            },
            "id": "mrs-shake-recent",
            "type": "tags",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'mrs-shake-recent\''
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/tags/mrs-shake-recent",
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
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Jordan Mccarthy",
            },
            "id": "mrs-shake-recent",
            "type": "tags",
        }
    },
    "status": 200,
}

snapshots["test_api_destroy[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_document_tags"."id", "alexandria_core_document_tags"."document_id", "alexandria_core_document_tags"."tag_id" FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
        'DELETE FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."id" IN (1)',
        'DELETE FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "request": {
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 204,
}

snapshots["test_api_patch[CategoryViewSet] 1"] = {
    "queries": [],
    "request": {
        "CONTENT_LENGTH": "447",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/categories/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "request_payload": {
        "data": {
            "attributes": {
                "color": "#ea8594",
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
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

snapshots["test_api_list[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color" FROM "alexandria_core_category"'
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/categories",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "response": {
        "data": [
            {
                "attributes": {
                    "color": "#ea8594",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
                },
                "id": "mrs-shake-recent",
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#e08dd8",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Size lead run then project find white. Those player foreign idea. Area media increase meeting article.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Angela Brown", "fr": ""},
                },
                "id": "reason-son-current",
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
                        "en": "Cup debate medical. Today morning standard effort summer.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Mathew White", "fr": ""},
                },
                "id": "everything-process",
                "type": "categories",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag"'
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/tags",
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
                        "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Jordan Mccarthy",
                },
                "id": "mrs-shake-recent",
                "type": "tags",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Size lead run then project find white. Those player foreign idea. Area media increase meeting article.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Angela Brown",
                },
                "id": "reason-son-current",
                "type": "tags",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Wide happy air represent. Cup debate medical. Today morning standard effort summer.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Justin Hunt",
                },
                "id": "structure",
                "type": "tags",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document"',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" IN (\'mrs-shake-recent\', \'reach-piece-it-all\', \'section-voice\')',
        'SELECT ("alexandria_core_document_tags"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid)',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/documents",
        "QUERY_STRING": "include=category%2Ctags%2Cfiles",
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
                        "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "John Fernandez", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {
                        "data": {"id": "mrs-shake-recent", "type": "categories"}
                    },
                    "files": {"data": [], "meta": {"count": 0}},
                    "tags": {
                        "data": [{"id": "fly-even-yourself", "type": "tags"}],
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
                    "description": {
                        "de": "",
                        "en": """Bank arm serious live by itself. Project find white continue none president. Idea eye plan third program.
Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Rebecca Gonzalez", "fr": ""},
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {
                    "category": {
                        "data": {"id": "reach-piece-it-all", "type": "categories"}
                    },
                    "files": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Take value eye sell them he. Less power relate fine. Where loss increase firm friend ability sing.
Food prevent trouble cold south which general. Never form leader fund task. Major talk late yes.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "Michelle Johnson", "fr": ""},
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "category": {"data": {"id": "section-voice", "type": "categories"}},
                    "files": {"data": [], "meta": {"count": 0}},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
        ],
        "included": [
            {
                "attributes": {
                    "color": "#ea8594",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
                },
                "id": "mrs-shake-recent",
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#e8a78f",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Outside capital direction capital Congress doctor land. Minute can second prove every check official. Stay culture create risk.
Daughter single product trade.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Nicholas Davidson", "fr": ""},
                },
                "id": "reach-piece-it-all",
                "type": "categories",
            },
            {
                "attributes": {
                    "color": "#72e5bb",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": """Expert pressure dog. Maybe kitchen mother.
Tell save term few military feeling. Avoid generation nearly laugh. Human great region administration bar rate threat.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Dr. Ashley Oliver DDS", "fr": ""},
                },
                "id": "section-voice",
                "type": "categories",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Character last guy. Plan contain task various few. Section rock event recent public final activity hope.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Amanda Boyd",
                },
                "id": "fly-even-yourself",
                "type": "tags",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_destroy[CategoryViewSet] 1"] = {
    "queries": [],
    "request": {
        "PATH_INFO": "/api/v1/categories/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 405,
}

snapshots["test_api_patch[FileViewSet] 1"] = {
    "queries": [],
    "request": {
        "CONTENT_LENGTH": "594",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/files/9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
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
                "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Devon Cooke",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Devon Cooke",
                "type": "original",
                "upload-url": "",
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

snapshots["test_api_detail[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."modified_at", "alexandria_core_category"."modified_by_user", "alexandria_core_category"."modified_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description", "alexandria_core_category"."color" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" IN (\'mrs-shake-recent\')',
        'SELECT ("alexandria_core_document_tags"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid) ORDER BY "alexandria_core_file"."created_at" DESC',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "include=category%2Ctags%2Cfiles",
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
                    "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "title": {"de": "", "en": "John Fernandez", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": {"id": "mrs-shake-recent", "type": "categories"}},
                "files": {"data": [], "meta": {"count": 0}},
                "tags": {
                    "data": [{"id": "fly-even-yourself", "type": "tags"}],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        },
        "included": [
            {
                "attributes": {
                    "color": "#ea8594",
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
                },
                "id": "mrs-shake-recent",
                "type": "categories",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": "admin",
                    "created-by-user": "admin",
                    "description": {
                        "de": "",
                        "en": "Character last guy. Plan contain task various few. Section rock event recent public final activity hope.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "name": "Amanda Boyd",
                },
                "id": "fly-even-yourself",
                "type": "tags",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_detail[FileViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."original_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."modified_at", "alexandria_core_document"."modified_by_user", "alexandria_core_document"."modified_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_file"."created_at", "alexandria_core_file"."created_by_user", "alexandria_core_file"."created_by_group", "alexandria_core_file"."modified_at", "alexandria_core_file"."modified_by_user", "alexandria_core_file"."modified_by_group", "alexandria_core_file"."meta", "alexandria_core_file"."id", "alexandria_core_file"."type", "alexandria_core_file"."original_id", "alexandria_core_file"."name", "alexandria_core_file"."document_id" FROM "alexandria_core_file" WHERE "alexandria_core_file"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid ORDER BY "alexandria_core_file"."created_at" DESC',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
    ],
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
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": "admin",
                "created-by-user": "admin",
                "download-url": "http://minio/download-url/9336ebf2-5087-d91c-818e-e6e9ec29f8c1_Devon Cooke",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "modified-by-group": "admin",
                "modified-by-user": "admin",
                "name": "Devon Cooke",
                "type": "original",
                "upload-url": "",
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
                    "description": {
                        "de": "",
                        "en": "Decade wall thing for east later still. Number inside put fire try cell.",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-group": "admin",
                    "modified-by-user": "admin",
                    "title": {"de": "", "en": "John Fernandez", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {
                        "data": {"id": "mrs-shake-recent", "type": "categories"}
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
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            }
        ],
    },
    "status": 200,
}

snapshots["test_api_destroy[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."modified_at", "alexandria_core_tag"."modified_by_user", "alexandria_core_tag"."modified_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'mrs-shake-recent\'',
        'SELECT "alexandria_core_document_tags"."id", "alexandria_core_document_tags"."document_id", "alexandria_core_document_tags"."tag_id" FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."tag_id" IN (\'mrs-shake-recent\')',
        'DELETE FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" IN (\'mrs-shake-recent\')',
    ],
    "request": {
        "PATH_INFO": "/api/v1/tags/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "request_payload": None,
    "status": 204,
}
