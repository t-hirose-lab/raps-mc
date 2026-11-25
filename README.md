# RAPS-MC
Multicohort Regional Amyloid PET Score: the fixed **26-region** model.

RAPS-MC was developed using 1,129 participants from ADNI (515), NACC SCAN (471) and OASIS-3 (143). It was evaluated exploratorily in the A4 placebo cohort. This repository provides the coefficients and a portable calculator.

## Model identity
- Model: RAPS-MC, 26 regions; initial software release: v1.0.0.
- This is a separate model from the [original nine-region RAPS](https://github.com/t-hirose-lab/raps-regional-amyloid-pet-score).
- The two models have different coefficients, input requirements and scaling. Their parameters must not be interchanged.
- RAPS-MC uses fixed development-sample scaling, including the score standard deviation. Do not re-centre or re-scale scores within a new cohort.
- Release: https://github.com/t-hirose-lab/raps-mc/releases/tag/v1.0.0

## Input
Supply the exact 26 column names listed in RAPS26_coefficients.csv. Each value must be a finite, positive regional SUVR **already referenced to cerebellar cortex**. Missing values or regions are rejected; there is no imputation.

The calculator does not perform segmentation, reference conversion or tracer harmonisation. Confirm the compatibility of regional labels and PET processing before applying it to new data. Clinical variables and Centiloid are not calculator inputs.

## Quick start
Python 3.9 or newer; no third-party packages are required. Download and extract the release ZIP, then run:

    python score_raps26.py --input synthetic_input.csv --output example_scores.csv --reference cerebellar_cortex

Replace synthetic_input.csv with your regional SUVR file for use with new data. Existing output files are not overwritten.

The output preserves input row order and contains row_number, RAPS_raw and RAPS_z. These output names are retained for computational compatibility; in this repository they refer to **RAPS-MC**, not the nine-region score.

## Calculation
For each region, subtract its development-sample mean and divide by its development-sample standard deviation. Multiply by its coefficient, sum across the 26 regions and add the intercept:

    RAPS_raw = intercept + sum(coefficient * (SUVR - training_mean) / training_sd)
    RAPS_z = (RAPS_raw - training_score_mean) / training_score_sd

RAPS26_constants.json also provides the equivalent raw-SUVR formula. Use the full-precision files, not rounded manuscript tables.

## Files
- RAPS26_coefficients.csv: 26 non-zero coefficients and input-scaling parameters.
- RAPS26_constants.json: intercepts, score-scaling constants, region order and model identifier.
- RAPS76_all_coefficients.csv: all 76 development inputs, including zero coefficients.
- score_raps26.py: calculator.
- synthetic_input.csv, synthetic_expected_output.csv: artificial examples, not participant records.
- test_score.py: reproducible checks of the supplied calculator.
- release.json, SHA256SUMS.txt: release identity and file integrity information.

## Interpretation
Higher scores indicate the direction associated with greater cognitive decline in model development. The score is a continuous PET summary; it is not an absolute risk probability, treatment-response estimate or calibrated CDR-SB slope.

A4 was excluded from estimation of the regional coefficients but was examined during exploratory model-design comparisons. The A4 evaluation is exploratory. This package contains the final full-development model, not the separately retrained cross-validation models or the full study analysis pipeline.

## Associated manuscript
Hirose T, Akamatsu W, Kato T, for ADNI. *A multicohort regional amyloid PET score (RAPS-MC) for predicting cognitive decline.*

Publication details will be added when available. For reproducible use, cite this repository and the specific release v1.0.0.

## Data and licence
No participant records, identifiers, source datasets or fitted training object are distributed. Original cohort data remain subject to their respective access conditions.

Code and model files are distributed under the MIT licence.
