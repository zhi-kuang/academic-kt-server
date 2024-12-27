import torch
import torch.utils.data as Data
from .readdata import DataReader


def getDataLoader(batch_size, num_of_questions, max_step):
    handle = DataReader('app/data/class_problem_sequence.csv', max_step,
                        num_of_questions)

    dtest = torch.tensor(handle.getTestData().astype(float).tolist(),
                         dtype=torch.float32)
    testLoader = Data.DataLoader(dtest, batch_size=batch_size, shuffle=False)
    return testLoader
