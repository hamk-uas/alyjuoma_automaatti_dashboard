CREATE TABLE sensor_data {
    id SERIAL PRIMARY KEY,
    dtime TIMESTAMP NOT NULL,
    farm_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    parameter_type TEXT NOT NULL,
    parameter_value DOUBLE PRECISION NOT NULL
};