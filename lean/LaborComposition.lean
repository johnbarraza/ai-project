import Mathlib

/-!
# Composición de horas, prototipo propio comprobado localmente

This file concerns the reduced interior labor block of the new course paper.
It does not formalize existence/concavity of the HJB or the GE fixed point.
It is not an AppliedModelingLib paper-contribution receipt.
-/
namespace Barraza26LaborComposition

noncomputable def labor (v R psi phi : ℝ) : ℝ := (v * R / psi) ^ phi

noncomputable def share (v RF RI psiF psiI phiF phiI : ℝ) : ℝ :=
  labor v RI psiI phiI / (labor v RF psiF phiF + labor v RI psiI phiI)

lemma labor_pos {v R psi phi : ℝ} (hv : 0 < v) (hR : 0 < R) (hp : 0 < psi) :
    0 < labor v R psi phi := by
  exact Real.rpow_pos_of_pos (by positivity) _

lemma labor_hasDerivAt {v R psi phi : ℝ} (hv : 0 < v) (hR : 0 < R)
    (hp : 0 < psi) :
    HasDerivAt (fun x => labor x R psi phi) (phi * labor v R psi phi / v) v := by
  have hx : 0 < v * R / psi := by positivity
  have h := (((hasDerivAt_id v).mul_const R).div_const psi).rpow_const
    (p := phi) (Or.inl (ne_of_gt hx))
  have he : (v * R / psi) ^ (phi - 1) = (v * R / psi) ^ phi / (v * R / psi) := by
    rw [Real.rpow_sub hx, Real.rpow_one]
  convert h using 1
  dsimp [labor]
  rw [he]
  field_simp [ne_of_gt hv, ne_of_gt hR, ne_of_gt hp]

theorem share_hasDerivAt {v RF RI psiF psiI phiF phiI : ℝ}
    (hv : 0 < v) (hRF : 0 < RF) (hRI : 0 < RI)
    (hpF : 0 < psiF) (hpI : 0 < psiI) :
    HasDerivAt (fun x => share x RF RI psiF psiI phiF phiI)
      (share v RF RI psiF psiI phiF phiI *
        (1 - share v RF RI psiF psiI phiF phiI) * (phiI - phiF) / v) v := by
  have hF := labor_hasDerivAt (phi := phiF) hv hRF hpF
  have hI := labor_hasDerivAt (phi := phiI) hv hRI hpI
  have hden : labor v RF psiF phiF + labor v RI psiI phiI ≠ 0 :=
    ne_of_gt (add_pos (labor_pos hv hRF hpF) (labor_pos hv hRI hpI))
  have h := hI.div (hF.add hI) hden
  convert h using 1
  dsimp [share]
  field_simp [ne_of_gt hv, hden]
  ring

theorem composition_hasDerivAt {V : ℝ → ℝ} {a d RF RI psiF psiI phiF phiI : ℝ}
    (hV : HasDerivAt V d a) (hv : 0 < V a)
    (hRF : 0 < RF) (hRI : 0 < RI) (hpF : 0 < psiF) (hpI : 0 < psiI) :
    HasDerivAt (fun x => share (V x) RF RI psiF psiI phiF phiI)
      (share (V a) RF RI psiF psiI phiF phiI *
        (1 - share (V a) RF RI psiF psiI phiF phiI) * (phiI - phiF) * d / V a) a := by
  convert (share_hasDerivAt hv hRF hRI hpF hpI).comp a hV using 1
  ring

theorem share_between_zero_one {v RF RI psiF psiI phiF phiI : ℝ}
    (hv : 0 < v) (hRF : 0 < RF) (hRI : 0 < RI) (hpF : 0 < psiF) (hpI : 0 < psiI) :
    0 < share v RF RI psiF psiI phiF phiI ∧
      share v RF RI psiF psiI phiF phiI < 1 := by
  have hF := labor_pos (phi := phiF) hv hRF hpF
  have hI := labor_pos (phi := phiI) hv hRI hpI
  constructor
  · exact div_pos hI (add_pos hF hI)
  · exact (div_lt_one (add_pos hF hI)).2 (by linarith)

theorem composition_sign {V : ℝ → ℝ} {a d RF RI psiF psiI phiF phiI : ℝ}
    (hV : HasDerivAt V d a) (hv : 0 < V a) (hd : d < 0)
    (hRF : 0 < RF) (hRI : 0 < RI) (hpF : 0 < psiF) (hpI : 0 < psiI) :
    (phiF < phiI → deriv (fun x => share (V x) RF RI psiF psiI phiF phiI) a < 0) ∧
    (phiI = phiF → deriv (fun x => share (V x) RF RI psiF psiI phiF phiI) a = 0) ∧
    (phiI < phiF → 0 < deriv (fun x => share (V x) RF RI psiF psiI phiF phiI) a) := by
  have hs := share_between_zero_one (phiF := phiF) (phiI := phiI) hv hRF hRI hpF hpI
  have ht : 0 < share (V a) RF RI psiF psiI phiF phiI *
      (1 - share (V a) RF RI psiF psiI phiF phiI) := mul_pos hs.1 (by linarith [hs.2])
  have he := (composition_hasDerivAt (phiF := phiF) (phiI := phiI) hV hv hRF hRI hpF hpI).deriv
  refine ⟨?_, ?_, ?_⟩
  · intro hphi
    rw [he]
    exact div_neg_of_neg_of_pos (mul_neg_of_pos_of_neg (mul_pos ht (sub_pos.mpr hphi)) hd) hv
  · intro hphi
    rw [he, hphi, sub_self, mul_zero, zero_mul, zero_div]
  · intro hphi
    rw [he]
    exact div_pos (mul_pos_of_neg_of_neg (mul_neg_of_pos_of_neg ht (sub_neg.mpr hphi)) hd) hv

#print axioms composition_hasDerivAt
#print axioms composition_sign
end Barraza26LaborComposition
