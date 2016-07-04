ALL:
	cp ssh-tool/* bin

clean:
	rm -fr bin/*
	rm -fr dist build
	rm -fr *.egg-info