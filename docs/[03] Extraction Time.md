## How does DoEjo compute the `Extraction Time` parameter? 
The extraction time thresholds are based on diffusion-limited mass transfer described by the Stokes-Einstein relation:
$$
D = \frac{k_BT}{6\pi\eta r}
$$

where
- D is the diffusivity
- $\eta$ the viscosity
- $r$ the hydrodynamic radius

Since molecular radius scales approximately as $r \propto M^{1/3}$, diffusivity decreases with molecular weight following $D \propto M^{-1/3}$. Consequently, the characteristic equilibration time over distance $L$ is 
$\tau \sim \frac{L^{2}}{D} \propto M^{1/3}$, implying that heavier molecules require longer extraction times. Assuming a reference molecule (benzene, $M_0 = 78 \ g \ mol^{-1}$) equilibrates in 10 min, the equilibration time scales as:

$$
\tau(M) = \tau_{0}\sqrt[3]{\left( M/M_0\right)}
$$

This yields characteristic times of approximately 20 min for M = 100, 30 min for M = 300 and 60 min for M = 600 $g \ mol^{-1}$, matching the:

- 10 - 20 min
- 20 - 30 min
- 30 - 60 min

extraction time bands used in the algorithm. The breakpoints at 100 $g \ mol^{-1}$ and 300 $g \ mol^{-1}$thus correspond to equal logarithmic increments in equilibration time.

This scaling is consistent with diffusion-limited SPME kinetics, where larger analytes exhibit reduced mass transfer and require proportionally longer extraction durations. Empirical guidelines (Sigma-Aldric, 2024) report 10-20 min for low-molecular-weight volatiles and 20-30 min for higher-molecular-weight semivolatiles, supporting the theoretical model.

---

### References 

[**α**] E. Martendal, E. Carasek, A new optimization strategy for gaseous phase sampling by an internally cooled solid-phase microextraction technique, Journal of Chromatography A,
Volume 1218, Issue 3, 2011, Pages 367-372, [DOI](https://doi.org/10.1016/j.chroma.2010.11.041).

[**β**] I. Déléris, I. Andriot, M, Gobet, C. Moreau, I. Souchon, E. Guichard, Determination of aroma compound diffusion in model food systems: Comparison of macroscopic and microscopic methodologies, Journal of Food Engineering, Volume 100, Issue 3, 2010, Pages 557-566, [DOI](https://doi.org/10.1016/j.jfoodeng.2010.05.006).

[**γ**] Shirey, R. (n.d.). Selecting the appropriate SPME fiber coating – Effect of analyte molecular weight and polarity. Sigma-Aldrich. Retrieved, [WEBPAGE](https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/analytical-chemistry/solid-phase-microextraction/selecting-the-appropriate?srsltid=AfmBOopJx9vw3a-CEHJDvn8JYBE6Y).
