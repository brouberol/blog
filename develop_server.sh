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
start_up
