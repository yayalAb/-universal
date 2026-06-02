# -*- coding: utf-8 -*-


def post_init_hook(env):
    """Recompute stored employee-contact flag on existing partners."""
    env['res.partner'].search([])._compute_is_employee_contact()
