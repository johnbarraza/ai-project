"""Final presentation: historical PE checks plus exported D73 GE diagnostics.

Called by verify.py. Regenerates figures without MATLAB or private paths.
Export checks do not rerun the HJB/KFE or certify precision globally.
"""
from pathlib import Path
import hashlib
import json

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from figures import style, INK, BASE, BLUE, TEAL, ORANGE, GRID

HERE = Path(__file__).resolve().parent
OUT = HERE / 'figures' / 'final'


def save(fig, name):
    fig.tight_layout(pad=.6)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ('pdf', 'png', 'svg'):
        options = {'dpi': 180} if ext == 'png' else {}
        if ext == 'pdf':
            options['metadata'] = {'CreationDate': None, 'ModDate': None}
        elif ext == 'svg':
            options['metadata'] = {'Date': None}
        fig.savefig(OUT / f'{name}.{ext}', bbox_inches='tight', pad_inches=.05, **options)
        if ext == 'svg':
            path = OUT / f'{name}.svg'
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)


def build_final(baseline, scenarios, summary, moments_data):
    style()
    source = HERE / 'data' / 'final_wedges.json'
    exported = json.loads(source.read_text(encoding='utf-8'))
    rows = exported['cases']
    if len(rows) != 17 or sum(r['mode'] == 'ge' for r in rows) != 14:
        raise AssertionError('D73: número y tipo de corridas distintos del registro')
    for row in rows:
        if row['status'] != 'passed' or not all(row['checks'].values()):
            raise AssertionError('D73: una corrida exportada no pasa sus controles')
        if not (row['hjb_residual'] < 1e-6 and row['kfe_residual'] < 1e-8
                and row['row_error'] < 1e-10 and row['closed_classes'] == 1):
            raise AssertionError('D73: diagnóstico exportado excede tolerancias originales')
        np.testing.assert_allclose(row['mean_assets']-row['capital'],row['capital_residual'],atol=1e-8,rtol=0)
    wide = [r for r in rows if r['mode'] == 'ge' and r['Na'] == 400
            and r['Nz'] == 40 and r['amax'] == 40]
    by_case = {r['case']: r for r in wide}
    expected = {'reference', 'chi_constant', 'kappa_constant', 'both_constant', 'both_constant_refit'}
    if len(wide) != 5 or set(by_case) != expected:
        raise AssertionError('D73: faltan los cinco GE comparables en dominio amplio')
    ref, refit = by_case['reference'], by_case['both_constant_refit']
    np.testing.assert_allclose(
        [refit['M1_informal_hours'], refit['M3_formal_zmax_minus_zmin']],
        [ref['M1_informal_hours'], ref['M3_formal_zmax_minus_zmin']], atol=1e-7, rtol=0)

    # Independent chain-rule check: derivative through a differentiable Va(a).
    a = sp.symbols('a', real=True)
    q = sp.symbols('q', positive=True)
    d = sp.symbols('d', real=True)
    va = sp.Function('V_a')(a)
    odds = q * va**d
    share = odds / (1 + odds)
    identity = sp.diff(share, a) - share*(1-share)*d*sp.diff(va,a)/va
    if sp.simplify(identity) != 0:
        raise AssertionError('Regla de la cadena para la composición laboral')

    fig, ax = plt.subplots(figsize=(9.8, 3.5))
    z_index = int(np.searchsorted(baseline['z'], 1))
    for index, color, line in [(0, BASE, '--'), (2, BLUE, '-'), (4, TEAL, '-')]:
        row = scenarios[index]
        values = row['ell_i'][:, z_index] / (row['ell_i'][:, z_index]+row['ell_f'][:, z_index])
        ax.plot(baseline['a'], 100*values, color=color, ls=line, lw=2.8,
                label=rf"$\phi_I={row['phi_I']:.2f}$")
    ax.set(xlabel='Activos del hogar a (unidades del modelo)',
           ylabel='Horas informales / horas totales (%)')
    ax.legend(frameon=False, ncol=3, loc='upper right')
    ax.grid(axis='y', color=GRID)
    save(fig, 'assets')

    fig, ax = plt.subplots(figsize=(9.8, 3.5))
    xx = [s['phi_I'] for s in scenarios]
    yy = [100*s['V3'] for s in scenarios]
    ax.plot(xx, yy, color=TEAL, marker='o', lw=2.8, ms=7)
    for x,y in zip(xx,yy):
        ax.annotate(f'{y:.2f}'.replace('.',','),(x,y),xytext=(0,9),textcoords='offset points',ha='center')
    ax.set(xlabel=r'Elasticidad informal $\phi_I$ (sensibilidad)',
           ylabel='Brecha de horas informales Q1−Q5 (pp)', ylim=(0,12), xticks=xx)
    ax.grid(axis='y', color=GRID)
    save(fig, 'phi_gap')

    fig, ax = plt.subplots(figsize=(7.9, 3.7))
    grid = np.linspace(.15,.8,150)
    ax.fill_between(grid,.15,grid,color='#F9E4D4')
    ax.fill_between(grid,grid,.8,color='#D8EEEE')
    ax.plot(grid,grid,color=BASE,lw=2,ls='--')
    ax.text(.28,.66,'Más activos, menor\nfracción informal',color=TEAL,ha='center',fontsize=15)
    ax.text(.65,.31,'Más activos, mayor\nfracción informal',color=ORANGE,ha='center',fontsize=15)
    ax.annotate('Canal nulo: elasticidades iguales',(.49,.49),(.48,.70),
                fontsize=11,arrowprops={'arrowstyle':'->','color':BASE})
    ax.set(xlabel=r'Elasticidad formal $\phi_F$',ylabel=r'Elasticidad informal $\phi_I$',
           xlim=(.15,.8),ylim=(.15,.8))
    save(fig, 'sign_map')

    fig, ax = plt.subplots(figsize=(9.8, 3.4))
    keys = ['reference','chi_constant','kappa_constant','both_constant']
    names = ['Dos sectores','Prima constante','Barrera constante','Ambas constantes']
    values = [100*by_case[k]['M3_formal_zmax_minus_zmin'] for k in keys]
    for n,v,color in zip(range(4),values,[BASE,BLUE,TEAL,TEAL]):
        ax.hlines(n,0,v,color=color,lw=6,alpha=.25)
        ax.plot(v,n,'o',color=color,ms=10)
        ax.text(v+.7,n,f'{v:.2f}'.replace('.',','),va='center',fontsize=14)
    ax.set(yticks=range(4),yticklabels=names,xlim=(0,43),
           xlabel='Brecha de formalidad entre extremos de productividad z (pp)')
    ax.invert_yaxis()
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x',color=GRID)
    save(fig, 'wedges')

    fig, axes = plt.subplots(1,2,figsize=(9.8,3.4))
    for ax, field, factor, title, limit in [
        (axes[0],'V3_assets_Q1_minus_Q5_fractional',100,'Brecha Q1−Q5 activos (pp)',6),
        (axes[1],'expenditure_ratio_dominant_formal_informal',1,'Razón de gasto F/I dominante',2.2)]:
        values = [factor*r[field] for r in [ref,refit]]
        ax.bar([0,1],values,color=[BASE,TEAL],width=.55)
        for n,v in enumerate(values):
            ax.text(n,v+.03*limit,f'{v:.3f}'.replace('.',','),ha='center',fontsize=14)
        ax.set(xticks=[0,1],xticklabels=['Dos sectores','Reajustado'],ylim=(0,limit),title=title)
        ax.grid(axis='y',color=GRID)
        ax.set_axisbelow(True)
        if factor==1:
            target=exported['registered_expenditure_target']
            ax.axhline(target,color=ORANGE,ls='--')
            ax.text(.5,target+.06,'Meta registrada: '+str(target).replace('.',','),ha='center',fontsize=10,color=ORANGE)
    save(fig, 'validation')

    fig, ax = plt.subplots(figsize=(9.8,3.5))
    data = moments_data['enaho_own_quintiles']['years']['2023']['quintiles']
    ax.bar(range(5),data,color=[TEAL]*4+[BLUE],width=.58)
    for n,v in enumerate(data):
        ax.text(n,v+2,f'{v:.1f}'.replace('.',','),ha='center',fontsize=16)
    ax.set(xticks=range(5),xticklabels=['Q1\nMenor gasto','Q2','Q3','Q4','Q5\nMayor gasto'],
           ylim=(0,110),ylabel='Empleo informal (% de personas ocupadas)')
    ax.grid(axis='y',color=GRID)
    ax.set_axisbelow(True)
    save(fig,'motivation')

    wealth_mass = baseline['mass'].sum(axis=1)
    mean_assets = float(np.sum(wealth_mass*baseline['a']))
    formal = float(np.sum(baseline['mass']*baseline['ell_f']))
    informal = float(np.sum(baseline['mass']*baseline['ell_i']))
    hours_fraction = np.array([formal,informal])/(formal+informal)
    np.testing.assert_allclose([wealth_mass.sum(),hours_fraction.sum()],[1,1],atol=1e-9,rtol=0)
    np.testing.assert_allclose(hours_fraction[1],summary['baseline']['M1'],atol=1e-12,rtol=0)
    fig,axes = plt.subplots(1,2,figsize=(9.8,3.5))
    axes[0].plot(baseline['a'],100*np.cumsum(wealth_mass),color=BLUE,lw=2.5)
    axes[0].set(xlabel='Activos a (unidades del modelo)',ylabel='Población acumulada (%)',ylim=(0,100),
                title='Distribución estacionaria de activos')
    axes[0].grid(axis='y',color=GRID)
    axes[1].bar([0,1],100*hours_fraction,color=[BLUE,TEAL],width=.55)
    for k,value in enumerate(100*hours_fraction):
        axes[1].text(k,value+2,f'{value:.2f}'.replace('.',','),ha='center')
    axes[1].set(xticks=[0,1],xticklabels=['Formales','Informales'],ylim=(0,100),
                ylabel='Horas agregadas / horas totales (%)',title='Agregación de las decisiones')
    axes[1].grid(axis='y',color=GRID)
    axes[1].set_axisbelow(True)
    save(fig,'macro_distribution')

    fig,axes = plt.subplots(1,2,figsize=(9.8,3.4))
    alternatives=['chi_constant','kappa_constant','both_constant','both_constant_refit']
    labels=['Prima constante','Barrera constante','Ambas constantes','Ambas reajustadas']
    interest_bp=[10000*(by_case[k]['r']-ref['r']) for k in alternatives]
    capital_change=[100*(by_case[k]['capital']/ref['capital']-1) for k in alternatives]
    for ax,values,title,xlabel in [
        (axes[0],interest_bp,'Tasa de interés','Cambio frente a referencia (puntos básicos)'),
        (axes[1],capital_change,'Capital agregado','Cambio frente a referencia (%)')]:
        for k,value in enumerate(values):
            ax.hlines(k,0,value,color=TEAL,lw=5,alpha=.25)
            ax.plot(value,k,'o',color=TEAL,ms=7)
            ax.annotate(f'{value:+.3f}'.replace('.',','),(value,k),xytext=(5,0),textcoords='offset points',va='center',fontsize=11)
        span=max(max(values)-min(values),.5)
        ax.set(xlim=(min(min(values),0)-.13*span,max(max(values),0)+.45*span),yticks=range(4),
               yticklabels=labels if ax is axes[0] else ['']*4,title=title,xlabel=xlabel)
        ax.invert_yaxis()
        ax.axvline(0,color=BASE,lw=1,ls='--')
        ax.grid(axis='x',color=GRID)
        ax.spines['left'].set_visible(False)
    save(fig,'macro_ge')

    numbers = {
        'PEGapLow':f'{100*scenarios[0]["V3"]:.2f}',
        'PEGapHigh':f'{100*scenarios[-1]["V3"]:.2f}',
        'PhiFormalFinal':f'{baseline["params"]["Frisch"]:.2f}',
        'PhiHighFinal':f'{scenarios[-1]["phi_I"]:.2f}',
        'PEMOne':f'{100*scenarios[0]["M1"]:.2f}',
        'PEMThree':f'{100*scenarios[0]["M3"]:.2f}',
        'PENoCap':f'{summary["baseline"]["mass_at_cap"]:.0f}',
        'PEMaxHours':f'{summary["baseline"]["max_hours"]:.3f}',
        'FixedZFinal':f'{baseline["z"][z_index]:.3f}',
        'WedgeMThreeRef':f'{100*ref["M3_formal_zmax_minus_zmin"]:.2f}',
        'WedgeMThreeConst':f'{100*by_case["kappa_constant"]["M3_formal_zmax_minus_zmin"]:.2f}',
        'WedgeMOneRef':f'{100*ref["M1_informal_hours"]:.3f}',
        'WedgeMThreeRefit':f'{100*refit["M3_formal_zmax_minus_zmin"]:.3f}',
        'WedgeVThreeRef':f'{100*ref["V3_assets_Q1_minus_Q5_fractional"]:.3f}',
        'WedgeVThreeRefit':f'{100*refit["V3_assets_Q1_minus_Q5_fractional"]:.3f}',
        'CountMATFinal':str(len(rows)), 'CountGEFinal':str(sum(r['mode']=='ge' for r in rows)),
        'MotivationQOne':f'{data[0]:.1f}', 'MotivationQFive':f'{data[-1]:.1f}',
        'MeanAssetsFinal':f'{mean_assets:.3f}',
        'InterestRefFinal':f'{100*ref["r"]:.3f}',
        'CapitalRefFinal':f'{ref["capital"]:.3f}',
    }
    text = '% Generated by code/verify.py. Do not edit numerical values.\n'
    text += ''.join('\\newcommand{\\'+k+'}{'+v+'}\n' for k,v in numbers.items())
    pe_rows = ''.join(f"{s['phi_I']:.2f} & {s['psi_I']:.3f} & {s['kappa_z1']:.5f} & {100*s['V3']:.3f} \\\\\n" for s in scenarios)
    text += '\\newcommand{\\FinalPERows}{%\n'+pe_rows+'}\n'
    names = {'reference':'Dos sectores','chi_constant':'Prima constante','kappa_constant':'Barrera constante',
             'both_constant':'Ambas constantes','both_constant_refit':'Ambas, reajuste'}
    wedge_rows = ''.join(f"{names[k]} & {100*by_case[k]['M1_informal_hours']:.3f} & {100*by_case[k]['M3_formal_zmax_minus_zmin']:.3f} & {100*by_case[k]['V3_assets_Q1_minus_Q5_fractional']:.3f} & {by_case[k]['expenditure_ratio_dominant_formal_informal']:.3f} \\\\\n" for k in names)
    text += '\\newcommand{\\FinalWedgeRows}{%\n'+wedge_rows+'}\n'
    (HERE/'output'/'final_numbers.tex').write_text(text,encoding='utf-8')
    receipt_path = HERE.parent/'lean'/'verification'/'local_check.json'
    lean_receipt = json.loads(receipt_path.read_text(encoding='utf-8')) if receipt_path.exists() else None
    if lean_receipt:
        lean_source = HERE.parent/'lean'/'LaborComposition.lean'
        if lean_receipt['status']!='passed' or lean_receipt['source_sha256']!=hashlib.sha256(lean_source.read_bytes()).hexdigest():
            raise AssertionError('Lean receipt failed or source changed since its check')
    report = {
        'scope':'PE reproducido desde exportación histórica; D73 verifica diagnósticos exportados, sin rerun HJB/KFE.',
        'export_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'original_audit_sha256':exported['source_sha256'],
        'checks':{'historical_PE':'passed','wealth_chain_rule':'passed','D73_export_diagnostics':'passed','refit_internal_targets':'passed'},
        'macro_aggregation':{'mass':float(wealth_mass.sum()),'mean_assets_historical':mean_assets,
                             'formal_hours_share':float(hours_fraction[0]),'informal_hours_share':float(hours_fraction[1]),
                             'D73_interest_change_bp':dict(zip(alternatives,interest_bp)),
                             'D73_capital_change_percent':dict(zip(alternatives,capital_change))},
        'numbers':numbers,
        'precision_certified':exported['full_precision_certification'],
        'ready_for_submission':False,
        'local_lean_checked':bool(lean_receipt),
        'official_applied_modeling_workflow':False,
        'remaining_requirements':(['Flujo oficial AppliedModelingLib sobre paper publicado en commit'] if lean_receipt else ['Formalización propia y fragmento Lean verificado'])+['Derivación manuscrita personal en pantalla'],
    }
    (HERE/'output'/'final_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('OK: final figures, chain rule and D73 exported diagnostics. Official workflow/handwritten evidence remain open.')
