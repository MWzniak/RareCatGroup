class RareCatGroup():
    '''
    A class for grouping categories with a certain amount of occurences in a column.

    When you are faced with a lot of rare categories, OneHotEncoding might create too many dimensions. 
    Mapping these as 'other' drastically reduces the dimensionality of the dataset.
    '''
    def __init__(self,dataset,n,col_list=False,map_value='other'):
        '''
        Parameters
        ----------
        dataset : pandas.DataFrame object
            Dataframe which you want to modify.
        
        n : int
            Categories with less or equal this amount will be converted to map_value

        col_list : list, optional
            Colums of the dataset which you want altered. 
            Defeault = False, every column in the dataset will be altered.

        map_value: string or numerical, optional
            Specify the replacement value of the rare categories
            Defeault = 'other'
        '''
        self.name_list=[]   
        self.dict_list=[]
        self.am=n
        self.dataset=dataset
        if col_list:
            self.cats=col_list
        else:
            self.cats=list(self.dataset.columns)
        self.map_value=map_value
    def make_dict(self):
        for n in self.cats:
            val_count=self.dataset[n].value_counts()
            d={}
            if len(val_count[val_count<=self.am].index)>1:
                self.name_list.append(val_count[val_count<=self.am].name)
                s=list(pd.Series(val_count[val_count<=self.am].index))
                for m in range(0,len(s)):
                    d[s[m]]=self.map_value
                self.dict_list.append(d)
        return [self.dict_list,self.name_list]
    def group_cats(self):
        '''
        Returns
        -------
        dataset: pandas.DataFrame object
            The modified dataframe.
        '''
        l=self.make_dict()
        dict_list=l[0]
        for n in range(0,len(dict_list)):
            self.dataset[self.name_list[n]]=self.dataset[self.name_list[n]].map(dict_list[n]).fillna(self.dataset[self.name_list[n]])
        return self.dataset
