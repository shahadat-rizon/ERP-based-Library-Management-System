# Library Management System (Odoo)

A simple Odoo module to manage Books, Authors and Purchases.

Features
- Models: Book, Author, Purchase
- Views: list and form (uses Char, Integer, Date, Many2one, One2many, Many2many)
- Validation: publish_date cannot be in the future
- Computed: author.book_count shows total books per author

Quick install
1. Copy module folder (e.g. `library_management/`) into your Odoo addons path.
2. Restart Odoo and update apps list.
3. Install the module from Apps (or run: `odoo-bin -d <db> -i library_management --stop-after-init`).

Common dev commands (Makefile)
- make init        # create venv and install deps
- make run         # start Odoo server
- make upgrade MODULE=library_management   # upgrade module after code changes

Notes
- Use `@api.constrains('publish_date')` to prevent future dates.
- Use a stored compute on author.book_count and trigger on relation changes.
- Add `ir.model.access.csv` entries for new models.

License & Author
- License: MIT (or choose your preferred license)
- Author: shahadat-rizon
