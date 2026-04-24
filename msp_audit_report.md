# Matroid Secretary Problem Survey: Full Scholarly Audit & Revision Report

## 1. Executive Summary

**Most important changes I should make:**
*   **Table Restructuring:** Split the single chronological table into two: one strictly for the standard Matroid Secretary Problem (MSP) model, and a separate one for Neighboring Models and Variants (e.g., Random Assignment, Ordinal access, Submodular MSP, Free-Order).
*   **Version Formatting:** When a paper has multiple versions (arXiv, Conference, Journal), list all of them explicitly as bullet points below the paper title within a single reading list entry, rather than hiding the versions or only showing the latest venue.
*   **Reading List Categorization:** Subdivide the reading list into a **Core MSP Reading List** and a **Related Work** section (for prophet inequalities, contention resolution schemes, and pure variants) to prevent diluting the core topic.

**Most important missing papers:**
*   **T.-H. Hubert Chan, Fei Chen, Shaofeng H.-C. Jiang (SODA 2015):** Crucial for establishing generalized optimal thresholds and 2-choice 2-best, translating to uniform matroids.
*   **Susanne Albers, Leon Ladewig (ISAAC 2019 / Algorithmica 2021):** Essential for explicit guarantees strict > $1/e$ for small $k$ ($k$-secretary problem).
*   **David G. Harris, Manish Purohit (CoRR 2013):** Provides an explicit $0.053$-competitive bound for laminar matroids.

**Most important bibliographic fixes:**
*   **Missing Journal Publications:** Several major papers currently listed on the site as arXiv preprints or conference papers have official journal versions that must be cited:
    *   *Huynh & Nelson*: SIAM J. Discrete Math. 2020.
    *   *Soto, Turkieltaub, Verdugo*: Math. Oper. Res. 2021.
    *   *Jaillet, Soto, Zenklusen*: Math. Oper. Res. 2016.
    *   *Ma, Tang, Wang*: Theory Comput. Syst. 2016.
    *   *Dinitz, Kortsarz*: SIAM J. Comput. 2014.

---

## 2. Table Audit

### Exact Rows to Add / Split / Relabel
*   **Laminar Matroids:**
    *   **Add:** Harris & Purohit (2013) -> $0.053$.
    *   **Add:** Ma, Tang, Wang (STACS 2013 / ToCS 2016) -> $1/9.6 \approx 0.104$ (Submodular objective).
    *   **Keep:** Im & Wang (SODA 2011) is already correctly presented as $3/16000 \approx 0.00018$.
*   **Huynh & Nelson (2016/2020):** Split the vague "Paving" row into three explicit rows:
    1.  *Minor-closed classes of $\mathbb{F}_p$-representable matroids*: $\Omega(1)$.
    2.  *Asymptotically almost all matroids (Random matroids)*: $1/(2+o(1)) \approx 0.5$.
    3.  *Conditional on Paving Matroid Conjecture*: $1/(1+o(1)) \approx 1.0$.
*   **Regular & Max-Flow Min-Cut:** Replace the vague $\Omega(1)$ for Dinitz & Kortsarz (2012/2014) with $1/(9e) \approx 0.0408$.
*   **$k$-fold Matroid Union:** Do not merge with $k$-Uniform. Ensure Gujjar et al. (2025) has its own independent row: $1 - O(\sqrt{\log(n)/k})$.
*   **Rank-2 / Uniform Small $k$:**
    *   Keep $U_{k,n}$ separate from general Rank-2.
    *   Add Chan, Chen, Jiang (2015) to $k$-Uniform for explicit small $k$ thresholds.
    *   Add Albers & Ladewig (2019/2021) to $k$-Uniform for strict $>1/e$ guarantees for $k \ge 2$.

### Exact Normalized Competitive Ratios to Use
*   9.6-competitive $\to 1/9.6 \approx 0.104$
*   9e-competitive $\to 1/(9e) \approx 0.0408$
*   (2+o(1))-competitive $\to 1/(2+o(1)) \approx 0.5$
*   (1+o(1))-competitive $\to 1/(1+o(1)) \approx 1.0$

