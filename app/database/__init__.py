from peewee import PostgresqlDatabase

DB = PostgresqlDatabase(
    database='main',
    user='docker',
    password='docker',
    host='db',
    port=5432
)