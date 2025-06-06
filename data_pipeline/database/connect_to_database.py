import pymysql
from dotenv import load_dotenv
import os 
import pandas as pd 

load_dotenv()


def fetch_data_as_pandas(query: str) -> pd.DataFrame:
    """_summary_

    Args:
        query (str): SQL Query

    Returns:
        pd.DataFrame: df resturns 
    """
    conn = pymysql.connect(
    
    host=os.getenv("MYSQL_HOST"),       
    user=os.getenv("MYSQL_USER_NAME"),
    password=os.getenv("MYSQL_USER_PASSWORD"),
    db=os.getenv("MYSQL_DATABASE"),
    port=int(os.getenv("MYSQL_PORT")),
    
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    
    )
    
    # 쿼리 실행

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    df = pd.DataFrame(result)
    
    return df
    