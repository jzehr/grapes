<<<<<<< HEAD
# Welcome to the Grapes Repo! 

```Snakefile_all ``` is for all the viruses from ncbi, i am currently working with only GLRaV3
    print(dir(Blast))

```python python/all_country_json.py --file rsrc/GLRaV3_10-2-19_sequence.gbc.xml -l rsrc/locations_to_test.json```
```python python/region_seq.py -x rsrc/GLRaV3_10-2-19_sequence.gbc.xml -j rsrc/GLRaV3_regions.json ```
```python python/protein_region_cat.py -f data/GOOD_PRODS.json```
In this repo you will find data from pathogens that impact grapevines. The goal of this repo is to use this data to analyze and examine pathogen diversity.

This repo was made by scraping NCBI with the following search term ```virus[ORGN] grapevine``` and downloading these results as an XML file. This XML file is placed in the ```rsrc``` folder of the pipeline and the rest is history. This pipeline works to compare selectio of these viruses across different locations throughout the world.

To get a quick overview of how the pipeline works, click on the `pipeline.svg` file!
___
### Dependencies:
	python=3.7
	pip=19.2.1
[MAFFT](https://mafft.cbrc.jp/alignment/software/): (MAFFT v7.427 (2019/Mar/24))

[IQ-TREE](http://www.iqtree.org/#download)  (IQ-TREE multicore version 1.6.11 for Mac OS X 64-bit built Jun  6 2019)
	
	hyphy
	hyphy-analysis
___

Make sure to read the docs for BOTH hyphy-develop and [hyphy-analyses](https://github.com/veg/hyphy-analyses). These external repos will allow you to run useful commands on the data.
Once you run the hyphy-develop code, CLONE THE hyphy-analyses REPO AND CD INTO IT TO USE IT.
___
### Install:

- navigate to the grapes directory:

	```cd to/the/grapes ```

- activate the virtual environment:

	```source envs/grapes/bin/activate```

- you should see a ```(grapes)``` show up to the left of your command line
 
- it might be useful to run:

	```pip install --upgrade pip```

- then, set up your virtual environment:

	``` pip install -r requirements.txt ``` 

- cd back to the base directory 
___

___
### To Run

- from the base grapes directory ```cd python/```
- then run this python script:

- then
```cd .. ```
```snakemake all ```

- you can spice this up by adding a ```-j #``` flag after that command to provide snakemake with the available number of cores to run on.
- if you use something like ```bpsh``` then just add ```bpsh #``` before the ```snakemake``` command

___
### Test:
___
### Visualizing:

When your tree files are created, you can use [Phylo Tree](phylotree.hyphy.org) to view it!

___

### Contact:

email: `jordan.zehr@temple.edu`
=======
# HyPhy - Hypothesis testing using Phylogenies

HyPhy is an open-source software package for the analysis of genetic sequences using techniques in phylogenetics, molecular evolution, and machine learning. It features a complete graphical user interface (GUI) and a rich scripting language for limitless customization of analyses. Additionally, HyPhy features support for parallel computing environments (via message passing interface (MPI)) and it can be compiled as a shared library and called from other programming environments such as Python and R. HyPhy is the computational backbone powering datamonkey.org. Additional information is available at hyphy.org.

## Quick Start

#### Install  
`conda install hyphy`

#### Run with Command Line Arguments
`hyphy <method_name> --alignment <path_to_alignment_file> <additional_method_specific_arguments>`  
+ _`<method_name>` is the name of the analysis you wish to run (can be: absrel, bgm, busted, fade, fel, fubar, gard, meme, relax or slac)_
+ _`<path_to_alignment_file>` is the relative or absolute path to a fasta, nexus or phylib file containing an alignment and tree_
+ _A list of the available `<additional_method_specific_arguments>` can be seen by running `hyphy <method_name> --help`_

or  

#### Run in Interactive Mode
`hyphy -i`  

## Building from Source

#### Requirements
* cmake >= 3.12
* gcc >= 4.9
* libcurl
* libpthread
* openmp (can be installed on mac via `brew install libomp`)

#### Download
You can download a specific release [here](https://github.com/veg/hyphy/releases) or clone this repo with

`git clone https://github.com/veg/hyphy.git`

Change your directory to the downloaded/cloned directory

`cd hyphy`

#### Build
`cmake .`

`make install`

## Additional Options for Building from Source

#### Build Systems
If you prefer to use other build systems, such as Xcode, configure using the -G switch

`cmake -G Xcode .`

CMake supports a number of build system generators, feel free to peruse these and use them if you wish.

If you are on an OS X platform, you can specify which OS X SDK to use

`cmake -DCMAKE_OSX_SYSROOT=/Developer/SDKs/MacOSX10.9.sdk/ .`

If building on a heterogeneous cluster with some nodes that do not support auto-vectorization  

`cmake -DNOAVX=ON .`.

If you're on a UNIX-compatible system, and you're comfortable with GNU make, then run `make` with one of the following build targets:

+   MP or hyphy - build a HyPhy executable (This used to be "HYPHYMP" but is now just "hyphy") using pthreads to do multiprocessing
+   MPI - build a HyPhy executable (HYPHYMPI) using MPI to do multiprocessing
+   HYPHYMPI - build a HyPhy executable (HYPHYMPI) using openMPI 
+   LIB - build a HyPhy library (libhyphy_mp) using pthreads to do multiprocessing
-   GTEST - build HyPhy's gtest testing executable (HYPHYGTEST)

#### Example (MPI build of hyphy using openMPI)
Ensure that you have openmpi installed and available on your  path. You can check if this is the case after running `cmake .` you should see something similar to this in your output

`-- Found MPI_C: /opt/scyld/openmpi/1.6.3/gnu/lib/libmpi.so;/usr/lib64/libibverbs.so;/usr/lib64/libdat.so;/usr/lib64/librt.so;/usr/lib64/libnsl.so;/usr/lib64/libutil.so;/usr/lib64/libm.so;/usr/lib64/libtorque.so;/usr/lib64/libm.so;/usr/lib64/libnuma.so;/usr/lib64/librt.so;/usr/lib64/libnsl.so;/usr/lib64/libutil.so;/usr/lib64/libm.so `

`-- Found MPI_CXX: /opt/scyld/openmpi/1.6.3/gnu/lib/libmpi_cxx.so;/opt/scyld/openmpi/1.6.3/gnu/lib/libmpi.so;/usr/lib64/libibverbs.so;/usr/lib64/libdat.so;/usr/lib64/librt.so;/usr/lib64/libnsl.so;/usr/lib64/libutil.so;/usr/lib64/libm.so;/usr/lib64/libtorque.so;/usr/lib64/libm.so;/usr/lib64/libnuma.so;/usr/lib64/librt.so;/usr/lib64/libnsl.so;/usr/lib64/libutil.so;/usr/lib64/libm.so `

Then run 

`make HYPHYMPI`

And then run make install to install the software

`make install`

+   hyphy will be installed at  `/location/of/choice/bin`
+   libhyphy_mp.(so/dylib/dll) will be installed at `/location/of/choice/lib`
+   HyPhy's standard library of batchfiles will go into `/location/of/choice/lib/hyphy`


#### Building for Testing
HYPHYGTEST isn't installed normally, because it serves no utility outside of testing.

To test HyPhy, build with the  GTEST target and run ./HYPHYGTEST from the source directory.  
`make GTEST`  
`./HYPHYGTEST`

#### Executable Location

By default, HyPhy installs into `/usr/local` but it can be installed on any location of your system by providing an installation prefix

`cmake -DINSTALL_PREFIX=/location/of/choice`

For example, this configuration will install hyphy at /opt/hyphy

`mkdir -p /opt/hyphy`

`cmake -DINSTALL_PREFIX=/opt/hyphy .`

#### Building Documentation

```
make docs
cd docs
python3 -m http.server
```

>>>>>>> 0d6820b3671a0218de6dada6b2edf1b79995b657
