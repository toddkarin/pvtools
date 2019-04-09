# pvtools
PVtools provides open source software related to photovoltaics.
This page is the github repo for the pvtools Heroku app built in plotly dash.

# Applications

The pvtools package contains multiple different applications for photovoltaics. These include:
- **String Length Calculator**. Method for calculating the maximum allowable string length for a photovoltaic system. 

# Files

- **index.py** - Homepage for pvtools website.
- **string_length_calculator.py** - Page for calculating string length.
- ...


# Todo

- Document! 
- Check AWS bucket region to minimize latency.

# Install Notes

In order to set up this application in Heroku, we followed the [Heroku install instructions](https://dash.plot.ly/deployment) but deleted the following lines from requirements.txt:
```
functools32==3.2.3.post2
futures==3.2.0
```