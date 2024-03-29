# -*- encoding: utf-8 -*-
#This file is part carrier_api module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Bool, Eval, Id
from genshi.template import TextTemplate

_STATES = {'required': Bool(Eval('required'))}
_DEPENDS = ['required']


class CarrierApiService(ModelSQL, ModelView):
    'Carrier API Service'
    __name__ = 'carrier.api.service'
    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', required=True)


class CarrierApi(ModelSQL, ModelView):
    'Carrier API'
    __name__ = 'carrier.api'
    name = fields.Char('Name', required=True)
    company = fields.Many2One('company.company', 'Company', required=True)
    warehouse = fields.Many2One('stock.location', 'Warehouse',
        domain = [('type', '=', 'warehouse')])
    carriers = fields.Many2Many('carrier.api-carrier.carrier',
            'api', 'carrier', 'Carriers', required=True)
    method = fields.Selection('get_carrier_app', 'Method', required=True)
    required = fields.Function(fields.Boolean('Required'),
        'on_change_with_required')
    services = fields.One2Many('carrier.api.service', 'api', 'Services')
    default_service = fields.Many2One('carrier.api.service', 'Service',
        help='Select a default service after save api and add services',
        domain=[('api', '=', Eval('id'))])
    vat = fields.Char('VAT', states=_STATES)
    url = fields.Char('URL', states=_STATES)
    username = fields.Char('Username', states=_STATES)
    password = fields.Char('Password', states=_STATES)
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
    email = fields.Char('Email')
    zips = fields.Text('Zip',
        help='Zip codes not send to carrier, separated by comma')
    debug = fields.Boolean('Debug')
    timeout = fields.Integer('Timeout',
        help='Total of seconds the connection will be lost')
    url_tracking_ref = fields.Char('URL Tracking Reference',
        help='Python expression that will be evaluated to generate the '
            'tracking uri:\n'
            '- ${record}: the record object')
    print_report = fields.Selection([
        (None, ''),
        ('png', 'PNG'),
        ('pdf', 'PDF'),
        ('zpl', 'Zebra'),
        ('tec', 'TEC'),
        ('ps', 'PS'),
        ('txt', 'TXT'),
        ], 'Print Report')

    @classmethod
    def __setup__(cls):
        super(CarrierApi, cls).__setup__()
        cls._buttons.update({
            'test_connection': {},
            })

    @classmethod
    def get_carrier_app(cls):
        'Get Carrier APP (Envialia, MRW, DHL,...)'
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
    def default_print_report():
        return None

    @fields.depends('method')
    def on_change_with_required(self, name=None):
        return True

    @staticmethod
    def get_default_carrier_service(api):
        """Get default service API"""
        return api.default_service

    @classmethod
    @ModelView.button
    def test_connection(cls, apis):
        'Test API carrier connection'
        for api in apis:
            getattr(cls, 'test_%s' % api.method)(api)

    @staticmethod
    def template_context(record):
        'Generate the template context'
        return {'record': record}

    def render_url_tracking_ref(self, record):
        'Render Genshi uri tracking ref'
        if not self.url_tracking_ref:
            return
        template = TextTemplate(self.url_tracking_ref)
        template_context = self.template_context(record)
        return template.generate(**template_context).render(encoding='UTF-8')

class CarrierApiService2(metaclass=PoolMeta):
    __name__ = 'carrier.api.service'
    api = fields.Many2One('carrier.api', 'API', required=True)


class CarrierApiCarrier(ModelSQL):
    'Carrier API - Carriers'
    __name__ = 'carrier.api-carrier.carrier'
    _table = 'carrier_api_carrier_rel'
    api = fields.Many2One('carrier.api', 'API', ondelete='CASCADE',
        required=True)
    carrier = fields.Many2One('carrier', 'Carrier', ondelete='RESTRICT',
        required=True)
