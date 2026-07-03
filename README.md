# Denoising PAUS image with N2V.
The project for the paper "The PAU survey: Self-supervised image denoising and photometry" Chen et al. (in prep)

We tested the Probabilistic Noise2Void (PN2V), the PN2V implementation is available at https://github.com/juglab/pn2v. According to the PN2V paper (https://arxiv.org/abs/1906.00651), PN2V provides the same functionality as N2V but without requiring an explicit noise model. We implement N2V using the PN2V package. Our proposed model, LoRA-N2V, is built on top of N2V by integrating LoRA adapters.

The simulation pipeline in the project is in another repository in our group: https://github.com/marberi/Flagship4ML. Feel free to adapt it to your needs.

A subset of the PAUS data, including the images necessary to reproduce the results in this repository, is publicly available. You can access the data via the official https://pausurvey.org/public-data-release/.

Since denoising the images take a long time, we save the denoised galaxy flux into .csv file. We also save the simulation images into .npy file. The .npy and .csv files were put in:
