# GNBR Neo4j Database

This repository contains code to download and build a dockerized neo4j graph database of the biomedical literature network generated in ["A Global Network of Biomedical Relationships Derived From Text"](https://dx.doi.org/2010.1093/bioinformatics/bty114) by Bethany Percha.  This update - [GNBR Version 5.0](https://zenodo.org/record/1495808) - includes publications through November 2018

#### New Features!

  - Download and format with single python executable
  - Themes scores are normalized by percentile rank
  - Revised data model for fast text search

Other improvements include:
  - Multithreaded dataset download
  - End-to-end file compression
  - Jupyter notebook documentation

## Prequisites
You will need an up to date version of Docker installed.  Download and installation instructions can be found on the [Docker website](https://docs.docker.com/install/).  They require you to sign up for an account, but Docker is incredibly useful and totally worth the minor annoyance.

You will also need to have Python 3+ with the `pandas` package installed.  Future versions of the build package will dockerize the python execution environment to  enable builds on systems without python or pandas.

I am assuming that you already have Python 3 installed as your default interpreter.  If not, then you should do so immediately.  To install `pandas` open a command terminal window and type 
```python
pip install pandas
```

## Configuration
Configuration options are stored in `config.py` in the build directory.  The most important configuation options are:
 - The GNBR download directory - `DWNLD_DIR`
 - Neo4j import directory - `NEO_DIR`

Set these with care as `NEO_DIR` needs to be harmonized with the neo4j import volume options in the docker shell script and docker-compose file.  Current default is to create these directories on the user's home directory.

## Download and Format
To download GNBR and format for neo4j import, simply run the python executable module:
```bash
python -m build
```
If you have a decent internet connection the download should be pretty fast.  The formatting takes a while (30 mins) and is quite memory intensive (20-30 GB peak usage).  Future updates will use the `dask` package for lazy, multi-threaded data processing and i/o.
## (Dockerized) Neo4J import
To import the data into neo4j, simply run the docker shell executable from your bash shell.
```bash
sh docker_neo4j_import.sh
```
Import should only take about 10-15 minutes.  Be sure that the environment (`--env=xxxx`) and volume (`--volume=xxxx`) flags point to the neo4j import directory specified in the `config.py` file as discussed above.

## Run Neo4J
Simply type:
```bash
docker-compose up
```
You should have a neo4j database running locally on port 7474.  You can access it at any time by pointing your web browser at `http://localhost:7474/browser/`.  As mentioned before, make sure that the volumes listed in `docker-compose.yaml` agree with those specified in the docker shell script and python executable.  Example: 
```
volumes:
  -path/to/import:/import
  -path/to/database:/data
  -path/to/logfile:/logs
``` 
## Shutdown Neo4J
Open a command terminal window and type:
```bash
docker-compose down
```
And that's it!  No need to  install or configure Neo4J.  Docker handles all that for you, no matter what system you run.  As stated before, newer versions of this build packacge will dockerize the python executable to completely remove dependencies other than docker.

## Caveats
Practice good docker hygiene. Don't bring up multiple local instances of the neo4j.  This can cause to weird and univtuitive behaviors.  When in doubt, run the shutdown command before bringing up a database instance.  I also recommend learning how to erase/remove docker images, which is beyond the scope of this README, but well within the scope of a Google search.

## Next Steps
In addition to all the other stuff I mentioned before, future iterations of this repository will include some cypher queries and a tutorial for using the Neo4J web browser interface with some cypher queries, as well as a Jupyter Notebook tutorial for using the high performance bolt interface.