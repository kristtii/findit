from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    db_name = '3dcarproject'
    def __init__( self , data ):
        self.id = data['id']
        self.car_make = data['car_make']
        self.car_model = data['car_model']
        self.car_engine = data['car_engine']
        self.car_fuel = data['car_fuel']
        self.car_transmissions = data['car_transmissions']
        self.car_drive = data['car_drive']
        self.car_mileage = data['car_mileage']
        self.car_price = data['car_price']
        self.images = data['images']

    @classmethod
    def get_all(cls):
        query = "SELECT carposts.id as id, carposts.car_make as car_make, carposts.car_model as car_model, carposts.car_engine as car_engine, carposts.car_fuel as car_fuel, carposts.car_transmissions as car_transmissions, carposts.car_drive as car_drive, carposts.car_mileage as car_mileage, carposts.car_price as car_price, carposts.images as images, COUNT(parkedcars.id) as parkedcars FROM carposts LEFT JOIN parkedcars ON carposts.id = parkedcars.carPost_id GROUP BY carposts.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
            return cars
        return cars