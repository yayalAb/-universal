# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_employee_contact = fields.Boolean(
        string='Employee Contact',
        compute='_compute_is_employee_contact',
        store=True,
        index=True,
        help='Hidden from Customer and Vendor menus when set.',
    )

    @api.depends('employee', 'employee_ids')
    def _compute_is_employee_contact(self):
        for partner in self:
            partner.is_employee_contact = bool(
                partner.employee or partner.employee_ids
            )

    @api.model
    def _customer_vendor_section_domain(self):
        """Extra domain for customer / vendor sections and many2one lookups."""
        return [('is_employee_contact', '=', False)]

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        domain = list(domain or [])
        mode = self.env.context.get('res_partner_search_mode')
        if mode == 'customer':
            domain = expression.AND([
                domain,
                [('customer_rank', '>', 0)],
                self._customer_vendor_section_domain(),
            ])
        elif mode == 'supplier':
            domain = expression.AND([
                domain,
                [('supplier_rank', '>', 0)],
                self._customer_vendor_section_domain(),
            ])
        return super()._search(domain, offset=offset, limit=limit, order=order)
