# libraries
import numpy as np
import pandas as pd



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

def current_coupon_dates(maturity, valuation_date):
    maturity = pd.Timestamp(maturity)
    valuation_date = pd.Timestamp(valuation_date)
    six_months = pd.DateOffset(months=6)

    coupon_end = maturity

    # Move backward until the next coupon is after valuation_date
    while coupon_end - six_months > valuation_date:
        coupon_end -= six_months

    coupon_start = coupon_end - six_months

    return pd.Series({
        "Accrual Start": coupon_start,
        "Accrual End": coupon_end,
    })