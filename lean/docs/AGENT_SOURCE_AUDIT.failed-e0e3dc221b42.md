# Final Adversarial Source Audit: Barraza26LaborComposition

## Overall status: FAIL

- Reviewed final holistic audit surface identity: `e0e3dc221b42af319c16aaa05ccdd44f049a421e6aeb181584ea5313928cccd6`
- Reviewer identity: `barraza26-final-adversary-20261126-session-01`
- Review policy: schema 3, `main_primary`, one required final adversary

I independently reread the complete 373-line canonical TeX source, challenged
the main-text terminal region rather than relying on the frozen inventory as
evidence, and then compared every selected terminal row with its current Lean
target, proof route, semantic ledger, report, dependency DAG, and human-review
packet. I did not use an earlier verdict or the proposed paper status as
evidence.

## Source inventory reviewed

- Canonical source: `papers/Barraza26LaborComposition/source-audited.tex`,
  SHA-256 `3bfd0418b0b7a74c6cf459e09e623f73d30ce1ccd132bb4449b9b379dafcaaa6`.
- Primary terminal region: source lines 1--340.
- Selected primary surface: Assumptions 1--4, the informal-hours-share
  definition, and Proposition 1, “Composición condicional de horas.”
- The numerical, diagnostic, figure, table, and appendix presentations were
  checked for an omitted governing dependency. None supplies an additional
  selected main-text theorem row under the frozen policy.

## Lean and proof comparison

The derivative identity, its three conditional sign cases, the fixed-
productivity unary slice, fixed scalar returns, open-neighborhood encoding,
interior FOCs, slackness, and boundary exclusion are otherwise represented on
the reviewed surface. The graph pairs
`compositionConditionalHoursSpec` with the distinct theorem endpoint
`compositionConditionalHours` in `proves` mode, reports no `sorry` or unsafe
declaration, and records only `Classical.choice`, `Quot.sound`, and `propext`
in the endpoint's axiom closure.

The frozen planner receipt's 17 content inputs still match their recorded
SHA-256 values. The current report/memo assessment and human-review packet
pass their deterministic document-currentness checks, and the rendered DAG
and packet were inspected. Those checks do not cure the semantic mismatch
below.

## Actionable findings

### F-01, Assumption 2 drops the selected separable labor-cost condition

- Source anchors: `source-audited.tex:58-63` defines the sector-separable
  labor cost
  `sum_s psi_s ell_s^(1+1/phi_s)/(1+1/phi_s)`, and
  `source-audited.tex:115-117` makes that exact cost and separability part of
  the named Assumption 2.
- Lean anchors: `PaperInterface.lean:78-80` defines
  `laborPreferencesCondition` only as positivity of `psiF`, `psiI`, `phiF`,
  and `phiI`. `PaperInterface.lean:83-89` separately assumes the two local
  FOCs, and `PaperInterface.lean:113-123` uses those two declarations in the
  result `Spec`.
- Conflicting evidence row:
  `audit/paper_semantic_prerequisites.json`, item
  `Barraza26LaborComposition.laborPreferencesCondition`, records `matches`
  even though its selected source bundle contains the omitted cost clause.

The two assumed FOCs do not encode that they arise from the source's stated
separable labor cost. A different or nonseparable objective can have hours
that satisfy the same two pointwise FOC equations on the reviewed
neighborhood. Consequently, the Lean `Spec` admits models that do not satisfy
the selected named Assumption 2: it weakens a source premise and proves an
unprinted generalization rather than displaying the complete source
condition. The report's claims that all four assumptions are matched, and the
corresponding DAG and packet presentation, therefore overstate the current
source-semantic coverage.

Owning repair lane: paper semantic prerequisite and source-to-expanded-Spec
review. The source-facing target must expose the selected labor-cost and
separability semantics, or the source item must receive a protocol-compliant
scope decomposition that no longer labels the full Assumption 2 bundle as a
match. Any material target change requires the affected prerequisite and
result judgments and a successor frozen final-audit surface before another
terminal adversarial review.

## Remaining obligations

- Resolve F-01 in its owning semantic lane.
- Reissue only the evidence invalidated by that material repair and freeze a
  successor terminal surface.
- Run a fresh final adversarial review against that successor surface.

No final-adversarial panel entry was created because schema-1 panel entries
can record only a genuine PASS for the exact frozen surface.
