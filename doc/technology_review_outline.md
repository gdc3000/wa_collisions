## Technology Review Outline 

- Compare visualization software 
- Found another [review](https://blog.modeanalytics.com/python-data-visualization-libraries/)

### Background

- Need for the package
- What type of map are we using? 
- What's the documentation like? error handling? how easy to learn? git history? 

### Review 

- Pick 2 
- Format:
    - Package functionality
    - Appeal
    - Drawbacks 

## [Dash](https://plot.ly/products/dash/)

- Found a [demo](https://github.com/plotly/dash-uber-rides-demo)
- [Installation instructions](https://dash.plot.ly/installation)

* Package Functionality:
    - Draw interactive graphs in a web app using react JS.
* Pros:
    - Very easy to draw interactive charts, easy to learn
    - Great documentation for supported features
    - Active github with many commits
    - Supports html and css so easy to customize
* Cons:
    - Dash only works with plotly as far as I could tell
    - Only some graph types are supported in Plotly. Other Matplotlib graphs would have to be ported over
    - Only supports some maps and with a mapbox account (not sure if Mapbox accounts are supported in this course)
    - Custom shape files such as Seattle neighbourhoods not supported
* Reommendation:
    - We can use this if we decide to have an interactive display. However it can only be used for charts (and possibly some simple heatmaps).

## [Django Map Widgets](https://github.com/erdem/django-map-widgets)

* Package Functionality:
    - Calls the Google API and shows the Google map on the page, see [example](http://django-map-widgets.readthedocs.io/en/latest/widgets/point_field_map_widgets.html#preview)
* Drawbacks: 
    - Need to learn both leaflet and django 
    - The examples all call the Google Maps API and do not appear to have [layering functionality](http://django-map-widgets.readthedocs.io/en/latest/widgets/google_static_overlay_map_widget.html)
    - In order to deploy, you need to create a webpage with [Django](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
* Recommendation:
    - I do not recommend using this package
    - I did not need to download the package because of the issues discovered in the documentation
    - The benefits of this package do not out way the issues
    - The user needs to set up a full Django framework in order to add a Google map with no layers

## [Python Folium](http://python-visualization.github.io/folium/)

## [Bokeh]

### Conclusion 


