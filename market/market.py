# -*- coding: utf-8 -*-
# stdlib froms
from functools import reduce

#: A mapping of product codes to their prices.
#
# Product names have been omitted as they have no bearing on this module and
# hopefully would be in a data store, in which case this module would ignore
# them via e.g. ``SELECT`` ing certain columns or ``db.collection.find(...)``
# ing certain fields.
PRODUCT_PRICES = {
    'CH1': 3.11,
    'AP1': 6.00,
    'CF1': 11.23,
    'MK1': 4.75,
    'OM1': 3.69
}

#: A mapping of discount codes and the amount that they reduce the register
#: total by, as a function of :py:const:`~market.market.PRODUCT_PRICES`.
DISCOUNT_AMOUNTS = {
    'BOGO': -PRODUCT_PRICES['CF1'],
    'APPL': 4.50 - PRODUCT_PRICES['AP1'],
    'CHMK': -PRODUCT_PRICES['MK1'],
    'APOM': -(PRODUCT_PRICES['AP1'] / 2.0)
}


def apom(basket):
    """Applies the APOM discount to the `basket`, if applicable.
    The APOM discount is defined as:

        Purchase a bag of Oatmeal and get 50% off a bag of Apples.

    :param list(str) basket: The basket to apply the APOM discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    :see: :py:const:`~market.market.DISCOUNT_AMOUNTS`
    :see: :func:`apply_discount`
    """
    def when(_, applied_count):
        return applied_count < basket.count('OM1')
    return apply_discount('OM1', 1, 'AP1', 'APOM', when, basket)


def apom_verbose(basket):
    """Applies the APOM discount to the `basket`, if applicable.

    .. deprecated:: 0.0.1
        Use :func:`apom` instead.

    :param list(str) basket: The basket to apply the APOM discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    """
    if basket.count('OM1') < 1:
        return basket
    half_off_apples = min(basket.count('OM1'), basket.count('AP1'))
    discounted_basket = []
    for item in basket:
        discounted_basket.append(item)
        if item == 'AP1' and half_off_apples > 0:
            discounted_basket.append('APOM')
            half_off_apples -= 1
    return discounted_basket


def appl(basket):
    """Applies the APPL discount to the `basket`, if applicable.
    The APPL discount is defined as:

        If you buy 3 or more bags of Apples, the price drops to $4.50.

    :param list(str) basket: The basket to apply the APPL discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    :see: :py:const:`~market.market.DISCOUNT_AMOUNTS`
    :see: :func:`apply_discount`
    """
    return apply_discount('AP1', 3, 'AP1', 'APPL', lambda *args: True, basket)


def appl_verbose(basket):
    """Applies the APPL discount to the `basket`, if applicable.

    .. deprecated:: 0.0.1
        Use :func:`appl` instead.

    :param list(str) basket: The basket to apply the APPL discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    """
    if basket.count('AP1') < 3:
        return basket
    discounted_basket = []
    for item in basket:
        discounted_basket.append(item)
        if item == 'AP1':
            discounted_basket.append('APPL')
    return discounted_basket


def apply_discount(trigger, triggers_needed, affected, discount, when, basket):
    """Adds the given `discount` to the `basket`, if all preconditions are met,
    returning the new basket with discounts present.

    This is the function that all discounts are expected to call, hence the
    deprecation of the ``*_verbose`` functions.

    Example::

        >>> market.PRODUCT_PRICES = {'FOO': 4, 'BAR': 2}
        >>> market.DISCOUNT_AMOUNTS = {'BAZ': -3.50}
        >>> def quux(basket):
        ...     return market.apply_discount('BAR', 1, 'BAR', 'BAZ',
        ...                                  lambda *args: True, basket)
        ...
        >>> setattr(market, 'quux', quux)
        >>> market.CURRENT_DISCOUNTS = [quux]
        >>> market.register(['FOO', 'FOO', 'BAR', 'BAR'])
        [('FOO', 4), ('FOO', 4), ('BAR', 2), ('BAZ', -3.5), ('BAR', 2),
         ('BAZ', -3.5)]
        >>> market.register(['FOO', 'BAR'])
        [('FOO', 4), ('BAR', 2), ('BAZ', -3.5)]
        >>> market.register(['BAR', 'FOO', 'BAR'])
        [('BAR', 2), ('BAZ', -3.5), ('FOO', 4), ('BAR', 2), ('BAZ', -3.5)]
        >>>

    :param str trigger: The product code that potentially triggers a discount.
    :param int triggers_needed: The minimum number of `triggers` that must be
        seen in `basket` to potentially apply a discount.
    :param str affected: The product code that is affected by the trigger,
        which determines the insertion position of `discount`.
    :param str discount: The product code representing the discount.
    :param function when: The function to call to ultimately determine whether
        or not to apply the discount. This function receives two arguments, in
        the following order:

        * **seen_count**: an `int` representing the number of times that
          `affected` has been seen
        * **affected_count**: an `int` representing the number of times that
          the discount has already been applied in the currently executing
          context of :func:`apply_discount`

    :param list(str) basket: The basket to apply `discount` to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    """
    if basket.count(trigger) < triggers_needed:
        return basket
    discounted_basket = []
    seen_count = 0
    applied_count = 0
    for item in basket:
        discounted_basket.append(item)
        if item == affected:
            seen_count += 1
            if when(seen_count, applied_count):
                discounted_basket.append(discount)
                applied_count += 1
    return discounted_basket


