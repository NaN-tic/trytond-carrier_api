# This file is part of the carrier_api module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import (doctest_setup, doctest_teardown,
    doctest_checker)
from trytond.modules.company.tests import CompanyTestMixin


class CarrierApiTestCase(CompanyTestMixin, ModuleTestCase):
    'Test Carrier Api module'
    module = 'carrier_api'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CarrierApiTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_carrier_api.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
