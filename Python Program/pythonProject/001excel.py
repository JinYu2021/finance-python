import pandas as pd

df = pd.DataFrame({'ID':[1,2,3],'Name':['Tim','Victor','Nick']})
df = df.set_index('ID')
df.to_excel('D:\APP\weinxin\WeChat Files\wxid_uud4dlficore41\FileStorage\Temp\Copy\output005.xlsx')
print('Done!')