def bogo(basket):
    """Applies the BOGO discount to the `basket`, if applicable.
    The BOGO discount is defined as:

        Buy-One-Get-One-Free Special on Coffee. (Unlimited)

    :param list(str) basket: The basket to apply the BOGO discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    :see: :py:const:`~market.market.DISCOUNT_AMOUNTS`
    :see: :func:`apply_discount`
    """
    def when(seen_count, _):
        return seen_count % 2 == 0
    return apply_discount('CF1', 2, 'CF1', 'BOGO', when, basket)


def bogo_verbose(basket):
    """Applies the BOGO discount to the `basket`, if applicable.

    .. deprecated:: 0.0.1
        Use :func:`bogo` instead.

    :param list(str) basket: The basket to apply the BOGO discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    """
    if basket.count('CF1') <= 1:
        return basket
    discounted_basket = []
    eligible_for_discount = False
    for item in basket:
        discounted_basket.append(item)
        if item == 'CF1':
            if eligible_for_discount:
                discounted_basket.append('BOGO')
                eligible_for_discount = False
            else:
                eligible_for_discount = True
    return discounted_basket


def chmk(basket):
    """Applies the CHMK discount to the `basket`, if applicable.
    The CHMK discount is defined as:

        Purchase a box of Chai and get milk free. (Limit 1)

    :param list(str) basket: The basket to apply the CHMK discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    :see: :py:const:`~market.market.DISCOUNT_AMOUNTS`
    :see: :func:`apply_discount`
    """
    def when(_, applied_count):
        return applied_count < 1
    return apply_discount('CH1', 1, 'MK1', 'CHMK', when, basket)


def chmk_verbose(basket):
    """Applies the CHMK discount to the `basket`, if applicable.

    .. deprecated:: 0.0.1
        Use :func:`chmk` instead.

    :param list(str) basket: The basket to apply the CHMK discount to.
    :returns: The `basket` with the applicable discount applied.
    :rtype: list(str)
    """
    if basket.count('CH1') < 1:
        return basket
    discounted_basket = basket.copy()
    if 'MK1' in basket:
        idx = basket.index('MK1')
        discounted_basket.insert(idx + 1, 'CHMK')
    return discounted_basket


#: A list of currently-applicable discounts of the form `list(function)`.
#:
#: Example::
#:
#:      CURRENT_DISCOUNTS = [bogo, appl]
#:
#: This would make it so the unlimited buy-one-get-one-free special on coffee
#: and the purchase a bag of oatmeal and get 50% off a bag of apples discount
#: are applied during :func:`~market.market.register`.
CURRENT_DISCOUNTS = [bogo, appl, chmk, apom]


def register(basket):
    """Returns a register for the given `basket`, which is a representation of
    codes and their associated values.

    Example::

        >>> market.register(['BAR', 'FOO', 'BAR'])
        [('BAR', 2), ('BAZ', -3.5), ('FOO', 4), ('BAR', 2), ('BAZ', -3.5)]

    :param list(str) basket: The basket to create a register from.
    :returns: The `basket` with all amounts associated to their codes.
    :rtype: list(tuple(str, float))
    """
    code_amounts = {**PRODUCT_PRICES, **DISCOUNT_AMOUNTS}
    discounted = reduce(lambda acc, f: f(acc), CURRENT_DISCOUNTS, basket)
    return [(code, code_amounts[code]) for code in discounted]


def total(register_lines):
    """Returns the total for the given `register_lines`.

    Example::

        >>> market.total([('FOO', 4), ('BAR', 2), ('BAZ', -3.5)]) == 2.50
        True


    :param register_lines: The register lines.
    :type register_lines: list(tuple(str, float))
    :returns: The total of all amounts in `register_lines`, rounded to two
        significant digits.
    :rtype: float
    :see: :func:`register`
    """
    return round(sum([amount for (_, amount) in register_lines]), 2)
