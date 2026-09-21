# libraries
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd



def treasury_form_2_decimal(x):
    """
    Change the treasury form of a bond to decimal form
    for the first two decimals divide by 32
    for the next decimal divide by 256

    98.086 is 98 + 08/32 + 6/256
    """

    # first divide price on cents, thousandths and units

    units = np.trunc(x)
    decimals = x - units
    cents = np.trunc(decimals * 100)
    thousandths = np.trunc((decimals * 100 - cents) * 10)

    # convert to decimal
    decimal_price = units + cents / 32 + thousandths / 256
    return decimal_price




def previous_coupon_date(date, preserve_month_end):
    """
    Get the previous coupon date for a given date.
    If the maturity date is a month end, then the previous coupon date should also be a month end.
    """ 

    previous = pd.Timestamp(date) - pd.DateOffset(months=6)

    if preserve_month_end:
        previous = previous + MonthEnd(0)

    return previous


def coupon_schedule(maturity, valuation_date):
    """
    Get the coupon schedule for a given maturity and valuation date.

    Parameters:
    maturity (str): The maturity date of the bond in 'YYYY-MM-DD' format.
    valuation_date (str): The valuation date in 'YYYY-MM-DD' format.
    """
    maturity = pd.Timestamp(maturity).normalize()
    valuation_date = pd.Timestamp(valuation_date).normalize()
    preserve_month_end = maturity.is_month_end

    dates = []
    coupon_date = maturity

    while coupon_date > valuation_date:
        dates.append(coupon_date)
        coupon_date = previous_coupon_date(
            coupon_date,
            preserve_month_end,
        )

    return sorted(dates)

def current_coupon_dates(maturity, valuation_date):
    """
    Get the current coupon dates for a given maturity and valuation date.

    Parameters:
    maturity (str): The maturity date of the bond in 'YYYY-MM-DD' format.
    valuation_date (str): The valuation date in 'YYYY-MM-DD'
    
    """
    maturity = pd.Timestamp(maturity).normalize()
    valuation_date = pd.Timestamp(valuation_date).normalize()
    preserve_month_end = maturity.is_month_end

    next_coupon = maturity

    while previous_coupon_date(
        next_coupon,
        preserve_month_end,
    ) > valuation_date:
        next_coupon = previous_coupon_date(
            next_coupon,
            preserve_month_end,
        )

    previous_coupon = previous_coupon_date(
        next_coupon,
        preserve_month_end,
    )

    return pd.Series({
        "Accrual Start": previous_coupon,
        "Accrual End": next_coupon,
    })