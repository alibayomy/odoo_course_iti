import re
from odoo import fields, models, api
from odoo.exceptions import  UserError, ValidationError
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    """Patient class represents patient details
    """
    _name = "hms.patient"
    _description = "Patient"
    _rec_name = 'f_name'

    f_name = fields.Char("First Name", required="true")
    l_name = fields.Char("Last Name", required="true")
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")
    cr_ratio = fields.Float("CR Ratio", required=True)
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
    age = fields.Integer(compute='calculate_age')
    department_id = fields.Many2one('hms.department')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ])
    doctor_ids = fields.Many2many('hms.doctor')
    line_ids = fields.One2many('hms.patient.line', 'patient_id')
    email = fields.Char(required=True)

    def action_add_log(self):
        """search for the add log action in my app
            return: the matched app + patient_id"""
        action = self.env['ir.actions.actions']._for_xml_id('hms_app.log_wizard_action')
        action['context'] = {
            'default_patient_id': self.id,
        }
        return action

    @api.onchange('age')
    def _onchange_pcr(self):
        """Set the pcr automatically if the is
        lower than 30 """
        for rec in self:
            if rec.age < 30:
                rec.pcr = True
                return {
                    'warning': {'title':"hello",}
                }
            else:
                rec.pcr = False

    def action_undetermined(self):
        for rec in self:
            rec.state = 'undetermined'

    def action_good(self):
        for rec in self:
            rec.state = 'good'

    def action_fair(self):
        for rec in self:
            rec.state = 'fair'

    def action_serious(self):
        for rec in self:
            rec.state = 'serious'

    def write(self, vals):
        if 'state' in vals:
            for patient in self:
                new_log = {
                    'patient_id': patient.id,
                    'description': f"State changed from {patient.state} to {vals['state']}"
                }
                patient.env['hms.patient.line'].create(new_log)
        return super().write(vals)
    @api.constrains('email')
    def _check_email_vali(self):
        for rec in self:
            patient = self.env['hms.patient'].search([('email', '=', rec.email),('id', '!=', rec.id)])
            if not re.match('(\w+[.|\w])@(\w+[.])\w+', self.email):
                raise UserError("Email not valid.")
            if patient:
                raise UserError("Email already exist.")

    @api.depends('age')
    def calculate_age(self):
        """calculate the age of the patient"""
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years


class PatientLine(models.Model):
    """Showing log history as patient lines"""
    _name = 'hms.patient.line'
    _description = 'Patient Line'

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Char(default=lambda self: self.env.user.name)
    date = fields.Date(default=fields.Date.today)
    description = fields.Text('')

