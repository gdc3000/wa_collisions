# Seattle Collisions Project

## Goals of the Project:

1. Clean and prepare Seattle area collision data for regression and other machine learning projects.
2. Integrate with crime data. This will be used to determine the crime rate in each neighborhood that a collision occurs.
3. Create a visualization of Seattle area collision data.
4. Advanced analysis of Seattle area collision data.

## Use Cases:

- For each use case, we plan to create on jypter notebook demo.
- The demo will call the components which will by python method(s) that are within our vehicle_collisions/

### Where do more accidents occur in Seattle?

* The user of this package will have an understanding of where the most accidents in Seattle are occuring by neighbourhood and in a visual form.
* We will visualize the locations of accidents in neighbourhoods on a map.
* We will make this analysis repeatable so that it could be re-used with similar datasets from different cities.
* Contact: Salik Warsi 
* The first iteration will not include: We will perform analysis on the characteristics of different locations (such as population density, road quality, traffic volumes - depending on
  data availability) to understanding the relationships between these variables and collisions.

### How does weather/climate effect driving?

* The user of this package will have the ability to dynamically analyze the correlation between collision density within a neighborhood in Seattle and temperature and weather type
* We will divide the Seattle city area into sub areas by density of collisions and proximities to the 10 weather stations. For each area, determine the effect of temperature, weather type on the density of collisions based on historical data.
* The user will be provided with an UI to select one of the sub areas
* The package returns a time series visualization of the temperatures of that neighborhood, together with the collision density
* The package will also fit a regression model on number of collisions with estimated road surface temperature, air temperature, precipitation and weather type for the selected neighborhood. It then renders the result of correlation coefficients and confidence intervels for each predictor variable to the user
* User should also be able to apply the same analysis to the entire Seattle city
* Contact: Fei Wang

### Do different types of accidents happen in different neighborhoods with different levels of crime (911 call)?

* Because of issues with the data integration, we are not working on this part at this time. The collision data needs to be mapped to the beats and then to the collision data.
* The user of this package will have the ability to correlate the types of accidents and the levels of crime in each neighboorhood.
* We will measure the type of accident based on the encoding from the Seattle collision dataset. The level of crime will be based on the frequency of 911 calls in each neighboorhood.
* There will be a way to visually and quantitatively coorrelate the two types of data. The user can then better determine where to live and drive in Seattle.
* Contact: Libby Montague

### Have the number of accidents changed over time? Can we see the change in Seattle speed limits in the Seattle collision data?

* The user of this will gain an understanding of how collisions have changed over time and by neighbourhood.
* We will perform time series analysis to understand if population growth or changes in speed limits have impacted the number of collisions in Seattle.
* Contact: Geoff Coyner

### If the user has similar data for another city, they can use the methods we create on their own data.

* Our methods will be reproducible. The user will need to have the data in a specific format, but they can use our methods for analysis or visualization.
* We will not do extensive testing, but the user will be able to pull in data from another city.
* We will document the specific data format so that the user is able to confirm that thier data are in the correct format.

## Components:

- The components are in the order that we will work through them.

### Create Dataframe

    - Name: ReadData
    - What it does?
        - Read the data in from the source
    - Input: dataset
    - Output: datafame
    - How it connects to the use cases?
        - Once the dataset is read in, then it can be cleaned using the Clean Data component

### Clean Data

    - Name: CleanData
    - What it does?
        - Cleans the data that is read from the source
        - Deals with any missing values, converts to NA
        - Converts data types to the data types necessary for analysis (text strings to dates, text to numeric, etc.)
        - Ensures that categorical data are in the correct categories (for instance fixes spelling mistakes)
    - Input: data frames
    - Output: cleaned data ready for integration
    - How it connects to other use cases?
        - The output of the CleanData will be used in the Integrate Data Source component

### Integrate Data Source

    - Name: FullDataset
    - What it does?
        - Integrate cleaned dataset into one dataset   
    - Input: cleaned data sorts
    - Ouput: cleaned integrated data ready for visualization and analysis
    - How it connects to the use cases?
        - The output of the Create Datafame and Clean Data components will be used as an input to create the FullDataset
        - This dataset will be used in all other components that depend on data

### Assign Neighborhoods

    - Name: GetNeighbourhoods
    - What it does?
        - given a dataframe containing latitudes and longitudes, assigns seattle neighbourhoods to them
    - Input:
        - Data frame containing latitudes and longitudes
    - Ouput:
        - Data frame with a columns attached about which neighborhood they are in.
    - How:
        - Read Seattle neighbour hood shapefile
        - Create shape using shapify (Python library)
        - using this shape file fine neighbour hood of each point and attach to dataframe.
    - How:
        - This allows us to later group data by neighbourhoods for visualization.

### Visualize Data Geographically in Neighborhoods

    - Name: PlotNeighbourhoods
    - What it does?
        - given a dataframe with data per neighbourhood, 1 row per neighbourhood, plot that that data in a neighbour hood map.
    - Input:
        - dataframe with data per neighbourhood, 1 row per neighbourhood. 1 column should state the value
    - Ouput:
        A map plot of the neighbourhood data
    - How it connects to the use cases  
        - This can be used as a module to draw different types of visualizations.

### Visualize Data Geographically individually

    - Name: PlotPoints
    - What it does?
        - given a dataframe with data per observation (columns for lattitude, longitude and value) plot that that data in a seattle map.
    - Input:
        - dataframe with columns: lattitude, longitude and value
    - Ouput:
        A map plot of the individual points in a seattle map (possibly as a heat map)
    - How it connects to the use cases  
        - This can be used as a module to draw different types of visualizations.

### Component to render the result of statistical analysis results
    - Name: RenderStats
    - What it does?
        - Given the resulting object of a statistical analysis, it renders the object to the user in a concise and visually pleasing way that is also consisitent to the rest of the package's visualizations.
    - Input:
        - A python object that contains result of a statistical analysis (regression for example)
    - Output:
        - A visualization of the result and a summary paragraph
    - How it connects to the user cases
        - This can be used in all the use cases where user perform ML/statistical analysis as a standard output framework

### Component to support juypter notebook analyzing crash locations
    - Name: AnalyzeCrashLocations
    - What it does?
        - Read the data in from the source
    - Suprports a Jupyter notebook which does the following:
        - Identifies hot spots for accidents
        - Performs regression analysis accidents do determine if certain
            features are related to accidents
        - Summarizes findings of analysis
    - Input: CleanData, RederStats, PlotPlot, PlotNeighbourhoods output.
    - Output: modules which can be render with only a few lines of code in a Jupyter notebook
    - How it connects to the use cases?
        - Utilizes cleaned data to perform useful analysis.

## Project Plan 

### 5/15/2018 

* Individually start researching the Use Cases (questions)
* Follium visualizations for the locations question (Salik)
* Framework for the Clean Data and the Integrate Data Source (Libby)

### 5/26/2018 
* Concentrate on the speed limit analysis (Geoff) and the visualizations (Fei and Salik)
* Create an example jupyter notebook to create the final dataset (Libby)
* Finish up the documentation (All)