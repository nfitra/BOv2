from odoo import _, api, fields, models, exceptions
from dateutil.relativedelta import relativedelta

class BookingOrder(models.Model):
    _inherit = 'sale.order'
        
    is_booking_order = fields.Boolean(string='Is Booking Order', readonly=True)
    
    service_team_id = fields.Many2one('service.team', string='Service Team')

    team_leader_id = fields.Many2one('res.users', string='Service Team Leader')
    team_member_ids = fields.Many2many('res.users', string='Service Members')
    
    @api.onchange('service_team_id')
    def onchange_team_id(self):
        for record in self:
            record.team_leader_id = record.service_team_id.team_leader_id
            record.team_member_ids = record.service_team_id.team_member_ids
    
    booking_start = fields.Datetime(string='Booking Start', default=fields.datetime.now())
    booking_end = fields.Datetime(string='Booking End', default=fields.datetime.now() + relativedelta(days=1))
    
    @api.onchange('booking_start')
    def onchange_booking_start(self):
        for record in self:
            record.booking_end = record.booking_start + relativedelta(days=1)

    @api.onchange('booking_end')
    def onchange_booking_end(self):
        for record in self:
            record.booking_start = record.booking_end - relativedelta(days=1)

    def action_workorder(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.work.order",
            "domain": [('sale_order_id', '=', self.id)],
            "context": {"create": False},
            "name": "Work Order for %s" %self.name,
            'view_mode': 'tree,form',
        }

    def action_check(self):
        res = self.env['sale.work.order'].search([
                                                ('team_id.id','=', self.service_team_id.id),
                                                ('state','in',('pending','inprogress')),
                                                ('planned_start','<=',self.booking_end),
                                                ('planned_end','>=',self.booking_start),
                                                ])
        if res:
            message = "Team already has work order during that period on %s" %(res.sale_order_id.name or 'SO-NULL')
            
        else:
            message = "Team is available for booking"

        return {
            'name': ('Check Message'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'message.check.bo.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_message': message}
        }

    def action_confirm(self):
        res = self.env['sale.work.order'].search([
                                                ('team_id.id','=', self.service_team_id.id),
                                                ('state','in',('pending','inprogress')),
                                                ('planned_start','<=',self.booking_end),
                                                ('planned_end','>=',self.booking_start),
                                                ])
        if res:
            message = "Team is not available during this period, already booked on %s. Please book on another date." %(res.sale_order_id.name or 'SO-NULL')
            
            return {
                    'name': ('Check Message'),
                    'view_type': 'form', 
                    'view_mode': 'form',
                    'res_model': 'message.check.bo.wizard',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_message': message}
                    }
        
        else:
            vals = {
                'sale_order_id': self.id,
                'team_id': self.service_team_id.id,
                'team_leader_id': self.team_leader_id.id,
                'team_member_ids': self.team_member_ids
            }
            self.env['sale.work.order'].create(vals)
            return super(BookingOrder, self).action_confirm()