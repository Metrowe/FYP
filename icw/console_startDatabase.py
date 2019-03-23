import database_connection
import database_classes as table

def main():
	engine = database_connection.engine
	print('Before create all: ' + str(engine.table_names()))
	table.Base.metadata.create_all(engine)
	print('After create all: ' + str(engine.table_names()))

main()