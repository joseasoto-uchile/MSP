# Strict Bibliographic and BibTeX Audit Plan

Based on the explicit rules and the discrepancies you highlighted, I have conducted a deep review of the `papers_metadata.json` data currently feeding the website. Due to connection resets with DBLP's API, I have cross-referenced the metadata using web searches and manual verification to build this audit plan.

## C. Problematic Papers Report

### 1. Kesselheim, Radke, Tönnis, Vöcking
*   **What is currently wrong:** The page lists the venue as SODA 2013 and the title as "An optimal online algorithm for bipartite matching and generalizations to matroids".
*   **Correct versions that exist:** 
    *   Conference: ESA 2013 (Title: *An Optimal Online Algorithm for Weighted Bipartite Matching and Extensions to Combinatorial Auctions*).
    *   arXiv: CoRR 2013.
*   **Correct display structure:** Single entry. Bulleted versions: "arXiv version", "ESA 2013 version".
*   **Current rule failure:** Yes. Listed as SODA 2013 with a single incorrect BibTeX block.

### 2. Oveis Gharan & Vondrák
*   **What is currently wrong:** The visible text says "Algorithmica 2013" but the BibTeX provided is exclusively the CoRR preprint. 
*   **Correct versions that exist:** arXiv, ESA 2011, Algorithmica 2013.
*   **Current rule failure:** Yes. The required separate BibTeX blocks for ESA and Algorithmica are missing.

### 3. Huynh & Nelson
*   **What is currently wrong:** Shows only the CoRR 2016 BibTeX block.
*   **Correct versions that exist:** arXiv, SIAM J. Discrete Math. 2020.
*   **Current rule failure:** Yes. Missing the journal BibTeX block.

### 4. Dinitz & Kortsarz
*   **What is currently wrong:** Only the SODA 2013 block is present.
*   **Correct versions that exist:** arXiv, SODA 2013, SIAM J. Comput. 2014.
*   **Current rule failure:** Yes. Missing the journal BibTeX block.

### 5. Jaillet, Soto, Zenklusen
*   **What is currently wrong:** Shows only IPCO 2013 block.
*   **Correct versions that exist:** arXiv, IPCO 2013, Math. Oper. Res. 2016.
*   **Current rule failure:** Yes. Missing the journal BibTeX block.

### 6. Soto, Turkieltaub, Verdugo
*   **What is currently wrong:** Showed only the Math. Oper. Res. 2021 block.
*   **Correct versions that exist:** arXiv, SODA 2018, Math. Oper. Res. 2021.
*   **Current rule failure:** Yes. Missing the conference BibTeX block.

### 7. Feldman, Svensson, Zenklusen
*   **What is currently wrong:** Earlier iterations favored the CoRR preprint.
*   **Correct versions that exist:** arXiv, SODA 2015, SIAM J. Comput. 2022 (note: they recently published the journal version).
*   **Current rule failure:** Yes. Missing the SODA/SIAM blocks.

### 8. Lachish (2014)
*   **What is currently wrong:** Only showed CoRR.
*   **Correct versions that exist:** arXiv, FOCS 2014.
*   **Current rule failure:** Yes. Missing the FOCS BibTeX block.

### 9. Ma, Tang, Wang
*   **What is currently wrong:** Missing the Theory of Computing Systems journal block.
*   **Correct versions that exist:** arXiv, STACS 2013, Theory Comput. Syst. 2016.

---

## D. Master List of All BibTeX / Bibliographic Errors

*   [ ] **Wrong venue:** Kesselheim et al. (Listed as SODA, is actually ESA).
*   [ ] **Wrong title:** Kesselheim et al. (Missing "Weighted" and "Extensions to Combinatorial Auctions").
*   [ ] **Missing journal version (BibTeX):** Dinitz & Kortsarz (SICOMP), Huynh & Nelson (SIDMA), Jaillet et al. (MOR), Ma et al. (ToCS), Oveis Gharan & Vondrák (Algorithmica), Feldman et al. (SICOMP).
*   [ ] **Missing conference version (BibTeX):** Soto et al. (SODA), Oveis Gharan & Vondrák (ESA), Lachish (FOCS).
*   [ ] **Displayed version and BibTeX mismatch:** Oveis Gharan & Vondrák (Text says Algorithmica, BibTeX gives CoRR).
*   [ ] **Failure to provide multiple BibTeX blocks:** *ALL* the multi-version papers currently fail to provide distinct, separate BibTeX blocks inside the `bibtex-container` div. They only provide a single block.

---

## Proposed Implementation

1. **Update `generate_html.py`:** I will modify the HTML generation so that if the `bibtex` key in JSON is an array of strings (e.g., `["@inproceedings{...}", "@article{...}"]`), it will render them as strictly separate blocks (separated by empty lines or multiple `<pre>` tags) inside the single entry.
2. **Update `papers_metadata.json`:** I will manually execute a Python patching script to inject the missing DBLP BibTeX blocks (conference and journal) for all the problematic papers listed above, ensuring no duplicates are created and that they map 1:1 with the bulleted versions list already present below the titles.
3. **Fix Kesselheim:** Completely replace the metadata for Kesselheim to correctly reflect ESA 2013 and its precise title.

## User Review Required
> [!IMPORTANT]
> Please review the Master List of Errors and the Problematic Papers report. If this audit aligns with your expectations, please approve so I can execute the Python scripts to permanently patch the JSON metadata and HTML generator!
