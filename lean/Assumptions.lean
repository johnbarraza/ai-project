import Barraza26LaborComposition.MainTheorems

/-!
# Paper Assumptions: Ahorro, flexibilidad de horas e informalidad en el Peru: Un mecanismo laboral en un modelo macroeconomico de agentes heterogeneos

This file is the only paper-local place for assumptions that are not derived in
Lean. Keep it small. Each declaration must be explicitly stated by the paper,
listed in `status.json` `review_surface.assumption_names`, and judged in
`audit/assumption_match_llm.json` as a true source/model assumption rather than a
proof convenience.

The audit discovers proposition-valued theorem premises from Lean's elaborated
claim manifests. Do not add `audit-premise` comments or duplicate a binder in a
sidecar to make it discoverable; instead, keep the proposition explicit in the
source-facing `Spec` and route any reusable paper assumption through this
module and `status.json`.

Start empty. Add a proposition here only after locating it as a literal source
antecedent. Never move an unproved lemma or target conclusion here merely to
make a statement skeleton compile.
-/

namespace Barraza26LaborComposition

end Barraza26LaborComposition
