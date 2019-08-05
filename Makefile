#/usr/bin/sh
# Build chuncker  package

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

install:
	sudo python setup.py install
install3:
	sudo python3 setup.py install
# Publish to github
publish:
	git push origin master 

md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst
md2html:
	pandoc -s -r markdown -w html README.md -o README.html
	
wheel:
	sudo python setup.py bdist_wheel
wheel3:
	sudo python3 setup.py bdist_wheel
sdist:
	sudo python setup.py sdist
upload:
	echo "use twine upload dist/PyArabic-0.6.1.tar.gz"
	
test:
	pytest pyarabic/test_araby.py
doc:
	epydoc --config epydoc.conf

temped:
	cd tests; python test_chunk.py -c temp --debug -f samples/dataset.csv > output/temp.txt
	tail -n 3 tests/output/temp.txt
named:
	cd tests; python test_chunk.py -c name --debug -f samples/nameddataset.csv > output/name.txt
	tail -n 3 tests/output/name.txt
number:
	cd tests; python test_chunk.py -c number --debug  -f samples/numberdataset.csv > output/number.txt
	tail -n 3 tests/output/number.txt
