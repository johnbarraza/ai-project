"""Verify and graph the November13 GE experiments for the final manuscript."""
from pathlib import Path
import hashlib
import json

import matplotlib.pyplot as plt
import numpy as np

from figures import BASE, BLUE, TEAL, ORANGE, GRID, style
from final_figures import save

HERE = Path(__file__).resolve().parent


def build_paper_results():
    source = HERE/'data/paper_ge_experiments.json'
    data = json.loads(source.read_text(encoding='utf-8'))
    groups = {name:[] for name in data['counts']}
    assert not data['full_precision_certification']
    for row in data['cases']:
        assert row['status'] == 'passed' and row['checks'] and all(row['checks'].values())
        assert (row['Na'],row['Nz'],row['amax']) == (400,40,40)
        assert row['hjb_residual'] < 1e-6 and row['kfe_residual'] < 1e-8
        assert row['closed_classes'] == 1 and row['row_error'] < 1e-10
        assert abs(row['capital_residual']) < .003 and abs(row['informal_goods_residual']) < 2e-4
        assert abs(row['formal_resource_residual']) < .002
        assert row['labor_diagnostics']['max_stationarity_error'] < 1e-6
        assert row['labor_diagnostics']['max_multiplier_sign_error'] < 1e-6
        assert row['labor_diagnostics']['max_time_error'] < 1e-8
        assert row['Va_max_increase_over_a'] < 0
        assets = np.asarray(row['assets'])
        assert len(assets)==400 and np.all(np.diff(assets)>0)
        for profile in row['profiles']:
            values = np.asarray(profile['informal_share'])
            assert values.shape == assets.shape and np.isfinite(values).all()
            assert np.all((values >= 0) & (values <= 1))
            if row['family'] in ('fixed_parameters','refit'):
                assert np.max(np.diff(values)) < 1e-8
        groups[row['family']].append(row)
    assert {k:len(v) for k,v in groups.items()} == {
        'fixed_parameters':8,'refit':7,'time_cap':6,'time_equality':2}
    fixed = sorted(groups['fixed_parameters'],key=lambda r:r['phi_I'])
    ref = fixed[0]
    assert ref['phi_I'] == .38
    old = json.loads((HERE/'data/ge_phi_continuation.json').read_text(encoding='utf-8'))
    assert {r['sha256'] for r in old['cases']} == {r['sha256'] for r in fixed}
    for row in groups['refit']:
        np.testing.assert_allclose([row['M1_informal_hours'],row['M3_formal_zmax_minus_zmin']],
                                   [ref['M1_informal_hours'],ref['M3_formal_zmax_minus_zmin']],
                                   atol=2e-4,rtol=0)
    refit = [ref,*sorted(groups['refit'],key=lambda r:r['phi_I'])]
    assert [r['phi_I'] for r in fixed] == [r['phi_I'] for r in refit]
    style()
    experiments = [(fixed,BASE,'--','Sin reajuste'),(refit,TEAL,'-','Reajuste M1/M3')]
    fig,axes = plt.subplots(1,2,figsize=(9.8,3.6))
    for rows,color,line,label in experiments:
        phi = [r['phi_I'] for r in rows]
        axes[0].plot(phi,[100*r['V3_assets_Q1_minus_Q5_fractional'] for r in rows],
                     color=color,ls=line,marker='o',label=label)
        axes[1].plot(phi,[100*r['M1_informal_hours'] for r in rows],color=color,ls=line,marker='o')
    for ax in axes:
        ax.set_xlabel(r'Elasticidad informal $\phi_I$')
        ax.set_xticks([.38,.50,.60,.70])
        ax.grid(axis='y',color=GRID)
    axes[0].set_ylabel('Brecha informal Q1−Q5 (pp)')
    axes[1].set_ylabel('Horas informales (%)')
    axes[0].legend(frameon=False,fontsize=11)
    save(fig,'paper_ge_sensitivity')

    fig,axes = plt.subplots(1,2,figsize=(9.8,3.6))
    for rows,color,line,label in experiments:
        phi = [r['phi_I'] for r in rows]
        axes[0].plot(phi,[10000*(r['r']-ref['r']) for r in rows],color=color,ls=line,marker='o',label=label)
        axes[1].plot(phi,[100*(r['capital']/ref['capital']-1) for r in rows],color=color,ls=line,marker='o')
    for ax in axes:
        ax.set_xlabel(r'Elasticidad informal $\phi_I$')
        ax.set_xticks([.38,.50,.60,.70])
        ax.grid(axis='y',color=GRID)
    axes[0].set_ylabel('Cambio de interés (pb)')
    axes[1].set_ylabel('Cambio de capital (%)')
    axes[0].legend(frameon=False,fontsize=11)
    save(fig,'paper_ge_aggregates')

    caps = sorted([ref,*groups['time_cap']],key=lambda r:r['hbar'])
    equal = sorted(groups['time_equality'],key=lambda r:r['hbar'])
    fig,axes = plt.subplots(1,2,figsize=(9.8,3.6))
    axes[0].plot([r['hbar'] for r in caps],[100*r['mass_at_cap'] for r in caps],
                 color=BLUE,marker='o')
    axes[0].set_ylabel('Población con el tope activo (%)')
    axes[1].plot([r['hbar'] for r in caps],[100*r['within_z_gap_fractional'] for r in caps],
                 color=BLUE,marker='o',label='Tope de horas')
    axes[1].plot([r['hbar'] for r in equal],[100*r['within_z_gap_fractional'] for r in equal],
                 color=ORANGE,marker='s',ls=':',label='Igualdad de horas')
    axes[1].axhline(0,color=BASE,lw=1)
    axes[1].set_ylabel('Brecha Q1−Q5 dentro de z (pp)')
    axes[1].legend(frameon=False,fontsize=11)
    for ax in axes:
        ax.set_xlabel(r'Tiempo disponible $\bar H$')
        ax.grid(axis='y',color=GRID)
    save(fig,'paper_time_constraints')

    fig,axes = plt.subplots(1,2,figsize=(9.8,3.6))
    for ax,j in zip(axes,[0,1]):
        for row,color,line,label in [(ref,BASE,'--','Tiempo holgado'),
                                     (equal[0],TEAL,'-',r'Igualdad: $\bar H=0{,}49$'),
                                     (equal[1],BLUE,'-',r'Igualdad: $\bar H=0{,}60$')]:
            profile = row['profiles'][j]
            ax.plot(row['assets'],100*np.asarray(profile['informal_share']),color=color,ls=line,label=label)
        ax.set(title=rf"Productividad $z={ref['profiles'][j]['z']:.2f}$",
               xlabel='Activos (unidades del modelo)',xlim=(-1,10),ylim=(0,100))
        ax.grid(axis='y',color=GRID)
    axes[0].set_ylabel('Horas informales (%)')
    axes[0].legend(frameon=False,fontsize=10)
    save(fig,'paper_equality_profiles')

    summary = {'scope':data['scope'],'run_date':data['run_date'],
               'export_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
               'counts':data['counts'],'checks':'passed','full_precision_certification':False,
               'within_z_definition':data['within_z_definition'],
               'fixed_high':{k:fixed[-1][k] for k in ('phi_I','r','pI','capital','M1_informal_hours','M3_formal_zmax_minus_zmin','V3_assets_Q1_minus_Q5_fractional')},
               'refit_high':{k:refit[-1][k] for k in ('phi_I','r','pI','capital','psi_I','kappa_max','M1_informal_hours','M3_formal_zmax_minus_zmin','V3_assets_Q1_minus_Q5_fractional')},
               'reference':{k:ref[k] for k in ('r','pI','capital','M1_informal_hours','M3_formal_zmax_minus_zmin','V3_assets_Q1_minus_Q5_fractional')},
               'time_cases':[{k:r[k] for k in ('family','hbar','mass_at_cap','within_z_gap_fractional','M1_informal_hours','M3_formal_zmax_minus_zmin','V3_assets_Q1_minus_Q5_fractional')} for r in [*caps,*equal]]}
    (HERE/'output/paper_results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    eq49,eq60 = equal
    cap55 = next(r for r in caps if r['hbar']==.55)
    evidence = json.loads((HERE/'data/frisch_evidence.json').read_text(encoding='utf-8'))['estimates']
    numbers = {
        'GEPaperCount':str(len(data['cases'])), 'GEFixedCount':str(len(fixed)),
        'GERefitCount':str(len(groups['refit'])),
        'GEBaseVThree':f"{100*ref['V3_assets_Q1_minus_Q5_fractional']:.2f}",
        'GEFixedHighVThree':f"{100*fixed[-1]['V3_assets_Q1_minus_Q5_fractional']:.2f}",
        'GERefitHighVThree':f"{100*refit[-1]['V3_assets_Q1_minus_Q5_fractional']:.2f}",
        'GEBaseMOne':f"{100*ref['M1_informal_hours']:.2f}",
        'GEFixedHighMOne':f"{100*fixed[-1]['M1_informal_hours']:.2f}",
        'GERefitPsi':f"{refit[-1]['psi_I']:.4f}",
        'GERefitKappa':f"{refit[-1]['kappa_max']:.5f}",
        'GERefitRChangeBP':f"{10000*(refit[-1]['r']-ref['r']):.2f}",
        'GERefitKChange':f"{100*(refit[-1]['capital']/ref['capital']-1):.3f}",
        'GEFixedKDecline':f"{100*(1-fixed[-1]['capital']/ref['capital']):.3f}",
        'CapMassAtLow':f"{100*cap55['mass_at_cap']:.2f}",
        'CapWithinGapLow':f"{100*cap55['within_z_gap_fractional']:.2f}",
        'EqLowVThree':f"{100*eq49['V3_assets_Q1_minus_Q5_fractional']:.2f}",
        'EqHighVThree':f"{100*eq60['V3_assets_Q1_minus_Q5_fractional']:.2f}",
        'EqWithinLow':f"{100*eq49['within_z_gap_fractional']:.2f}",
        'EqWithinHigh':f"{100*eq60['within_z_gap_fractional']:.2f}",
        'EmpiricalPhiFormal':f"{evidence['formal']:.2f}",
        'EmpiricalPhiInformal':f"{evidence['informal']:.2f}",
    }
    tex = '% Generated by code/verify.py; no manual numerical edits.\n'
    tex += ''.join('\\newcommand{\\'+k+'}{'+v+'}\n' for k,v in numbers.items())
    selected = [('Referencia',ref), *[(label,r) for label,rows in [('Sin reajuste',fixed),('Con reajuste',refit)]
                                     for r in rows if r['phi_I'] in (.50,.70)]]
    table = ''.join(f"{label} & {r['phi_I']:.2f} & {100*r['M1_informal_hours']:.2f} & {100*r['M3_formal_zmax_minus_zmin']:.2f} & {100*r['V3_assets_Q1_minus_Q5_fractional']:.2f} & {100*r['r']:.3f} & {r['capital']:.3f} \\\\\n" for label,r in selected)
    tex += '\\newcommand{\\PaperGERows}{%\n'+table+'}\n'
    selected_time = [('Referencia',ref),('Tope',next(r for r in caps if r['hbar']==.60)),('Tope',cap55),
                     ('Igualdad',eq49),('Igualdad',eq60)]
    table = ''.join(f"{label} & {r['hbar']:.2f} & {100*r['M1_informal_hours']:.2f} & {100*r['V3_assets_Q1_minus_Q5_fractional']:.2f} & {100*r['within_z_gap_fractional']:.2f} \\\\\n" for label,r in selected_time)
    tex += '\\newcommand{\\PaperTimeRows}{%\n'+table+'}\n'
    (HERE/'output/paper_numbers.tex').write_text(tex,encoding='utf-8',newline='\n')
    print('OK: 23 saved GE audited exports, recalibration targets, constraints and four paper figures.')
    return summary


if __name__ == '__main__':
    build_paper_results()
