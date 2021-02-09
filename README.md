# CSI-Murder

### Description

Passive device-free localization of a person exploiting the Channel State Information (CSI) from Wi-Fi signals is quickly becoming a reality. While this capability would enable new applications and services, it also raises concerns about citizens’ privacy. In this work, we propose a carefully-crafted obfuscating technique against one of such CSI-based localization methods. In particular, we modify the transmitted I/Q samples by leveraging an irreversible randomized sequence. I/Q symbol manipulation at the transmitter distorts the location-specific information in the CSI while preserving communication, so that an attacker can no longer derive information on user’s location. We test this technique against a Neural Network (NN)-based localization system and show that the randomization of the CSI makes undesired localization practically unfeasible. Both the localization system and the randomization CSI management are implemented in real devices. The experimental results obtained in our laboratory show that the considered localization method (first proposed in an MSc thesis) works smoothly regardless of the environment, and that adding random information to the CSI mess up the localization, thus providing the community with a system that preserve location privacy and communication performance at the same time.

---

### What's included in the repository 


- [CSI Randomizer](https://github.com/ansresearch/csi-murder/tree/master/csi-randomizer)

Generates WiFi frames using the Matlab WLAN Toolbox and transmits them using a SDR platform.
The CSI of each frame can be artificially altered at will to disrupt a localization framework and prevent unauthorized surveillance attacks.
Tested on a Ettus USRP N300.

- [Device Free Indoor Localization](https://github.com/ansresearch/csi-murder/tree/master/device-free-localization):

Trains a simple convolutinal neural network (CNN) to localize one human inside a room by exploiting CSI of received packets only.
More details on this project can be found in the master thesis [Device-Free Indoor Localization: A User-Privacy Perspective](http://dx.doi.org/10.13140/RG.2.2.25468.56965).
			
### Usage

Instructions for running the programs in this repository are included in the READMEs in the corresponding subfolders.
For futher details, please have a look at the documents in the references.

### References

This repository contains the source code of [An Experimental Study of CSI Management to Preserve Location Privacy](https://dl.acm.org/doi/10.1145/3411276.3412187) by M. Cominelli, F. Kosterhon, F. Gringoli, R. Lo Cigno and A. Asadi
