# pvtools
PVtools provides open source software related to photovoltaics.
This page is the github repo for the pvtools Heroku app built in plotly dash.

# Applications

The pvtools package contains multiple different applications for photovoltaics. These include:
- **String Voltage Calculator**. Method for calculating the maximum string voltage for a photovoltaic system. 

# Todo

- Add 
- Check AWS bucket region to minimize latency.

# Install Notes

In order to set up this application in Heroku, we started 
with the [Heroku install instructions](https://dash.plot.ly/deployment) and then deleted the following lines from requirements.txt:
```
functools32==3.2.3.post2
futures==3.2.0
```