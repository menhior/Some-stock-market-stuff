import os
  

#root = "C:\\Users\\user\\Desktop\\Python\\Small_Python_Things\\Python_For_Finance\\YahooStockData\\GetData\\test" 
root = os.path.join(os.getcwd(), 'stock_data')
folders = list(os.walk(root))[1:]

for folder in folders:
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:
        os.rmdir(folder[0])
        print(folder[0])