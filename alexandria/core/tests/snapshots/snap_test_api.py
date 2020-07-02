# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_api_list[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."name", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document"',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" IN (NULL)',
        'SELECT ("alexandria_core_document_tags"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid)',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/documents",
        "QUERY_STRING": "include=category%2Ctags",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": """Morning option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                        "fr": "",
                    },
                    "meta": {},
                    "name": "Pamela Horton",
                    "title": {"de": "", "en": "David Romero", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "category": {"data": None},
                    "tags": {
                        "data": [{"id": "industry-call", "type": "tags"}],
                        "meta": {"count": 1},
                    },
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": """Serious live by. Run then project find white continue.
Effort partner area media increase meeting. Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "meta": {},
                    "name": "Rebecca Gonzalez",
                    "title": {"de": "", "en": "Olivia Miller", "fr": ""},
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {
                    "category": {"data": None},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": """Later now over myself can bed. Land prevent minute can second prove every. Check new stay culture.
Risk against capital factor. Product trade for brother weight.""",
                        "fr": "",
                    },
                    "meta": {},
                    "name": "Lorraine Reynolds",
                    "title": {"de": "", "en": "John Woods", "fr": ""},
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "category": {"data": None},
                    "tags": {"data": [], "meta": {"count": 0}},
                },
                "type": "documents",
            },
        ],
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Of themselves garden weight table same method work. Mean finally realize us movie. Truth deep public these.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "David Benson", "fr": ""},
                },
                "id": "industry-call",
                "type": "tags",
            }
        ],
    },
    "status": 200,
}

snapshots["test_api_list[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description" FROM "alexandria_core_category"'
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/categories",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
                },
                "id": "mrs-shake-recent",
                "type": "categories",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Size lead run then project find white. Those player foreign idea. Area media increase meeting article.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "Angela Brown", "fr": ""},
                },
                "id": "reason-son-current",
                "type": "categories",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Wide happy air represent. Cup debate medical. Today morning standard effort summer.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "Justin Hunt", "fr": ""},
                },
                "id": "structure",
                "type": "categories",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag"'
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/tags",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
                },
                "id": "mrs-shake-recent",
                "type": "tags",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Size lead run then project find white. Those player foreign idea. Area media increase meeting article.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "Angela Brown", "fr": ""},
                },
                "id": "reason-son-current",
                "type": "tags",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Wide happy air represent. Cup debate medical. Today morning standard effort summer.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "Justin Hunt", "fr": ""},
                },
                "id": "structure",
                "type": "tags",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_detail[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."name", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" IN (NULL)',
        'SELECT ("alexandria_core_document_tags"."document_id") AS "_prefetch_related_val_document_id", "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "include=category%2Ctags",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": None,
                "description": {
                    "de": "",
                    "en": """Morning option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "meta": {},
                "name": "Pamela Horton",
                "title": {"de": "", "en": "David Romero", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": None},
                "tags": {
                    "data": [{"id": "industry-call", "type": "tags"}],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        },
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-group": None,
                    "created-by-user": None,
                    "description": {
                        "de": "",
                        "en": "Of themselves garden weight table same method work. Mean finally realize us movie. Truth deep public these.",
                        "fr": "",
                    },
                    "meta": {},
                    "name": {"de": "", "en": "David Benson", "fr": ""},
                },
                "id": "industry-call",
                "type": "tags",
            }
        ],
    },
    "status": 200,
}

snapshots["test_api_detail[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'mrs-shake-recent\''
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/categories/mrs-shake-recent",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": None,
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
            "type": "categories",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'mrs-shake-recent\''
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/tags/mrs-shake-recent",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": None,
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
            "type": "tags",
        }
    },
    "status": 200,
}

snapshots["test_api_create[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'industry-call\'',
        """INSERT INTO "alexandria_core_document" ("created_at", "created_by_user", "created_by_group", "meta", "id", "name", "title", "description", "category_id") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'admin\', NULL, \'{}\', \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'Pamela Horton\', hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'David Romero\',\'\',\'\']), hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Morning option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.','','']), NULL)""",
        'SELECT "alexandria_core_tag"."slug" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
        'SELECT "alexandria_core_document_tags"."tag_id" FROM "alexandria_core_document_tags" WHERE ("alexandria_core_document_tags"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid AND "alexandria_core_document_tags"."tag_id" IN (\'industry-call\'))',
        'INSERT INTO "alexandria_core_document_tags" ("document_id", "tag_id") VALUES (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'industry-call\') RETURNING "alexandria_core_document_tags"."id"',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "564",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/documents",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Morning option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "meta": {},
                "name": "Pamela Horton",
                "title": {"de": "", "en": "David Romero", "fr": ""},
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "relationships": {
                "category": {"data": None},
                "tags": {
                    "data": [{"id": "industry-call", "type": "tags"}],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "status": 201,
}

snapshots["test_api_create[CategoryViewSet] 1"] = {
    "queries": [
        "INSERT INTO \"alexandria_core_category\" (\"created_at\", \"created_by_user\", \"created_by_group\", \"meta\", \"slug\", \"name\", \"description\") VALUES ('2017-05-21T00:00:00+00:00'::timestamptz, 'admin', NULL, '{}', '', hstore(ARRAY['en','de','fr'], ARRAY['Jordan Mccarthy','','']), hstore(ARRAY['en','de','fr'], ARRAY['Bit among again across environment long line. Team suggest traditional boy above.','','']))"
    ],
    "request": {
        "CONTENT_LENGTH": "331",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/categories",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "",
            "type": "categories",
        }
    },
    "status": 201,
}

snapshots["test_api_create[TagViewSet] 1"] = {
    "queries": [
        "INSERT INTO \"alexandria_core_tag\" (\"created_at\", \"created_by_user\", \"created_by_group\", \"meta\", \"slug\", \"name\", \"description\") VALUES ('2017-05-21T00:00:00+00:00'::timestamptz, 'admin', NULL, '{}', '', hstore(ARRAY['en','de','fr'], ARRAY['Jordan Mccarthy','','']), hstore(ARRAY['en','de','fr'], ARRAY['Bit among again across environment long line. Team suggest traditional boy above.','','']))"
    ],
    "request": {
        "CONTENT_LENGTH": "325",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/tags",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "",
            "type": "tags",
        }
    },
    "status": 201,
}

