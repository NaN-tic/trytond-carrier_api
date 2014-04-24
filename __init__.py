#This file is part carrier_api module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from .api import *
from .carrier import *


def register():
    Pool.register(
        CarrierApiService,
        CarrierApi,
        CarrierApiService2,
        CarrierApiCarrier,
        Carrier,
        module='carrier_api', type_='model')
