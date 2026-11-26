"""Symbolic checks of the paper's production and resource accounting identities."""
from pathlib import Path
import json

import sympy as sp


def verify_macro_identities():
    AF, AI, KF, LF, KI, LI, alpha, alphaI, betaI = sp.symbols(
        'AF AI KF LF KI LI alpha alphaI betaI',positive=True)
    YF = AF*KF**alpha*LF**(1-alpha)
    YI = AI*KI**alphaI*LI**betaI
    assert sp.simplify(KF*sp.diff(YF,KF)-alpha*YF)==0
    assert sp.simplify(LF*sp.diff(YF,LF)-(1-alpha)*YF)==0
    assert sp.simplify(YF-KF*sp.diff(YF,KF)-LF*sp.diff(YF,LF))==0
    assert sp.simplify(YI-KI*sp.diff(YI,KI)-LI*sp.diff(YI,LI)
                       -(1-alphaI-betaI)*YI)==0

    cF, cI, weight = sp.symbols('cF cI weight',positive=True)
    power = sp.Symbol('power',real=True,nonzero=True)
    C = ((weight*cF**power+cI**power)/(1+weight))**(1/power)
    assert sp.factor(cF*sp.diff(C,cF)+cI*sp.diff(C,cI)-C)==0
    cobb = cF**(weight/(1+weight))*cI**(1/(1+weight))
    assert sp.factor(cF*sp.diff(cobb,cF)+cI*sp.diff(cobb,cI)-cobb)==0

    f,i,p,r,delta,tau,cf,ci,barrier,premium,S = sp.symbols(
        'YF YI pI r delta tau CF CI barrier premium S')
    wageF = f-(r+delta)*KF
    incomeI = p*i-(r+delta)*KI
    asset_drift = ((1-tau)*wageF-barrier+incomeI+r*S-premium
                   +tau*wageF-cf-p*ci)
    closed = sp.simplify(asset_drift.subs({S:KF+KI,ci:i}))
    assert sp.simplify(closed-(f-cf-delta*(KF+KI)-barrier-premium))==0
    assert sp.diff(closed,barrier)==-1 and sp.diff(closed,premium)==-1

    report = {
        'checks':'passed','sympy_version':sp.__version__,
        'formal_factor_payments_and_zero_profit':'passed',
        'informal_decreasing_returns_profit_identity':'passed',
        'CES_and_Cobb_Douglas_Euler_identity':'passed',
        'stationary_resource_accounting_with_both_wedges':'passed',
        'conditions':[
            'Interior positive factors; formal shares alpha and 1-alpha.',
            'Informal exponents positive with sum below one for positive profits.',
            'Positive consumption and normalized CES weights; positive differentiable basket.',
            'Log consumption utility and zero consumption tax for Va=1/expenditure.',
            'Stationary normalized population with integrable asset drift, S=K and CI=YI.',
            'Formal labor tax rebated; barrier/debt-premium payments are not rebated in this specification.'
        ],
        'scope':'Algebra conditional on the stated model; not GE existence, numerical precision or handwritten evidence.'
    }
    output = Path(__file__).resolve().parent/'output'
    output.mkdir(exist_ok=True)
    (output/'macro_identities.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('OK: symbolic firm payments/profits, CES homogeneity and aggregate resource accounting.')
    return report


if __name__=='__main__':
    verify_macro_identities()
