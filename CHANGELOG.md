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
