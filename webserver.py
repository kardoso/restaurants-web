# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# importar operações CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# importar classes do arquivo "database_setup"
from database_setup import Restaurant, Base, MenuItem

from flask import (Flask, render_template,
                   request, redirect, url_for, flash, jsonify)
app = Flask(__name__)

# selecionar banco de dados
engine = create_engine('sqlite:///restaurantmenu.db')
# estabelecer conexão
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def mainRestaurants():
    restaurants = session.query(Restaurant).all()
    session.close()
    return render_template("main_restaurants.html", restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        if request.form['name']:
            newEntry = Restaurant(name=request.form['name'])
            session.add(newEntry)
            session.commit()
            session.close()
        return redirect(url_for('mainRestaurants'))
    else:
        session.close()
        return render_template('new_restaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurantToEdit = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['newName']:
            restaurantToEdit.name = request.form['newName']
            session.add(restaurantToEdit)
            session.commit()
            session.close()
        return redirect(url_for('mainRestaurants'))
    else:
        session.close()
        return render_template('edit_restaurant.html',
                               restaurant_id=restaurant_id,
                               restaurant=restaurantToEdit)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):

    restaurantToDelete = session.query(
        Restaurant).filter_by(
        id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        session.close()
        return redirect(url_for('mainRestaurants'))
    else:
        session.close()
        return render_template('delete_restaurant.html',
                               restaurant_id=restaurant_id,
                               restaurant=restaurantToDelete)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=port)
