"""Check the retained native MATLAB audit; regenerate its numerical summary."""
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np

from figures import BASE, BLUE, TEAL, ORANGE, GRID, style
from final_figures import save
from verify_lean import source_sha256

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LIMITS = {'capital':.003, 'informal_good':2e-4, 'formal_resources':.002,
          'government':2e-6, 'hjb':1e-6, 'kfe':1e-8, 'generator_row_sum':1e-10}


def check_native_report(report, experiments):
    assert report['passed'] and not report['new_ge_solve']
    assert not any(report[key] for key in (
        'continuous_model_global_concavity_proved',
        'continuous_model_global_existence_proved','global_precision_certified'))
    expected = {row['sha256']:row for row in experiments['cases']}
    actual = {row['mat_sha256']:row for row in report['cases']}
    assert len(actual)==len(report['cases'])==len(expected)==23
    assert actual.keys()==expected.keys(), 'Native audit must cover the same saved model files.'
    for digest, row in actual.items():
        source = expected[digest]
        assert row['passed'] and all(row['checks'].values())
        assert (row['asset_nodes'],row['productivity_nodes'],row['asset_min'],row['asset_max'])==(400,40,-1,40)
        assert row['phi_I']==source['phi_I'] and row['hbar']==source['hbar']
        s = row['shape']
        assert all(np.isfinite(value) for value in s.values())
        assert s['minimum_secant_slope']>0 and s['minimum_marginal_value']>0
        assert s['value_concavity_violations']==s['marginal_value_violations']==0
        assert s['maximum_value_curvature']<0 and s['maximum_secant_slope_increase']<0
        assert s['maximum_marginal_value_increase']<0
        for name, tolerance in LIMITS.items():
            assert np.isfinite(row['residuals'][name])
            assert abs(row['residuals'][name])<tolerance, (row['case_id'],name)
    return actual, expected


def build_numerical_validation():
    source_path = HERE/'data/matlab_value_equilibrium_audit.json'
    report = json.loads(source_path.read_text(encoding='utf-8'))
    experiments = json.loads((HERE/'data/paper_ge_experiments.json').read_text(encoding='utf-8'))
    actual, expected = check_native_report(report, experiments)
    receipt = json.loads((ROOT/'docs/matlab-validation.json').read_text(encoding='utf-8'))
    assert receipt['native_execution_completed'] and receipt['independent_python_comparison_passed']
    for name, digest in receipt['artifacts'].items():
        assert source_sha256(ROOT/name)==digest, f'Native audit evidence changed: {name}'
    maxima = {key:max(abs(row['residuals'][key]) for row in actual.values()) for key in LIMITS}
    families = list(experiments['counts'])
    curvature = {family:max(row['shape']['maximum_value_curvature']
                           for key,row in actual.items() if expected[key]['family']==family)
                 for family in families}
    summary = {'audit_date':report['audit_date'], 'matlab_version':report['matlab_version'],
        'cases':len(actual), 'all_checks_passed':True, 'computed_value_concavity_violations':0,
        'maximum_computed_value_curvature':max(curvature.values()),
        'maximum_marginal_value_increase':max(row['shape']['maximum_marginal_value_increase'] for row in actual.values()),
        'maximum_absolute_residuals':maxima, 'declared_residual_tolerances':LIMITS,
        'maximum_curvature_by_family':curvature,
        'source_sha256':source_sha256(source_path),
        'continuous_global_theorems_proved':False, 'global_precision_certified':False,
        'ci_scope':'Verify retained native output, source identities and numerical inequalities; no MATLAB run in CI.'}
    (HERE/'output/numerical_validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    style()
    fig, axes = plt.subplots(1,2,figsize=(10,3.8))
    axes[0].bar(range(4),list(curvature.values()),color=[BASE,TEAL,BLUE,ORANGE],width=.55)
    axes[0].axhline(0,color=BASE,lw=1)
    axes[0].set_xticks(range(4),['Fijos\n(8 GE)','Reajuste\n(7 GE)','Topes\n(6 GE)','Igualdad\n(2 GE)'])
    axes[0].set_ylabel(r'Mayor diferencia segunda $D_{aa}v$')
    axes[0].set_title('Valor calculado: curvatura negativa')
    names=['Capital','Bien informal','Recursos','Gobierno','HJB','KFE']
    keys=list(LIMITS)[:6]
    ratios=[maxima[key]/LIMITS[key] for key in keys]
    axes[1].barh(names,ratios,color=TEAL)
    axes[1].set_xscale('log')
    axes[1].axvline(1,color=ORANGE,ls='--',lw=1.5)
    axes[1].set_xlim(1e-12,2)
    axes[1].set_xlabel('Mayor residuo absoluto / tolerancia')
    axes[1].set_title('23 candidatos: residuos bajo tolerancia')
    axes[1].text(1e-11,3,'0',fontsize=10,va='center')
    axes[1].grid(axis='x',color=GRID)
    save(fig,'numerical_validation')
    print('OK: fresh MATLAB audit retained; 23 concave computed values and GE residual checks. Global continuous-model theorems remain unproved.')
    return summary
