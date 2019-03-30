import torch
from network import Net4SA
import matplotlib.pyplot as plt
from load_data import MemoryFriendlyLoader4SA, CorpusLoader4SA

torch.cuda.set_device(1)
plt.switch_backend('agg')

SAdir = '../data/aclImdb_v1/aclImdb/test'
full_model = './models/SA_just_best_params.pkl'

Dataset = MemoryFriendlyLoader4SA(SAdir=SAdir, word2vec='../word2vec/en/en.bin')
train_loader = torch.utils.data.DataLoader(dataset=Dataset, batch_size=1, shuffle=False, num_workers=0)
sample_size = Dataset.__len__()

net = Net4SA()
net.load_state_dict(torch.load(full_model))
net.cuda()
net.eval()

t = 0
count = 0

TP = 0
TN = 0

for step, (s1, ground_truth) in enumerate(train_loader):
    s1 = s1.cuda()
    ground_truth = ground_truth.cuda()

    label = net(s1)

    if (label[:, :, 0] >= label[:, :, 1] and ground_truth[:, 0] == 1):
        TP += 1
        t += 1
    elif (label[:, :, 0] < label[:, :, 1] and ground_truth[:, 1] == 1):
        TN += 1
        t += 1

    count += 1
    print('%d/%d' % (count, sample_size))

print('Accuracy: %f' % (t / count))
print('F1 Score: %f' % (2 * TP / (count + TP - TN)))