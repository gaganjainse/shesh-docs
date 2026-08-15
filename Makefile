.PHONY: check build serve generate clean

check:
	python3 tools/check_docs.py
	mdbook build

build:
	mdbook build

serve:
	mdbook serve --open

generate:
	python3 tools/generate_components.py ../shesh-ecosystem/manifests/components.toml

clean:
	rm -rf book
