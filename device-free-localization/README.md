# CNN for device-free localization

This script contains a minimal implementation (based on Tensorflow) of a CNN that can be used for device-free localization. Some additional packages apart from Tensorflow are needed; they're all required at the beginning of the script.

The sample data files "clean_32pos.mat" and "positions32.mat" mentioned in the script are not included in this repository because they are very large, but they can be downloaded using the following links:

- [clean_32pos.mat](http://netweb.ing.unibs.it/ntw/tools/csimurder/clean_32pos.mat)
- [positions32.mat](http://netweb.ing.unibs.it/ntw/tools/csimurder/positions32.mat)

The CSI files have been obtained with Matlab using the tools from the [nexmon-csi](https://github.com/seemoo-lab/nexmon_csi) project. Their structure is briefly commented in the script. It is also possible to load them into Matlab and plot the different CSI profiles.

The original implementation of the CNN, based on PyTorch, can be found [at this repository](https://github.com/seemoo-lab/csicloak) (**WARNING:** repository very large!)
