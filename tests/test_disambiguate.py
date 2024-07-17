def test_disambiguate():
    search_pattern = os.path.join('..','experiments', '*.tre')

    # Use glob to find all files with the given extension
    files = glob.glob(search_pattern)

    # Loop over the list of files and process each one
    for file_path in files:
        print(file_path)
        print(quickparse(file_path).getText())
        print(disambiguate(quickparse(file_path)))