#!/usr/bin/env bash
##
# This section should match your Makefile
##
PY=${PY:-python}
PELICAN=${PELICAN:-pelican}
PELICANOPTS=

BASEDIR=$(pwd)
INPUTDIR=$BASEDIR/content
OUTPUTDIR=$BASEDIR/output
CONFFILE=$BASEDIR/pelicanconf.py

###
# Don't change stuff below here unless you are sure
###


function die {
    echo "Shutting down..."
    ps aux | grep '[p]elican' | awk '{ print $2 }' | xargs kill
}

function start_up(){
  local port=8000
  echo "Starting up Pelican and HTTP server"
  shift
  $PELICAN --debug --autoreload -r $INPUTDIR -o $OUTPUTDIR -s $CONFFILE $PELICANOPTS&
  cd $OUTPUTDIR
  $PY -m pelican.server $port
}

###
#  MAIN
###

trap die SIGTERM EXIT
start_up
