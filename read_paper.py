def read_file(file_name):
	ret = open(file_name).readlines()

	for line in ret:
		line = line.split(";")
		