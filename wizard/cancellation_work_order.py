from odoo import api, fields, models

class CancellationWorkOrderWizard(models.TransientModel):
    _name = 'cancellation.work.order.wizard'
    _description = 'Cancellation Work Order Wizard'

    notes = fields.Text(string='Reason')

    def action_cancel(self):
        self.env['sale.work.order'].browse(self.env.context['active_id']).update({'notes':self.notes, 'state':'cancelled'})