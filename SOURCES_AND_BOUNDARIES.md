# Data and model provenance

**Inputs:** The two parameter snapshots are transcriptions from historical user-supplied educational equity-valuation files. This public repository deliberately does **not** redistribute course templates, cohort files, unredacted spreadsheets or third-party material. The original source workbooks remain private to their owner.

- `data/later_model.json`: `FSF_Reliance_Yuktha_Project5_completed(1).xlsx`, `PROJECT4`, market reference 28 Aug 2026.
- `data/older_scenario.json`: `Reliance_Project4_Completed_OneSheet.xlsx`, market reference 25 Aug 2026.
- Cross-reference: `P4_DCF_Valuation.pdf` academic project report.
- The data were **not obtained through a live API** when the public repository was prepared. File-level computations are reproduced, but underlying issuer amounts, comparable-company calculations, and external price sources require independent historical reconciliation.

**Original cited public sources (from coursework):**

- Reliance FY2025-26 report: https://www.ril.com/ar2025-26/
- Reliance Financial Performance: https://www.ril.com/ar2025-26/financial-performance-and-review.html
- RIL financial reporting: https://www.ril.com/investors/financial-reporting
- Market reference quote was recorded in the analyst workbook; it is **not a current price**: https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI
- India risk-free rate historical data source cited in workbook: https://in.investing.com/rates-bonds/india-10-year-bond-yield-historical-data
- Damodaran country risk premiums cited in model: https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/ctryprem.html

**Analyst judgments, not factual market data:** projected FY27–FY31 revenue growth, EBITDA margins, D&A, capital expenditures, reinvestment, terminal growth, risk-free, beta, ERP, debt rate and comparables are point-in-time inputs and may be unreliable.

**Important audit:** the later Project 5 investment-thesis worksheet states 85% DCF + 10% P/E + 5% EV/EBITDA while listing an approximately ₹1,453 target. Recomputing its published method outputs produces approximately ₹1,420.52, a difference around ₹32.48. Therefore **no ₹1,453 investment target is claimed or presented as verified**. Peer multiples are not independently reconciled in this repository.

Not investment advice; no real-time trading recommendation or proprietary financial data.
