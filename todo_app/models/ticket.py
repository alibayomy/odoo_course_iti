from odoo import fields, models


class Ticket(models.Model):
    """ticket model has the following attributes:
    * `name`: name of the ticket
    * 'tag': tags included the ticket
    * 'state': the current state of the ticket
    * 'file': the file of the ticket
    * `description`: description of the ticket"""
    _name = 'todo.ticket'
    _description = 'Ticket'

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ])
    file = fields.Binary()
    description = fields.Text()

