# Legend:
# $@ The target directory.  More typically, a file that is a build target.

# Identify the directories that contain a Dockerfile.
source-dirs := $(sort $(dir $(shell find . -name Dockerfile)))

.PHONY: all $(source-dirs)
all: $(source-dirs)

$(source-dirs):
	$(MAKE) --directory=$@
