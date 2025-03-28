from odoo import models, fields

STATES = [
    ('draft', 'New'),
    ('confirmed', 'Confirmed')
]

ALIAS_CONTACTS = [
    ('everyone', 'Everyone'),
    ('partners', 'Partners only'),
    ('followers', 'Followers only')
]

class BusinessTrip(models.Model):
    _name = "business.trip"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Business Trip"

    name = fields.Char(tracking=True)
    partner_id = fields.Many2one("res.partner", "Responsible", tracking=True)
    guest_ids = fields.Many2many("res.partner", "Participants")
    state = fields.Selection(STATES, tracking=True)

    expense_ids = fields.One2many('business.expense', 'trip_id', 'Expenses')
    alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict", required=True)
    alias_name = fields.Char()
    alias_domain = fields.Char(compute="_compute_alias_domain")
    alias_contact = fields.Selection(ALIAS_CONTACTS, default="everyone")

    def _compute_alias_domain(self):
        for record in self:
            record.alias_domain = self.env['ir.config_parameter'].sudo().get_param('mail.catchall.domain', '')

    def _track_subtype(self, initial_values):
        self.ensure_one()
        if 'state' in initial_values and self.state == 'confirmed':
            return self.env.ref('my_module.mt_state_change')
        return super()._track_subtype(initial_values)
    
    def action_cancel(self):
        self.write({
            'state': 'draft'
        })

    def _notify_get_groups(self, message, groups):
        groups = super()._notify_get_groups(message, groups)

        self.ensure_one()
        if self.state == 'confirmed':
            app_action = self._notify_get_action_link('method', method='action_cancel')
            trip_actions = [{'url': app_action, 'title': _('Cancel')}]
        
        new_group = (
            'group_trip_manager',
            lambda partner: any(
                user.sudo().has_group('base.group_user')
                for user in partner.user_ids
            ),
            {"actions": trip_actions}
        )

        return [new_group] + groups
    
    def _get_alias_model_name(self, vals):
        return "business.expense"
    
    def _get_alias_values(self):
        values = super()._get_alias_values()
        values["alias_defaults"] = {"trip_id": self.id}
        values["alias_contact"] = "followers"
        
        return values