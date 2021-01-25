# Webinar Data Solutions DEMO

This repository contains the demo code used in the

> [Bright Webinar "The Hitchhiker's Guide to Data Solutions".](https://www.meetup.com/Bright-Cubes-Bright-Sessions/events/275582047/)

It contains two examples:

* Corona, an example of a statistical simulation for epidemology
* Line detector, a classical Computer Vision model on line detection

Both examples are completely stand-alone examples.

## Setup

Setup is easy. From the Git root directory, follow the following steps
(replace `<example_directory>` with `corona` for the statistical simulator
example, and with `line-detector` for the Computer Vision example).

### Linux

```bash
cd <example_directory>/
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Windows

```powershell
cd <example_directory>/
python3 -m venv venv
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Corona Simulator

This is the statistical simulation example for an epidemic outbreak.

### Running the Corona Simulator

Running can be done as a standalone python program using the following script.

#### Running `corona.py` in Linux

```bash
cd corona/
source venv/bin/activate
python3 line_detector.py
```

#### Running `corona.py` in Windows

```powershell
cd corona\
.\venv\Scripts\activate
.\venv\Scripts\python.exe line_detector.py
```

### Running `corona` tests

Tests can be run using the following script.

#### Running `corona` tests in Linux

```bash
cd corona/
source venv/bin/activate
python3 -m pytest
```

#### Running `corona` tests in Windows

```powershell
cd corona\
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pytest
```

## Line Detector

This is the classical Computer Vision example.

It comes with a small example data set in the `data/` sub-directory.

### Running the Line Detector

Running can be done either as an interactive IPython notebook using
Visual Studio Code, or as a full Python program using

#### Running `line_detector.py` in Linux

```bash
cd line-detector/
source venv/bin/activate
python3 line_detector.py
```

#### Running `line_detector.py` in Windows

```powershell
cd line-detector\
.\venv\Scripts\activate
.\venv\Scripts\python.exe line_detector.py
```
