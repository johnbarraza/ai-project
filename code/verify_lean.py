"""Check the new paper's reduced labor result, preserving a source-bound receipt.

Linux/macOS with dependencies: python code/verify_lean.py
Windows, existing WSL cache: python code/verify_lean.py --wsl-cache /home/johnb/EconCSLib
This is a local Lean check, not the official AppliedModelingLib contribution workflow.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shlex
import subprocess

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT/'lean'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wsl-cache', help='Existing Lake project with a compatible Mathlib cache')
    args = parser.parse_args()
    source = LEAN/'LaborComposition.lean'
    text = source.read_text(encoding='utf-8')
    if re.search(r'\b(sorry|admit|axiom)\b',text):
        raise AssertionError('Proof source contains a gap or new axiom')
    if args.wsl_cache:
        drive = source.drive[0].lower()
        target = '/mnt/'+drive+source.as_posix()[2:]
        lake = '/home/johnb/.elan/bin/lake'
        lean = '/home/johnb/.elan/bin/lean'
        command = 'cd '+shlex.quote(args.wsl_cache)+' && '+lake+' env '+lean+' '+shlex.quote(target)
        run = subprocess.run(['wsl','-d','Ubuntu','--','bash','-lc',command],capture_output=True,text=True,encoding='utf-8')
        version = subprocess.run(['wsl','-d','Ubuntu','--',lean,'--version'],capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()
        mathlib = subprocess.run(['wsl','-d','Ubuntu','--','git','-C',args.wsl_cache+'/.lake/packages/mathlib','rev-parse','HEAD'],capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()
    else:
        run = subprocess.run(['lake','env','lean',source.name],cwd=LEAN,capture_output=True,text=True,encoding='utf-8')
        version = subprocess.run(['lake','env','lean','--version'],cwd=LEAN,capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()
        mathlib = subprocess.run(['git','-C',str(LEAN/'.lake/packages/mathlib'),'rev-parse','HEAD'],capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()
    output = run.stdout+run.stderr
    axiom_reports = re.findall(r'depends on axioms:\s*\[([^\]]*)\]',output)
    actual_axioms = sorted({a.strip() for report in axiom_reports for a in report.split(',')})
    expected_axioms = {'propext','Classical.choice','Quot.sound'}
    valid = run.returncode==0 and len(axiom_reports)==2 and set(actual_axioms)==expected_axioms
    folder = LEAN/'verification'
    folder.mkdir(exist_ok=True)
    (folder/'local_check.txt').write_text(output,encoding='utf-8')
    receipt = {
        'status':'passed' if valid else 'failed',
        'exit_code':run.returncode,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'lean_version':version,'mathlib_commit':mathlib,
        'checked_declarations':['Barraza26LaborComposition.composition_hasDerivAt','Barraza26LaborComposition.composition_sign'],
        'axioms':actual_axioms,
        'scope':'Explicit interior labor policies: derivative, chain rule and signs. HJB concavity and GE existence are not proved.',
        'official_applied_modeling_workflow':False,'published_paper_commit':None,
        'human_semantic_review_recorded':False,
    }
    (folder/'local_check.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    print(output,end='')
    if receipt['status']!='passed':
        raise SystemExit(run.returncode or 1)
    print('PASS: source-bound local check; official pinned-paper workflow remains pending.')


if __name__=='__main__':
    main()
