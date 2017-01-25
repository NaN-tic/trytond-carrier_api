# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Carrier']


class Carrier:
    __metaclass__ = PoolMeta
    __name__ = 'carrier'
    apis = fields.Many2Many('carrier.api-carrier.carrier',
        'carrier', 'api', 'Carrier API')
    services = fields.Function(fields.Many2Many('carrier.api.service', None,
        None, 'Services'), 'on_change_with_services')
    service = fields.Many2One('carrier.api.service', 'Service',
        domain=[('id', 'in', Eval('services'))],
        depends=['services'])

    @fields.depends('apis')
    def on_change_with_services(self, name=None):
        services = []
        for api in self.apis:
            for service in api.services:
                services.append(service.id)
        return services
