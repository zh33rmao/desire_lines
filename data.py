# -*- coding:utf-8 -*-
__author__ = 'zh33rmao'

import pandas as pd

class CalculateOD:
    def __init__(self, path, flname, dealrq):
        self.df = pd.read_csv(path,dtype={'flname': str, 'fldirection': str, 'dealrq': str
                                          ,'hh': str,'fOsname': str,'fDsname': str,'vol': int})
        # print(self.df.dtypes)
        self.lineName = flname
        # print(type(self.lineName))
        self.dealrq = dealrq
        # print(type(self.dealrq))

    def calOD(self):
        oddf = self.df[self.df['flname'] == self.lineName]
        oddf = oddf[oddf['dealrq'] == self.dealrq]
        oddf = oddf[oddf['vol'] > 5]
        od = oddf.groupby(by=['fOsname', 'fDsname'], as_index=False)['vol'].sum().reset_index()
        od = pd.DataFrame(od)
        # print(od)
        return od