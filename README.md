# New American Publc Art: Color Commons

## Summary
Color commons is an interactive public art exhibit on the Boston Greenway created by [New American Public Art](http://www.newamericanpublicart.com/).  It consists of several color towers that change color based on user text messages. There are ~950 possible colors based on the [xkcd](www.xkcd.com) color survey.  This project contains functions to analyze the text message data including some visualizations requested by my friends at NAPA.

I performed some quick summaries in the [Basic Analysis Notebook](./docs/Basic+Descriptive+Stats.html), which is automatically rendered by github.  In addition to creating some basic visualizations, that notebook will produce two json files (date_sunburst.json and user_sunburst.json) that are part of the sunburst visualizations found in the js (javascript) folder. Unfortunately, I don't currently know how to easily render those interactive plots in github, but I'll figure that out soon hopefully.

In order to render those html files, you must clone the repositories.  Once they are cloned locally, you should be able to just open them up in firefox or chrome. There is also a brush/zoom plot that shows the frequency of text messages. The interactive components were completely copied from exising d3 blocks. I did almost nothing to the javascript.  The reference information should be in the js/html files.  If not, I will add them soon.

The napa/ folder contains a python class for generating summary statistics and plots. One day these will be adapted to run in realtime on a NAPA run server to enable live updates to web content. The sunburst json data can and will be handled by this class, but currently that is not supported.

Note to self: I will also include a requirements file.  In short, this analysis requires pandas, seaborn, and (maybe) numpy.

## Contents 

- [Basic Analysis Notebook](./docs/Basic+Descriptive+Stats.html)
- js/brush_zoom.html
- js/date_sunburst.html
- js/ser_sunburst.html
