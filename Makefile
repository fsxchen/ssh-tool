ALL:
	cp src/*.py bin

clean:
	rm -fr bin/*
	rm -fr dist build
	rm -fr *.egg-info