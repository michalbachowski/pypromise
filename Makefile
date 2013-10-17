subdir="test"

test:
	make -C $(subdir) test

coverage:
	make -C $(subdir) coverage

.PHONY: test coverage
