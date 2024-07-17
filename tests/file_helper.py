import glob
import os


def all_tre_files(fail_files = None):

    if not fail_files:
        fail_files = []

    # Here I just test all tre files.
    search_pattern = os.path.join('..', 'experiments', '*.tre')
    files = glob.glob(search_pattern)

    # List of tuples with file paths and whether they are expected to fail
    tests = [
        (file_path, False) for file_path in set(files) - set(fail_files)  # only those that should work
    ]

    tests += [(file_path, True) for file_path in fail_files]

    return sorted(tests, key=lambda x: (x[1], x[0]), reverse=True)

def selected_tre_files(positive_files, negative_files = None):
    if not negative_files:
        fail_files = []



    # List of tuples with file paths and whether they are expected to fail
    tests = [
        (file_path, False) for file_path in positive_files  # only those that should work
    ]

    tests += [(file_path, True) for file_path in negative_files]

    return sorted(tests, key=lambda x: (x[1], x[0]))
