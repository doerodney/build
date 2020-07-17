REPOSITORY := $(shell cat metadata.json | jq '.repository' | sed -e 's/"//g')
TAG := $(shell cat metadata.json | jq '.tag' | sed -e 's/"//g')
MANIFEST := $(subst /,-,$(REPOSITORY))-manifest.txt

BUILD_IMAGE := $(shell docker build --tag $(TAG) .)
BUILD_MANIFEST := $(shell docker image inspect $(REPOSITORY) > $(MANIFEST))

define build-manifest
echo "Creating $@ for repository $(REPOSITORY)..."
$(BUILD_IMAGE)
$(BUILD_MANIFEST)
endef

$(MANIFEST): Dockerfile metadata.json	
	$(build-manifest)

