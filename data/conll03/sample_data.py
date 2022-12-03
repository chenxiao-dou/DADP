import csv
from itertools import compress
def get_conll_data(file_path) -> dict:
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter = ' ')
        for row in reader:
            data.append([row])

    sentences = []
    sentence = []
    entities = []
    tags = []
    result=[]
    for row in data:
        # extract first element of list.
        row = row[0]
        # TO DO: move to data reader.
        if len(row) > 0 and row[0] != '-DOCSTART-':
            sentence.append(row[0])
            tags.append(row[-1])        
        if len(row) == 0 and len(sentence) > 0:
            # clean up sentence/tags.
            # remove white spaces.
            selector = [word != ' ' for word in sentence]#单词!=' '的位置是True
            sentence = list(compress(sentence, selector))#选择sentence中对应位置是True的word
            tags = list(compress(tags, selector))
            # append if sentence length is still greater than zero..
            if len(sentence) > 0:
                result.append([sentence,tags])
            sentence = []
            tags = []
            
    
    return result



train_data=get_conll_data('/home/xhsun/.conll/train.txt')
test_data=get_conll_data('/home/xhsun/.conll/test.txt')

print(len(train_data),len(test_data))
print(train_data[0])
print(test_data[10])

import random
random.seed(42)
random.shuffle(train_data)
random.shuffle(test_data)
sample_rate=0.3
sample_train_nums=int(len(train_data)*sample_rate)
sample_test_nums=int(len(test_data)*sample_rate)

saved_train_data=train_data[:sample_train_nums]
saved_test_data=test_data[:sample_test_nums]

def write_to_path(save_path,data):
    with open(save_path,'w') as f:
        for example in data:
            sentence,label = example[0],example[1]
            assert len(sentence)==len(label)
            for word,tag in zip(sentence,label):
                f.write(word+'\t'+tag+'\n')
            f.write('\n')


write_to_path(save_path='/home/xhsun/Desktop/model9001/data/conll03/train.txt',data=saved_train_data)
write_to_path(save_path='/home/xhsun/Desktop/model9001/data/conll03/test.txt',data=saved_test_data)