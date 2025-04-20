# #!/bin/bash

# # Get the directory where the script is located
# PROJECT_DIR=$(dirname "$(realpath "$0")")
# echo "PROJECT_DIR: $PROJECT_DIR"

# # Find all files starting with test_ and ending with .py in the project directory
# test_files=$(find "$PROJECT_DIR" -type f -name 'test_*.py')

# echo "Found test files:"
# echo "$test_files"

# # Check if any test files were found
# if [ -z "$test_files" ]; then
#     echo "No test files found!"
#     exit 1
# fi

# # Run unittest on each test file found
# for test_file in $test_files; do
#     echo "Running tests in $test_file..."
#     python3 -m unittest "$test_file"
# done

#!/bin/bash

# Get the directory where the script is located
PROJECT_DIR=$(dirname "$(realpath "$0")")

# Find all files starting with test_ and ending with .py in the project directory
test_files=$(find "$PROJECT_DIR" -type f -name 'test_*.py')

# Check if any test files were found
if [ -z "$test_files" ]; then
    echo "No test files found!"
    exit 1
fi

# Run unittest on all found test files
echo "Running all found tests..."
python3 -m unittest $(echo "$test_files") -v

echo "\nAll tests execution finished."

# Capture the exit code of the unittest command
test_exit_code=$?
if [ $test_exit_code -ne 0 ]; then
    echo "\nSome tests failed. Exiting with status $test_exit_code"
fi

exit $test_exit_code
