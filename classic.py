import pandas as pd

class ClassicPrice:
    def __init__(self, csv_file, servers=None, rate=.75):
        self.csv_file = csv_file
        self.servers =  servers
        self.rate = rate

    #This is if you don't have filter your data
    def filter_data(self):
        #read the csv
        df = pd.read_csv(self.csv_file)
        #change the price to buy price 75% of total value
        df['price'] = (df['price'] *self.rate).round(2)
        #filter tru the server we want to buy
        df = df[df['server'].isin(self.servers.keys())]
        #create a new column with the server and faction combined as string
        df['server_faction'] = df['server'] + '-' + df['faction']
        #filter the data to only include the True values eg: server-faction is in server buy list
        df = df[df['server_faction'].apply(lambda x: (self.servers[x.split('-')[0]] == [x.split('-')[1]]) if len(self.servers[x.split('-')[0]]) == 1 else True)]
        #now eliminate the server_faction column is not needed and sort the values alphabetically
        df = df.drop('server_faction', axis=1).sort_values(by='server', ascending=True)
        #pivot the data frame to make the server have a column for each faction with the value of his price and fill the NAN
        df = df.pivot(index='server', columns='faction', values='price').fillna('---')
        #name the columns
        df.columns = ['Alianza', 'Horda']
        #reset the index
        df = df.reset_index()
        return df
    
    def filtered_data(self):
        #read data frame
        df = pd.read_csv(self.csv_file)
        #change the price to buying price
        df['price'] = (df['price'] *self.rate).round(2)
        #sort values alphabetically
        df = df.sort_values(by='server', ascending=True)
        #pivot the data frame to make the server have a column for each faction with the value of his price and fill the NAN
        df = df.pivot(index='server', columns='faction', values='price').fillna('---')
        #name the columns
        df.columns = ['Alianza', 'Horda']
        #reset the index
        df = df.reset_index()
        return df
