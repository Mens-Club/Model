from connect_to_db import get_db_connection
from process import process_recommendations

def main():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            process_recommendations(cursor)
        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    main()