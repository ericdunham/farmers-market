import unittest

from market import market


class MarketTestCase(unittest.TestCase):
    def assert_cases(self, cases, func):
        """a small helper function for parameterizing test cases"""
        for (got, expected) in cases:
            with self.subTest(got=got, expected=expected):
                func(expected, got)

    def assert_basket_totals(self, basket_cases):
        """converts basket cases to totals by way of register then asserts"""
        results = [(market.total(market.register(basket)), expected)
                   for (basket, expected) in basket_cases]
        self.assert_cases(results, self.assertEqual)

    def test_apom(self):
        """apply APOM discount"""
        basket = ['OM1', 'AP1']
        expected = ['OM1', 'AP1', 'APOM']
        self.assertEqual(expected, market.apom(basket))

    def test_apom_verbose(self):
        """apply APOM discount (deprecated)"""
        cases = [
            ['OM1', 'AP1'],
            ['OM1'],
            ['AP1', 'CH1'],
            ['CF1']
        ]
        results = [(market.apom_verbose(case), market.apom(case))
                   for case in cases]
        self.assert_cases(results, self.assertEqual)

    def test_appl(self):
        """apply APPL discount"""
        basket = ['AP1', 'AP1', 'CH1', 'AP1']
        expected = ['AP1', 'APPL', 'AP1', 'APPL', 'CH1', 'AP1', 'APPL']
        self.assertEqual(expected, market.appl(basket))

    def test_appl_verbose(self):
        """apply APPL discount (deprecated)"""
        cases = [
            ['AP1', 'AP1', 'CH1', 'AP1'],
            ['AP1', 'AP1'],
            ['AP1', 'CH1'],
            ['CF1']
        ]
        results = [(market.appl_verbose(case), market.appl(case))
                   for case in cases]
        self.assert_cases(results, self.assertEqual)

    def test_bogo(self):
        """apply BOGO discount"""
        basket = ['CF1', 'CF1', 'CF1', 'CF1']
        expected = ['CF1', 'CF1', 'BOGO', 'CF1', 'CF1', 'BOGO']
        self.assertEqual(expected, market.bogo(basket))

    def test_bogo_verbose(self):
        """apply BOGO discount (deprecated)"""
        cases = [
            ['CF1', 'CF1', 'CF1', 'CF1'],
            ['AP1', 'AP1'],
            ['AP1', 'CH1'],
            ['CF1']
        ]
        results = [(market.bogo_verbose(case), market.bogo(case))
                   for case in cases]
        self.assert_cases(results, self.assertEqual)

    def test_chmk(self):
        """apply CHMK discount"""
        basket = ['CH1', 'AP1', 'CF1', 'MK1']
        expected = ['CH1', 'AP1', 'CF1', 'MK1', 'CHMK']
        self.assertEqual(expected, market.chmk(basket))

    def test_chmk_verbose(self):
        """apply CHMK discount (deprecated)"""
        cases = [
            ['CH1', 'AP1', 'CF1', 'MK1'],
            ['CH1', 'AP1', 'CF1', 'MK1', 'MK1'],
            ['AP1', 'CH1'],
            ['CF1']
        ]
        results = [(market.chmk_verbose(case), market.chmk(case))
                   for case in cases]
        self.assert_cases(results, self.assertEqual)

    def test_register(self):
        """basic register with no discounts applied"""
        # Extended register testing is covered by all the total_* tests.
        # If there is a need to explicitly test more cases for register, that
        # can be revisited in the future.
        cases = [
            (['MK1', 'AP1'], [('MK1', 4.75), ('AP1', 6.00)]),
            ([], [])
        ]
        results = [(market.register(case), expected)
                   for (case, expected) in cases]
        self.assert_cases(results, self.assertEqual)

    def test_total(self):
        """basic totals with no discounts applied"""
        cases = [
            (['MK1', 'AP1'], 10.75),
            ([], 0.00)
        ]
        self.assert_basket_totals(cases)

    def test_total_apom(self):
        """totals with only the APOM discount"""
        cases = [(['OM1', 'AP1'], 6.69)]
        self.assert_basket_totals(cases)

    def test_total_apom_appl(self):
        """totals with the APOM and APPL discounts"""
        cases = [
            (['OM1', 'AP1', 'AP1', 'AP1'], 14.19),
            (['OM1', 'AP1', 'AP1', 'OM1', 'AP1'], 14.88)
        ]
        self.assert_basket_totals(cases)

    def test_total_appl(self):
        """totals with only the APPL discount"""
        cases = [
            (['AP1', 'AP1', 'CH1', 'AP1'], 16.61),
            (['AP1', 'AP1', 'AP1', 'AP1'], 18.00)
        ]
        self.assert_basket_totals(cases)

    def test_total_bogo(self):
        """totals with only the BOGO discount"""
        cases = [
            (['CF1', 'CF1'], 11.23),
            (['CF1', 'CF1', 'CF1', 'CF1'], 22.46)
        ]
        self.assert_basket_totals(cases)

    def test_total_chmk(self):
        """totals with only the CHMK discount"""
        cases = [
            (['CH1', 'AP1', 'CF1', 'MK1'], 20.34),
            (['CH1', 'MK1', 'MK1'], 7.86),
            (['CH1', 'MK1', 'CH1', 'MK1'], 10.97)
        ]
        self.assert_basket_totals(cases)
