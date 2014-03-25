# -*- encoding: utf-8 -*-
#This file is part carrier_api module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.transaction import Transaction
from trytond.pyson import Eval
import unicodedata

__all__ = ['CarrierApi']


class CarrierApi(ModelSQL, ModelView):
    'Carrier API'
    __name__ = 'carrier.api'
    _rec_name = 'carrier'
    company = fields.Many2One('company.company', 'Company', required=True)
    carrier = fields.Many2One('carrier', 'Carrier', required=True)
    method = fields.Selection('get_carrier_app', 'Method', required=True)
    service = fields.Many2One('carrier.service', 'Service', required=True, 
            depends=['carrier'], domain=[('carrier', '=', Eval('carrier'))])
    vat = fields.Char('VAT', required=True)
    url = fields.Char('URL', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    reference = fields.Boolean('Reference', help='Use reference from carrier')
    phone = fields.Char('Phone')
    zips = fields.Text('Zip',
            help='Zip codes not send to carrier, separated by comma')
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

    @staticmethod
    def get_default_carrier_service(api):
        """Get default service carrier"""
        for service in api.carrier.services:
            if service.default:
                return service
        return api.service

    @classmethod
    @ModelView.button
    def test_connection(self, apis):
        """
        Test connection Carrier API - Webservices
        Call method test_methodname
        """
        for api in apis:
            test = getattr(api, 'test_%s' % api.method)
            test(api)
