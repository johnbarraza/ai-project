import Barraza26LaborComposition.PaperInterface

/-!
# Proof Interface: Ahorro, flexibilidad de horas e informalidad en el Peru: Un mecanismo laboral en un modelo macroeconomico de agentes heterogeneos

This file contains exact-type proof endpoints for the transparent propositions
in `PaperInterface.lean`. It is not a human semantic-review surface: one source
claim is reviewed once, against its expanded `...Spec : Prop` declaration.
-/

namespace Barraza26LaborComposition

/--
Lean proof endpoint for `compositionConditionalHoursSpec`.

This theorem is intentionally outside `PaperInterface.lean`: Lean Meta checks
that it has exactly the transparent Spec type, while source-to-Lean semantic
review compares the raw source bundle only to that Spec.
-/
theorem compositionConditionalHours :
  compositionConditionalHoursSpec := by
  intro laborCost V ellF ellI a d aLower Hbar RF RI psiF psiI phiF phiI hcomparison
    hpreferences hbranch
  rcases hcomparison with ⟨_, hRF, hRI⟩
  rcases hpreferences with ⟨hpF, hpI, hphiF, hphiI, _⟩
  rcases hbranch with ⟨hV, hVa, hev⟩
  have hkey := share_eventuallyEq_of_foc (V := V) (RF := RF) (RI := RI) hpF hpI hphiF hphiI hev
  have hD := (composition_hasDerivAt (phiF := phiF) (phiI := phiI) hV hVa hRF hRI hpF hpI)
    |>.congr_of_eventuallyEq hkey
  have ha := hkey.self_of_nhds
  have hderiv := hkey.deriv_eq
  simp only [informalHoursShare, localConcavityCondition] at ha hderiv ⊢
  refine ⟨?_, fun hd => ?_⟩
  · rw [ha]; exact hD
  · change
      (phiF < phiI → deriv (fun x => ellI x / (ellF x + ellI x)) a < 0) ∧
      (phiI = phiF → deriv (fun x => ellI x / (ellF x + ellI x)) a = 0) ∧
      (phiI < phiF → 0 < deriv (fun x => ellI x / (ellF x + ellI x)) a)
    rw [hderiv]
    exact composition_sign (phiF := phiF) (phiI := phiI)
      hV hVa hd hRF hRI hpF hpI

end Barraza26LaborComposition
