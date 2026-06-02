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
    def _search_skip_section_filter(self, domain):
        """Do not apply list filters when loading/opening a specific partner."""
        for leaf in domain:
            if isinstance(leaf, (list, tuple)) and len(leaf) >= 3 and leaf[0] == 'id':
                if leaf[1] in ('=', 'in'):
                    return True
        return False

    @api.model
    def _get_company_partner_ids(self):
        return self.env['res.company'].sudo().search([]).mapped('partner_id').ids

    @api.model
    def _customer_vendor_section_domain(self, mode):
        """Domain for customer / vendor menus and lookups."""
        if mode == 'customer':
            section_domain = [('customer_rank', '>', 0)]
        elif mode == 'supplier':
            section_domain = [('supplier_rank', '>', 0)]
        else:
            return []

        company_partner_ids = self._get_company_partner_ids()
        return expression.AND([
            section_domain,
            [('is_employee_contact', '=', False)],
            [('id', 'not in', company_partner_ids)] if company_partner_ids else [],
        ])

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        domain = list(domain or [])
        mode = self.env.context.get('res_partner_search_mode')
        if (
            mode in ('customer', 'supplier')
            and not self._search_skip_section_filter(domain)
        ):
            domain = expression.AND([
                domain,
                self._customer_vendor_section_domain(mode),
            ])
        return super()._search(domain, offset=offset, limit=limit, order=order)
