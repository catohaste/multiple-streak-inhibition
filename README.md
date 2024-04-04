# multiple-streak-inhibition
Solving a system of ODEs to model interactions preventing the formation of multiple streaks

## Quickstart

Code has been tested with Python 3.9.13. Please note that the creation of the animated output requires `ffmpeg` to be installed, which can be found [here](https://ffmpeg.org/).

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
