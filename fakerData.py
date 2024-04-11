import psycopg2
from faker import Faker

conn_string = "postgres://postgresql_aedp_user:F3ayf0Hj7WwBZ6jn5dFoS5mq7Nwd8gTT@dpg-coc35l8l6cac73ep3jr0-a.singapore-postgres.render.com/postgresql_aedp"

def create_table_and_insert_data():
    connection = None
    try:
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        # Generate test data using Faker
        fake = Faker()
        for _ in range(200):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
            is_active = fake.boolean()
            registration_date = fake.date_this_decade()
            phone_number = fake.phone_number()[:20]
            address = fake.address().replace("\n", ", ")  # Address may contain line breaks

            cursor.execute(
                "INSERT INTO customers (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address)
            )
        connection.commit()
        print(f"Created table 'customers' and inserted 200 test records with Faker data!")
    except Exception as e:
        print(f"Error creating table or inserting data: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_table_and_insert_data()