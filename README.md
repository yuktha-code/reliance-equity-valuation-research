# Reliance Industries | Reproducible DCF and Equity Research Review

[![DCF and valuation checks](https://github.com/yuktha-code/reliance-equity-valuation-research/actions/workflows/ci.yml/badge.svg)](https://github.com/yuktha-code/reliance-equity-valuation-research/actions/workflows/ci.yml)

**Independent calculation notebook-equivalent** that reconstructs two dated FCFF/DCF scenarios found in previous finance apprenticeship workbooks. Unlike a generic DCF template, the repository includes original dated input snapshots, source notes, an explicit revenue/operating forecast, a debt-to-equity bridge and **18 automated numerical checks**. The central purpose is transparent *reconciliation*, not a buy/sell recommendation.

## Primary dated result: 28 August 2026 analytical scenario

- Forecast FY27–FY31: revenue growth **9.0% to 7.0%**, 18.5% EBITDA margin, 5.5% normalized capex/revenue, 0.5% reinvestment/revenue.
- CAPM inputs: risk-free 6.913%, beta 0.93, equity risk premium 6.0%; implied cost of equity 12.493%.
- Debt cost 7.497% pre-tax; capital weights 82.306% equity / 17.694% debt, effective tax rate 22.4%.
- Computed WACC **11.3118%**, terminal growth **3.5%**.
- PV FY27–FY31 FCFF ≈ **₹508,928 crore**; PV terminal ≈ **₹1,256,434 crore**; DCF EV ≈ **₹1,765,362 crore**.
- Less gross debt ₹374,421 crore, add cash ₹145,977 crore, divide by 1,353.246 crore diluted shares: **~₹1,135.73 per share**, versus dated **₹1,287** price reference.

All these figures are derived from **analyst assumptions recorded in coursework**, not an exchange-grade historical fundamentals feed or an updated valuation today. See [`SOURCES_AND_BOUNDARIES.md`](SOURCES_AND_BOUNDARIES.md).

## Why another version reported ₹517.48

An earlier 25 August 2026 workbook uses lower modeled free cash flows due in large part to materially higher initial capex assumptions (11.5% gradually to 9.5% of revenue), a different terminal-growth assumption of 4.5%, and slightly different capital costs. Its calculated outcome is **~₹517.48 per share**. Both models are reproduced **independently**; numbers from these scenarios must not be combined. The earlier outcome is not a correction of the later one or evidence that the market fundamentally moved.

## Project 5 issue found during audit

The later research workbook combines three valuation methods using a declared 85% DCF / 10% P/E / 5% EV/EBITDA mix. Using the workbook's own values gives **~₹1,420.52**, not its stated ₹1,453 target. That mismatch is documented and explicitly **not treated as an investment prediction**. More information in [`SOURCES_AND_BOUNDARIES.md`](SOURCES_AND_BOUNDARIES.md).

## Reproduce with Python 3.11+

```bash
python -m unittest discover -s tests -v
python -m src.valuation
python -m scripts.plot_sensitivity  # optional: pip install matplotlib
```

No external data download or Python dependencies are required for the DCF itself. Script writes `results/model_output.json`, including a WACC/terminal-growth sensitivity grid. For changes to inputs, edit `data/later_model.json` and rerun. Formula validation, monotonicity and independent prior-scenario reconciliation are in `tests/test_valuation.py`.

## Source files and intellectual-property precautions

The original First Step Finance project workbooks were used for a private audit. **They are not uploaded to this public repository**: only transcribed numerical assumptions and original public-safe calculation code are included. This project does not claim complete company/peer financial statement verification, real Azure/Bloomberg/API connectivity, live share prices, executed trades, or profitable investment decisions.

## For interviews

Explain the bridge from market capitalization to EV vs the DCF EV-to-equity bridge, WACC and its tax shield, why normalized capex changes FCFF, discounting convention and terminal-value share, forecasting assumptions, and why simple P/E/EV-EBITDA comparables are weak when business mixes diverge.
