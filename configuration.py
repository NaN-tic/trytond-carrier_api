# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Configuration']


class Configuration(metaclass=PoolMeta):
    __name__ = 'stock.configuration'
    carrier_api_check_country = fields.Boolean('Carrier API Country',
        help='Check country method before send to carrier API when packed '
            'a shipment')

    @staticmethod
    def default_carrier_api_check_country():
        return True
