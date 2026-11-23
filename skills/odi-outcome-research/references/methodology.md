# Quantitative and qualitative decisions

## Job and outcome
A job map describes what must be achieved, not a product's screen sequence. Probe eight standard stages, but mark inapplicable ones explicitly. Separate consumption-chain work (purchase/setup/maintenance) from the core functional job. An outcome statement combines improvement direction, measurable criterion, object/context, and step; it must not smuggle a preferred feature into the criterion.

## Measurement gate
Before scoring, identify population/executor, questionnaire wording, response categories, recruitment and sample, valid n for each dimension/outcome, missingness, weighting, and source. A mean ordinal rating does not establish a top-two-box proportion. Team importance scores do not become customer data. Qualitative evidence alone cannot supply a numeric opportunity map.

For unweighted top-two-box counts: I = 10 × important_count / importance_valid_n; S = 10 × satisfied_count / satisfaction_valid_n. State that this maps proportions to 0–10. Different valid denominators must be disclosed; they do not make the two dimensions incomparable automatically, but missingness may bias their comparison. Weighted surveys require their actual weighting protocol and cannot be reconstructed from unweighted counts.

## Formula convention and disagreement
The default is O = I + max(I − S, 0), supported by Strategyn's “Why Innovation Fails”. Another official article (“Quantify Your Customers' Unmet Needs”) displays I + (I − S) without the clamp. These differ when S > I. Report the selected convention and implications; do not silently combine scores across variants or describe the discrepancy as resolved universally.

On a 0–10 scale, I=8 and S=3 gives O=13 in both variants. I=3 and S=8 gives O=3 with the clamp and −2 without it. These are teaching calculations, not customer findings. Changing the scale changes numerical cutoffs. Do not apply a 0–10 cutoff to a 0–100 score.

Use the supplied stdlib script for unweighted count arithmetic. It rejects invalid denominators, nonfinite/out-of-range counts, duplicate IDs, and missing variant selection. It cannot diagnose sampling bias or certify ODI. A high score is not product demand or success probability.

## Segmentation and uncertainty
Inspect outcome patterns within meaningful executor situations before choosing solutions. Do not invent clusters from aggregate means or treat demographics alone as need-based segmentation. If sample design cannot support a population estimate, report descriptive sample results and explicit limits. State sensitivity to missingness, formula choice, and sample composition rather than fabricating confidence intervals.
