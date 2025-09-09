import pandas as pd
import random

class ThicketMultiplierStub:

    def __init__(self, th_ens):
        df = th_ens.dataframe
        df_arr = []

        length_of = len(th_ens.dataframe)

        print("length_of=" + str(length_of))

        for j in range(2):
            for i in range(length_of):
                one_item = th_ens.dataframe.iloc[i]
                df_arr.append( one_item )

        th_ens = df_arr


    def old_constructor(self, th_ens):
        df = th_ens.dataframe
        rand_prof = self.random_int(100000000)

        new_obj = {
            "node":{'name': 'StubTimeIncrement', 'type': 'function'},
            "profile": rand_prof,
            "nid": self.random_int(10000),
            "min#inclusive#sum#time.duration": self.random_float(1),
            "max#inclusive#sum#time.duration": self.random_float(1),
            "avg#inclusive#sum#time.duration": self.random_float(1),
            "name": "TimeIncrement",
            "Name": 2000 + self.random_int(1000)
        }


        # Get the first row
        #first_row = df.iloc[[0]]
        length_of = len(th_ens.dataframe)

        print( "length_of=" + str(length_of))

        for j in range(2):
            for i in range( length_of ):
                first_row = pd.DataFrame(th_ens.dataframe.iloc[i]).transpose()

                # Concatenate the DataFrame with its first row
                th_ens.dataframe = pd.concat([th_ens.dataframe, first_row], ignore_index=False)

        #th_ens.dataframe.repeat(5)

        #print("len2=" + str(len(th_ens.dataframe)))


    def random_float(self, max):
        return random.uniform(0, max)

    def random_int(self, max):
        return random.randint(0, max)