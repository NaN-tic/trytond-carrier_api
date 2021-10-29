# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    def carrier_api_check_country_es(self):
        # Spain postal code is 5 digits and only digits
        if not self.delivery_address.postal_code:
            raise UserError(gettext('carrier_api.msg_required_postal_code',
                shipment=self.rec_name))

        postal_code = self.delivery_address.postal_code
        if not len(postal_code) == 5 or not postal_code.isdigit():
            raise UserError(gettext('carrier_api.msg_invalid_postal_code',
                shipment=self.rec_name,
                postal_code=postal_code,
                country=self.delivery_address.country.code))

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

        super().pack(shipments)