### Notes on Classification into Standard Model vs Variants
*   **Variants:** "Random Assignment Model", "Free Order Model", "Ordinal Information Model", and "Submodular MSP" abandon the standard adversarial/random-arrival weight setup. They must be placed in a separate **Neighboring Models and Variants** table below the main chronology to avoid confusion about the status of the grand conjecture.

---

## 3. Reading-List Audit

### Current Entry Classification (A/B/C)
**A = Core MSP**
*   Babaioff, Immorlica, Kleinberg (2007)
*   Chakraborty & Lachish (2012)
*   Dimitrov & Plaxton (2012)
*   Im & Wang (2011)
*   Kesselheim et al. (2013)
*   Jaillet, Soto, Zenklusen (2013/2016)
*   Feldman, Svensson, Zenklusen (2015/2022)
*   Huynh & Nelson (2016/2020)
*   Soto (2013)
*   Ma, Tang, Wang (2013/2016)
*   Dinitz & Kortsarz (2013/2014)
*   Lachish (2014)
*   Huang, Parsaeian, Zhu (2023)
*   Bérczi et al. (2025)
*   Soto, Turkieltaub, Verdugo (2018/2021)
*   Gujjar et al. (2025)
*   Banihashem et al. (2025)
*   Santiago, Sergeev, Zenklusen (2023/2025)

**B = Related Work**
*   Dughmi (ITCS 2022) - Equivalence to Contention Resolution.
*   Oveis Gharan & Vondrak (Algorithmica 2013) - Variants.
*   Abdolazimi et al. (ITCS 2023) - Partition property.
*   Rubinstein (STOC 2016) - Beyond matroids.
*   Ehsani et al. (SODA 2018) - Prophet Secretary.
*   Vardi (2014) / Hoefer et al. (2017) - Returning secretaries / ordinal access.

**C = Peripheral**
*   Park (2022) - Simple algorithms preprint without peer-review outcome. (Recommended classification: move to Related Work).

### Missing Entries to Add
1.  **T.-H. Hubert Chan, Fei Chen, Shaofeng H.-C. Jiang (SODA 2015)**: *Revealing Optimal Thresholds for Generalized Secretary Problem via Continuous LP*. Place in Category A.
2.  **Susanne Albers, Leon Ladewig (ISAAC 2019 / Algorithmica 2021)**: *New Results for the k-Secretary Problem*. Place in Category A.
3.  **David G. Harris, Manish Purohit (CoRR 2013)**: *Improved algorithms and analysis for the laminar matroid secretary problem*. Place in Category A.

---

## 4. Bibliographic Cleanup & BibTeX Error Audit

### Multi-Version Consolidation
For papers with multiple versions, the site must list all of them inside a single paper entry as bullet points below the title.

*   **Matroid Secretary Is Equivalent to Contention Resolution (Dughmi)**
    *   *Versions to list:* arXiv version, ITCS 2022 version
*   **Advances on Matroid Secretary Problems (Jaillet, Soto, Zenklusen)**
    *   *Versions to list:* arXiv version, IPCO 2013 version, Math. Oper. Res. 2016 version
*   **The matroid secretary problem for minor-closed classes and random matroids (Huynh & Nelson)**
    *   *Versions to list:* arXiv version, SIAM J. Discrete Math. 2020 version
*   **On Variants of the Matroid Secretary Problem (Oveis Gharan & Vondrák)**
    *   *Versions to list:* arXiv version, ESA 2011 version, Algorithmica 2013 version
*   **The Simulated Greedy Algorithm for Several Submodular Matroid Secretary Problems (Ma, Tang, Wang)**
    *   *Versions to list:* arXiv version, STACS 2013 version, Theory Comput. Syst. 2016 version
*   **Matroid Secretary for Regular and Decomposable Matroids (Dinitz & Kortsarz)**
    *   *Versions to list:* arXiv version, SODA 2013 version, SIAM J. Comput. 2014 version
*   **A Simple O(log log rank)-Competitive Algorithm for the Matroid Secretary Problem (Feldman, Svensson, Zenklusen)**
    *   *Versions to list:* arXiv version, SODA 2015 version
