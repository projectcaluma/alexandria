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
