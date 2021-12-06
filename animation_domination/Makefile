publish:
	(cd ..; ./gitpush.sh)

Base=tbutzer/base-miniconda-pangeo
Image=tbutzer/anim-stac-odc

build-base:
	docker build -f Dockerfile.base -t ${Base} .


build:
	docker build -f Dockerfile -t ${Image} .


run:
	docker run -it ${Image} bash
