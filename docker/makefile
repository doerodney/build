MANIFEST := inspect.txt
TAG := $(shell cat metadata.json | jq '.tag' | sed -e 's/"//g')
BUILD_IMAGE := $(shell docker build --tag $(TAG) .)
BUILD_MANIFEST := $(shell docker image inspect $(TAG) > $(MANIFEST))

define build-manifest
echo "Creating $@ for tag $(TAG)..."
$(BUILD_IMAGE)
$(BUILD_MANIFEST)
endef

$(MANIFEST): Dockerfile metadata.json	
	$(build-manifest)

