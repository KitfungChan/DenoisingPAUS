The project for the paper "The PAU survey: Self-supervised image denoising and photometry" Chen et al. (in prep)

We tested the Probabilistic Noise2Void (PN2V), the PN2V implementation is available at https://github.com/juglab/pn2v. According to the PN2V paper (https://arxiv.org/abs/1906.00651), PN2V provides the same functionality as N2V but without requiring an explicit noise model. We implement N2V using the PN2V package. Our proposed model, LoRA-N2V, is built on top of N2V by integrating LoRA adapters.

The simulation pipeline in the project is in another repository from our group: https://github.com/marberi/Flagship4ML.

The PAUS images necessary to reproduce the results in this repository, is publicly available. You can access the data via the official https://pausurvey.org/public-data-release/.

The simulations used in Appendix C are generated using the noiseless fluxes from the "Flagship-PAU" catalogue in CosmoHub, which is currently internal to the PAUS collaboration and is not publicly available.

Since denoising the images is time-consuming, we save the denoised galaxy fluxes and the aperture fluxes in CSV files and the simulation images in NPY files. Both these data files and the trained models are publicly available on Zenodo. Download the files and unzip them into the corresponding folder. Description of the data and models is in the README.md in the zenodo.
