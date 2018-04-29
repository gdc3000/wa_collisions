# Seattle Collisions Project 

## Goals of the Project:

1. Clean and prepare Seattle area collision data for regression and other machine learning projects. 
2. Integrate with crime data. This will be used to determine the crime rate in each neighborhood that a collision occurs. 
3. Create a visualization of Seattle area collision data. 
4. Advanced analysis of Seattle area collision data. 

## Use Cases:

- For each use case, we plan to create on jypter notebook demo. 
- The demo will call the components which will by python method(s) that are within our vehicle_collisions/

### Where do more accidents occur in Seattle? Where should I avoid driving or living?

Add description - to each 

Assign: Geoff   

### How does weather/climate effect driving?

Assign: Fei

### Do different types of accidents happen in different neighborhoods with different levels of crime (911 call)?

    The user of this package will have the ability to correlate the types of accidents and the levels of crime in each neighboorhood. 
    We will measure the type of accident based on the encoding from the Seattle collision dataset. The level of crime will be based on the frequency of 911 calls in each neighboorhood. 
    There will be a way to visually and quantitatively coorrelate the two types of data. The user can then better determine where to live and drive in Seattle. 

### Have the number of accidents changed over time? Can we see the change in Seattle speed limits in the Seattle collision data?

Assign: Geoff 

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

### Add more!!! 