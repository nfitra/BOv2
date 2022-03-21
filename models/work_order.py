from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta

class WorkOrder(models.Model):
    _name = 'sale.work.order'
    _description = 'Sale Work Order'

    name = fields.Char(string='WO Number', readonly=True, default='New', required=True, copy=False)
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Booking Order Ref', domain="[('is_booking_order','=',True)]")

    team_id = fields.Many2one(comodel_name='service.team', string='Service Team', required=True)
    team_leader_id = fields.Many2one(comodel_name='res.users', string='Service Team Leader', required=True)
    team_member_ids = fields.Many2many(comodel_name='res.users', string='Service Members', required=True)

    @api.onchange('team_id')
    def onchange_team_id(self):
        for record in self:
            record.team_leader_id = record.team_id.team_leader_id
            record.team_member_ids = record.team_id.team_member_ids

    planned_start = fields.Datetime(string='Planned Start', default=fields.datetime.now(), required=True)

    @api.onchange('planned_start')
    def onchange_planned_start(self):
        for record in self:
            record.planned_end = record.planned_start + relativedelta(days=1)

    planned_end = fields.Datetime(string='Planned End', default=fields.datetime.now() + relativedelta(days=1), required=True)

    @api.onchange('planned_end')
    def onchange_planned_end(self):
        for record in self:
            record.planned_start = record.planned_end - relativedelta(days=1)

    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection(string='Status', selection=[('pending', 'Pending'), ('inprogress', 'In Progress'), ('done', 'Done'), ('cancelled', 'Cancelled')], readonly=True, default='pending', required=True)
    notes = fields.Text(string='Notes')

    def action_start_work(self):
        for record in self:
            record.state = 'inprogress'
            record.date_start = fields.datetime.now()

    def action_end_work(self):
        for record in self:
            record.state = 'done'
            record.date_end = fields.datetime.now()

    def action_reset(self):
        for record in self:
            record.state = 'pending'
            record.date_start = None

    def popup_cancellation(self):
        return {
            'name': ('Add Reason'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cancellation.work.order.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    @api.model
    def create(self, vals):
        # if vals.get('name', 'New') == 'New':
        vals['name'] = self.env['ir.sequence'].next_by_code('sale.work.order') or 'New'
        return super(WorkOrder, self).create(vals)