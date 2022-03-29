Gene Project Data
=====

This repository contains the [salmon](https://combine-lab.github.io/salmon/) quantification result of RNA sequences from
17 organs.

## Data

- [salmon_quants](salmon_quants) : contains the `.csv` files of salmon quantification for each organ. Each file contains
  all samples associated with the organ.
    - The rows of the table are the run number of samples (starting with SRR), and the column of the table is a list of
      genes.
    - The quantification result is derived from the length scaled TPM (Transcripts Per Million) of the raw salmon
      output. Numbers are rounded to the nearest integer value.


- [Tissue_Age_Tables](Tissue_Age_Tables): contains the Excel table of the quantification for the 17 organs. Each Excel
  file includes several sheets, where each sheet contains samples of the same age.
    - The rows and columns are the same as the above `.csv` files.
    - In each sheet, mean and standard deviation values from the samples in that sheet (same age and tissue) are
      included.
    - `age_analysis.py` is used to generate Excel files in `Tissue_Age_Tables` from `salmon_quants`
 