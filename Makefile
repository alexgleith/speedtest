create_db:
	python3 -c "from main import db; db.create_all()"

run:
	python3 main.py

virtualenv:
	./speedtest/bin/activate

run-prod:
	gunicorn -b 0.0.0.0:8000 --daemon
