# -*- encoding: utf-8 -*-
#This file is part carrier_api module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval, Id

__all__ = ['CarrierApiService', 'CarrierApi', 'CarrierApiService2', 'CarrierApiCarrier']


class CarrierApiService(ModelSQL, ModelView):
    'Carrier API Service'
    __name__ = 'carrier.api.service'
    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', required=True)


class CarrierApi(ModelSQL, ModelView):
    'Carrier API'
    __name__ = 'carrier.api'
    _rec_name = 'method'
    company = fields.Many2One('company.company', 'Company', required=True)
    carriers = fields.Many2Many('carrier.api-carrier.carrier',
            'api', 'carrier', 'Carriers', required=True)
    method = fields.Selection('get_carrier_app', 'Method', required=True)
    services = fields.One2Many('carrier.api.service', 'api', 'Services')
    default_service = fields.Many2One('carrier.api.service', 'Service',
        help='Select a default service after save api and add services',
        domain=[('api', '=', Eval('id'))],
        depends=['id'])
    vat = fields.Char('VAT', required=True)
    url = fields.Char('URL', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    reference = fields.Boolean('Reference', help='Use reference from carrier')
    reference_origin = fields.Boolean('Reference Origin',
        help='Use origin field as the reference record')
    weight = fields.Boolean('Weight',
        help='Send shipments with weight')
    weight_unit = fields.Many2One('product.uom', 'Weight Unit',
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        help='Default shipments unit')
    weight_api_unit = fields.Many2One('product.uom', 'Weight API Unit',
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        help='Default API unit')
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
    def default_weight():
        return True

    @staticmethod
    def default_reference():
        return True

    @staticmethod
    def get_default_carrier_service(api):
        """Get default service API"""
        return api.default_service

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


class CarrierApiService2:
    __metaclass__ = PoolMeta
    __name__ = 'carrier.api.service'
    api = fields.Many2One('carrier.api', 'API', required=True)


class CarrierApiCarrier(ModelSQL):
    'Carrier API - Carriers'
    __name__ = 'carrier.api-carrier.carrier'
    _table = 'carrier_api_carrier_rel'
    api = fields.Many2One('carrier.api', 'API', ondelete='CASCADE',
        select=True, required=True)
    carrier = fields.Many2One('carrier', 'Carrier',
            ondelete='RESTRICT', select=True, required=True)
