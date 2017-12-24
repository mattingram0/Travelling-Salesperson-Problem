def writeTourFile(filename, size, length, tour):

    path = '/Users/matt/Documents/Durham/2nd Year/Software Methodologies/AI Search Assignment/checker/gkxx72/TourfileA/tour' + filename
    f = open(path, "w+")
    data = "NAME = " + filename[:len(filename) - 4] + ",\nTOURSIZE = " + str(
        size) + ",\nLENGTH = " + str(length) + ",\n"
    tourString = ",".join(str(i) for i in tour)

    f.write(data + tourString)
