import matplotlib.pyplot as plt
from numpy.random import normal
import pandas as pd
import io

# data = pd.read_csv('Accounts_Bots_Gasolinazo.csv')
# x = data.Score
# x = [account for account in x if account != "Null"]
#
# print (x)
# plt.hist(x)
# plt.title("Gaussian Histogram")
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# plt.show()


df = pd.read_csv('Accounts_Bots_Gasolinazo.csv', sep=',')
x = df
x = [account for account in x if account != 'Null']
plt.hist(x['Score'], bins=30)


#
# import matplotlib.pyplot as plt
# import pandas as pd
#
# data = pd.read_csv('Accounts_Bots_Gasolinazo.csv', sep=',',header='Score', index_col =1)
# x = data
# x = [account for account in x if account != "Null"]
# data.plot(kind='bar')
# plt.ylabel('Frequency')
# plt.xlabel('Words')
# plt.title('Title')
#
# plt.show()
#
# import numpy as np
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
# import pandas as pd
#
#
# import matplotlib.pyplot as plt
# import numpy as np
# df = pd.read_csv('Accounts_Bots_Gasolinazo.csv')
# x = df.Score
# x = [account for account in x if account != "Null"]
# x = np.fromstring(x)
# print (x)
# plt.hist(x)
