# Final Validation Report: Ahorro, flexibilidad de horas e informalidad en el Perú: Un mecanismo laboral en un modelo macroeconómico de agentes heterogéneos

Updated: 2026-11-25

## 1. Human Verdict

The paper's named theoretical result is formalized on its stated local,
interior branch. The derivative identity and all three conditional sign cases
were independently compared with the pinned source and matched. Human author
review remains pending and is not inferred from the technical closeout.

## 2. Closeout Status

- Completion status: formalized.
- One-sentence recap: Proposition 1, its four stated assumptions, and the
  governing informal-hours-share definition are covered without an additional
  theorem premise; human review is still open.

## 3. Source and Scope

- Paper: John Svante Barraza Ratachi, *Ahorro, flexibilidad de horas e
  informalidad en el Perú: Un mecanismo laboral en un modelo macroeconómico de
  agentes heterogéneos*.
- Source version: [merged manuscript dated 24 November 2026](https://github.com/johnbarraza/ai-project/blob/6777134ba22670ebd53b65d21a48d719c09b3fbd/paper/paper.pdf).
- Formalized scope: the four assumptions in the local-results block, the
  informal-hours-share definition, and Proposition 1, “Composición condicional
  de horas.”
- Scope boundary: the proposition is a conditional comparison at one interior
  asset point and fixed productivity. It does not establish global regularity
  or concavity of the HJB, behavior at the borrowing boundary or an active time
  cap, aggregation, or existence of a general equilibrium.

## 4. Researcher Summary of Checked Results

| Result | Comparison with source |
| --- | --- |
| Proposition 1, Composición condicional de horas | **Exact.** The derivative identity is proved under Assumptions 1--3, and Assumption 4 yields the negative, zero, and positive sign cases according as the informal-hours elasticity is greater than, equal to, or less than the formal-hours elasticity. |

## 5. Remaining Boundaries and Gaps

None within Proposition 1. Global HJB regularity and concavity, boundary and
binding-cap regimes, aggregation, and general-equilibrium existence are outside
the proposition's stated conclusion and remain outside this formalization.

## 6. Additional Assumptions Beyond Paper

None.

## 7. Proof-Strategy Deviations

The source differentiates the positive hours ratio and then rewrites the
informal share as a function of that ratio. The checked proof instead
differentiates the two explicit positive hour policies and their quotient
directly. The routes give the same derivative identity under the same local
premises, so the proposition's statement is unchanged.

## 8. Proof Tricks Worth Reusing

An eventual equality on the source's open interior branch transfers a
derivative proved for explicit policies back to the original hours functions.
This keeps the theorem local and avoids claiming regularity away from the
neighborhood used by the proposition.

## 9. Generalizations, Conjectures, and Extensions

None are claimed. Active time caps, borrowing-boundary points, endogenous
price changes, aggregation, and equilibrium existence require separate
statements.

## 10. Source Clarifications and Exact Readings

None. Fixing productivity and returns, and representing an open neighborhood
locally, preserve the ordinary reading of the stated comparison.

## 11. Paper Issues or Caveats

None within the reviewed named theoretical surface.

## 12. Detailed Formalization Evidence

The current paper surface has one transparent result specification in
[PaperInterface.lean](PaperInterface.lean) and one separately checked endpoint
in [ProofInterface.lean](ProofInterface.lean). The exact source routes and four
individually anchored conclusion clauses are recorded in the
[statement map](audit/paper_statement_map.json). The current direct result
review records one match, and the paper-prerequisite review records five
matches, with no mismatch or uncertainty.

## 13. Paper Assumption Provenance

The result uses the four assumptions printed immediately before Proposition 1.
They are routed as source-semantic prerequisites rather than duplicate theorem
rows.

| Source condition | Mathematical role | Current disposition |
| --- | --- | --- |
| Assumption 1, Comparación individual | Fixes productivity and positive asset-independent returns in an open neighborhood of an interior asset point. | Source condition, matched. |
| Assumption 2, Preferencias laborales | Requires positive labor parameters and the separable hours cost. | Source condition, matched. |
| Assumption 3, Rama interior regular | Supplies positive differentiable marginal value, positive hours, slack time, and the two labor FOCs locally. | Source condition, matched. |
| Assumption 4, Concavidad local para la interpretación | Adds the negative local derivative of marginal value only for the three sign conclusions. | Source condition, matched. |

## 14. Displayed Formula Provenance

The displayed identity in Proposition 1 is split into four anchored clauses in
the [statement map](audit/paper_statement_map.json): the derivative identity,
the negative-sign case, the zero-sign case, and the positive-sign case. The
source-proof ledger checks the FOC-to-policy bridge, the hours-ratio algebra,
the quotient derivative, the share identity, domain conditions, and all three
signs in [source_proof_fidelity.json](audit/source_proof_fidelity.json).

## 15. Library Lift Pass

- Reusable library extraction candidates: none.
- The formalization is paper-local and introduces no material reusable-library
  semantic prerequisite.
- The graph-owned proof route uses only the standard Lean and Mathlib
  foundation boundary.

## 16. DAG Audit

[DependencyDAG.tex](docs/DependencyDAG.tex) and
[DependencyDAG.pdf](docs/DependencyDAG.pdf) show the four printed assumptions,
the informal-hours-share definition, and Proposition 1. Solid arrows identify
the proposition's stated dependencies; the graph contains no proof helpers or
unstated global model claim. The rendered PDF was visually inspected for
readable labels, arrow direction, clipping, and node-edge overlap.

## 17. Validation Checks

The current Lean import closure, direct semantic result review, five
prerequisite reviews, theorem-realization relation, and source-proof fidelity
review are current for the pinned source and saved graph. Focused interface
builds passed without `sorry` or unsafe declarations. The terminal paper-root
build and ten-gate strict closeout are recorded only by the canonical receipt
when that receipt is issued; this report does not substitute for it.

## 18. Paper Definitions Checked

The informal-hours share is the fraction of informal hours in total formal and
informal hours. Its hours-based interpretation and strict interior range are
matched as a governing semantic prerequisite. The four assumptions listed in
Section 13 are also checked as source conditions.

## 19. Named Theorem Statements Checked

### Proposition 1, Composición condicional de horas

**Paper statement.** Under Assumptions 1--3, the derivative of the informal
hours share equals the share times one minus the share, the difference between
the two labor elasticities, and the ratio of the derivative of marginal value
to marginal value. Under Assumption 4, its sign is negative, zero, or positive
as the informal elasticity is greater than, equal to, or less than the formal
elasticity.

**Lean interface statement.** The transparent paper-facing specification
exposes the interior-point condition, positive fixed returns and labor
parameters, local differentiability and positivity, eventual interior FOCs and
slackness, the derivative identity, and the conditional three-way sign result.

**Status.** Formalized exactly on the source's stated local branch.

## 20. Paper-Facing Statement Validator Ledger

| Paper-facing statement | Machine review | Human review |
| --- | --- | --- |
| Proposition 1, Composición condicional de horas | Independent source-to-expanded-spec review: match. Lean theorem realization: exact checked endpoint. | Pending, 0 of 1 rows reviewed. |

The [human review packet](docs/HUMAN_REVIEW_PACKET.pdf) presents the current
source and expanded target for optional human annotation. Machine review does
not increment the human-review count.

## 21. Source-Coverage Audit Ledger

- Source inventory: the complete 373-line TeX source and all 15 rendered PDF
  pages were reviewed independently.
- Selected named result: one proposition, directly covered.
- Governing semantic prerequisites: four numbered assumptions and one
  hours-share definition, all matched.
- Deep-audit material: four supporting or diagnostic presentations were
  inventoried and do not constitute additional named theoretical results.
- Human review: pending; no author approval is inferred.

| Source presentation | Linked review surface | Coverage judgment | Current check |
| --- | --- | --- | --- |
| Assumptions 1--4 | Four paper prerequisites | Covered as source conditions | Four matches. |
| Informal-hours-share definition | One paper prerequisite | Covered as governing definition | Match. |
| Proposition 1 | One result specification and proof endpoint | Directly covered | Match; exact theorem realization. |
