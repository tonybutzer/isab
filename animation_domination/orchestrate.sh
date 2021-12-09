#! /bin/bash

dock='docker run -i'
img='tbutzer/anim-stac-odc'
vol='-v /home/ec2-user/data/:/home/data/'
cmd='python anim_api.py'


g='canberra.geojson'

for g in canberra.geojson siouxfalls2.geojson hobart.geojson; do {
    $dock --rm --name $g $vol $img $cmd $g &
}; done
