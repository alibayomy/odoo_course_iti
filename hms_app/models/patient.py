from odoo import fields, models


class Patient(models.Model):
    """Patient class represents patient details
    """
    _name = "hms.patient"
    _description = "Patient"
    _rec_name = 'f_name'

    f_name = fields.Char("First Name")
    l_name = fields.Char("Last Name")
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")
    cr_ratio = fields.Float("CR Ratio")
    blood_type = fields.Selection([
        ('o-', 'O-'),
        ('o+', 'O+'),
        ('a-', 'A-'),
        ('a+', 'A+'),
        ('b-', 'B-'),
        ('b+', 'B+'),
        ('ab-', 'AB-'),
        ('ab+', 'AB+')
    ])
    pcr = fields.Boolean(default=True, string='PCR')
    image = fields.Binary()
    address = fields.Text('Address')
    age = fields.Integer('Age')
    department_id = fields.Many2one('hms.department')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ])
    doctor_ids = fields.Many2many('hms.doctor')
