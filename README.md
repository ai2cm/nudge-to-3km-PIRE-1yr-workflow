# Nudged-to-3km PIRE experiments

The code in this repository reproduces the results of our nudge-to-fine-res paper using the yearlong fine-grid run. 
The fine-grid C3072 simulation was run on NOAA's Gaea supercomputer. 
This data was made available to us at an intermediate coarsened C384 resolution and stored in the AI2 Climate Modeling Google Cloud Storage buckets.
Below is an outline of the workflow to reproduce the training data, ML model training, offline and prognostic evaluation, and figures.

Before submitting any argo workflows, make sure to `make deploy` in the `workflows` directory to use the correct images.

## Data

### C48 coarsening
The fine-grid simulation data is stored at C384 resolution (coarsened down from its native C3072 resolution).
Running `scripts/coarsen_restarts.sh` and `scripts/coarsen_pire_dyn.sh` will coarsen this data to C48 resolution, which is the resolution of our coarse-grid FV3GFS model.

### Nudged training run

#### Prescribed surface data
The nudged run has the sea ice fraction, land sea mask, SSTs, precipitation, and surface radiative fluxes prescribed to the values from the coarsened fine-res reference.
Running the scripts `scripts/prescribed_seaice.py, scripts/prescribed_ssts.py, scripts/prescribed-sfc-fluxes-precip.py` will create the datasets of prescribed fields for use in the nudged run.

#### Nudged FV3GFS run
The nudged run is created by submitting the argo workflow via `workflows/nudge-to-fine-run/run.sh`.

### Training ML models
Models used in the final results as well as sensitivity tests are trained by running the `*/run.sh` scripts in the subdirectories of `train-evaluate-prognostic-run`.
The offline diagnostics are also created automatically by those argo workflows.


### Prognostic runs
Baseline and ML-corrected coarse-grid simulations can be reproduced by running the `run.sh` scripts in the correspondingly named subdirectories of `prognostic-run`.

### Figures
Figures from the paper are created in the notebooks in the folder `figure_notebooks`. The notebook `figure_notebooks/composite_figures.ipynb` reduces the size of the eps files and combines subfigures into a single file.