import numpy as np
import pandas as pd

class FuelAnalysis:

    def __init__(self):
        self.df = pd.read_csv("D:\\Downloads\\Bot Tutorial\\AI Australia\\botdialog\\FuelPrice.csv")
        # Remove all observation with NA values(missing values)
        self.df = self.df.dropna()
        # for out purpose we require only require records which are E10 fuel type
        self.df=self.df.loc[self.df['FuelCode']== 'E10']
        self.df['PriceUpdatedDate'] = pd.to_datetime(self.df['PriceUpdatedDate'])
        self.df['DayofWeek'] = self.df['PriceUpdatedDate'].dt.day_name()
        self.df = self.df.reset_index(drop=True)
        self.df['Postcode'] = self.df['Postcode'].astype(int)

    def checkPostCode(self,pincode):
        return not(self.df[self.df['Postcode'].isin([pincode])].empty)

    def getInfo(self,pincode):
        sub_df = self.df[self.df['Postcode'] == pincode] # dataframe with user defined Pincode 
        df1 = sub_df.groupby(['Address','Brand']).mean()
        df1 = df1.sort_values(by=['Price'], ascending= True)
        rec = df1.reset_index()
        return rec.iloc[0]['Address'] , round(rec.iloc[0]['Price'],2)

    def getBestDays(self,pincode):
        sub_df = self.df[self.df['Postcode'] == pincode] # dataframe with user defined Pincode 
        df1 = sub_df.groupby(['DayofWeek']).mean()
        df1 = df1.sort_values(by=['Price'], ascending= True)
        df2 = sub_df.groupby(['Brand']).mean()
        df2 = df2.sort_values(by = ['Price'],ascending= True)
        rec1 = df1.reset_index()
        rec2 = df2.reset_index()
        return rec1.iloc[0]['DayofWeek'],rec1.iloc[1]['DayofWeek'], rec2.iloc[0]['Brand']



# sub_df[sub_df['PriceUpdatedDate']==sub_df['PriceUpdatedDate'].min()]
# print(sub_df.groupby(['Address','Brand','Suburb']).mean())
# print(sub_df.groupby(['DayofWeek']).mean())
# print(df.groupby(['Address']).mean())

obj = FuelAnalysis()
print(obj.getBestDays(2137))
print(obj.checkPostCode(2137))
print(obj.getInfo(2137))