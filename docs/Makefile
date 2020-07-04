define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
    from urllib import pathname2url
except:
    from urllib.request import pathname2url
path = "file:" + pathname2url(os.path.abspath(sys.argv[1]))
print(path)
webbrowser.open(path)
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


build: ## builds the documentation
	mkdocs build

serve: ## run html server watching file changes in realtime
	$(BROWSER) site/index.html
	mkdocs serve
