# pvtools
PVtools provides open source software related to photovoltaics.
This page is the github repo for the pvtools Heroku app built in plotly dash.

# Applications

The pvtools package contains multiple different applications for photovoltaics. These include:
- **String Length Calculator**. Method for calculating the maximum allowable string length for a photovoltaic system. 

# Files

- **index.py** - Homepage for pvtools website. To run the app, run this script.
- **string_length_calculator.py** - Page for calculating string length.
- 

# Logging

We take privacy seriously.

We use coralogix to log basic usage information. This allows us to determine how many unique users have accessed the site.

We also log each time the 'calculate' button is pressed, but do not record any metadata about the system design.  

# Todo

- Change name of mean yearly min drybulb to exactly correspond to NEC.
- Document! 
- Remove mapbox access token from code.
- Add click callback for map.
- Fix references.

# Change log

- Jinja2 ~> 2.10.1. to fix security vulnerability.


# Install Notes

In order to set up this application in Heroku, we followed the [Heroku install instructions](https://dash.plot.ly/deployment) but deleted the following lines from requirements.txt:
```
functools32==3.2.3.post2
futures==3.2.0
```

# Copyright

String Length Calculator Copyright (c) 2020, The Regents of the University of
California, through Lawrence Berkeley National Laboratory (subject to receipt of 
any required approvals from the U.S. Dept. of Energy).  All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.
