from odoo import api, fields, models

class MessageCheckBOWizard(models.TransientModel):
    _name = 'message.check.bo.wizard'
    _description = 'Message Check Booking Order Wizard'

    message = fields.Text(string='Message', stored=False)