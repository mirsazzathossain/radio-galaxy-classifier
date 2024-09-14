# CHANGELOG

## v0.6.0 (2024-09-14)

### Feature

* feat: Add Masking Functionality for Single and Batch Image Processing

- Implemented mask_image function to apply a mask to a single image.
- Added mask_image_bulk function to apply masks to all images in a directory.
- Included unit tests for both functions to verify correct functionality.
- Updated documentation for the new functions and exceptions. ([`f3c1c28`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/f3c1c28b5936e4cd1e30390e1dfecd2d741b1afa))

### Refactor

* refactor: update test_mask_image_bulk.py for improved readability and maintainability ([`76cc569`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/76cc569dac5bd3e0cb468ac81e52eaca554ffa29))

* refactor: update mask_image_bulk function for improved error handling and dimension checking ([`5fbda73`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/5fbda737d3f35e6b363e320dc5417da6bb88145a))

* refactor: Refactor test_mask_image_bulk.py for improved readability and maintainability ([`3772f59`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/3772f5998b073edd5cfcc69a67380f7e268f0a1c))

### Unknown

* Merge pull request #15 from mirsazzathossain/dev

feat: Add Masking Functionality for Single and Batch Image Processing ([`3cdff2d`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/3cdff2d76b9dd573b2e7cee95ca0cdf281f7effc))

* Create FUNDING.yml ([`35fd8ff`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/35fd8ffa83e89be1c6663f4a1f1bb4530115bdee))

* Update issue templates ([`d47bc41`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/d47bc4194f06bb8a0bf59f318830e642c68b8ceb))

## v0.5.0 (2024-09-14)

### Chore

* chore(release): update version to 0.5.0 ([`cc1b107`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/cc1b107213368a884cc5a44bd0caf973c6361ab0))

* chore(ci): update Python versions in CI workflow ([`c58aef9`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/c58aef9371e8837f0c17e0ea601c157f716c169b))

### Feature

* feat(utils): add functionality to convert FITS images to PNG

- Implemented `fits_to_png` function to convert a single FITS image to PNG.
- Implemented `fits_to_png_bulk` function to convert all FITS images in a directory to PNG.
- Handled normalization of pixel values between 0 and 255.
- Added `_FileNotFoundError` for handling missing FITS files.
- Included unittests for both `fits_to_png` and `fits_to_png_bulk`.
- Mocked external dependencies such as file reading and saving in tests. ([`f01229b`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/f01229bf5ecb06d0fd011c7796814f5938a54228))

### Refactor

* refactor: update test_fits_to_png_bulk.py to add test for None image ([`66714f2`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/66714f2e186f0e0c15df77f74ff679537780156a))

### Unknown

* Merge pull request #13 from mirsazzathossain/dev

feat(utils): add functionality to convert FITS images to PNG ([`c49aa05`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/c49aa056ed447d949c4eef9b64739c776dc3be59))

## v0.4.0 (2024-09-14)

### Chore

* chore(release): update version to 0.4.0 ([`cbeac5b`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/cbeac5b743a4aba09155a5192a8b6a812710dbb8))

* chore: Update build status badge URL in README.md and docs/index.md ([`ce88c2e`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/ce88c2e169ec227296c23593a61fcb0862b1c8af))

### Feature

* feat: Add celestial_tag function for generating names from catalog entries

- Modify the celestial_tag function to accept a pandas Series entry instead of a DataFrame entry.
- Update the function to generate a name tag for a celestial object based on its coordinates.
- Refactor the function to handle different coordinate formats and handle missing coordinates.
- Add unit tests for the celestial_tag function to ensure its correctness.

Fixes #123 ([`d4b7dcd`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/d4b7dcde2cb39e703056ef9c257a807095858f9b))

* feat: Add celestial_tag function for generating names from catalog entries

- Implemented `celestial_tag` function to generate names for astronomical objects based on catalog data (Issue #4).
- Handles different catalog formats including RA/Dec coordinates and filenames.
- Added custom exception `_NoValidCelestialCoordinatesError` for handling missing or invalid coordinates. ([`3131518`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/313151816534ae77e4fb1dec159542e13787e24d))

### Unknown

* Merge pull request #12 from mirsazzathossain/dev

feat: Add celestial_tag function for generating names from catalog entries ([`3aadc94`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/3aadc94d5a330680d97ab0e9e62eabe30b44e05d))

## v0.3.0 (2024-09-14)

### Build

* build: vpdate python version ([`228576b`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/228576b19d9ec3b61cbcebe4c365656329dd362b))

### Chore

* chore(release): update version to 0.3.0 ([`276517a`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/276517aa3ff869187dd26a94af107024f1e23da5))

* chore: Update pandas-stubs dependency to version 3.14.0 ([`4f71c30`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/4f71c302ab8bd3f63514acc54c7c4d7fd7395b1c))

* chore: Update pandas dependency to version 2.0.3 ([`cf2c81e`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/cf2c81ebe5536eafedd05c58a0ef5f035e2b91d4))

* chore: Update pandas dependency to pandas-stubs 2.0.2.230605 ([`8534477`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/85344774b9f2ce7e7a36bb63525d0cfa78f82074))

* chore: remove mypy configuration file and update pyproject.toml ([`a11bfaf`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/a11bfaf680f751431069251c109f856ebcabe778))

### Ci

* ci: Update python-version options in ci.yml ([`838f27c`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/838f27cf85b9aef31afbf3f485e9cc5289b0d994))

* ci: update default Python version to 3.11 in setup-python-env action.yml ([`4ee87b6`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/4ee87b65b5e8d650ea2d4b745c2602549e5c9578))

### Documentation

* docs: refactor module import in docs ([`42f3b65`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/42f3b65463a09147157363a626c25d0ca6466197))

* docs: update CHANGELOG.md ([`217fb5a`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/217fb5acf400880bf1a15a9d2ca7cb336fcd0ef5))

### Feature

* feat: Add celestial_capture function for downloading images from SkyView

- Implemented `celestial_capture` function to retrieve and save celestial images from the NASA SkyView Virtual Observatory using given sky coordinates.
- Supports various image surveys and includes error handling for invalid coordinates.
- Saves FITS images with cleaned header comments and ensures directory creation.

Closes #2 ([`39bccaa`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/39bccaaacb183aef9b4e049d5dc6c601cd816057))

### Refactor

* refactor: update data.py to use type hinting for catalog_quest return value ([`77ea8c4`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/77ea8c46cfb8a88a5608b937faba42b4c9f111cf))

### Test

* test: Add unit test for celestial_capture function ([`c04cf53`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/c04cf5357e5e06dddb822b00597fa1165f84f9df))

* test: Add mypy configuration file ([`c76f67f`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/c76f67f8769f7945f5bdea780957086312fb7fe7))

### Unknown

* Merge pull request #10 from mirsazzathossain/dev

feat: Add celestial_capture function for downloading images from SkyView ([`1496ccf`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/1496ccf3060dd0a4ddf8229a186db222b5d16117))

## v0.2.0 (2024-09-14)

### Chore

* chore(release): update version to 0.2.0 ([`1573da9`](https://github.com/mirsazzathossain/radio-galaxy-classifier/commit/1573da9e5b08326c5c62feb29403aa20382ac700))

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
