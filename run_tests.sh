#!/bin/bash

PROJECT_DIR=$(dirname "$(realpath "$0")")
cd "$PROJECT_DIR" || exit 1

test_files=()

while IFS= read -r file; do
    relative_path="${file#./}"
    test_files+=("$relative_path")
done < <(find . -type f -name 'test_*.py')

if [ ${#test_files[@]} -eq 0 ]; then
    echo "No test files found!"
    exit 1
fi

echo "Running all found tests..."

python3 -m unittest -v "${test_files[@]}"
test_exit_code=$?

echo -e "\nAll tests execution finished."

if [ $test_exit_code -ne 0 ]; then
    echo -e "\nSome tests failed. Exiting with status $test_exit_code"
fi

exit $test_exit_code
