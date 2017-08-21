
def formatToHHMM(timeInSeconds):
    m = timeInSeconds // 60
    return "{0:02d}:{1:02d}".format(m, timeInSeconds % 60)
