# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Carrier']


class Carrier:
    __metaclass__ = PoolMeta
    __name__ = 'carrier'
    service = fields.Many2One('carrier.api.service', 'Service')
