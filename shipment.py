# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['ShipmentOut']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    def carrier_api_check_country_es(self):
        # Spain zip is 5 digits and only digits
        if not self.delivery_address.zip:
            raise UserError(gettext('smtp.msg_required_zip',
                shipment=self.rec_name))

        zip_ = self.delivery_address.zip
        if not len(zip_) == 5 or not zip_.isdigit():
            raise UserError(gettext('smtp.msg_invalid_zip',
                shipment=self.rec_name,
                zip=zip_,
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

        super(ShipmentOut, cls).pack(shipments)
