create_db:
	python3 -c "from main import db; db.create_all()"

run:
	python3 main.py

virtualenv:
	./speedtest/bin/activate
