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
        self.car_images = data['car_images']
        self.car_description = data['car_description']  

    @classmethod
    def get_all(cls):
        query = "SELECT carposts.id as id, carposts.car_make as car_make, carposts.car_model as car_model, carposts.car_engine as car_engine, carposts.car_fuel as car_fuel, carposts.car_transmissions as car_transmissions, carposts.car_drive as car_drive, carposts.car_mileage as car_mileage, carposts.car_price as car_price, carposts.car_images as images, COUNT(parkedcars.id) as parkedcars FROM carposts LEFT JOIN parkedcars ON carposts.id = parkedcars.carPost_id GROUP BY carposts.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
            return cars
        return cars
    
    @classmethod
    def createCarPost(cls, data):
        query = "INSERT INTO carposts (car_make, car_model, car_engine, car_fuel, car_transmissions, car_drive, car_mileage, car_price, car_images, car_description) VALUES (%(car_make)s, %(car_model)s, %(car_engine)s, %(car_fuel)s, %(car_transmissions)s, %(car_drive)s, %(car_mileage)s, %(car_price)s, %(car_images)s, %(car_description)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)