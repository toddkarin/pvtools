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

- Add pvtools@gmail.com contact.
- Document! 
- make input fields more obvious.
- Check AWS bucket region to minimize latency.
- Load default .npz file into github in order to speed up the default calculation slightly.
- Remove mapbox access token from code.
- Add click callback for map. "If I click the NREL location just outside of Golden, CO, I get the Lat and long from the blue dot. It did not autofill that onto the entry boxes. Was it supposed to?"
- Add pvlib icon.

# Install Notes

In order to set up this application in Heroku, we followed the [Heroku install instructions](https://dash.plot.ly/deployment) but deleted the following lines from requirements.txt:
```
functools32==3.2.3.post2
futures==3.2.0
```