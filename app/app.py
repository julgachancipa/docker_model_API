import pandas as pd
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from modeler.Modeler import Modeler

app = Flask(__name__)

# ENV = os.environ['ENVIROMENT']
# ENV = 'dev'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:password@postgresdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False)
    to_user_distance = db.Column(db.Float, nullable=False)
    to_user_elevation = db.Column(db.Float, nullable=False)
    total_earning = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String, nullable=False)
    taken = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def order_to_db(order_data, prediction):
    order = (
        db.session.query(Order)
        .filter_by(order_id=order_data['order_id'])
        .first()
    )

    if order is None:
        order = Order(order_id=order_data['order_id'])

    order.store_id = order_data['store_id']
    order.to_user_distance = order_data['to_user_distance']
    order.to_user_elevation = order_data['to_user_elevation']
    order.total_earning = order_data['total_earning']
    order.created_at = order_data['created_at']
    order.taken = prediction

    db.session.add(order)
    db.session.commit()


@app.route('/test')
def test():
    return jsonify({200: 'Hi there :)'})


@app.route('/')
def index():
    orders = []
    orders_obj = db.session.query(Order).all()
    for order in orders_obj:
        orders.append(order.as_dict())
    return jsonify(orders)


@app.route('/predict', methods=['POST'])
def predict():
    predictions = {}
    orders = request.get_json()
    modeler = Modeler()

    for order in orders:
        order_id = order['order_id']
        store_id = order['store_id']
        to_user_distance = order['to_user_distance']
        to_user_elevation = order['to_user_elevation']
        total_earning = order['total_earning']
        created_at = order['created_at']

        date = pd.to_datetime(created_at)
        day_of_year = date.dayofyear
        day_of_week = date.dayofweek
        minutes = date.hour * 60 + date.minute

        order_info = [store_id, to_user_distance, to_user_elevation,
                      total_earning, day_of_year, day_of_week, minutes]
        prediction = modeler.predict(order_info)

        predictions[order_id] = {
            'input': {
                'order_id': order_id,
                'store_id': store_id,
                'to_user_distance': to_user_distance,
                'to_user_elevation': to_user_elevation,
                'total_earning': total_earning,
                'created_at': created_at
            },
            'taken': prediction
        }
        order_to_db(order, prediction)

    return jsonify(predictions)


if __name__ == '__main__':
    # db.create_all()
    # if ENV == 'dev':
    #    app.run(debug=True, host='0.0.0.0')
    # else:
    app.run()
