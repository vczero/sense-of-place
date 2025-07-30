import pandas as pd
import numpy as np

userinfo = pd.read_csv('../clean_data/userinfo.csv')
userinfo = userinfo.drop_duplicates(subset='userid', keep='first')

userinfo.to_csv('../clean_data/userinfo.csv', index=None)