PANDOC ?= pandoc

# Pandoc filters.
FILTERS = $(wildcard tools/filters/*.py)

all : index.htm

index.htm : slides.md
	$(PANDOC) -f markdown-grid_tables+pipe_tables+backtick_code_blocks+fenced_code_blocks+fenced_code_attributes+inline_code_attributes -s --template=pandoc-revealjs.template -t revealjs -o $@ --section-divs --filter tools/filters/notes.py --filter tools/filters/divclass.py --no-highlight $<

test.htm : test.md
	$(PANDOC) -f markdown-grid_tables+pipe_tables+backtick_code_blocks+fenced_code_blocks+fenced_code_attributes+inline_code_attributes -s --template=pandoc-revealjs.template -t revealjs -o $@ --section-divs --filter tools/filters/notes.py --filter tools/filters/divclass.py --filter tools/filters/code_snippets.py --no-highlight $<

clean :
	rm -fv links.md index.htm?

distclean : clean
	rm -rf node_modules

present :
    #use a local webserver to show the slides
	npm start

prepare :
    #installs all nodejs dependencies in this directory
	npm install
