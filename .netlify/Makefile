.PHONY: build website docs clean

build: website docs

website: $(patsubst website/%,build/%,$(shell find website/ -type f))

docs:
	cd .. && invoke docs
	@rm -rf build/docs
	cp -r ../build/docs build/docs

build/%: website/%
	@mkdir -p $(dir $@)
	cp $< $@

clean:
	rm -rf build
