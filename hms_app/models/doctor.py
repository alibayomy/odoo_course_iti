from odoo import fields, models


class Doctor(models.Model):
    """Class representing a hosbital doctor with attr:
    * f_name: First name of the doctor
    * l_name: Last name of the doctor
    * image: the image of the doctor"""
    _name = 'hms.doctor'
    _description = 'Doctor'

    f_name = fields.Char('First Name')
    l_name = fields.Char('Last Name')
    image = fields.Binary()
    patient_ids = fields.Many2many('hms.patient')