# Mini-Project 2: U.S. Treasury Zero-Coupon Yield Curve

**Jiayi Chen and Esteban Lopez Araiza Bravo**  
**Valuation date:** September 4, 2026  
**Sample:** 353 U.S. Treasury notes and bonds

## Methodology

We estimate the continuously compounded zero-coupon curve from U.S. Treasury
note and bond ask prices reported by the Wall Street Journal. WSJ quotations are
first converted from Treasury fractional notation to decimal clean prices. For
each security, a semiannual coupon schedule is generated backward from maturity,
preserving end-of-month dates. Accrued interest is computed on an Actual/Actual
coupon-period basis, and the observed dirty price is

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

## Results

The final estimates are
$(-0.072031, 0.109233, 0.081970, 0.359281, 2.709100, 17.330593)$ for
$(\beta_0,\beta_1,\beta_2,\beta_3,\tau_1,\tau_2)$. The optimizer converged with
a least-squares cost of 3.89998. The mean absolute dirty-price error is 0.0902
per $100 of principal, the price RMSE is 0.1486, and the mean absolute yield
error is 2.87 basis points.
