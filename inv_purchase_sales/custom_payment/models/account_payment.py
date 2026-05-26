# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    maturity_date = fields.Date(
        string='Maturity Date',
        tracking=True,
        help='Due date used on payment journal items when set.',
    )

    @api.onchange('date')
    def _onchange_date_set_maturity_date(self):
        if not self.maturity_date:
            self.maturity_date = self.date

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        line_vals_list = super()._prepare_move_line_default_vals(
            write_off_line_vals=write_off_line_vals,
            force_balance=force_balance,
        )
        maturity = self.maturity_date or self.date
        for vals in line_vals_list:
            if 'date_maturity' in vals:
                vals['date_maturity'] = maturity
        return line_vals_list
