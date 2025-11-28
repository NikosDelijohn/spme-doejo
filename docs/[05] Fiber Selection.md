## How does DoEjo perform `Fiber Selection`?

Fiber selection is governed by the analyte’s polarity and volatility, expressed through its octanol–water partition coefficient ($logP$ or $XLogP$). The objective is to maximize the fiber–water distribution coefficient $K_{f/w}$, which determines extraction efficiency. For nonpolar PDMS coatings, the relationship between $K_{f/w}$ and $K_{ow}$ follows:

$$
log⁡K_{f/w} = 0.92 \times log ⁡K_{ow} - 0.45 \ (R^2=0.98) \ \text{\textbf{[α]}} 
$$

A threshold of $log⁡K_{f/w} > 4$ ($\approx$ 90 % recovery in 30 min) corresponds to $log⁡P>3.0$. For mid-polarity mixed coatings such as PDMS/DVB and for more polar phases (PA or PEG), regression intersections occur near $log⁡P \approx 1.5$ and $log⁡P \approx 3.0$, consistent with manufacturer guidelines **[β]** and QSPR models **[γ]**.

Accordingly, the algorithm uses the **maximum** $XLogP$ among the analytes to classify optimal fiber polarity:

- **PDMS** (7–100 µm) — Nonpolar phase for hydrophobic, high-molecular-weight or semi-volatile analytes ($XLogP>3.0$). Provides strong absorption and thermal stability for long-chain hydrocarbons, alkanes, and aromatic compounds (typical $ M= 125 - 600 \ Da$).

- **PDMS/DVB** (65 µm) — Biphasic (absorption + adsorption) coating suitable for moderately polar compounds ($1.5 < XLogP \leq 3.0$). The DVB layer increases surface area and retention of small to mid-volatility species such as phenols, esters, and amines.

- **DVB/CAR/PDMS** (50/30 µm) — Multimodal composite phase providing broad selectivity from highly volatile to semi-volatile organics ($0.5<XLogP<3.0$).
The CAR micropores trap small molecules (< C₆), while the DVB and PDMS layers capture higher-mass volatiles, making this coating optimal for complex or mixed matrices.

- **CW/DVB/PA** — Polar composite phase designed for low-molecular-weight, hydrophilic compounds ($XLogP≤1.5$). The carbowax and polyacrylate components enhance hydrogen-bonding interactions and extraction of alcohols, organic acids, and aldehydes.

- **CAP-PDMS/PEG/CW** — Highly polar, hydrophilic coating for ionic, charged, or very low-volatility compounds ($XLogP \lesssim 1.0$ and $M < 200 \  Da$ ).

This coating targets strongly polar analytes such as short-chain acids, small amines, or environmental micropollutants that are poorly retained on conventional fibers. 

In this framework, fiber selection follows a monotonic polarity hierarchy: 

PDMS → PDMS/DVB → DVB/CAR/PDMS → CW/DVB/PA → CAP-PDMS/PEG/CW

with transition thresholds at XLogP ≈ 3.0, 1.5, and 1.0. This quantitative mapping reproduces manufacturer performance charts and maintains strong correlation with the calculated partition coefficients that govern extraction sensitivity.

---

### References:

[**α**] A. Paschke, P. Popp, Solid-phase microextraction fibre–water distribution constants of more hydrophobic organic compounds and their correlations with octanol–water partition coefficients, Journal of Chromatography A, Volume 999, Issues 1–2, 2003, Pages 35-42, [DOI](https://doi.org/10.1016/S0021-9673(03)00538-7).

[**β**] SPME for GC Analysis, Getting Started with Solid Phase Microextraction, Supelcro [PDF](http://www.supelco.com.tw/C-01-SPME-FIber.pdf).

[**γ**] C. Lancioni, C. Castells, R. Candal, M. Tascon, Headspace solid-phase microextraction: Fundamentals and recent advances, Advances in Sample Preparation, Volume 3, 2022, 100035, [DOI](https://doi.org/10.1016/j.sampre.2022.100035).

---

### Index

❓[Home](Home.md)\
❓[How does DoEjo compute the **Agitation Rate** parameter? 
](agitation_rate.md)\
❓[How does DoEjo compute the **Extraction Temperature** parameter? ](extraction_temperature.md)\
❓[How does DoEjo compute the **Extraction Time** parameter?](extraction_time.md)\
❓[How does DoEjo compute the **Salt Addition** parameter? ](salt_addition.md)\
✅[How does DoEjo perform **Fiber Selection**?](fiber_selection.md)\
❓[Information about **BBD Center Points**](bbd_centers.md)