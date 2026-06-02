# -*- coding: utf-8 -*-


def post_init_hook(env):
    """Recompute flag and refresh menu action domains (exclude company partners)."""
    Partner = env['res.partner']
    Partner.search([])._compute_is_employee_contact()

    customer_domain = Partner._customer_vendor_section_domain('customer')
    supplier_domain = Partner._customer_vendor_section_domain('supplier')

    for xml_id in (
        'account.res_partner_action_customer',
        'account.res_partner_action_supplier',
        'base.action_partner_customer_form',
        'base.action_partner_supplier_form',
    ):
        action = env.ref(xml_id, raise_if_not_found=False)
        if action:
            domain = customer_domain if 'customer' in xml_id else supplier_domain
            action.sudo().write({'domain': domain})
