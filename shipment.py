# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOut']


class ShipmentOut:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out'

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls._error_messages.update({
                'required_zip': ('Required ZIP number '
                    'on shipment "%(shipment)s".'),
                'invalid_zip': ('Invalid ZIP number "%(zip)s" '
                    'and country "%(country)s" on shipment "%(shipment)s".'),
                })

    def carrier_api_check_country_es(self):
        # Spain zip is 5 digits and only digits
        if not self.delivery_address.zip:
            self.raise_user_error('required_zip', {
                    'shipment': self.rec_name,
                    })

        zip_ = self.delivery_address.zip
        if not len(zip_) == 5 or not zip_.isdigit():
            self.raise_user_error('invalid_zip', {
                    'shipment': self.rec_name,
                    'zip': zip_,
                    'country': self.delivery_address.country.code,
                    })

    @classmethod
    def pack(cls, shipments):
        Config = Pool().get('stock.configuration')

        config = Config(1)
        if config.carrier_api_check_country:
            for shipment in shipments:
                country_code = (shipment.delivery_address.country.code.lower()
                    if shipment.delivery_address.country else None)
                if not country_code:
                    continue

                check_country = 'carrier_api_check_country_' + country_code
                if hasattr(cls, check_country):
                    check_country = getattr(cls, check_country)
                    check_country(shipment)

        super(ShipmentOut, cls).pack(shipments)
