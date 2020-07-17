# Legend:
# $@ The filename representing the target

# Identify the directories that contain a Dockerfile.
# source-dirs = alpha beta
source-dirs := $(sort $(dir $(shell find . -name Dockerfile)))

.PHONY: all $(source-dirs)
all: $(source-dirs)

$(source-dirs):
	$(MAKE) --directory=$@
