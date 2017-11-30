#This file is part carrier_api module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import api
from . import carrier
from . import shipment


def register():
    Pool.register(
        api.CarrierApiService,
        api.CarrierApi,
        api.CarrierApiService2,
        api.CarrierApiCarrier,
        carrier.Carrier,
        configuration.Configuration,
        shipment.ShipmentOut,
        module='carrier_api', type_='model')
