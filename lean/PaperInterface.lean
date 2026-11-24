import Barraza26LaborComposition.MainTheorems
import Barraza26LaborComposition.Assumptions

/-!
# Human-Facing Paper Interface: Ahorro, flexibilidad de horas e informalidad en el Peru: Un mecanismo laboral en un modelo macroeconomico de agentes heterogeneos

This is the compact Lean file a human should read after formalization to check
whether the paper's definitions and named theorem statements were represented
correctly. Keep the row-level dashboard and LLM audit statements in this file
for every paper. Move implementation details, proof aliases, and bulky helper
lemmas behind imported modules such as `AuditInterface.lean`, but expose the
audited paper-facing statements directly here; do not use
`paper_interface.audit_surface_path`.

Rules for completing this file:

- Keep the paper's definitions/formatted objects first, in source order.
- Expose the actual paper formulas here; do not only point to generic library
  definitions or implementation witnesses.
- A material reusable `AppliedModelingLib` primitive may remain a reference here only
  after `audit/library_semantic_review.json` records its exact bounded library
  declaration and an explicit byte-pinned paper-source connection. The
  dashboard and human-review packet show and source-check that declaration
  before the dependent Spec; a library name, docstring, or glossary is not a
  semantic bridge. Do not add a duplicate paper claim merely to restate it.
- If a named theorem needs a hypothesis that is not derived from earlier Lean
  declarations, declare that hypothesis in `Assumptions.lean` and list it in
  `status.json` `review_surface.assumption_names`.
- Then state the named results directly, with assumptions visible in each
  theorem signature by referencing named paper assumptions imported from
  `Assumptions.lean`.
- In the statement-first phase, write every complete source-facing statement as
  a transparent `<name>Spec : Prop` here, exactly once. Put the paired
  theorem/lemma of that exact type in `ProofInterface.lean`; its temporary
  proof body may be `by sorry` only in a private draft. This separation keeps
  the human semantic surface free of thin wrapper declarations.
- Before drafting that Lean surface, independently inventory every material
  source atom from exact pinned source quote bytes. Do not infer source atoms
  from declaration, binder, field, function, or source-map names.
- Run raw-source-to-expanded-Spec statement matching plus Lean-emitted
  premise/conclusion claim-atom review on the skeleton. The semantic comparison uses
  only byte-pinned source quotes (and separately pinned source context) against
  the expanded transparent Spec; map summaries and proof wrappers are not
  semantic inputs. Then freeze each canonical Lean declaration-manifest digest.
- In the proof phase, replace the `ProofInterface.lean` `sorry` with a short
  proof that calls into `MainTheorems.lean` or lower proof files without
  changing the specification or theorem type. Any specification/type change
  invalidates the freeze and requires a fresh statement audit.
- At formalized closeout, complete the v11 realization receipt: Lean Meta checks
  the theorem has exactly the transparent Spec type; each source atom is bound
  to the elaborated Spec surface; closure traversal includes proof and instance
  arguments; and every material terminal has a source, approved correction or
  additional assumption, checked derivation, or version-pinned foundation
  disposition. No data, container, or identifier-based exemption is allowed.
- The transparent `...Spec` is the sole semantic-review target for its source
  claim. The paired theorem/lemma is a proof endpoint whose exact Spec type is
  verified by Lean Meta, not a duplicate source-to-Lean comparison row.
- Keep proof endpoints, exhaustive endpoint aliases, and proof-seam checks in
  `ProofInterface.lean`, implementation modules, or `ProofLedger.lean`, not
  here. Do not create new `PostPaperAudit.lean` or `AuditLedger.lean` files;
  those names are legacy.

## Named Results

Each entry has one semantic-review target (`Spec`) and one proof endpoint (the
paired theorem/lemma). The human dashboard and review packet present that pair
once rather than treating the two declarations as duplicate paper claims.

- `compositionConditionalHoursSpec` -> `compositionConditionalHours`: Proposición 1 (Composición condicional de horas), paper.pdf p. 4, sección 4, Proposición 1; canonical paper.tex lines 126-134.
-/

namespace Barraza26LaborComposition

/-- Fixed-productivity, fixed-return comparison at an interior asset point. -/
def comparisonIndividualCondition (a aLower RF RI : ℝ) : Prop :=
  aLower < a ∧ 0 < RF ∧ 0 < RI

/-- Positivity of the sector-specific labor-disutility parameters. -/
def laborPreferencesCondition (psiF psiI phiF phiI : ℝ) : Prop :=
  0 < psiF ∧ 0 < psiI ∧ 0 < phiF ∧ 0 < phiI

/-- Local regular interior branch, including slackness and both sector FOCs. -/
def interiorRegularBranchCondition
    (V ellF ellI : ℝ → ℝ) (a d Hbar RF RI psiF psiI phiF phiI : ℝ) : Prop :=
  HasDerivAt V d a ∧ 0 < V a ∧
    ∀ᶠ x in nhds a,
      0 < ellF x ∧ 0 < ellI x ∧ ellF x + ellI x < Hbar ∧
        V x * RF - psiF * (ellF x) ^ (1 / phiF) = 0 ∧
        V x * RI - psiI * (ellI x) ^ (1 / phiI) = 0

/-- Local decreasing-marginal-value condition used only for sign conclusions. -/
def localConcavityCondition (d : ℝ) : Prop := d < 0

/-- Informal hours as a share of formal plus informal hours. -/
noncomputable def informalHoursShare (ellF ellI : ℝ → ℝ) : ℝ → ℝ :=
  fun x => ellI x / (ellF x + ellI x)

/--
Proposición 1 (Composición condicional de horas)

Paper statement: Proposición 1 (Composición condicional de horas). Bajo los supuestos 1–3, la política interior satisface ∂s_I(a_0,z)/∂a = s_I(a_0,z)(1-s_I(a_0,z))(φ_I-φ_F)V_aa(a_0,z)/V_a(a_0,z). Si además se cumple el supuesto 4, la derivada es negativa cuando φ_I>φ_F, cero cuando φ_I=φ_F y positiva cuando φ_I<φ_F.

Source location: paper.pdf p. 4, sección 4, Proposición 1; canonical paper.tex lines 126-134
Source status: pinned statement-spec transcription; independent source audit pending

This transparent proposition is the exact statement-audit target. It is not
proof evidence. Its exact-type proof endpoint is declared in
`ProofInterface.lean`, so this human-facing file presents the full semantic
proposition once. At closeout, source atoms must be independently inventoried
from pinned source quote bytes and bound to this elaborated proposition rather
than inferred from identifiers.
-/
def compositionConditionalHoursSpec : Prop :=
  ∀ (V ellF ellI : ℝ → ℝ) (a d aLower Hbar RF RI psiF psiI phiF phiI : ℝ),
    comparisonIndividualCondition a aLower RF RI →
    laborPreferencesCondition psiF psiI phiF phiI →
    interiorRegularBranchCondition V ellF ellI a d Hbar RF RI psiF psiI phiF phiI →
    let sI := informalHoursShare ellF ellI
    HasDerivAt sI (sI a * (1 - sI a) * (phiI - phiF) * d / V a) a ∧
      (localConcavityCondition d →
        (phiF < phiI → deriv sI a < 0) ∧
        (phiI = phiF → deriv sI a = 0) ∧
        (phiI < phiF → 0 < deriv sI a))

end Barraza26LaborComposition
