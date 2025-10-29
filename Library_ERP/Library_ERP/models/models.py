from odoo import fields,models,api

class author(models.Model):
    _name= "library.author"
    _description= "This is author profile."

    author_name= fields.Char("Author Name")

    booktoauthor_ids = fields.One2many("library.book","author_id")

    books_count = fields.Integer(
        string="Total_Books",
        compute="_compute_books_count",
        store=True,
    )

    @api.depends("booktoauthor_ids")
    def _compute_books_count(self):
        for y in self:
            author.books_count = len(y.booktoauthor_ids)




class borrow(models.Model):
    _name = "library.borrow"
    _description = "This is borrow profile."

    user_name = fields.Char("User Name")
    booktoborrow_ids = fields.One2many("library.book", "borrow_id")
    borrow_date= fields.Datetime("Borrow Date")
    return_date= fields.Datetime("Return Date")



class book(models.Model):
    _name= "library.book"
    _description= "This is book profile."

    book_id= fields.Integer("Book Id")
    book_name= fields.Char("Book Name")
    publish_date= fields.Datetime("Publish Date")
    genre= fields.Char("Genre")
    author_id= fields.Many2one("library.author" )
    borrow_id= fields.Many2one("library.borrow")

    @api.constrains("publish_date")
    def _check_publish_date(self):
        for x in self:
            if x.publish_date:
                if x.publish_date > fields.Datetime.now():
                    raise ValidationError("This field can't be future..!")


