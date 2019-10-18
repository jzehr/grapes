# Welcome to the Grapes Repo! 

```Snakefile_all ``` is for all the viruses from ncbi, i am currently working with only GLRaV3
    print(dir(Blast))

```python python/all_country_json.py --file rsrc/GLRaV3_10-2-19_sequence.gbc.xml ```
``` python python/region_seq.py -x rsrc/GLRaV3_10-2-19_sequence.gbc.xml -j rsrc/GLRaV3_regions.json ```

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

- you should see a ```(grape)``` show up to the left of your command line
 
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

```bash starter.sh```


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
