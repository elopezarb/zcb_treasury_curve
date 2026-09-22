# U.S. Treasury Zero-Coupon Yield Curve

This project estimates the continuously compounded zero-coupon yield curve from
U.S. Treasury note and bond prices using the Nelson-Siegel-Svensson (Svensson)
parametric model. It was prepared for Mini-Project 2 in Valuation for Financial
Engineering.

**Authors:** Jiayi Chen and Esteban Lopez Araiza Bravo<br>
**Valuation date:** September 4, 2026<br>
**Market data:** 353 U.S. Treasury notes and bonds from the
[Wall Street Journal Treasury quotations](https://www.wsj.com/market-data/bonds/treasuries)

## Objective

The objective is to estimate a continuously compounded spot rate for every
remaining coupon and principal payment date represented in the Treasury sample.
The resulting curve can be used to discount any deterministic cash flow on those
dates:

$$
DF(t)=e^{-z(t)t},
$$

where $t$ is measured in years from the valuation date and $z(t)$ is the
continuously compounded zero rate.

## Methodology

1. **Clean the market data.** WSJ bid and ask quotations are converted from
   Treasury notation into decimal prices. The ask quotation is treated as the
   observed clean price.
2. **Construct coupon schedules.** Treasury notes and bonds are assumed to pay
   semiannual coupons. Schedules are generated backward from maturity while
   preserving end-of-month payment dates.
3. **Calculate dirty prices.** Accrued interest is calculated using the actual
   number of days elapsed and the actual number of days in the coupon period:

   $$
   AI_i=\frac{Coupon_i}{2}
   \frac{\text{days since previous coupon}}
        {\text{days in coupon period}},
   \qquad
   P_i^{dirty}=P_i^{clean}+AI_i.
   $$

4. **Build the cash flows.** Every remaining coupon is included, and the final
   payment contains the last coupon plus $100 of principal.
5. **Fit the Svensson curve.** For parameter vector
   $\theta=(\beta_0,\beta_1,\beta_2,\beta_3,\tau_1,\tau_2)$, the model rate is:
   

   $$
   \begin{aligned}
   z(t)={}&\beta_0
   +\beta_1\left(\frac{1-e^{-t/\tau_1}}{t/\tau_1}\right) \\
   &+\beta_2\left(\frac{1-e^{-t/\tau_1}}{t/\tau_1}-e^{-t/\tau_1}\right) \\
   &+\beta_3\left(\frac{1-e^{-t/\tau_2}}{t/\tau_2}-e^{-t/\tau_2}\right).
   \end{aligned}
   $$

   The model-implied dirty price is

   $$
   P_i(\theta)=\sum_{j=1}^{N_i}CF_{ij}
   e^{-z(t_{ij};\theta)t_{ij}}.
   $$

   SciPy's nonlinear least-squares solver estimates the common parameter vector
   by minimizing

   $$
   \widehat{\theta}=\operatorname*{arg\,min}_{\theta}
   \sum_{i=1}^{N}\left(P_i^{observed}-P_i(\theta)\right)^2.
   $$

The implementation reparameterizes the model to enforce
$\beta_0+\beta_1>0$, which makes the limiting short rate positive. The decay
parameters are bounded by $0.01\leq\tau_1\leq5$ and
$5\leq\tau_2\leq30$ years.

## Results

The fitted parameters in the final notebook run are:

| Parameter | Estimate |
|---|---:|
| $\beta_0$ | -0.072031 |
| $\beta_1$ | 0.109233 |
| $\beta_2$ | 0.081970 |
| $\beta_3$ | 0.359281 |
| $\tau_1$ | 2.709100 years |
| $\tau_2$ | 17.330593 years |

The optimizer converged with a least-squares cost of `3.89998`. Across the 353
securities, the mean absolute dirty-price error is `0.0902`, the dirty-price
RMSE is `0.1486`, and the mean absolute yield error is approximately `2.87`
basis points. The curve should be interpreted over the observed cash-flow
horizon rather than extrapolated indefinitely.

## Repository Structure

```text
data/
  raw/                 Original Treasury quotations
  processed/           Cleaned bond data and model comparison table
notebooks/
  ZCB Bond Yield Curve.ipynb
src/
  bond_funs.py         Coupon schedules, Svensson model, pricing and YTM
  utils.py             Treasury quotation conversion
```

## Running the Project

Create a Python environment and install the required packages:

```bash
pip install numpy pandas scipy matplotlib openpyxl jupyter
jupyter notebook "notebooks/ZCB Bond Yield Curve.ipynb"
```

Run the notebook from top to bottom. It produces cleaned bond data, a comparison
of observed and model-implied prices and yields, the zero-rate curve, and discount
factors.

## Notes

- Rates in the Svensson function are decimals, not percentages.
- Time is measured in years using calendar days divided by `365.25`.
- WSJ Treasury prices are clean prices quoted in Treasury fractional notation.
- Dirty prices, rather than clean prices, are matched to the present value of
  future cash flows.
