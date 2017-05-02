# New American Publc Art: Color Commons

## Background
Color commons is an interactive public art exhibit.  It consists of several color towers that change color based on user text messages.

## Notes from Bevan

The pertinent data we receive (from our Twilio server) is:

    From : [ the phone number of the person sending the color ]
    Body : [ the color sent ] 
    SentDate : [ sent date ] 

Some of the trends we'd like to interpret are:

    Total amount of texts
    Top 5 Colors
    How many times “secret” was texted
    Peak use times of day / week 
    Unique users 
    Repeat users 
    Highly engaged users (over 15 texts)
    Clustering - are there clusters of numbers that occur within temporal proximity

## Other things to do for this project

Determine the relationship between time, weather, ?, and usage.

Plotting
    - tools
        - javascript: D3.js, chart.js, Google Charts
        - python using seaborn, matplotlib, bokeh?
    - content
        - display time variance of usage (date, day of week, time)
        - a plot of the most influential factors
        - network diagrams with the user clusters
