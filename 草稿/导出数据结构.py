import mysql.connector

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '6152434',
    'database': 'tiktok_擦边'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Successfully connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_table_create_statements():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        create_statements = {}
        for (table_name,) in tables:
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_table_statement = cursor.fetchone()
            create_statements[table_name] = create_table_statement[1]
        
        cursor.close()
        connection.close()
        
        return create_statements
    return {}

def save_create_statements_to_file(statements, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for table_name, create_statement in statements.items():
            file.write(f"-- Table: {table_name}\n")
            file.write(create_statement)
            file.write(";\n\n")

if __name__ == "__main__":
    create_statements = get_table_create_statements()
    if create_statements:
        save_create_statements_to_file(create_statements, 'db_structure.sql')
        print("Database structure has been successfully exported to 'db_structure.sql'.")
    else:
        print("Failed to retrieve database structure.")
