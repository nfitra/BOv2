from odoo import api, fields, models


class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Service Team'

    name = fields.Char(string='Team Name', readonly=False, default=False, required=True)
    team_leader_id = fields.Many2one(comodel_name='res.users', string='Team Leader', readonly=False, default=False, required=False)
    team_member_ids = fields.Many2many(comodel_name='res.users', string='Team Members', readonly=False, default=False, required=False)

    
    
