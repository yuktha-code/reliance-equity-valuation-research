import unittest
from pathlib import Path
from copy import deepcopy
from src.valuation import read_json,main_dcf,older_scenario_dcf,sensitivity_grid,project5_target_reconciliation

ROOT=Path(__file__).resolve().parents[1]
D=read_json(ROOT/'data/later_model.json')
OLDER=read_json(ROOT/'data/older_scenario.json')

class DCFTests(unittest.TestCase):
    def setUp(self): self.r=main_dcf(D)
    def test_reference_wacc(self): self.assertAlmostEqual(self.r['wacc'],D['workbook_reference']['wacc'],places=11)
    def test_wacc_weights(self): self.assertAlmostEqual(D['equity_weight']+D['debt_weight'],1,places=12)
    def test_fy27_revenue(self): self.assertAlmostEqual(self.r['forecast'][0]['revenue'],1281751.71,places=2)
    def test_fy27_fcff(self): self.assertAlmostEqual(self.r['forecast'][0]['fcff'],120229.37548951432,places=6)
    def test_discount_factor(self): self.assertAlmostEqual(self.r['forecast'][-1]['discount_factor'],1/(1+self.r['wacc'])**5,places=12)
    def test_explicit_pv_matches_workbook(self): self.assertAlmostEqual(self.r['pv_explicit'],D['workbook_reference']['pv_forecast_fcff'],delta=.001)
    def test_terminal_value_matches_workbook(self): self.assertAlmostEqual(self.r['terminal_value'],D['workbook_reference']['terminal_value'],places=5)
    def test_ev_matches_workbook(self): self.assertAlmostEqual(self.r['enterprise_value'],D['workbook_reference']['enterprise_value'],delta=.001)
    def test_per_share_matches_workbook(self): self.assertAlmostEqual(self.r['fair_value_per_share'],D['workbook_reference']['per_share'],delta=.0001)
    def test_debt_cash_equity_bridge(self): self.assertAlmostEqual(self.r['equity_value'],self.r['enterprise_value']-374421+145977,places=6)
    def test_price_return_reference(self): self.assertAlmostEqual(self.r['implied_upside_downside'],-.11753931020071684,delta=.00001)
    def test_growth_below_wacc(self):
        with self.assertRaises(ValueError):main_dcf(D,wacc_override=.03,terminal_growth_override=.04)
    def test_monotonic_wacc(self):
        self.assertGreater(main_dcf(D,wacc_override=.10)['fair_value_per_share'],main_dcf(D,wacc_override=.12)['fair_value_per_share'])
    def test_monotonic_growth(self):
        self.assertGreater(main_dcf(D,terminal_growth_override=.035)['fair_value_per_share'],main_dcf(D,terminal_growth_override=.025)['fair_value_per_share'])
    def test_invalid_share_count(self):
        d=deepcopy(D);d['diluted_shares_crore']=0
        with self.assertRaises(ValueError):main_dcf(d)
    def test_earlier_case_independently_reproduced(self):
        old=older_scenario_dcf(OLDER)
        self.assertAlmostEqual(old['fair_value_per_share'],OLDER['workbook_reference_per_share'],delta=.001)
        self.assertAlmostEqual(old['enterprise_value'],OLDER['workbook_reference_ev'],delta=.001)
    def test_sensitivity_grid(self): self.assertEqual(len(sensitivity_grid(D,[.10,.11,.12],[.025,.03,.035])),9)
    def test_project5_stated_target_is_not_weighted_output(self):
        rec=project5_target_reconciliation(D)
        self.assertAlmostEqual(rec['target_from_declared_85_10_5_weights'],1420.5245909,places=4)
        self.assertGreater(abs(rec['difference_stated_minus_recomputed']),30)

if __name__ == '__main__': unittest.main()
