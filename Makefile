.DEFAULT_GOALi := serve
.PHONY := serve

serve:
	@poetry run pelican --listen --autoreload -o output -s pelicanconf.py --debug

html:
	poetry run pelican content -o output -s pelicanconf.py
