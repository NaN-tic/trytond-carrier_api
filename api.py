#This file is part carrier_api module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import Pool
from trytond.transaction import Transaction

__all__ = ['CarrierApi']


class CarrierApi(ModelSQL, ModelView):
    'Carrier API'
    __name__ = 'carrier.api'
    _rec_name = 'carrier'
    company = fields.Many2One('company.company', 'Company', required=True)
    carrier = fields.Many2One('carrier', 'Carrier', required=True)
    method = fields.Selection('get_carrier_app', 'Method', required=True)
    url = fields.Char('URL', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    reference = fields.Boolean('Reference', help='Use reference from carrier')
    debug = fields.Boolean('Debug')

    @classmethod
    def __setup__(cls):
        super(CarrierApi, cls).__setup__()
        cls._error_messages.update({
            'connection_successfully': 'Test connection are successfully!',
            'connection_error': 'Test connection failed!',
        })
        cls._buttons.update({
                'test_connection': {},
                })

    @classmethod
    def get_carrier_app(cls):
        '''
        Get Carrier APP (Envialia, MRW, DHL,...)
        '''
        res = [('','')]
        return res

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_reference():
        return True

    @classmethod
    @ModelView.button
    def test_connection(self, apis):
        """
        Test connection Carrier API - Webservices
        Call method test_namecarrier - if exist
        """
        for api in apis:
            try:
                test = getattr(api, 'test_%s' % api.carrier)
                test(api)
            except:
                self.raise_user_error('connection_error')
