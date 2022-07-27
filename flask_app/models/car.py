from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

db='car_dealz'

class Car:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller_first_name = data['first_name']
        self.seller_last_name = data['last_name']

    @classmethod
    def save(cls,data):
        query = 'insert into cars (price, model, make, year, description, seller_id) values (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(seller_id)s)'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = 'delete from cars where id = %(id)s'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_cars(cls):
        query = 'select * from cars left join users on cars.seller_id = users.id'
        cars = connectToMySQL(db).query_db(query)
        all_cars = []
        for one_car in cars:
            all_cars.append(cls(one_car))
        return all_cars

    @classmethod
    def get_car_by_id(cls,data):
        query = "select * from cars left join users on cars.seller_id = users.id where cars.id = %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data, id):
        query = f'update cars set price= %(price)s, description= %(description)s, model= %(model)s, make = %(make)s , year = %(year)s where id ={id}'
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def purchase_car(cls,data,id):
        query = f'update cars set buyer_id = %(buyer_id)s where id = {id}'
        result = connectToMySQL(db).query_db(query,data)
        return result

    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data['price']) < 1:
            is_valid = False
            flash('The price of the car cannot be blank!', 'car')
        elif int(data['price']) < 1:
            is_valid = False
            flash('The price has to be greater than 0!', 'car')
        if len(data['year']) < 1:
            is_valid = False
            flash('The year of the car cannot be blank!', 'car')
        elif int(data['year']) < 1:
            is_valid = False
            flash('The year has to be greater than 0!', 'car')
        if len(data['model'])<1:
            is_valid = False
            flash('The model of the car cannot be blank!', 'car')
        if len(data['make'])<1:
            is_valid = False
            flash('The make of the car cannot be blank!', 'car')
        if len(data['description'])<1:
            is_valid = False
            flash('The description of the car cannot be blank!', 'car')
        return is_valid
