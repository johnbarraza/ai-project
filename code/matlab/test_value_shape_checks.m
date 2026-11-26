function test_value_shape_checks
% Include a convex counterexample and nonuniform assets to catch false passes.
a = [1; 1.5; 3; 7];
concave = value_shape_checks(a, log(1+a), 1./(1+a));
assert(concave.concave_computed_value_with_tolerance);
assert(concave.strictly_negative_computed_curvature);
assert(concave.nonincreasing_marginal_value_with_tolerance);
convex = value_shape_checks(a, a.^2, 2*a);
assert(~convex.concave_computed_value_with_tolerance);
assert(~convex.nonincreasing_marginal_value_with_tolerance);
linear = value_shape_checks(a, 2*a, 2*ones(size(a)));
assert(linear.concave_computed_value_with_tolerance);
assert(~linear.strictly_negative_computed_curvature);
mixed = value_shape_checks(a, [log(1+a), a.^2], [1./(1+a), 2*a]);
assert(~mixed.concave_computed_value_with_tolerance);
fprintf('PASS: value-shape checks reject convex/mixed cases and distinguish weak from strict concavity.\n');
end
