import os
import pandas as pd
from tqdm import tqdm
  
# List to store all empty 
# directories 
empty = [] 
  
# Traversing through Test 
for root, dirs, files in tqdm(os.walk('.')): 
    # Checking the size of tuple 
    if not len(dirs) and len(files) < 4:
        # Adding the empty directory to 
        # list 
        empty.append(root[2:])

#empty.remove('')
  

df = pd.DataFrame(empty)

df.to_csv("retry_tickers.csv")