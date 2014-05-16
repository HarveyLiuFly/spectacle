clean:
	find . -name *.pyc -delete

test: clean
	nosetests -s
