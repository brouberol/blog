.PHONY := serve html

serve:
	@poetry run pelican --listen --autoreload -o output -s pelicanconf.py --debug

html:
	@poetry run python -m pelican -o output -s pelicanconf.py
