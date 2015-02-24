import re
import math
def diagnose(str):
    syndrome = []

    #telephone
    if(re.search('\d{5,}|(?:\d{3,}\s+)+\d+|(?:\d{3,}-+)+\d+', str)):
        syndrome.append(True)
    else: syndrome.append(False)

    #money
    if(re.search('(?i)(win|prize|reward|award|cash)', str)):
        syndrome.append(True)
    else: syndrome.append(False)

    #website
    if(re.search('(?i)(www|http|\.com)', str)):
        syndrome.append(True)
    else: syndrome.append(False)

    #sales
    if(re.search('(?i)(sale|free|subscri|customer|reply|text|txt)', str)):
        syndrome.append(True)
    else: syndrome.append(False)

    #you
    if(re.search('(?i)(you|your|u|yr)', str)):
        syndrome.append(True)
    else: syndrome.append(False)

    #length
    if(len(str) > median_len):
        syndrome.append(True)
    else: syndrome.append(False)

    return syndrome

def learn(stat):
    N = len(stat)                # number of data points
    m = len(stat[0])             # number of features
    class_cond = []
    for i in range(0, m):
        class_cond.append(float(count(stat, i))/N)
    return class_cond

def count(list, i):
    N = len(list)
    count = 0
    for x in range(0, N):
        if list[x][i]:
            count = count + 1
    return count

def bayes_classify(test_list, spam_prior, spam_conditional, ham_prior, ham_conditional):
    prediction = []
    for str in test_list:
        syndrome = diagnose(str)
        spam = math.log(spam_prior)
        ham = math.log(ham_prior)
        for i in range(0, len(spam_conditional)):
            if syndrome[i]:
                spam = spam + math.log(spam_conditional[i])
                ham = ham + math.log(ham_conditional[i])
            else:
                spam = spam + math.log(1-spam_conditional[i])
                ham = ham + math.log(1-ham_conditional[i])
        if spam > ham:
            prediction.append(True)
        else:
            prediction.append(False)
    return prediction

def testset_prep(data):
    spam = []
    test_set = []
    for sms in data:
        assert re.match('(^ham\t|^spam\t)', sms)

        if re.match('^ham\t', sms):
            test_set.append(re.sub('^ham\t', '', sms))
            spam.append(False)
        elif re.match('^spam\t', sms):
            test_set.append(re.sub('^spam\t', '', sms))
            spam.append(True)
    return [spam, test_set]

#do training
f = open('SMSSpamCollection.train');
collection = f.readlines();
spam_corpus = [];
ham_corpus = [];
length = [];
for sms in collection:
    assert re.match('(^ham\t|^spam\t)', sms)
    spam = False
    if re.match('^ham\t', sms):
        sms = re.sub('^ham\t', '', sms)
        ham_corpus.append(sms)
    elif re.match('^spam\t', sms):
        sms = re.sub('^spam\t', '', sms)
        spam_corpus.append(sms)
    length.append(len(sms))

length.sort()
median_len = length[len(length)/2]

spam_stat = []
for sms in spam_corpus:
    spam_stat.append(diagnose(sms))

ham_stat = []
for sms in ham_corpus:
    ham_stat.append(diagnose(sms))

#learn the likelihood of each features
spam_conditional = learn(spam_stat)
ham_conditional = learn(ham_stat)

#prior probability
spam_prior = float(len(spam_stat))/len(collection)
ham_prior = float(len(ham_stat))/len(collection)

f = open('SMSSpamCollection.test');
test_set = f.readlines();
test_set = testset_prep(test_set)
spam = test_set[0]
test = test_set[1]
bayes_prediction = bayes_classify(test, spam_prior, spam_conditional, ham_prior, ham_conditional)
count = 0
for i in range(0, len(test)):
    if spam[i] != bayes_prediction[i]:
        count = count + 1
error = float(count)/len(test)
print 'The misclassfication rate of spam SMS is ' + str(error*100) +'%'
