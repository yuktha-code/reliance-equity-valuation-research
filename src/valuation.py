"""Independent deterministic DCF reproducer for the dated analyst scenarios.

All monetary amounts are INR crore. Historical assumptions come from supplied
academic-workbook versions; code makes no independent source-verification claim.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def validate_main(d: dict[str, Any]) -> None:
    if len(d['forecast_years']) != 5 or len(d['revenue_growth']) != 5:
        raise ValueError('Exactly five forecast years and growth rates required')
    if any(not (-1 < g < 1) for g in d['revenue_growth']):
        raise ValueError('Implausible growth assumption')
    for k in ('fy26_revenue','gross_debt','cash_equivalents','diluted_shares_crore'):
        if float(d[k]) <= 0: raise ValueError(k+' must be positive')
    for k in ('ebitda_margin','da_revenue_ratio','effective_tax_rate',
              'capex_revenue_ratio','nwc_investment_revenue_ratio','terminal_growth_rate'):
        if not 0 <= d[k] < 1: raise ValueError('Invalid ratio: '+k)
    if d['equity_weight'] < 0 or d['debt_weight'] < 0 or abs(d['equity_weight']+d['debt_weight']-1)>1e-8:
        raise ValueError('Capital-structure weights must sum to one')
    if not (0 < d['pretax_cost_of_debt'] < 1 and 0 < d['equity_risk_premium'] < 1):
        raise ValueError('Invalid funding assumptions')


def main_dcf(d: dict[str, Any], *, wacc_override: float | None = None,
             terminal_growth_override: float | None = None) -> dict[str, Any]:
    validate_main(d)
    cost_equity = d['risk_free_rate'] + d['beta']*d['equity_risk_premium']
    cost_debt_after_tax = d['pretax_cost_of_debt']*(1-d['effective_tax_rate'])
    base_wacc=d['equity_weight']*cost_equity+d['debt_weight']*cost_debt_after_tax
    wacc=base_wacc if wacc_override is None else float(wacc_override)
    g=d['terminal_growth_rate'] if terminal_growth_override is None else float(terminal_growth_override)
    if wacc <= g: raise ValueError('WACC must exceed terminal growth')
    if wacc <= -1: raise ValueError('Discount factor must be well defined')
    revenue=float(d['fy26_revenue'])
    forecasts=[]
    for n,(year,growth) in enumerate(zip(d['forecast_years'],d['revenue_growth']),1):
        revenue*=(1+growth)
        ebitda=revenue*d['ebitda_margin']
        da=revenue*d['da_revenue_ratio']
        ebit=ebitda-da
        nopat=ebit*(1-d['effective_tax_rate'])
        capex=revenue*d['capex_revenue_ratio']
        nwc=revenue*d['nwc_investment_revenue_ratio']
        fcff=nopat+da-capex-nwc
        discount=1/(1+wacc)**n
        forecasts.append({'year':year,'revenue':revenue,'ebitda':ebitda,'da':da,
                         'ebit':ebit,'nopat':nopat,'capex':capex,'nwc_investment':nwc,
                         'fcff':fcff,'discount_factor':discount,'pv_fcff':fcff*discount})
    pv_explicit=sum(r['pv_fcff'] for r in forecasts)
    terminal=forecasts[-1]['fcff']*(1+g)/(wacc-g)
    pv_terminal=terminal*forecasts[-1]['discount_factor']
    enterprise=pv_explicit+pv_terminal
    equity=enterprise-d['gross_debt']+d['cash_equivalents']
    price=equity/d['diluted_shares_crore']
    return {'wacc':wacc,'cost_equity':cost_equity,'after_tax_cost_of_debt':cost_debt_after_tax,
            'terminal_growth':g,'forecast':forecasts,'pv_explicit':pv_explicit,
            'terminal_value':terminal,'pv_terminal':pv_terminal,
            'terminal_value_pv_share':pv_terminal/enterprise,
            'enterprise_value':enterprise,'equity_value':equity,'fair_value_per_share':price,
            'market_reference_price':d['market_price_reference'],
            'implied_upside_downside':price/d['market_price_reference']-1}


def older_scenario_dcf(d: dict[str, Any]) -> dict[str,float]:
    fcff=d['fcff_forecast']; wacc=d['wacc'];g=d['terminal_growth_rate']
    if len(fcff)!=5 or wacc<=g: raise ValueError('Invalid earlier scenario')
    pv_explicit=sum(x/(1+wacc)**i for i,x in enumerate(fcff,1))
    terminal=fcff[-1]*(1+g)/(wacc-g)
    pv_terminal=terminal/(1+wacc)**5
    ev=pv_explicit+pv_terminal
    eq=ev-d['gross_debt']+d['cash_equivalents']
    return {'pv_explicit':pv_explicit,'terminal_value':terminal,'pv_terminal':pv_terminal,
            'enterprise_value':ev,'equity_value':eq,'fair_value_per_share':eq/d['diluted_shares_crore']}


def sensitivity_grid(d: dict[str, Any], wacc_values: list[float], terminal_g_values:list[float]):
    return [{'wacc':w,'terminal_growth':g,'fair_value_per_share':main_dcf(d,wacc_override=w,terminal_growth_override=g)['fair_value_per_share']}
            for w in wacc_values for g in terminal_g_values]


def project5_target_reconciliation(d: dict[str, Any]) -> dict[str, float]:
    """Project 5 workbook output review: this is arithmetic reconciliation, not a forecast."""
    r=main_dcf(d)
    pe_target=2614.777443017076
    evebitda_target=3873.579499068972
    calculated=0.85*r['fair_value_per_share']+0.10*pe_target+0.05*evebitda_target
    stated=1453.0
    return {'workbook_stated_target':stated,'target_from_declared_85_10_5_weights':calculated,
            'difference_stated_minus_recomputed':stated-calculated,
            'source_note':'The PROJECT5 stated target and declared weights disagree; not an endorsed target.'}


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    model=read_json(root/'data/later_model.json')
    report={'scenario':'Later Project4 base case', 'results':main_dcf(model),
            'sensitivity':sensitivity_grid(model,[.10,.105,.11,.115,.12],[.025,.03,.035]),
            'project5_reconciliation':project5_target_reconciliation(model),
            'older_scenario':older_scenario_dcf(read_json(root/'data/older_scenario.json'))}
    target=root/'results/model_output.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"Later scenario DCF ₹{report['results']['fair_value_per_share']:.2f} per share")
    print(f"Earlier scenario DCF ₹{report['older_scenario']['fair_value_per_share']:.2f} per share")
    print(f"Project 5 stated weighted target ₹{report['project5_reconciliation']['workbook_stated_target']:.2f} vs computed ₹{report['project5_reconciliation']['target_from_declared_85_10_5_weights']:.2f}")
