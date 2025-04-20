PROJECT_DIR=$(dirname "$(realpath "$0")")

test_files=$(find "$PROJECT_DIR" -type f -name 'test_*.py')

if [ -z "$test_files" ]; then
    echo "No test files found!"
    exit 1
fi

echo "Running all found tests..."
python3 -m unittest $(echo "$test_files") -v

echo "\nAll tests execution finished."

test_exit_code=$?
if [ $test_exit_code -ne 0 ]; then
    echo "\nSome tests failed. Exiting with status $test_exit_code"
fi

exit $test_exit_code
