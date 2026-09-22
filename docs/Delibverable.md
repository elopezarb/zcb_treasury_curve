# U.S. Treasury Zero-Coupon Yield Curve

**Jiayi Chen and Esteban Lopez Araiza Bravo**  
**Valuation date:** September 4, 2026

## Methodology

We estimate the continuously compounded zero-coupon curve from U.S. Treasury
note and bond ask prices reported by the Wall Street Journal. WSJ quotations are
first converted from Treasury fractional notation to decimal clean prices. For
each security, a semiannual coupon schedule is generated backward from maturity,
preserving end-of-month dates. Accrued interest is computed on an Actual/Actual
coupon-period basis, and the observed dirty price is:

$$
P_i^{dirty}=P_i^{clean}+\frac{Coupon_i}{2}
\frac{\text{days since previous coupon}}
     {\text{days in coupon period}}.
$$

Each remaining coupon is represented as a cash flow, with the $100 principal
added to the final payment. If $t_{ij}$ is the time in years from the valuation
date to cash flow $j$ of bond $i$, its model price is

$$
P_i(\theta)=\sum_{j=1}^{N_i}CF_{ij}
e^{-z(t_{ij};\theta)t_{ij}},
\qquad DF(t)=e^{-z(t)t}.
$$

The continuously compounded zero rate follows the Svensson specification:

$$
\begin{aligned}
z(t)={}&\beta_0
+\beta_1\left(\frac{1-e^{-t/\tau_1}}{t/\tau_1}\right)
+\beta_2\left(\frac{1-e^{-t/\tau_1}}{t/\tau_1}-e^{-t/\tau_1}\right)\\
&+\beta_3\left(\frac{1-e^{-t/\tau_2}}{t/\tau_2}-e^{-t/\tau_2}\right).
\end{aligned}
$$

The six parameters are common to all securities and are estimated with nonlinear
least squares:

$$
\widehat{\theta}=\operatorname*{arg\,min}_{\theta}
\sum_{i=1}^{N}\left[P_i^{dirty}-P_i(\theta)\right]^2.
$$

The optimization uses a reparameterization that enforces
$\beta_0+\beta_1>0$, together with
$0.01\leq\tau_1\leq5$ and $5\leq\tau_2\leq30$ years. After calibration, the
function $z(t)$ is evaluated at every unique coupon and principal payment date.

# Results

## Estimated Parameters

| Parameter | Estimate |
|---|---:|
| $\beta_0$ | -0.072031 |
| $\beta_1$ | 0.109233 |
| $\beta_2$ | 0.081970 |
| $\beta_3$ | 0.359281 |
| $\tau_1$ | 2.709100 |
| $\tau_2$ | 17.330593 |

## Zero-Coupon Yield Curve

![Continuously compounded zero-coupon yield curve](zero_curve.png)

## Selected Payment Dates

| Payment date | Time | Zero rate | Discount factor |
|---|---:|---:|---:|
| 2026-09-15 | 0.0301 | 3.7361% | 0.998875 |
| 2027-08-31 | 0.9884 | 4.1126% | 0.960168 |
| 2031-08-31 | 4.9884 | 4.5116% | 0.798471 |
| 2036-08-15 | 9.9466 | 4.7621% | 0.622714 |
| 2046-08-15 | 19.9452 | 5.3628% | 0.343137 |
| 2056-08-15 | 29.9466 | 5.2425% | 0.208056 |

<div class="page"></div>

