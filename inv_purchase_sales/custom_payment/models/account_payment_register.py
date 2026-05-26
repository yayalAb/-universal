# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    maturity_date = fields.Date(
        string='Maturity Date',
        help='Due date stored on the created payment.',
    )

    @api.onchange('payment_date')
    def _onchange_payment_date_set_maturity_date(self):
        if not self.maturity_date:
            self.maturity_date = self.payment_date

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        if self.maturity_date:
            payment_vals['maturity_date'] = self.maturity_date
        return payment_vals

    def _create_payment_vals_from_batch(self, batch_result):
        payment_vals = super()._create_payment_vals_from_batch(batch_result)
        if self.maturity_date:
            payment_vals['maturity_date'] = self.maturity_date
        return payment_vals
