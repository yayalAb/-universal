# -*- coding: utf-8 -*-
from odoo import api, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)
        employees._refresh_work_contact_employee_flag()
        return employees

    def write(self, vals):
        contacts_before = self.mapped('work_contact_id')
        res = super().write(vals)
        (contacts_before | self.mapped('work_contact_id'))._compute_is_employee_contact()
        return res

    def unlink(self):
        contacts = self.mapped('work_contact_id')
        res = super().unlink()
        contacts._compute_is_employee_contact()
        return res

    def _refresh_work_contact_employee_flag(self):
        self.mapped('work_contact_id')._compute_is_employee_contact()