snapshots["test_api_patch[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."name", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'industry-call\'',
        """UPDATE "alexandria_core_document" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user" = \'admin\', "created_by_group" = NULL, "meta" = \'{}\', "name" = \'Pamela Horton\', "title" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'David Romero\',\'\',\'\']), "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Morning option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.\',\'\',\'\']), "category_id" = NULL WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid""",
        'SELECT "alexandria_core_tag"."slug" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" INNER JOIN "alexandria_core_document_tags" ON ("alexandria_core_tag"."slug" = "alexandria_core_document_tags"."tag_id") WHERE "alexandria_core_document_tags"."document_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "564",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": """Morning option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "meta": {},
                "name": "Pamela Horton",
                "title": {"de": "", "en": "David Romero", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "category": {"data": None},
                "tags": {
                    "data": [{"id": "industry-call", "type": "tags"}],
                    "meta": {"count": 1},
                },
            },
            "type": "documents",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'mrs-shake-recent\'',
        "UPDATE \"alexandria_core_category\" SET \"created_at\" = '2017-05-21T00:00:00+00:00'::timestamptz, \"created_by_user\" = 'admin', \"created_by_group\" = NULL, \"meta\" = '{}', \"name\" = hstore(ARRAY['en','de','fr'], ARRAY['Jordan Mccarthy','','']), \"description\" = hstore(ARRAY['en','de','fr'], ARRAY['Bit among again across environment long line. Team suggest traditional boy above.','','']) WHERE \"alexandria_core_category\".\"slug\" = 'mrs-shake-recent'",
    ],
    "request": {
        "CONTENT_LENGTH": "331",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/categories/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
            "type": "categories",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'mrs-shake-recent\'',
        "UPDATE \"alexandria_core_tag\" SET \"created_at\" = '2017-05-21T00:00:00+00:00'::timestamptz, \"created_by_user\" = 'admin', \"created_by_group\" = NULL, \"meta\" = '{}', \"name\" = hstore(ARRAY['en','de','fr'], ARRAY['Jordan Mccarthy','','']), \"description\" = hstore(ARRAY['en','de','fr'], ARRAY['Bit among again across environment long line. Team suggest traditional boy above.','','']) WHERE \"alexandria_core_tag\".\"slug\" = 'mrs-shake-recent'",
    ],
    "request": {
        "CONTENT_LENGTH": "325",
        "CONTENT_TYPE": "application/vnd.api+json; charset=None",
        "PATH_INFO": "/api/v1/tags/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "created-by-group": None,
                "created-by-user": "admin",
                "description": {
                    "de": "",
                    "en": "Bit among again across environment long line. Team suggest traditional boy above.",
                    "fr": "",
                },
                "meta": {},
                "name": {"de": "", "en": "Jordan Mccarthy", "fr": ""},
            },
            "id": "mrs-shake-recent",
            "type": "tags",
        }
    },
    "status": 200,
}

snapshots["test_api_destroy[DocumentViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."name", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "alexandria_core_document_tags"."id", "alexandria_core_document_tags"."document_id", "alexandria_core_document_tags"."tag_id" FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."document_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."id" IN (1)',
        'DELETE FROM "alexandria_core_document" WHERE "alexandria_core_document"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "request": {
        "PATH_INFO": "/api/v1/documents/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_destroy[CategoryViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_category"."created_at", "alexandria_core_category"."created_by_user", "alexandria_core_category"."created_by_group", "alexandria_core_category"."meta", "alexandria_core_category"."slug", "alexandria_core_category"."name", "alexandria_core_category"."description" FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" = \'mrs-shake-recent\'',
        'SELECT "alexandria_core_document"."created_at", "alexandria_core_document"."created_by_user", "alexandria_core_document"."created_by_group", "alexandria_core_document"."meta", "alexandria_core_document"."id", "alexandria_core_document"."name", "alexandria_core_document"."title", "alexandria_core_document"."description", "alexandria_core_document"."category_id" FROM "alexandria_core_document" WHERE "alexandria_core_document"."category_id" IN (\'mrs-shake-recent\')',
        'DELETE FROM "alexandria_core_category" WHERE "alexandria_core_category"."slug" IN (\'mrs-shake-recent\')',
    ],
    "request": {
        "PATH_INFO": "/api/v1/categories/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_destroy[TagViewSet] 1"] = {
    "queries": [
        'SELECT "alexandria_core_tag"."created_at", "alexandria_core_tag"."created_by_user", "alexandria_core_tag"."created_by_group", "alexandria_core_tag"."meta", "alexandria_core_tag"."slug", "alexandria_core_tag"."name", "alexandria_core_tag"."description" FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" = \'mrs-shake-recent\'',
        'SELECT "alexandria_core_document_tags"."id", "alexandria_core_document_tags"."document_id", "alexandria_core_document_tags"."tag_id" FROM "alexandria_core_document_tags" WHERE "alexandria_core_document_tags"."tag_id" IN (\'mrs-shake-recent\')',
        'DELETE FROM "alexandria_core_tag" WHERE "alexandria_core_tag"."slug" IN (\'mrs-shake-recent\')',
    ],
    "request": {
        "PATH_INFO": "/api/v1/tags/mrs-shake-recent",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}
