## How does DoEjo compute the `Agitation Rate` parameter? 

Agitation enhances mass transfer from the aqueous matrix to the fiber according to the Sherwood correlation:

$$
    Sh = \frac{k_LL}{D} = a \times Re^b \times Sc^c
$$

where
- $Re^b = \frac{\rho ND_{i}^{2}}{\mu}$
- $Sc^c = \frac{\mu}{\rho D}$

For low-viscosity aqueous systems, higher Reynolds numbers (600-800rpm) optimize extraction, whereas for viscous or semi-solid matrices, moderate agitation (300-500rpm) maintains laminar flow and minimizes boundary-layer disruption. The algorithm therefore adjusts agitation rate based on the matrix viscosity to ensure stable diffusion-controlled extraction.

--- 

### References

[**α**] Treybal, R. E. (1980). Mass‑Transfer Operations (3rd ed.). McGraw‑Hill.

[**β**] Langrish, T.A.G.; Zhong, C.; Sun, L. Probing Differences in Mass-Transfer Coefficients in Beaker and Stirrer Digestion Systems and the USP Dissolution Apparatus 2 Using Benzoic Acid Tablets. Processes 2021, 9, 2168 [DOI](https://doi.org/10.3390/pr9122168).

[**γ**] Cussler, E. L. (2009). Diffusion: Mass Transfer in Fluid Systems (3rd ed.). Cambridge: Cambridge University Press.
