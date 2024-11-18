# 6.4.1
### Fix
* **document:** Revalidate mimetypes after moving document to different category ([`46066ac`](https://github.com/projectcaluma/alexandria/commit/46066ac030808fde94bfc263f8b303e21bea0482))

# 6.4.0
### Feature

* **file:** Move thumbnail generation to celery ([`6d30dcd`](https://github.com/projectcaluma/alexandria/commit/6d30dcd0533be084b8596cc1536ca69894fdc174))

### Fix
* Stricter mime type handling ([`4b8ab5b`](https://github.com/projectcaluma/alexandria/commit/4b8ab5b71b19d34d0000ba5fe008ee80aecc1c4c))

# 6.3.0
### Feature
* Move the fulltext search code to a proper filterset (088a897820f88e3078bd20488ca0437e575a8372)

# 6.2.0
### Feature
* Add celery to allow for background tasks (d6f995c5137b01fc2366bbf1011ea56a0a6c17a7)

# 6.1.1
### Fix
* **api:** Add missing "download_path" param to verify_signed_components ([`f0cca6c`](https://github.com/projectcaluma/alexandria/commit/f0cca6c28754a34c2f094a59b10805bb1883c5fb))

# 6.1.0
### Feature
* Add presigning functions to public api ([`a6a56a6`](https://github.com/projectcaluma/alexandria/commit/a6a56a6d857f53c26d93f275aeea02d41a11a4a0))

### Fix
* **convert:** Change file extension in document title on conversion ([`c91d7fa`](https://github.com/projectcaluma/alexandria/commit/c91d7faf947b0e16cc3222b844d782a0944bfdaf))

# 6.0.0
### Fix
* Make document title and description not localized ([`39436b7`](https://github.com/projectcaluma/alexandria/commit/39436b7739d8a06c9da2a51f7a7b5bed82a84d4c))
* **dockerfile:** Use correct settings ([`ddccc4d`](https://github.com/projectcaluma/alexandria/commit/ddccc4d27aeda004bcf69130787b46585d1ae137))

### Breaking
* Turn the document's `title` and `description` into regular CharFields/TextFields, instead of localized ones, because localized fields do not make sense for user-generated data. ([`39436b7`](https://github.com/projectcaluma/alexandria/commit/39436b7739d8a06c9da2a51f7a7b5bed82a84d4c))
* drop poetry from prod build by building a wheel ([`249544d`](https://github.com/projectcaluma/alexandria/commit/249544df7eadbe73a452164f73639f87966cb323))

# 5.1.1
### Fix
* fix(deps): update dependencies ([`2144e0b`](https://github.com/projectcaluma/alexandria/commit/2144e0b0b91de626c3994fde266e4de35d4258c9))

# 5.1.0
### Feature
* Search over all configured stemmings (1d9cca20db4d5054fa55cb8db490db3eebbe53b5)
* Allow opening webdav links with custom URI schemes (9f4516631dfb25aa5bcbf3b3500bcb5d0ab131be)

# 5.0.2
### Fix
* fix(file): improve content vector generation ([`b6841da`](https://github.com/projectcaluma/alexandria/commit/b6841da326198065d5d838febf360eaf28aa0389))

### Refactor
* refactor(file): move check for optional feature methods ([`a8420c5`](https://github.com/projectcaluma/alexandria/commit/a8420c5597579809d759a0d7d0daca8768f04379))

# 5.0.1
### Fix
* fix(file): improve content vector generation command ([`145ae23`](https://github.com/projectcaluma/alexandria/commit/145ae23aee4241922af21d88d88050423c3d894b))
* fix(tika): use module path imports ([`2df7b7a`](https://github.com/projectcaluma/alexandria/commit/2df7b7ad814905de87c9bb3a8be9c5ec8f0e707b))

# 5.0.0
### Feature
* **file:** Add search view ([`c9d3766`](https://github.com/projectcaluma/alexandria/commit/c9d37661f7cf4acb0fed55d088f07e7d6cd5d886))
* **file:** Add management command to fill content_vector ([`79b1978`](https://github.com/projectcaluma/alexandria/commit/79b1978ca4b0801cb3eb2edc84340d334d67022f))
* **file:** Add SearchVector field for extracted content ([`b0e5bad`](https://github.com/projectcaluma/alexandria/commit/b0e5baddf41aa03a249bac39c2bc875447cc2c13))
* **file:** Add apache tika for file content extraction ([`0557c59`](https://github.com/projectcaluma/alexandria/commit/0557c5997f6a92055f7b0db56e9a04e93f1f3464))
* **webdav:** Add allowed list of mime types for webdav ([`343a2ee`](https://github.com/projectcaluma/alexandria/commit/343a2eee4b0620c26cec5ced6cd499f5ecb8f4f0))
* **webdav:** Webdav_url to sperate webdav view ([`7162f28`](https://github.com/projectcaluma/alexandria/commit/7162f28d4cdfe8c7059d1b8cd95c5fa7dbeb93a5))

### Fix
* **clamav:** Inline django-clamd to resolve version problems ([#564](https://github.com/projectcaluma/alexandria/issues/564)) ([`fe6e98d`](https://github.com/projectcaluma/alexandria/commit/fe6e98dcb4f80e76234d4e1d61315e5a8554e92e))
* Update dgap for webdav get permission check ([`4b1bb74`](https://github.com/projectcaluma/alexandria/commit/4b1bb74ba5be445db2f3cb6f06fd998045fd7ac6))
* **webdav:** Remove default doc, xls files ([`94df87f`](https://github.com/projectcaluma/alexandria/commit/94df87f0d3d34f20054b606edfcf3455a8017d78))

### Breaking
* removed django-clamd clamav will only be called over tcp, unix socket capabilities have been removed ([`fe6e98d`](https://github.com/projectcaluma/alexandria/commit/fe6e98dcb4f80e76234d4e1d61315e5a8554e92e))
* webdav_url to sperate webdav view ([`7162f28`](https://github.com/projectcaluma/alexandria/commit/7162f28d4cdfe8c7059d1b8cd95c5fa7dbeb93a5))

The URL for WebDAV editing is now in a seperate endpoint, to allow for checking the Permissions before serving it.
Previously the WebDAV URL was served even if the Permissions were denied, as getting the WebDAV URL was a Visibility check.

### Documentation
* **readme:** Improve documentation for available features and config ([`a19b8cb`](https://github.com/projectcaluma/alexandria/commit/a19b8cb57c2c7222d2ff8943db6a5fc5b42e2341))

# 4.1.0
### Feature
* Allow custom implementation of username and group getters ([`72bf2e4`](https://github.com/projectcaluma/alexandria/commit/72bf2e42862bb72fbd34cda059b8df0aa107ef7a))

### Fix
* **core:** Add get_user_and_group for serializer ([`b5bc3b6`](https://github.com/projectcaluma/alexandria/commit/b5bc3b67645bb2fe46dc547f94f8399ee5c2ecb7))

# 4.0.2
### Fix
* **mime:** Allow file extension checking if all fails ([`ddaa134`](https://github.com/projectcaluma/alexandria/commit/ddaa1344b2cde98a0c52f3311772d36da6e28c28))
* Use atomic for document and file creation ([`1a630ad`](https://github.com/projectcaluma/alexandria/commit/1a630adb83a8351d1ed01b3070790e65b00cc43d))

# 4.0.1
### Fix
* **thumbnails:** Enlarge the thumbnails ([`a80f7b5`](https://github.com/projectcaluma/alexandria/commit/a80f7b535ba21e3c8a3c23318cb95ca4be70f273))

# 4.0.0
### Feature
* **document:** Create document and file in one request! ([`444912d`](https://github.com/projectcaluma/alexandria/commit/444912d4cb584c05096ca8a78dd455b8471e9441))

### Breaking
* The document post endpoint now requires the file data to be provided as well. The reason for this change is allowing the frontend to create documents and files in one request, preventing documents with no associated files. Which fixes the problem if the file got rejected for any reason, the application would create an empty document. ([`444912d`](https://github.com/projectcaluma/alexandria/commit/444912d4cb584c05096ca8a78dd455b8471e9441))

# 3.1.0
### Feature
* **category:** Define allowed mime types ([`d4fd84e`](https://github.com/projectcaluma/alexandria/commit/d4fd84e6edb0502818f885082217aa48f0e56c5b))

### Fix
* **mimetypes:** Cleanup, simplify error handling ([`3bde9c4`](https://github.com/projectcaluma/alexandria/commit/3bde9c490f5ba67d4859767fa37afeabba3f1326))
* **translation:** Use string replacement instead of f string ([`74dd485`](https://github.com/projectcaluma/alexandria/commit/74dd485587e30765bea4a784beead595a33df405))
* **migrations:** Add missing migration for modified by description ([`7f53058`](https://github.com/projectcaluma/alexandria/commit/7f5305820f3e76e1ff6d06bfaa2d7af7d97cd08c))
* **upload:** Use content-type and filename to infer mime types ([`d475321`](https://github.com/projectcaluma/alexandria/commit/d475321d23a7a21037b3012fd4aebeb6cb78b134))

# 3.0.0
### Fix
* **dav:** Set created_by_* attributes on new files ([`f480cb6`](https://github.com/projectcaluma/alexandria/commit/f480cb670bf359adee82ac49ec59ee2c018df8ab))

# 3.0.0-beta.18
### Feature
* Add python api for creating files ([#487](https://github.com/projectcaluma/alexandria/issues/487)) ([`a26f058`](https://github.com/projectcaluma/alexandria/commit/a26f0588a6a4365598079283d8dd26d5a580e3e3))

# 3.0.0-beta.17
### Fix
* **webdav:** Split alexandria provider out of dav.py ([`a0c7d64`](https://github.com/projectcaluma/alexandria/commit/a0c7d64412bc8fada912b94c5206823278a76052))

# 3.0.0-beta.16
### Fix
* **webdav:** Make scheme a setting ([`a634c86`](https://github.com/projectcaluma/alexandria/commit/a634c863c3219ca465c15b40f6e80971b6905b9f))

# 3.0.0-beta.15
### Fix
* Disable manabi by default ([`eea655c`](https://github.com/projectcaluma/alexandria/commit/eea655c01a66761efd227fd8bd39f3984251fc7b))
* **manabi:** Set sane TTL and configure `secure` ([`6eb0ca2`](https://github.com/projectcaluma/alexandria/commit/6eb0ca23c6b3d030f30b700ab16a3724786dc47f))
* **webdav:** Only serve webdav link if manabi is enabled ([`ef2e0b9`](https://github.com/projectcaluma/alexandria/commit/ef2e0b9d1d29fd1cdabb7507f3004d9c62297c8f))
* **webdav:** Use `webdav`-scheme as default for webdav links ([`d513916`](https://github.com/projectcaluma/alexandria/commit/d51391655dd27b1dd7fa4bda82dd84f846666051))
* Only serve newest File form Document ([`27bc67f`](https://github.com/projectcaluma/alexandria/commit/27bc67f0614cbc48ba0cde803d3f423f2e8c614b))
* Only create webDAV links for original Files ([`279d31d`](https://github.com/projectcaluma/alexandria/commit/279d31d4e773283fd5fd76773a65d6c8f192a891))
* Run hooks after file save was successful ([`6d12b7a`](https://github.com/projectcaluma/alexandria/commit/6d12b7ac7eaa6e4ce82bf52803a5b92d179e0014))

# 3.0.0-beta.14
### Feature
* Integrate manabi for editing files over WebDAV ([`7e0ec86`](https://github.com/projectcaluma/alexandria/commit/7e0ec86291606945302734579e0868f05cbf73bf))

# 3.0.0-beta.13
### Fix
* **convert:** Copy over metainfo ([#468](https://github.com/projectcaluma/alexandria/issues/468)) ([`4d0b7c0`](https://github.com/projectcaluma/alexandria/commit/4d0b7c0f995e2065443fdd6fc2a9328cd97fd20b))

# 3.0.0-beta.12
### Feature
* Add optional dms integration ([`38ecbec`](https://github.com/projectcaluma/alexandria/commit/38ecbec4e2c5cb088be4a74abd81b3cadbeb1ea5))

### Fix
* **dms:** Return json document after conversion ([`357bae9`](https://github.com/projectcaluma/alexandria/commit/357bae96e433a128622edcc0bc6754d5520d3c81))
* **dms:** Improve dms integreation ([`4bbf1c3`](https://github.com/projectcaluma/alexandria/commit/4bbf1c3aaec78a48138400cf3cf252defd6e61ec))

# 3.0.0-beta.11
### Feature
* **security:** Add ClamAV integration ([`fe314ca`](https://github.com/projectcaluma/alexandria/commit/fe314ca80433de1c866c40fa8673cbb7eee90a80))

# 3.0.0-beta.10
### Feature
* **file:** Add method to generate a download url for a file ([`d28664e`](https://github.com/projectcaluma/alexandria/commit/d28664e82ed0253ca3cffad6a8d6d53af95e89a2))

# 3.0.0-beta.9
### Fix
* **document:** Fix clone method on document ([`fbac20b`](https://github.com/projectcaluma/alexandria/commit/fbac20b5c86bc97ae3f8b74da071f27f3e0612ea))

# 3.0.0-beta.8
### Feature
* **file:** Add mime type and size on file model ([`026f30d`](https://github.com/projectcaluma/alexandria/commit/026f30d47f2726d7c1314745755c019d3a93b6b0))

# 3.0.0-beta.7
### Feature
* **storage:** Don't use django default storage configuration ([`1c124fd`](https://github.com/projectcaluma/alexandria/commit/1c124fdc31cdc936beed2b553d7c06558b7a7180))

### Breaking
* Instead of overwriting `DEFAULT_FILE_STORAGE` in the host app, Alexandria now uses a separate setting `ALEXANDRIA_FILE_STORAGE` to configure the used file storage backend. ([`1c124fd`](https://github.com/projectcaluma/alexandria/commit/1c124fdc31cdc936beed2b553d7c06558b7a7180))

# 3.0.0-beta.6
### Fix
* Remove dry from encryption command ([`a3a7238`](https://github.com/projectcaluma/alexandria/commit/a3a72389450c547acaf6888055242fb8abf23fda))
* Minor cleanups, disable encryption in local setup ([`033da5e`](https://github.com/projectcaluma/alexandria/commit/033da5e2edf2033124b597850784abb085caf947))
* **model:** Max length of file field ([`7d4b0c9`](https://github.com/projectcaluma/alexandria/commit/7d4b0c9061276a03ba3d08019ab212eb95334fe3))

# 3.0.0-beta.5
### Fix
* **tests:** Fix broken tests ([#415](https://github.com/projectcaluma/alexandria/issues/415)) ([`0bd0cab`](https://github.com/projectcaluma/alexandria/commit/0bd0cab60b1733fd5479affb8dc7ecdec57524ac))
* **file:** Add missing create permission check ([#427](https://github.com/projectcaluma/alexandria/issues/427)) ([`34a57c1`](https://github.com/projectcaluma/alexandria/commit/34a57c1001be5d574676d77d5dab22ab7338db99))
* Remove modified at update for file creation ([#425](https://github.com/projectcaluma/alexandria/issues/425)) ([`86cfbf2`](https://github.com/projectcaluma/alexandria/commit/86cfbf2245f54e2126cc51329110a744a2752a4d))

# 3.0.0-beta.4
### Fix
* Fix factory import ([#424](https://github.com/projectcaluma/alexandria/issues/424)) ([`c9e4165`](https://github.com/projectcaluma/alexandria/commit/c9e4165020c25511cea1209a66037448e51defa6))

# 3.0.0-beta.3
### Feature
* **storage:** use Django's storage backend for object storage
* Add command to encrypt existing files ([`ac4a910`](https://github.com/projectcaluma/alexandria/commit/ac4a91022d011385931b37f8f6798cf2c8bf60bc))
* **files:** Add signed download_url to file ([`922f55a`](https://github.com/projectcaluma/alexandria/commit/922f55a67299aa42a94ef539ac0949ba375901b6))

### Fix
* **document:** Adjust cloning for use with storage backends ([`26c4331`](https://github.com/projectcaluma/alexandria/commit/26c4331648945772ad697bbce8b3a6140c5de43a))

# 3.0.0-beta.2
### Feature
* **document:** Update modfied data when creating new file ([`0b9dd76`](https://github.com/projectcaluma/alexandria/commit/0b9dd76be012cb71ce25a634cd4d004968d7a152))

# 3.0.0-beta.1
### Feature
* Change tag primariy key to uuid ([`0284115`](https://github.com/projectcaluma/alexandria/commit/0284115171214b92fc206ecdb1a81e0421b4d383))
* Use dgap instead of custom visibilities and permissions ([#289](https://github.com/projectcaluma/alexandria/issues/289)) ([`2a92203`](https://github.com/projectcaluma/alexandria/commit/2a92203ed90f1858f6ba5af6c13a22a0014d0ba4))

### Fix
* Regression in modified_by_user ([`ed70dd0`](https://github.com/projectcaluma/alexandria/commit/ed70dd0d5a5391fe14c89d1116326da784d695d9))
* Set default created by user ([`f8aafd7`](https://github.com/projectcaluma/alexandria/commit/f8aafd7e7777aa8ea5f970159e4ac0d82ae9d5ee))

### Breaking
* this changes the primariy key for Tag to uuid the tag filter now also filters by the new uuid ([`0284115`](https://github.com/projectcaluma/alexandria/commit/0284115171214b92fc206ecdb1a81e0421b4d383))
* This removes the custom permission system for DGAP. ([`2a92203`](https://github.com/projectcaluma/alexandria/commit/2a92203ed90f1858f6ba5af6c13a22a0014d0ba4))

# 2.9.1
### Fix
* Dont overwrite created by ([`7923265`](https://github.com/projectcaluma/alexandria/commit/792326593b0bffc161417706853c4c97f91819ca))

# 2.9.0
### Feature
* **document:** Add a method to clone documents ([`ebefcbd`](https://github.com/projectcaluma/alexandria/commit/ebefcbd0cb9af6ae251d69e5527d1b185c03c280))

### Fix
* **filter:** Change to iexact for name search ([`282ed95`](https://github.com/projectcaluma/alexandria/commit/282ed9500b916f14e23d73f5ec4045a1d945d5ce))

# 2.8.0
This release accidentially contained a breaking change, please don't use it!

# 2.7.0
### Feature
* **tags:** Add new filters, fix search ([`0962045`](https://github.com/projectcaluma/alexandria/commit/09620453e15ee04bf1eb97b41c689fde831d4a4d))
* Add mark model ([#382](https://github.com/projectcaluma/alexandria/issues/382)) ([`a9da2fd`](https://github.com/projectcaluma/alexandria/commit/a9da2fdc36d97d3d7d23b5d870c14b1fab0a4d83))

# v2.6.0
### Feature
* **file:** Write checksum of file in hook view ([`0011c81`](https://github.com/projectcaluma/alexandria/commit/0011c81afa499c29fccce7d79b8b3ec48c5bbf56))

# v2.5.1
### Fix
* **thumbs**: set content-type ([`bb77127`](https://github.com/projectcaluma/alexandria/commit/bb771277c0e72543a54100062be92d46e23448e9))

# v2.5.0
### Feature
* **thumbnails:** Upload thumbnails using upload url ([`aa03128`](https://github.com/projectcaluma/alexandria/commit/aa031285ae6e64adc6f5de6d14f9e8b850ab9d7b))

# v2.4.0
### Feature
* **document:** Add manual document date field ([`4a4fcbe`](https://github.com/projectcaluma/alexandria/commit/4a4fcbe5cfb09a5665f378ab4e7d7ad203655dad))

# v2.3.0
### Feature
* Return documents from child categories ([`b992a3f`](https://github.com/projectcaluma/alexandria/commit/b992a3f1cbc045e6a4bb8eb64c822b0cb3a462e9))
* **document:** Add categories filter ([#351](https://github.com/projectcaluma/alexandria/issues/351)) ([`a9cb293`](https://github.com/projectcaluma/alexandria/commit/a9cb293ae5211eae8688e8b15305be011bbd4a74))

### Fix
* **zip:** Append number to duplicate file names ([#337](https://github.com/projectcaluma/alexandria/issues/337)) ([`8f09c5f`](https://github.com/projectcaluma/alexandria/commit/8f09c5f0c304764a8a71afa451cbe2e9fa76d5fe))

# v2.2.1
### Fix
* **settings:** Fix wrong types of boolean settings ([`80e2564`](https://github.com/projectcaluma/alexandria/commit/80e2564ab10327f8e7339bea325c6b4cb2dffb8c))

# v2.2.0
### Feature
* **category:** Add slug filters for category list ([`23f7d7e`](https://github.com/projectcaluma/alexandria/commit/23f7d7e0bed21953e003d2ec33a1348ff2050525))

# v2.1.0
### Feature
* **category:** Add has_parent filter for categories ([`1ba5aa8`](https://github.com/projectcaluma/alexandria/commit/1ba5aa83f4d8545ca923a82b8464e0ee6e6fb42f))
* **category:** Allow nesting of categories ([`9b38fc7`](https://github.com/projectcaluma/alexandria/commit/9b38fc746a68f9de4f0c94d16d6aca91e8dcd1c5))
* Generate thumbnails without s3 hooks ([`a96a917`](https://github.com/projectcaluma/alexandria/commit/a96a917610a380ab0b89913346a31f339f099907))

### Fix
* Add validation if a thumbnail was generated ([`665fb50`](https://github.com/projectcaluma/alexandria/commit/665fb508b7fd8607a6ff67be4fc1848f402ba5ce))
* Remove redundant thumbnail option ([`9788962`](https://github.com/projectcaluma/alexandria/commit/9788962d3eaff84969c15e570a11c5468c619ed4))

# v2.0.1
### Fix
* **settings:** Remove import in settings init file ([`3a86060`](https://github.com/projectcaluma/alexandria/commit/3a8606069ef257b8d8fa08d12e0cc46ab3d2e05c))

# v2.0.0
### Fix
* **docker:** Remove obsolete system dependencies ([`2e2f8a2`](https://github.com/projectcaluma/alexandria/commit/2e2f8a2081aa0603157d7df41e0981ac4824def4))
* **settings:** Prefix alexandria settings ([`5791f3d`](https://github.com/projectcaluma/alexandria/commit/5791f3d8fbb7cf4a9fa37917ac2b1ac2a1b71ce2))

### Breaking
* Removed image previews for RAW, VTK and scribus files. ([`2e2f8a2`](https://github.com/projectcaluma/alexandria/commit/2e2f8a2081aa0603157d7df41e0981ac4824def4))
* All alexandria specific settings and environment variables have been renamed to include a prefix in order to avoid conflicts when using alexandria as a django app instead of a container. ([`5791f3d`](https://github.com/projectcaluma/alexandria/commit/5791f3d8fbb7cf4a9fa37917ac2b1ac2a1b71ce2))
The following breaking changes in settings and environment variables have been made:

  * `ALLOW_ANONYMOUS_WRITE` was renamed to `ALEXANDRIA_ALLOW_ANONYMOUS_WRITE`
  * `DEV_AUTH_BACKEND` was renamed to `ALEXANDRIA_DEV_AUTH_BACKEND`
  * `ENABLE_THUMBNAIL_GENERATION` was renamed to `ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION`
  * `MEDIA_STORAGE_SERVICE` was renamed to `ALEXANDRIA_MEDIA_STORAGE_SERVICE`
  * `MINIO_PRESIGNED_TTL_MINUTES` was renamed to `ALEXANDRIA_MINIO_PRESIGNED_TTL_MINUTES`
  * `MINIO_STORAGE_ACCESS_KEY` was renamed to `ALEXANDRIA_MINIO_STORAGE_ACCESS_KEY`
  * `MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET` was renamed to `ALEXANDRIA_MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET`
  * `MINIO_STORAGE_ENDPOINT` was renamed to `ALEXANDRIA_MINIO_STORAGE_ENDPOINT`
  * `MINIO_STORAGE_MEDIA_BUCKET_NAME` was renamed to `ALEXANDRIA_MINIO_STORAGE_MEDIA_BUCKET_NAME`
  * `MINIO_STORAGE_SECRET_KEY` was renamed to `ALEXANDRIA_MINIO_STORAGE_SECRET_KEY`
  * `MINIO_STORAGE_USE_HTTPS` was renamed to `ALEXANDRIA_MINIO_STORAGE_USE_HTTPS`
  * `THUMBNAIL_HEIGHT` was renamed to `ALEXANDRIA_THUMBNAIL_HEIGHT`
  * `THUMBNAIL_WIDTH` was renamed to `ALEXANDRIA_THUMBNAIL_WIDTH`
  * `PERMISSION_CLASSES` has been removed in favor of already existing `ALEXANDRIA_PERMISSION_CLASSES`
  * `VALIDATION_CLASSES` has been removed in favor of already existing `ALEXANDRIA_VALIDATION_CLASSES`
  * `VISIBILITY_CLASSES` has been removed in favor of already existing `ALEXANDRIA_VISIBILITY_CLASSES`

# v1.2.0
### Feature
* Make properties for created_by configurable ([`c18dc06`](https://github.com/projectcaluma/alexandria/commit/c18dc06224fd8bf25090fc64906ac058aac8024f))
* Let the oidc user model be configurable ([`74c673a`](https://github.com/projectcaluma/alexandria/commit/74c673aff740b2c495f36ed4ca67468f8fd140e3))

### Fix
* Extract serializer permissions ([`775f2b7`](https://github.com/projectcaluma/alexandria/commit/775f2b7f56fd822e644fea04bf96a6857e8c9609))
* Use correct minio error ([`86ef544`](https://github.com/projectcaluma/alexandria/commit/86ef5442f2cfb3d9a094a26f071a38e258ff6a4e))
# v1.1.2
### Fix
* Visibility config default ([`1275d26`](https://github.com/projectcaluma/alexandria/commit/1275d26b192818d5603bd43a91207943f4dad377))

# v1.1.1 (broken, don't use!)
### Fix
* Make deprecated VISIBILITY_CLASSES env var optional ([`20f4553`](https://github.com/projectcaluma/alexandria/commit/20f45538e4bc4ce789fa65b522cfdd45f2a587c3))

# v1.1.0
### Feature
* Prefix config keys ([`e48dae9`](https://github.com/projectcaluma/alexandria/commit/e48dae92fd5ffbb5cda110bad057c155b1f5e53d))

### Fix
* Add missing migration ([`35fbb1e`](https://github.com/projectcaluma/alexandria/commit/35fbb1ede287bf0e249c390cddcfcb53b5a40abd))

# v1.0.0
### Feature
* Add pypi deployment worklow ([`8c341cc`](https://github.com/projectcaluma/alexandria/commit/8c341ccf0a293d6def06abae82347a1a9a6aef98))
* Split settings for packaging ([`7827984`](https://github.com/projectcaluma/alexandria/commit/7827984391cccac3440e8e54c01a414692910f9b))

### Fix
* Use caluma-alexandria as package name ([`9baec0d`](https://github.com/projectcaluma/alexandria/commit/9baec0dfc88abf65c19dd4f659d06e7a48f1ec12))
* Relax version ranges ([`25fbb68`](https://github.com/projectcaluma/alexandria/commit/25fbb6833f6bebdf24fe526ea745a7d010a5ac3b))
* Fix jsonfilter ([`551d1e2`](https://github.com/projectcaluma/alexandria/commit/551d1e2fdd3d5245df0ae3b98a4a787b0b708853))
* Rename fields to metainfo and variant ([`4bfb7ed`](https://github.com/projectcaluma/alexandria/commit/4bfb7ed4aa149df0cdde70fe55c1f48f23687711))
* Upgrade dependencies ([`2eacf22`](https://github.com/projectcaluma/alexandria/commit/2eacf221610e648bcd3cd82a3833a674fc1e8f00))
* Fix default auth backend settings ([`18ef3d9`](https://github.com/projectcaluma/alexandria/commit/18ef3d94dcd52c8021aa38faba97df550e8319b2))

### Breaking
* renames meta to metainfo, type to variant ([`4bfb7ed`](https://github.com/projectcaluma/alexandria/commit/4bfb7ed4aa149df0cdde70fe55c1f48f23687711))
* drops django 2.2 ([`2eacf22`](https://github.com/projectcaluma/alexandria/commit/2eacf221610e648bcd3cd82a3833a674fc1e8f00))

# v0.3.0
### Feature
* Make authentication backend configurable ([`23ebe28`](https://github.com/projectcaluma/alexandria/commit/23ebe28fda16b9f8133100554d03b0ca1541b643))
* Add documents filtering with tag synonyms ([`3b68a74`](https://github.com/projectcaluma/alexandria/commit/3b68a7400b9eb31b99af592534c8e965afe1d76c))
* Add upload_status field to file models to track upload status ([`ea6cf87`](https://github.com/projectcaluma/alexandria/commit/ea6cf87eb31570ad1a8d0ec1fa7f3bc3d285ef51))

### Fix
* **Dockerfile:** Use poetry to run uwsgi ([`72fe409`](https://github.com/projectcaluma/alexandria/commit/72fe4091211cc1ead70033980be9977c08034fed))
* Make psycopg2 a regular dependency ([`301baf5`](https://github.com/projectcaluma/alexandria/commit/301baf569f297b6db434664852f8c9f012a48915))
* **deps:** Move psycopg2-binary to dependencies ([`6d6e4e7`](https://github.com/projectcaluma/alexandria/commit/6d6e4e7411320ccf4814a7f1ed0f2fc2be778ea6))

# v0.2.2

### Fix
* **thumbnail:** Use temporary directory instead of THUMBNAIL_CACHE_DIR ([`bb6aee4`](https://github.com/projectcaluma/alexandria/commit/bb6aee4ce388bd9de1bc13efdaba7893b72e9be7))
* **core:** Delete unused tags ([`69dab65`](https://github.com/projectcaluma/alexandria/commit/69dab6523bff4ff8233afe5fac3faf410ac90059))


# v0.2.1

### Fix
* Add the document_meta filter ([`6921558`](https://github.com/projectcaluma/alexandria/commit/692155820033dfd8737ad2f53305658b2de5475f))
* Extend uwsgi buffer ([`e2863e9`](https://github.com/projectcaluma/alexandria/commit/e2863e9b3eff2f7d485531a1ea32d24f262812c5))

### Feature
* Add endpoint for downloading multiple files as zip ([`bc15973`](https://github.com/projectcaluma/alexandria/commit/bc15973957e33ffce5a81a717b25a6e224cf1cc9))
* Support more formats ([`4d5a656`](https://github.com/projectcaluma/alexandria/commit/4d5a656c2741750b489086738eb240f2fc57c7c0))

### Fix
* **docs:** Add hint about UID in .env to README ([`1506ea0`](https://github.com/projectcaluma/alexandria/commit/1506ea0256a9fd37435273f2974250ded9c218f6))
* Use debug auth backend by default ([`b47a7f0`](https://github.com/projectcaluma/alexandria/commit/b47a7f09038f574c53771b4798caf7b0cf6d1d77))
* **ci:** Use correct claims for username ([`a1a2f0a`](https://github.com/projectcaluma/alexandria/commit/a1a2f0a246feb89d80ac1bfb677f903b3bc3ad35))


# v0.1.0

This is the first initial release. Things are still changing around here...

### Feature
* Custom validations ([`a969e06`](https://github.com/winged/alexandria/commit/a969e06cc87efba06feec06b29bca05b544bde4a))
* Search document description as well ([`a549e71`](https://github.com/winged/alexandria/commit/a549e718534ecd3b376fa59af3f0f5f7f7f3ae0e))
* **dev:** Fake auth backend ([`656e342`](https://github.com/winged/alexandria/commit/656e342702654c20061d8c0a9dd231746b4a2123))
* With_documents_meta filter for tags ([`5b94ea2`](https://github.com/winged/alexandria/commit/5b94ea2fbcb5d82da9336d37bf69b270f6aefe91))
* Make tag name monolingual ([`c00b831`](https://github.com/winged/alexandria/commit/c00b83126bcbadb186166daaaacaea94a2b10a08))
* **validation:** Validate created_by_group ([`ffb2ecf`](https://github.com/winged/alexandria/commit/ffb2ecf343310e0321c3095997f2983422d9fca3))
* **filters:** New active_group filter ([`795970b`](https://github.com/winged/alexandria/commit/795970bf5fd41898734c585c09e08dba6383ac18))
* **example data:** Add a command to load example data ([`57daf08`](https://github.com/winged/alexandria/commit/57daf088ceedd48c9315e5de88f86a3f396fbd1f))
* **permissions:** Authenticated user checks ([`ca6acd0`](https://github.com/winged/alexandria/commit/ca6acd02d2ed738cdac01b9e8334892a57c76b04))
* **tags:** Add with-documents-in-category filter ([`5c8aab1`](https://github.com/winged/alexandria/commit/5c8aab1422ccb5702577ddfd391d4111735f8e1a))
* **document:** Add search filter ([`02f768b`](https://github.com/winged/alexandria/commit/02f768b271691887760dfe799194fd41478369bd))
* **document:** Add filters for category and tags ([`66714ba`](https://github.com/winged/alexandria/commit/66714bab67b62eabd5ded3d8fc7c391383180366))
* **category:** Add color field ([`24e8d0f`](https://github.com/winged/alexandria/commit/24e8d0f52ed70fcfd496a7e96b1c56c265305e09))
* **thumbnails:** Implement generation of thumbnails ([`fdc4562`](https://github.com/winged/alexandria/commit/fdc4562b036c21d5a4566b210fcc03cc122827d7))
* **permissions:** Add permission layer ([`67f3cd1`](https://github.com/winged/alexandria/commit/67f3cd1957527b56842937d654ab318cf957a75f))
* **visibility:** Add visibilities ([`a30a7f7`](https://github.com/winged/alexandria/commit/a30a7f74b9815877d9e91a9c6dc9745dfc61c748))
* **filter:** Add meta filter ([`aa5322d`](https://github.com/winged/alexandria/commit/aa5322d42077cb6e12efa0ede905273928033c5d))
* **files:** Add file models and api ([`6a7622c`](https://github.com/winged/alexandria/commit/6a7622c509eb897ebafcb149095fdcd2dab151d2))
* **models:** Add modified_{by,at} fields ([`74b9ee1`](https://github.com/winged/alexandria/commit/74b9ee12abacad72cc82aa3e12613175157862e9))
* **auth:** Add oidc authentication ([`76b99fe`](https://github.com/winged/alexandria/commit/76b99fe022172afb9c38640ea57f2021e1397697))
* Initial models and api ([`5527540`](https://github.com/winged/alexandria/commit/5527540f58b0085c6e69b7c4bcca32839216db8d))

### Fix
* **filters:** Allow json value filter to do indirect lookups ([`617b3c0`](https://github.com/winged/alexandria/commit/617b3c0fe68514caecaf4d5fc678a4774c84c52b))
* **json filter:** Be more tolerant ([`e3c13a0`](https://github.com/winged/alexandria/commit/e3c13a0672beeee0307e06a9dcbd31867c19ed0c))
* Deduplicate tags ([`7c42bde`](https://github.com/winged/alexandria/commit/7c42bde413e495f1808052ec6af83046d3193098))
* Correctly handle created_by_group, updated_by_group ([`588ef7a`](https://github.com/winged/alexandria/commit/588ef7ae1f4d341603e0905052edcd73c8548d30))
* **filters:** Tag filter should accept multiple values ([`97f48cb`](https://github.com/winged/alexandria/commit/97f48cb62f7d4d253e3a1278d74ac8fd36cdf6a1))
* **validation:** Correctly set created-by-(user/group) ([`5a3551d`](https://github.com/winged/alexandria/commit/5a3551deb0ffcaa5fdc9a8c99d0b50d0558edf5c))
* **slug models:** Make creation of slug models work correctly ([`60cddcb`](https://github.com/winged/alexandria/commit/60cddcb90310ddd21b08301f5af3be203a60086a))
* Categories are read-only on the API ([`6da613b`](https://github.com/winged/alexandria/commit/6da613bab8839d40f59388b6d2ccdb54c56360dc))
* Add app label ([`eef26cf`](https://github.com/winged/alexandria/commit/eef26cf62739b7f933d8bf34e88899e4a63e3400))

### Documentation
* **rfc:** Add original rfc ([`a148b69`](https://github.com/winged/alexandria/commit/a148b6955e138d1b22e601cff53c4fa8e04a9ecd))
