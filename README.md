# Älyjuoma-automaatti Dashboard

## Description

Web app that will act as the dashboard for the Älyjuoma-automaatti project. Meant to provide an intuitive interface from which data can be viewed and superficially analyzed. Data can also be downloaded from the database for more specific or detailed analysis.

## API

The backend API is broken down into two modules:

- **'data'** module (via ```'/data/...'```):
  - ```'/data/write'``` - ***POST***
    - Endpoint for writing to database
    - Data **must** follow the ```b'farm_id;station_id;realtime;parameter_type;parameter_value'``` format
  - ```'/data/all'``` - ***GET***
    - Returns all data from database as JSON response
  - ```'/data/slice'``` - ***POST***
    - Returns a slice of data from database based on format defined in JSON request as a JSON response
    - Requests **must** follow the format:

        ```json
        {
            "dtime": ["dtime_start", "dtime_end"],
            "farm_id": ["selected", "farms"],
            "station_id": ["selected", "stations"],
            "parameter_type": ["selected", "parameters"],
            "parameter_value": [0.0, 0.0]
        }
        ```

    - Any combination of columns is permissible (no slicing with ```reatime``` as of ```v0.2.0-alpha```)
    - Any column can be omitted (including multiple)

- **'download'** module (via ```/download/...```):
  - ```/download/all``` - ***GET***
    - Returns all data from database as **.csv** file
  - ```/download/slice``` - ***POST***
    - Returns a slice of data from database based on format defined in JSON request as a **.csv** file.
    - Requests **must** follow the same format as ```/data/slice```
