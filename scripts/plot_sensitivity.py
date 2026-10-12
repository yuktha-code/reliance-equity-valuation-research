"""Optional matplotlib figure generation from model's own sensitivity computations."""
from pathlib import Path
import matplotlib.pyplot as plt
from src.valuation import read_json,main_dcf,sensitivity_grid
root=Path(__file__).resolve().parents[1]
d=read_json(root/'data/later_model.json'); result=main_dcf(d)
x=[i+1 for i in range(5)]
y=[row['fcff'] for row in result['forecast']]
fig,ax=plt.subplots(figsize=(8.4,4.2))
ax.plot(x,y,marker='o',linewidth=2)
ax.set_xticks(x, d['forecast_years']); ax.set_ylabel('Modeled FCFF (₹ crore)')
ax.set_title('Reliance: Dated 2026 analyst FCFF scenario (illustrative)')
ax.grid(alpha=.25); fig.tight_layout()
fig.savefig(root/'figures/fcff_forecast.png',dpi=160);plt.close(fig)
ws=[.10,.105,.11,.115,.12]; gs=[.025,.03,.035]
z=[[main_dcf(d,wacc_override=w,terminal_growth_override=g)['fair_value_per_share'] for g in gs] for w in ws]
fig,ax=plt.subplots(figsize=(7.5,4.3))
im=ax.imshow(z,aspect='auto')
ax.set_xticks(range(len(gs)),[f'{g:.1%}' for g in gs]); ax.set_yticks(range(len(ws)),[f'{w:.1%}' for w in ws]);ax.set_xlabel('Terminal growth assumption');ax.set_ylabel('WACC assumption')
for i in range(len(ws)):
 for j in range(len(gs)):
  ax.text(j,i,f'₹{z[i][j]:,.0f}',ha='center',va='center',color='white' if z[i][j]<1100 else 'black',fontsize=9)
ax.set_title('DCF sensitivity: per-share value (illustrative)');fig.colorbar(im,ax=ax,label='₹/share');fig.tight_layout()
fig.savefig(root/'figures/wacc_terminal_sensitivity.png',dpi=160);plt.close(fig)
