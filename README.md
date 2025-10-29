# Library Management System (Odoo module)

A lightweight Library Management System module for Odoo that adds Book, Author and Purchase management.  
Designed for demonstration and small library workflows: add books and authors, record purchases, validate data and compute author statistics.

Table of contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Technical details](#technical-details)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Authors / Contact](#authors--contact)

## Overview
This module provides three top-level menus in Odoo:
- Books — list & form views with fields such as title (Char), isbn (Char), pages (Integer), publish_date (Date), authors (Many2many), publisher (Many2one), copies (Integer) etc.
- Authors — list & form views with fields such as name (Char), biography (Text), books (One2many) and a computed field that displays the total number of books for the author.
- Purchases — record when new books are purchased with relations to the Book model (Many2one/One2many), purchase_date (Date), quantity (Integer) and vendor (Many2one).

Validation is applied so that a book's publish date cannot be in the future. Each author has a computed and (optionally) stored field counting how many books are linked to that author.

## Features
- Models: Book, Author, Purchase
- Views: list/tree, form, search where applicable
- Field types used: Char, Text, Integer, Date, Many2one, One2many, Many2many, Selection
- Business rule: publish_date cannot be a future date (constraint)
- Computed field: author.book_count (calculates total number of books authored)
- Simple access rules (add ir.model.access.csv if adding new models)
- Basic UI and menu structure suitable for quick demos

## Installation
1. Copy the module folder (for example `library_management/`) to your Odoo addons path.
2. Update your Odoo server addons path to include the directory (or place the module in an existing addons folder).
3. Restart Odoo.
4. Update apps list and install the module from the Odoo Apps interface.

Or from command line:
- Place the module in a directory included in `--addons-path`
- Restart Odoo and run:
  - Install via web UI, or
  - Install from command line:
    odoo-bin -d <db_name> -i library_management --stop-after-init

If you use the provided Makefile:
- Initialise environment:
  make init
- Run the server:
  make run
- Upgrade (reinstall/update) your module after changes:
  make upgrade MODULE=library_management

## Configuration
Typical minimal `odoo.conf` snippet for development:
```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/your/addons
db_host = False
db_port = False
db_user = odoo
db_password = False
log_level = info
```

Adjust paths and DB settings to your environment.

## Usage
- Books menu:
  - Create a new book: fill title, ISBN, publish date, authors, number of pages and number of copies.
  - Publish date validation: you will get an error if you set a publish date in the future.
- Authors menu:
  - Create an author and link books (or link from the Book form).
  - The `Total books` computed column shows how many books are linked to the author.
- Purchases:
  - Create a purchase record for arriving stock, select book and quantity.

Example: Create Author "Jane Doe", create Book "Odoo for Libraries" with publish_date = 2024-06-10 and link the author. The author's `book_count` will show 1.

## Technical details
- Model names (example):
  - library.book (model: `library.book`)
  - library.author (model: `library.author`)
  - library.purchase (model: `library.purchase`)
- Constraint example (publish_date not future):
  - Implemented using @api.constrains('publish_date') and raising ValidationError when publish_date > fields.Date.context_today(self)
- Computed field example:
  - `book_count = fields.Integer(string='Total books', compute='_compute_book_count', store=True)`  
  - `_compute_book_count` implementation counts related books and stores result (consider recompute triggers on relation changes)
- Views:
  - Use XML view inheritance (form/tree/search) and sensible xpaths to avoid replacing core templates.
- Security:
  - Add an `ir.model.access.csv` row for each new model and adjust record rules if needed.

## Development
- Recommended workflow
  1. Create a virtualenv and install dependencies (see requirements.txt).
  2. Use the included Makefile to simplify common tasks:
     - make init — create venv and install deps
     - make run — start Odoo with `odoo.conf`
     - make upgrade MODULE=library_management — upgrade the module on your dev DB
     - make test MODULE=library_management — run module tests
     - make fmt / make lint — format and lint code (if tools installed)
  3. When changing computed/constraint logic, add unit tests that cover edge cases (publish_date future, recompute of book_count on add/remove).

- Tips:
  - Use `@api.model_create_multi` for bulk create where appropriate.
  - Preserve method signatures and call `super()` when extending existing behavior.
  - For JS changes, add assets in the module manifest under `assets` (Odoo 14+ style) or `qweb`/`web.assets_backend` as needed.
  - Keep XML changes minimal using xpath to help future upgrades.

## Testing
- Add tests under `tests/` using Odoo's test framework (`unittest` style with `TransactionCase` or `HttpCase`).
- Run tests via the command shown in Development:
  make test MODULE=library_management

Example test cases to include:
- Creating a book with a future publish_date raises ValidationError.
- Creating author and associating books updates `book_count` as expected.
- Creating purchase increases stock / purchase-related behavior (if implemented).

## Contributing
Contributions are welcome. Please open an issue describing the change you propose or submit a pull request with:
- Clear description of the change
- Unit tests for new behavior or bug fixes
- Updated documentation if behavior or API changes

When submitting code:
- Follow code style (PEP8), format with black where applicable.
- Add/adjust `ir.model.access.csv` if you add new models or change access.

## License
Specify your license here, e.g.:
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Authors / Contact
- Author: Your Name (replace with your name)
- GitHub: shahadat-rizon
- Module maintained by: shahadat-rizon
