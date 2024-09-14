# CHANGELOG

## v0.2.0 (2024-09-14)

### Documentation

* docs: update license in CHANGELOG.md ([`ebb7f39`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/ebb7f3950cd8cf340e8d78e3e6ee0d2135f10023))

### Feature

* feat: implement catalog fetching from Vizier

- Add `fetch_catalog` function to retrieve catalogs from Vizier service.
- Implement `_UnsupportedServiceError` exception class for unsupported services.
- Add tests for successful retrieval from Vizier and error handling for unsupported services.

Closes #1 ([`19dbdad`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/19dbdada32defef0893a79be43408140dbe59438))

### Refactor

* refactor: refactor `fetch_catalog` function to `catalog_quest` ([`b752bc2`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/b752bc2c453154381cbc2bbbccec1c1b853cbeac))

### Unknown

* Merge pull request #8 from mirsazzathossain/dev

feat: implement catalog fetching from Vizier #1 ([`1b0f41e`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/1b0f41ef0f2129d65c31710b7386fc9fb66d4b0a))

## v0.1.0 (2024-09-14)

### Chore

* chore(release): update version to 0.1.0 ([`2fd7066`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/2fd7066b52c3d3d8248be042d420663c1024095b))

### Documentation

* docs: update license ([`6f67257`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/6f67257a4527d5882f5c1acf3482358e1a535021))

### Feature

* feat: Add bug report and feature request issue templates ([`81dfb9b`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/81dfb9bbd2568a8ac9ff7235d7163cf17fe32993))

### Refactor

* refactor: remove unused foo.py and test_foo.py files ([`0267301`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/026730149289a50c4e06115cd498dae059456b78))

* refactor: update build status badge URL in README.md ([`d3cfb5d`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/d3cfb5df6fa9fe75dcbff53e5dca9b7f6b659079))

* refactor: refactor build process in cd.yml workflow ([`7525ac5`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/7525ac595dff64d35a9cdb9d9b48e98ccf57981e))

## v0.0.0 (2024-09-14)

### Chore

* chore(release): update version to 0.0.0 ([`3859775`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/38597753b89c0b6b78c7b456deb0cc7728039c3e))

* chore: update pre-commit instructions in CONTRIBUTING.md

- Added instructions to run pre-commit checks manually
- Updated mkdocs.yml to fix indentation
- Removed unnecessary lines from LICENSE file
- Updated devcontainer.json to remove empty features object
- Added classifiers in pyproject.toml
- Added dev dependencies in pyproject.toml
- Updated semantic-release configuration in pyproject.toml ([`c739435`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/c7394356962540a91355550c5262552f4c2f1a77))

### Unknown

* Init commit ([`9f8a983`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/9f8a983680c581346f6c4822f8ee4b2123e86519))
