# Au-alloy-supported-on-graphene
Workflow-driven approach for stability and catalytic modulation in the evolution of single-atom catalysts to Au-alloy clusters supported on graphene, as applied in [https://doi.org/10.1038/s41598-025-85891-6](https://doi.org/10.1038/s41598-025-85891-6).
<img title="Workflow" src="workflow.png">

# Colab
* Colab notebook for data visualization [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nlk0nvFGPDAAtO6J8oSc2dNsEmlUh2c0?usp=sharing)

This notebook calculates and provides a preview of the adsorption energy (*E<sub>ads</sub>*) and excess energy (*E<sub>exc</sub>*) in function of composition for clusters in both vacuum (vac) and adsorbed on graphene (ads) conditions. Users can apply it to the data generated in this work or their own datasets, as long as the output folders are named accordingly the `energy.py` requirement. Feel free to modify the code as needed.

# Output File Arrangement
All calculations were performed with Vienna *Ab initio* Simulation Package (VASP), in witch the files follows its syntax. The `converged_structures` folder contains the most stable configurations, written out in the `CONTCAR` file format. It also includes the `INCAR` file used for geometry optimization and the `OUTCAR` file containing only the final energy obtained from self-consistent field (SCF) minimization. Additionally, for evaluating covalent bond contributions through [Crystal Orbital Hamilton Population (COHP)](http://www.cohp.de/) analysis, the `lobsterin` input files used are also provided.

A calculation folder is named as `[condition]_[cluster]_[isomer]_[configuration]`, highlighting key aspects of the system. This structure is based organization of `converged_structures`, which follows:

**condition:** `vac` or `ads`&rarr; **atomicity:** `n_1` ... `n_4` &rarr; **composition:** `ni4`... `ni2au2`...`au4` &rarr; **isomers:** `vac_ni2au2_16`.

For adsorbed conditions, the folder names also include the `configuration`, which indicates the number of contact points (fold) and the geometry, e.g., `ads_ni3au1_30_3f_tetrahedron` represents a tetrahedral cluster with three contact points.






