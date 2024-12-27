import numpy as np
import itertools


class DataReader():
    def __init__(self, test_path, maxstep, numofques):
        self.test_path = test_path
        self.maxstep = maxstep
        self.numofques = numofques

    def getData(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            for len, ques, ans in itertools.zip_longest(*[file] * 3):
                len = int(len.strip().strip(','))
                ques = [int(q) for q in ques.strip().strip(',').split(',')]
                ans = [int(a) for a in ans.strip().strip(',').split(',')]
                slices = len//self.maxstep + (1 if len % self.maxstep > 0 else 0)
                for i in range(slices):
                    temp = temp = np.zeros(shape=[self.maxstep, 2 * self.numofques])
                    if len > 0:
                        if len >= self.maxstep:
                            steps = self.maxstep
                        else:
                            steps = len
                        for j in range(steps):
                            if ans[i*self.maxstep + j] == 1:
                                temp[j][ques[i*self.maxstep + j]] = 1
                            else:
                                temp[j][ques[i*self.maxstep + j] + self.numofques] = 1
                        len = len - self.maxstep
                    data.append(temp.tolist())
            print('done: ' + str(np.array(data).shape))
        return data


    def getTestData(self):
        print('loading test data...')
        testData = self.getData(self.test_path)
        return np.array(testData)
