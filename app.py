from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS, cross_origin
from psycopg2 import extras

app = Flask(__name__)
CORS(app)
conn_string = "postgres://postgresql_aedp_user:F3ayf0Hj7WwBZ6jn5dFoS5mq7Nwd8gTT@dpg-coc35l8l6cac73ep3jr0-a.singapore-postgres.render.com/postgresql_aedp"

def connect_to_db():
  """Connects to the PostgreSQL database using RealDictCursor."""
  connection = None
  try:
    connection = psycopg2.connect(conn_string, cursor_factory=extras.RealDictCursor)
    return connection
  except Exception as e:
    print(f"Error connecting to database: {e}")
    return None

def get_all_customers():
  """Retrieves all customer data from the database."""
  connection = connect_to_db()
  if not connection:
    return None
  cursor = connection.cursor()
  try:
    cursor.execute("SELECT * FROM customers WHERE is_active = TRUE;")
    customers = cursor.fetchall()
    connection.commit()
    return customers
  except Exception as e:
    print(f"Error retrieving customers: {e}")
    return None
  finally:
    if connection:
      connection.close()

def get_customer_by_id(customer_id):
  """Retrieves a specific customer based on ID."""
  connection = connect_to_db()
  if not connection:
    return None
  cursor = connection.cursor()
  try:
    cursor.execute("SELECT * FROM customers WHERE id = %s AND is_active = TRUE;", (customer_id,))
    customer = cursor.fetchone()
    connection.commit()
    return customer
  except Exception as e:
    print(f"Error retrieving customer: {e}")
    return None
  finally:
    if connection:
      connection.close()

def soft_delete_customer(customer_id):
  """Soft deletes a customer by setting the active flag to False."""
  connection = connect_to_db()
  if not connection:
    return None
  cursor = connection.cursor()
  try:
    cursor.execute("UPDATE customers SET is_active = FALSE WHERE id = %s;", (customer_id,))
    connection.commit()
    return True
  except Exception as e:
    print(f"Error soft deleting customer: {e}")
    return None
  finally:
    if connection:
      connection.close()

@app.route("/customers", methods=["GET"])
def get_customers():
  """API endpoint to retrieve all active customers."""
  customers = get_all_customers()
  if not customers:
    return jsonify({"error": "Error retrieving customers"}), 500
  return jsonify(customers), 200

@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
  """API endpoint to retrieve a specific active customer by ID."""
  customer = get_customer_by_id(customer_id)
  if not customer:
    return jsonify({"error": "Customer not found"}), 404
  return jsonify(customer), 200

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
  """API endpoint to soft delete a customer by ID."""
  success = soft_delete_customer(customer_id)
  if not success:
    return jsonify({"error": "Error deleting customer"}), 500
  return jsonify({"message": "Customer soft deleted successfully"}), 200

if __name__ == "__main__":
  app.run(debug=True)
