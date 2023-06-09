class EmbeddingSETEStandalone :
    """
    This class takes the embedding operations on cdr3 sequences from SETE.
    Each cdr3 sequence will be embedded into 1d numpy ndarray.
    This standalone version can run directly and does not require any source code from SETE.

    reference:
        - Article: SETE: sequence-based ensemble learning approach for TCR epitope binding prediction
        - Authors: Tong, Y. et al
        - Article link: https://www.sciencedirect.com/science/article/abs/pii/S1476927120303194
        - GitHub link: https://github.com/wonanut/SETE
    """

    def __init__(self, input_file_path = './data/test.csv'):
        '''
        Set original csv path.

        :param input_file_path: original input file path.
        '''
        self.input_file_path = input_file_path

    def splitCDR(self, CDRseq, k=3):
        '''
        Note:
            This function is copied from SETE.py in SETE-master.
            See https://github.com/wonanut/SETE for original source code.
        '''
        retDict = []
        for i in range(len(CDRseq) - k + 1):
            retDict.append(CDRseq[i:i + k])
        return retDict

    def statisticsKmer(self, epiDict, k=3):
        '''
        Note:
            This function is copied from SETE.py in SETE-master.
            See https://github.com/wonanut/SETE for original source code.
        '''
        kmerDict = {}
        for epi in epiDict:
            for i in range(len(epiDict[epi])):
                splitList = self.splitCDR(epiDict[epi][i], k)
                for split in splitList:
                    if split not in kmerDict:
                        kmerDict[split] = 1
                    else:
                        kmerDict[split] += 1
        return kmerDict

    def splitCDR(self, CDRseq, k=3):
        '''
        Note:
            This function is copied from SETE.py in SETE-master.
            See https://github.com/wonanut/SETE for original source code.
        '''
        retDict = []
        for i in range(len(CDRseq) - k + 1):
            retDict.append(CDRseq[i:i + k])
        return retDict

    def buildFeatures(self, epiDict, kmerDict, k=3):
        '''
        Note:
            This function is copied from SETE.py in SETE-master.
            See https://github.com/wonanut/SETE for original source code.
        '''
        import numpy as np
        counter = 0
        for epi in epiDict:
            counter += len(epiDict[epi])
        retArr = np.zeros((counter, len(kmerDict)))

        kmerList = kmerDict.keys()
        retLabel = []

        iter = 0
        epinum = 0
        for epi in epiDict:
            for cdr in range(len(epiDict[epi])):
                splitlist = self.splitCDR(epiDict[epi][cdr], k)
                retLabel.append(epinum)
                i = 0
                for kmer in kmerList:
                    retArr[iter][i] = splitlist.count(kmer)
                    i += 1
                iter += 1
            epinum += 1
        print()
        return np.array(retArr), np.array(retLabel)

    def embed(self, k=3, remove_duplicate=False):
        '''
        
        Embed cdr3 sequence into 1d numpy ndarray.

        :param k:
        :param remove_duplicate: remove duplicate data if True
        :return: embedded cdr3 sequence and kmer dictionary
        '''
        import pandas as pd

        print("Reading file: ", self.input_file_path)
        df = pd.read_csv(self.input_file_path)

        if remove_duplicate:
            head_list = df.columns.values.tolist()
            assert 'epitope' in head_list and 'cdr3b' in head_list and 'vb_gene' in head_list
            subset = ['epitope', 'cdr3b', 'vb_gene']
            if 'vb_gene' in head_list:
                df.drop_duplicates(subset=subset, inplace=True)

        epiDict = {}
        for index, row in df.iterrows():
            if row['epitope'] not in epiDict:
                epiDict[row['epitope']] = []
            epiDict[row['epitope']].append(row['cdr3b'])

        statistics_epi = []
        statistics_num = []
        # print('{:22s} {:s}'.format('Epitope', 'Number'))
        for epi in epiDict:
            statistics_epi.append(epi)
            statistics_num.append(len(epiDict[epi]))
            # print('{:22s} {:d}'.format(epi, len(epiDict[epi])))

        kmerDict = self.statisticsKmer(epiDict, k)
        X, y = self.buildFeatures(epiDict, kmerDict, k)

        return X, kmerDict

if __name__ == '__main__':
    embedding = EmbeddingSETEStandalone('./data/epitope_tcr_pairs.csv')
    X, kmerDict = embedding.embed(k=3)
    print(X.shape)
    print(kmerDict)