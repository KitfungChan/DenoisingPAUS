The project for the paper "The PAU survey: Self-supervised image denoising and photometry" Chen et al. (in prep)

We tested the Probabilistic Noise2Void (PN2V), the PN2V implementation is available at https://github.com/juglab/pn2v. According to the PN2V paper (https://arxiv.org/abs/1906.00651), PN2V provides the same functionality as N2V but without requiring an explicit noise model. We implement N2V using the PN2V package. Our proposed model, LoRA-N2V, is built on top of N2V by integrating LoRA adapters.

The simulation pipeline in the project is in another repository from our group: https://github.com/marberi/Flagship4ML.

The PAUS images necessary to reproduce the results in this repository, is publicly available. You can access the data via the official https://pausurvey.org/public-data-release/.

The simulations used in Appendix C are generated using the noiseless fluxes from the "Flagship-PAU" catalogue in CosmoHub, which is currently internal to the PAUS collaboration and is not publicly available.

Since denoising the images is timeconsuming, we save the denoised galaxy fluxes and the aperture fluxes in CSV files and the simulation images in NPY files. Both these data files and the trained models are publicly available on Zenodo. Download the files and unzip them into the corresponding folder. Description of the data and models:

Fig.3 uses the data 'stampcor_bright.npy', 'stampcle_bright.npy', and model "N2V_simulation.net". We denoise one simulated image in 'stampcor_bright.npy' with the model "N2V_simulation.net", and comparing with other baselines. The noiseless target is in the 'stampcle_bright.npy'.

Fig.4 used the data 'stampcor.npy', 'stampcle.npy', 'stampcor_small.npy', 'stampcle_small.npy' and model "N2V_simulation2.net". With the model "N2V_simulation2.net", we denoise the simulated images in the 'stampcor.npy' and 'stampcor_small.npy' and calculated the galaxy flux from the denoised images and the noiseless images in the 'stampcle.npy' 'stampcle_small.npy'.

Fig.5 uses the data 'stampcor_bright.npy', 'stampcle_bright.npy', and model "N2V_simulation.net", "constrained_N2V_simulation.net". We denoise one simulated galaxy in the 'stampcor_bright.npy' with model "N2V_simulation.net" and "constrained_N2V_simulation.net" to plot the 800 outputs.

Fig.6 uses the data 'constrained_n2v_denoised.csv' and 'standard_n2v_denoised.csv'. We plot the galaxy flux ratio after denoising with standard N2V and constrained N2V.

Fig.7 uses the data 'lora-n2v_trainingset.csv', 'constrained_n2v_denoised.csv', 'standard_n2v_denoised.csv', 'lora-n2v_denoised_singleband_22-23.csv', 'lora-n2v_denoised_singleband_17-21.csv' and 'lora-n2v_denoised_singleband_21-22.csv'. We plot the df histograms of no denoising, standard N2V denoising, constrained N2V denoising and LoRA-N2V denoising. Note that the 'lora-n2v_trainingset.csv' is the training set of the LoRA-N2V, we should remove this part when calculating the df of LoRA-N2V denoising.

Fig.8 uses the data 'denoisedgalaxy17-20brightmodel.csv', 'denoisedgalaxy22-23model1.csv', 'denoisedgalaxy21-22model1.csv', 'denoisedgalaxy20-21brightmodel.csv'. We plot the galaxy flux ratio before and after denoising with LoRA-N2V in band NB645.

Fig.9 uses the data 'bands_denoisedfaint_part1.csv', 'bands_denoisedfaint_part2.csv', 'bands_denoisedmedian.csv' and 'bands_denoisedbright.csv'. We plot the sigma68 of the df in the function of PAUS bands. (They can be also used to calculated the df histogram and the flux ratio of the multiple bands.)

Fig.10 uses the data 'sigma68_denoise.csv', 'sigma68_ori.csv', and model "lora_bands_bright.pth". We denoise one exposure in different bands and plot the SED. The error bars are calculated with the sigma68 data in 'sigma68_denoise.csv' and 'sigma68_ori.csv'.

Fig.A2 uses the model "N2V_PAUS.net", "PN2V_PAUS.net" and 'PAUSnoiseModel.npy'. We denoise one galaxy with standard N2V and standard PN2V to show the N2V behaves better than PN2V when denoising the PAUS images.

Fig.C1 uses the data 'flagship.csv'. We plot the flux-ratio diagnostics to distinguish genuine noise reduction from systematic flux bias.

Figs.D uses the model "lora_model_final2.pth". We plot the different denoising examples with LoRA-N2V.

The LoRA-N2V for single band is trained with the data 'lora-n2v_trainingset.csv'(for bright galaxy the magnitude < 21, the faint galaxy magnitude > 21), and LoRA-N2V for multiple bands is train with 'selectbrightdata.csv' (for bright galaxy), 'selectfaintdata.csv'(for faint galaxy).

'train n2v with PAUS.ipynb' uses the PAUS data 'stamps_515.zarr' to train the standard N2V.

'train n2v with simulation.ipynb' uses the simulated images 'stampcor.npy' to train the standard N2V.

'train pn2v with PAUSdm.ipynb' uses the data 'stamps_515.zarr' and noise model 'PAUSnoiseModel.npy' to train the PN2V.

'generate PAUS noisemodel.ipynb' uses the data 'denoised_stamps.npy' and 'cleanstamps_allbandsnew.zarr' to generate the empirical noise model.

'test(faster_version).ipynb' use the data 'bright_middle.csv', 'median_middle.csv', 'faint_middle.csv' to directly denoise the PAUS images in multiple bands with LoRA-N2V. Note that here 'bright_middle.csv' is the galaxy in the magntitude <20, 'median_middle.csv' is the galaxy in the magntitude [20,22], 'faint_middle.csv' is the galaxy in the magntitude [22,23]. Since the dataset is too large, we have to seperate it into 3 parts. When denoising, we still use the bright model for the the galaxy in the magntitude < 21, the faint model for the galaxy in the magntitude > 21.
