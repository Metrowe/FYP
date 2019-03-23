import database_connection
import database_classes as table

def main():
	engine = database_connection.engine
	print('Before drop all: ' + str(engine.table_names()))
	table.Base.metadata.drop_all(engine)
	print('After drop all: ' + str(engine.table_names()))
	table.Base.metadata.create_all(engine)
	print('After create all: ' + str(engine.table_names()))

main()