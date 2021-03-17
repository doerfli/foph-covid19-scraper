def extractIdx(row, *idxNames):
    idxs = []
    for idx in idxNames:
        for i in range(len(row)):
            if row[i] == idx:
                idxs.append(i)
    return idxs
