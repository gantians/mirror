# -*- coding: cp936 -*-
import re, collections
class Corrector:
    

    def words(self,text): return re.findall('[a-z]+', text.lower()) 

    def train(self,features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def __init__(self):
        
    # ����һ���ֵ�

        Corrector.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        Corrector.NWORDS =self.train(self.words(file('big.txt').read()))    


    def edits1(self,word):
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       # ��word�ֳ������� word = a + b
       deletes    = [a + b[1:] for a, b in splits if b]
       # �� b�ĵ�һλɾ�� 
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       # �� b��ǰ��λ����
       replaces   = [a + c + b[1:] for a, b in splits for c in Corrector.alphabet if b]
       # �� b�ĵ�һλ�滻��
       inserts    = [a + c + b     for a, b in splits for c in Corrector.alphabet]
       # �� a,b �м����һ���ַ�
       return set(deletes + transposes + replaces + inserts)

    def known_edits2(self,word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in Corrector.NWORDS)

    def known(self,words): return set(w for w in words if w in Corrector.NWORDS)

    def correct(self,word):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        #print list(candidates)
        return max(candidates, key=Corrector.NWORDS.get)