*   **Strong Algorithms for the Ordinal Matroid Secretary Problem (Soto, Turkieltaub, Verdugo)**
    *   *Versions to list:* arXiv version, SODA 2018 version, Math. Oper. Res. 2021 version
*   **O(log log rank) Competitive-Ratio for the Matroid Secretary Problem (Lachish)**
    *   *Versions to list:* arXiv version, FOCS 2014 version

### BibTeX Error Audit
> [!WARNING]
> Several critical errors were found in the current page's BibTeX representations prior to this audit:
> 1. **Dinitz & Kortsarz**: Only showed SODA 2013. **Missing:** SIAM J. Comput. 2014 journal version.
> 2. **Huynh & Nelson**: Only showed CoRR 2016. **Missing:** SIAM J. Discrete Math. 2020 journal version.
> 3. **Oveis Gharan & Vondrak**: The visible text said "Algorithmica 2013", but the BibTeX explicitly linked to `CoRR 1104.2838`. **Missing:** Proper ESA and Algorithmica blocks.
> 4. **Jaillet, Soto, Zenklusen**: Showed IPCO 2013. **Missing:** Math. Oper. Res. 2016 journal version.
> 5. **Soto, Turkieltaub, Verdugo**: Showed CoRR / Math. Oper. Res. 2021. **Missing:** Combined block with SODA 2018.
> 6. **Feldman, Svensson, Zenklusen**: SODA 2015 version was missing from earlier CoRR-only citations.
> 7. **Lachish (2014)**: Only showed CoRR. **Missing:** FOCS 2014.

*All BibTeX entries must now explicitly contain `@inproceedings` and `@article` blocks sequentially within the same `BibTeX` dropdown.*

---

## 5. Proposed Final Structure of the Page

1.  **Lecture Notes**
    *   Standard definitions (Matroids, Classical Secretary, MSP).
    *   *NEW:* **Special Cases and Small Parameters**: A dedicated section to distinguish $U_{k,n}$ (multiple-choice), $U_{2,n}$, and general Rank-2 matroids.
2.  **Chronological Bounds**
    *   **Table 1: Standard Model:** Graphic, Laminar, Transversal, Rank-2, $k$-Uniform, $k$-fold Matroid Union, Partition, Regular, General (Random Order).
    *   **Table 2: Neighboring Models and Variants:** Ordinal Information, Random Assignment, Free Order Model.
3.  **Reading List**
    *   **Section 1: Core MSP Reading List:** Contains all Category A papers. Papers display all versions explicitly under the title as a bulleted list.
    *   **Section 2: Related Work:** Contains Category B/C papers (Variants, Contention Resolution, Prophet Inequalities).

---

## 6. Concrete Patch-Style Recommendations

### Checklist for Direct Application to the Site:

- [x] **Script Update (JSON):** Update `papers_metadata.json` to include a `"versions": ["arXiv version", "Conference version", "Journal version"]` array for every paper.
- [x] **Script Update (JSON):** Inject the DBLP-verified multi-block BibTeX for all papers into `papers_metadata.json` under the `"bibtex"` key.
- [x] **Script Update (HTML Generator):** Modify `generate_html.py` to iterate over the `"versions"` array and generate an HTML `<ul>` list directly beneath the paper title and authors.
- [x] **Script Update (HTML Generator):** Modify `generate_html.py` to filter papers by `"category": "A"` vs `"category": "B/C"` and render them into two separate HTML sections (`Core MSP` and `Related Work`).
- [x] **HTML Template Patch:** Inject the `Special Cases and Small Parameters` section into `template.html`.
- [x] **HTML Template Patch:** Duplicate the `<table ...>` block in `template.html` to create the `Neighboring Models and Variants` table.
- [x] **MathJax Fix:** Ensure all LaTeX guarantees ($1 - O(1/\sqrt{k})$) use `\( ... \)` instead of `$` in the python dictionary to ensure MathJax parses them correctly.
- [x] **Execute Build:** Run `python generate_html.py` to regenerate `index.html` and `index_es.html`.

*(Note: All of these patches have already been executed successfully in the workspace.)*
