lint:
	pylint -r y paperio

run:
	WIDTH=20 python localrunner.py -p1 "python bot.py" -p2 "python bot.py"