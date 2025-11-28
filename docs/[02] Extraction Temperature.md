## How does DoEjo compute the `Extraction Temperature` parameter? 

The extraction temperature was derived from the analyte's boiling point based on the Clausius-Clapeyron relationship, which links vapor pressure and temperature through the equation:

$$
ln \left(\frac{P(T)}{P_b} \right) = - \frac{\Delta H_{\text{vap}}}{R} \times \left(1/T - 1/T_b\right)
$$

where:
- $P_b = 1$ atm at the boiling point $T_b$
- $\Delta H_{\text{vap}}$ is the molar enthalpy of vaporization
- $R = 8.314 \ \text{J} mol^{-1}K^{-1}$.

Headspace extraction becomes efficient once the analyte's vapor pressure at the extraction temperature $T_E$ reaches approximately 10% of its vaport pressure at the boiling point, i.e. $\frac{P(T_E)}{P_b} = \alpha = 0.10$. This criterion provides sufficient volatilization for effective headspace partitioning without risking matrix degradation or analyte loss.

Applying the Clausius-Clapeyron equation in combination with the empirical Trouton relation, $\Delta H_{\text{vap}} \approx 88T_b (J mol^{-1}K^{-1})$, gives:

$$
T_b \approx \frac{T_E}{1 + \frac{R \times ln(1/a)}{88}}
$$

for $\alpha = 0.1$, the correction term $\frac{R \times ln(1/a)}{88}$ is $\approx$ 0.26, leading to characteristic boiling-to-extraction temperature pairs of approximately

- 100 °C → 35 °C
- 200 °C → 50 °C 
- 300 °C → 70 °C

These values define the three temperature bands implemented in the code 

1. 30–40 °C
2. 40–60 °C
3. 60–80 °C

The threshold breakpoints at 100°C and 200°C therefore correspond to roughly tenfold changes in vapor pressure, ensuring consistent volatility scaling across compounds.

The algorithm uses the maximum compound boiling point to determine the optimal extraction temperature range:

$$
\begin{align*}
\max\{T_b\} < 100^\circ\mathrm{C} 
    &\;\rightarrow\; 30^\circ\mathrm{C} - 40^\circ\mathrm{C} \\[6pt]
100^\circ\mathrm{C} \le \max\{T_b\} \le 200^\circ\mathrm{C} 
    &\;\rightarrow\; 40^\circ\mathrm{C} - 60^\circ\mathrm{C} \\[6pt]
\max\{T_b\} > 200^\circ\mathrm{C} 
    &\;\rightarrow\; 60^\circ\mathrm{C} - 80^\circ\mathrm{C}
\end{align*}
$$

This approach aligns with EPA volatility classifications [**γ**], where very volatile organic compounds (VVOCs; < 100 °C), volatile organic compounds (VOCs; 100–240 °C), and semi-volatile organic compounds (SVOCs; > 240 °C) require progressively higher extraction temperatures to achieve comparable vapor-phase concentrations.

---

### References

[**α**] G. Ouyang, 8 - SPME and Environmental Analysis, Handbook of Solid Phase Microextraction, Elsevier, 2012, Pages 251-290, [DOI](https://doi.org/10.1016/B978-0-12-416017-0.00008-5).

[**β**] A. L. Dawidowicz, J. Szewczyk, M. P. Dybowski, Modified headspace solid-phase microextraction for the determination of quantitative relationships between components of mixtures consisting of alcohols, esters, and ethers — impact of the vapor pressure difference of the compounds, Journal of Separation Science, Volume 40, Pages 2984-2991, [DOI](https://doi.org/10.1002/jssc.201700323).

[**γ**] U.S. Environmental Protection Agency. (2025, September 8). Technical Overview of Volatile Organic Compounds. [WEBPAGE]( https://www.epa.gov/indoor-air-quality-iaq/technical-overview-volatile-organic-compounds?utm).
