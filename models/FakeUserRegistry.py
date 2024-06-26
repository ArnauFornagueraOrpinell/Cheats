from odoo import models, fields
from datetime import timedelta
import random
from odoo import api
from datetime import datetime

class FakeUserRegistry(models.Model):
    _name = 'fake.user.registry'
    _description = 'User Registry'

    name = fields.Char(string='Name')
    login = fields.Datetime(string='Last Login')
    email = fields.Char(string='Email')
    user_id = fields.Many2one('res.users', string='User')

    tolerance_hours = fields.Integer(string='Tolerancia Horas', default=0)
    tolerance_minutes = fields.Integer(string='Tolerancia Minutos', default=0)
    # default actual date with hour 7:55:00 minus 3 months fields.Datetime.now.replace(hour=7, minute=55, second=0) - timedelta(days=90)
    start_date = fields.Datetime(string='Start Date', default=str((datetime.now().replace(hour=5, minute=55) - timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")))
    # default actual date
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now)
    parent = fields.Boolean(string='Parent', default=True)

    @api.model
    def create(self, vals):
        #  Por cada usuario repetir:
        for user in self.env['res.users'].search([]):
           
            copy = vals
            result = self.create_loggins(vals, user)   
            vals = copy

        return result
    
    def create_loggins(self, vals, user):
        if vals['parent'] == True:
            vals['parent'] = False
            return super(FakeUserRegistry, self).create(vals)
        # else:
        #     vals['parent'] = True

        #if it is a user_id, then we need to get the user's email
        vals['user_id'] = user.id
        vals['email'] = user.email
        vals['name'] = user.name
    
        #Por cada dia entre start_date y end_date, crear un registro
        #con la fecha y el email del usuario
        #Convertir la fecha de string a datetime a partir de vals
        start_date = fields.Datetime.from_string(vals['start_date'])
        end_date = fields.Datetime.from_string(vals['end_date'])
        
        for i in range(0, (end_date - start_date).days):
            #si es fin de semana, no crear registro
            if (start_date + timedelta(days=i)).weekday() in [5,6]:
                continue
            #crear registro con una variacion random de tolerance(minutos)
            vals['login'] = start_date + timedelta(days=i) + timedelta(minutes=random.randint(0, vals['tolerance_minutes'])) + timedelta(hours=random.randint(0, vals['tolerance_hours'])) + timedelta(seconds=random.randint(0, 59)) 
            child = super(FakeUserRegistry, self).create(vals)

        return super(FakeUserRegistry, self).create(vals)

