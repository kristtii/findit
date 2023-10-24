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
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT carposts.id as id, carposts.car_make as car_make, carposts.car_model as car_model, carposts.car_engine as car_engine, carposts.car_fuel as car_fuel, carposts.car_transmissions as car_transmissions, carposts.car_drive as car_drive, carposts.car_description as car_description, carposts.car_mileage as car_mileage, carposts.car_price as car_price, carposts.car_images as images, carposts.user_id as user_id, COUNT(parkedcars.id) as parkedcars FROM carposts LEFT JOIN parkedcars ON carposts.id = parkedcars.carPost_id GROUP BY carposts.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
            return cars
        return cars
    
    @classmethod
    def search(cls, search_query):

        query = f"""
            SELECT carposts.id as id, carposts.car_make as car_make, carposts.car_model as car_model, 
                carposts.car_engine as car_engine, carposts.car_fuel as car_fuel, 
                carposts.car_transmissions as car_transmissions, carposts.car_drive as car_drive, 
                carposts.car_description as car_description, carposts.car_mileage as car_mileage, 
                carposts.car_price as car_price, carposts.car_images as images, carposts.user_id as user_id
            FROM carposts
            LEFT JOIN parkedcars ON carposts.id = parkedcars.carPost_id
            WHERE carposts.car_make LIKE '{search_query}%'
            GROUP BY carposts.id;
        """

        try:
            results = connectToMySQL(cls.db_name).query_db(query)

            cars = []
            if results:
                for car in results:
                    cars.append(car)
            return cars

        except Exception as e:
            print("An error occurred:", str(e))
            return []


    @classmethod
    def createCarPost(cls, data):
        query = "INSERT INTO carposts (car_make, car_model, car_engine, car_fuel, car_transmissions, car_drive, car_mileage, car_price, car_images, car_description, user_id) VALUES (%(car_make)s, %(car_model)s, %(car_engine)s, %(car_fuel)s, %(car_transmissions)s, %(car_drive)s, %(car_mileage)s, %(car_price)s, %(car_images)s, %(car_description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_car_by_id(cls, data):
        query = 'SELECT * FROM carposts WHERE id= %(car_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def update_car(cls, data):
        query = "UPDATE carposts SET car_make = %(car_make)s, car_model = %(car_model)s, car_engine = %(car_engine)s, car_fuel = %(car_fuel)s, car_transmissions = %(car_transmissions)s, car_drive = %(car_drive)s, car_mileage = %(car_mileage)s, car_price = %(car_price)s, car_description = %(car_description)s WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_car_parkedcars(cls, data):
        query = "DELETE from parkedcars WHERE carPost_id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM carposts WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def getUserWhoParkedCars(cls, data):
        query = "SELECT parkedcars.carPost_id as id from parkedcars WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        parkedCars = []
        if results:
            for car in results:
                parkedCars.append(car['id'])
            return parkedCars
        return parkedCars
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO parkedcars (user_id, carPost_id) VALUES ( %(user_id)s, %(car_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def unsave(cls, data):
        query = "DELETE FROM parkedcars WHERE user_id = %(user_id)s AND carPost_id = %(car_id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getParkedCarsByUser(cls, data):
        query = "SELECT * FROM parkedcars WHERE user_id = %(user_id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllParkedCarsByUser(cls, data):
        query = "SELECT parkedcars.id as id, carposts.car_make as car_make, carposts.car_model as car_model, carposts.car_engine as car_engine, carposts.car_fuel as car_fuel, carposts.car_transmissions as car_transmissions, carposts.car_drive as car_drive, carposts.car_description as car_description, carposts.car_mileage as car_mileage, carposts.car_price as car_price, carposts.car_images as images, carposts.user_id as user_id FROM parkedcars LEFT JOIN carposts ON parkedcars.carPost_id = carposts.id WHERE parkedcars.user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validateImage(data):
        is_valid = True
        if len(data) < 1:
            flash('Please select at least one image', 'car_images')
            is_valid = False 
        return is_valid
              
    @staticmethod
    def validate_car(data):
        is_valid = True

        if not data['car_make']:
            flash('Car make is required', 'car_make')
            is_valid = False

        if not data['car_model']:
            flash('Car model is required', 'car_model')
            is_valid = False

        if not data['car_engine']:
            flash('Car engine is required', 'car_engine')
            is_valid = False

        if not data['car_fuel']:
            flash('Car fuel is required', 'car_fuel')
            is_valid = False

        if not data['car_transmissions']:
            flash('Car transmissions is required', 'car_transmissions')
            is_valid = False

        if not data['car_drive']:
            flash('Car drive is required', 'car_drive')
            is_valid = False

        if not data['car_mileage']:
            flash('Car mileage is required', 'car_mileage')
            is_valid = False

        if not data['car_price']:
            flash('Car price is required', 'car_price')
            is_valid = False

        if len(data['car_description']) < 3:
            flash('Description must be more than 3 characters', 'car_description')
            is_valid = False

        return is_valid
        