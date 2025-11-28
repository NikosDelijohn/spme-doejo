## How does DoEjo compute the `Salt Addition` parameter? 

Salt addition enhances headspace concentration through the salting-out effect, described by the Setschenow equation:

$$
    ln\left(\frac{S_0}{S}\right) = k_sI
$$

Where $I$ is the ionic strength. A significant salting-out effect ($\geq 1$ log unit decrease in solubility) typically occurs for compounds with $logP < 2$. The corresponding algorithmic threshold therefore applies 20-30 % NaCl ($\approx 3-4 M$) only when $XLogP < 2.0, as the gain diminishes for more hydrophobic analytes.

Reported Setchenow constants decrease with increasing hydrophobicity. From $k_s \approx 0.25 M^{-1}$ for polar solutes ($log P \approx 1-2$) to $k_s \approx 0.05M^{-1}$ for nonpolar compounds ($logP > 2$). Hence, corresponding to enhancement factors of $\times 4.5$ and $\times 1.1$ at 6 $M$ NaCl. Thus, salting-out is beneficial primarily for polar or moderately polar compounds.

---

### References

[**α**] Psillakis E, Kalogerakis N. Hollow-fibre liquid-phase microextraction of phthalate esters from water. J Chromatogr A. 2003 May 30;999(1-2):145-53 [DOI](10.1016/s0021-9673(03)00390-x).

[**β**] Hyde, A. M., Zultanski, S. L., Waldman, J. H., Zhong, Y.-L., Shevlin, M., & Peng, F. (2017). General principles and strategies for salting-out informed by the Hofmeister series. Organic Process Research & Development, 21(9), 1355–1370 [DOI](https://doi.org/10.1021/acs.oprd.7b00197).

[**γ**] DiFilippo, E. L., & Eganhouse, R. P. (2010). Assessment of PDMS-water partition coefficients: Implications for passive environmental sampling of hydrophobic organic compounds. Environmental Science & Technology, 44(18), 6917–6925 [DOI](https://doi.org/10.1021/es101103x).

[**δ**] Smedes, F., Geertsma, R. W., van der Zande, T., & Booij, K. (2009). Polymer–water partition coefficients of hydrophobic compounds for passive sampling: Application of cosolvent models for validation. Environmental Science & Technology, 43(18), 7047–7054 [DOI](https://doi.org/10.1021/es9009376).
