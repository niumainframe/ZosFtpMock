VERSION=$(shell python setup.py --version)
DIST=dist/ZosFtpMock-$(VERSION).tar.gz

all: $(DIST)

$(DIST):
	python setup.py sdist

test:
	bash test.sh

clean:
	rm -rf dist *.egg-info
	find -name *.pyc -exec rm {} \;
