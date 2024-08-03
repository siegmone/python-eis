TEST_DIR = tests

all:
	echo "Hello World"

test:
	echo "Test"
	pytest $(TEST_DIR)
