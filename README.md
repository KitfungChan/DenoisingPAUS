# The PAU survey: Self-supervised image denoising and photometry

This repository contains the project associated with the paper:

**“The PAU survey: Self-supervised image denoising and photometry”** Chen et al. (in prep.)

## Denoising models

We tested **Probabilistic Noise2Void (PN2V)** using the public PN2V implementation:

● PN2V repository: <https://github.com/juglab/pn2v>


● PN2V paper: <https://arxiv.org/abs/1906.00651>

In this project, we implement **Noise2Void (N2V)** using the PN2V package. Our proposed model, **LoRA-N2V**, is built on top of N2V by integrating **LoRA adapters**.

## Simulation pipeline

The simulation pipeline used in this project is maintained in a separate repository from our group:

● Flagship4ML: <https://github.com/marberi/Flagship4ML>

## PAUS data

The PAUS images required to reproduce the results in this repository are publicly available through the official PAUS public data release:

● PAUS public data release: <https://pausurvey.org/public-data-release/>

## Additional data and trained models

Denoising the PAUS images is time-consuming. For convenience, we provide precomputed data products, including:

● Denoised galaxy fluxes


● Aperture fluxes


● Simulation images


● Trained models


● Selected training data for the LoRA-N2V



The denoised fluxes and aperture fluxes are stored as CSV files, while the simulation images are stored as NPY files. These files, together with the trained models, are available on Zenodo (The descriptions and details of the files are in the README.md in the zenodo):

● Zenodo record: https://doi.org/10.5281/zenodo.21197885

After downloading the files, unzip them into the corresponding folders ('data saved' and 'model saved') in this repository.

## Non-public simulation inputs

The simulations used in Appendix C are generated using noiseless fluxes from the **Flagship-PAU** catalogue in CosmoHub. This catalogue is currently internal to the PAUS collaboration and is not publicly available.
