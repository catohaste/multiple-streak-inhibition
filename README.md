# multiple-streak-inhibition
Solving a system of ordinary differential equations to model interactions preventing the formation of multiple primitive streaks in developing chick embryos.

## Introduction

This software models interactions between a streak-inducer, a streak-inhibitor and calcium activity in a ring of cells during chick embryonic development. The interactions result in the initiation of primitive streak formation in biologically realistic positions and over relevant timescales. The dynamics are studied in an intact embryo and in an isolated anterior half. A representation of the latter is shown below.

https://github.com/user-attachments/assets/ba1ae332-57f2-49c6-98c2-76c674605bdd

## Quickstart

Code has been tested with Python 3.12.2. Please note that the creation of the animated output requires `ffmpeg` to be installed, which can be found at the [FFmpeg website](https://ffmpeg.org/).

#### Download code
```
git clone https://github.com/catohaste/multiple-streak-inhibition.git
cd multiple-streak-inhibition
```

#### Create and activate virtual environments with all required packages
```
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

#### Run files
```
python intact_embryo.py
python make_cut.py
```
