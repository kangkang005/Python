# %%
import pandas as pd
import numpy as np

# %%
# 2d array create DataFrame
print("####### array ##########")
data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
df = pd.DataFrame(data, columns=['Site', 'Age'])
df['Site'] = df['Site'].astype(str)
df['Age'] = df['Age'].astype(float)
print(df)

# %%
# dict create DataFrame
print("####### dict ##########")
data = {'Site':['Google', 'Runoob', 'Wiki'], 'Age':[10, 12, 13]}
df = pd.DataFrame(data)
print(df)

# %%
# np create DataFrame
print("###### np #########")
ndarray_data = np.array([
    ['Google', 10],
    ['Runoob', 12],
    ['Wiki', 13]
])
df = pd.DataFrame(ndarray_data, columns=['Site', 'Age'])
print(df)

# %%
# list of dict create DataFrame
print("###### list of dict #########")
data = [{'a': 1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]
df = pd.DataFrame(data)
print(df)

# %%
# dict of list create DataFrame
print("###### dict of list #########")
data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
df = pd.DataFrame(data, index=['row1', 'row2', 'row3'])
print(df)

# %%
# Series create DataFrame
print("###### Series #########")
s1 = pd.Series(['Alice', 'Bob', 'Charlie'])
s2 = pd.Series([25, 30, 35])
s3 = pd.Series(['New York', 'Los Angeles', 'Chicago'])
df = pd.DataFrame({'Name': s1, 'Age': s2, 'City': s3})
print(df)

# %%
print("###### Method #########")
print(df.empty)
print(pd.DataFrame().empty)
print(df.T)     # transpose
print(df.axes)
print(df.shape)
print(df.head())
print(df.tail())
print(df.info())
# print(df.mean())
# print(df.sum())

# %%
print("###### Element #########")
print("\ndf=")
print(df)
print("\ndf['Name']=")
print(df['Name'])   # columns name
print("\ndf[['Name', 'Age']]=")
print(df[['Name', 'Age']])
print("\ndf.Age=")
print(df.Age)      # columns name
print("\ndf['Name'][0]=")
print(df['Name'][0])    # [col][row]
print("\ndf['Name'][1:]=")
print(df['Name'][1:])
print("\ndf[1:]=")
print(df[1:])

# %%
print("###### loc #########")
df = pd.DataFrame({'Brand': ['Maruti', 'Hyundai', 'Tata',
                               'Mahindra', 'Maruti', 'Hyundai',
                               'Renault', 'Tata', 'Maruti'],
                     'Year': [2012, 2014, 2011, 2015, 2012,
                              2016, 2014, 2018, 2019],
                     'Kms Driven': [50000, 30000, 60000,
                                    25000, 10000, 46000,
                                    31000, 15000, 12000],
                     'City': ['Gurgaon', 'Delhi', 'Mumbai',
                              'Delhi', 'Mumbai', 'Delhi',
                              'Mumbai', 'Chennai',  'Ghaziabad'],
                     'Mileage':  [28, 27, 25, 26, 28,
                                  29, 24, 21, 24]})
print(df)
print()
# support boolean
# loc[row, col]
print(df.loc[:, 'City'])
print()
print(df.loc[:, ['Brand', 'Mileage', 'Year']])
print()
print(df.loc[:, df.columns[[0, 1]]])    # same as df.iloc[:, [0,1]]
print()
print(df.loc[0, 'City'])
print()
print(df.loc[0, :])
print()
print(df.loc[1:, 'City'])
print()
# same as 'where' method
print(df.loc[(df.Brand == 'Maruti') & (df.Mileage > 25)])   # selecting cars with brand 'Maruti' and Mileage > 25
print()
print(df.loc[2: 5]) # selecting range of rows from 2 to 5
print()
print(df.loc[[0, 2, 4, 7]]) # selecting 0th, 2th, 4th, and 7th index rows
print()
print(df.loc[[0, 2, 4, 7], ['Brand', 'Mileage', 'Year']]) # selecting 0th, 2th, 4th, and 7th index rows
print()
mask = ((df.Brand == 'Maruti') & (df.Mileage > 25))
print(df.loc[mask, ['Brand', 'Mileage', 'Year']])

# %%
print("###### iloc #########")
# only support number index
print(df.iloc[:, 0])
print()
print(df.iloc[[0, 2, 4, 7]])    # selecting 0th, 2th, 4th, and 7th index rows
print()
print(df.iloc[1: 5, 2: 5])    # selecting rows from 1 to 4 and columns from 2 to 4
print()
print(df.iloc[0, :])
print()
print(df.iloc[0, [0, 1]])

# %%
print("###### statistic #########")
print(df.describe())
print()
print(df['Year'].mean())
print()
print(df['Year'].min())
print()
print(df['Year'].sum())

# %%
print("###### type #########")
print(df.dtypes)
df['Mileage'] = df['Mileage'].astype('float64')
print(df)

# %%
print("###### modify and add new element #########")
# modify
df['Mileage'] = [10, 11, 12, 13, 45, 14, 53, 89, 71]
print(df)
print()
# append new col, Country is not in DataFrame
df['Country'] = ["China", "China", "USA", "China", "USA", "USA", "USA", "China", "USA"]
print(df)
print()
df.loc[0, 'Mileage'] = 100
print(df)
print()
df.loc[:1, 'Mileage'] = [10, 2]
print(df)
print()
df.loc[:1, ['Mileage', 'Country']] = [[10, "US"], [2, "US"]]
print(df)
print()
# append new row
# https://stackoverflow.com/questions/19365513/how-to-add-an-extra-row-to-a-pandas-dataframe
df.loc[len(df)] = ["Tata", 2016, 32000, "Delhi", 200, "US"]
print(df)
print()
df.loc[df.index.max() + 1] = ["Tata", 2016, 32000, "Delhi", 200, "US"]
print(df)
print()
# modify row
df.loc[0] = ["Tata", 2016, 32000, "Delhi", 200, "US"]
print(df)
print()
# append new row with concat
new_row = {"Brand":["Tata"], "Year":[2016], "Kms Driven": [32000], "City":["Delhi"], "Mileage":[200], "Country":["US"]}
df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
print(df)

# %%
print("###### del, pop and drop #########")
# del column, axis=1
df_dropped = df.drop('Country', axis=1)
print(df_dropped)
print()
df_dropped = df.drop(['Country', "City"], axis=1)
print(df_dropped)
print()
df_dropped = df.drop(columns=['Country', "City"])
print(df_dropped)
print()
# del row, not change row index
df_dropped = df.drop(0)
print(df_dropped)
print()
df_dropped = df.drop([3, 6])
print(df_dropped)
print()
df_dropped = df.drop(index=[3, 6])
print(df_dropped)
print()
# del row, reset index
df_dropped = df.drop(index=[3, 6])
df_dropped = df_dropped.reset_index(drop=True)
print(df_dropped)
print()
# del column and row
df_dropped = df.drop(index=[3, 6], columns=df.columns[[0, 1]])
print(df_dropped)
print()
df_dropped = df.drop(index=[3, 6], columns=['Country', "City"])
print(df_dropped)
print()
# modify raw data, inplace = True, no return
df.drop([3, 6], inplace=True)
print(df)
print()
# pop
df.pop("City")
print(df)
print()
# del
del df["Country"]
print(df)
print()

# %%
print("###### index and columns #########")
print(df.columns)
print(df.columns[[0, 2]])
print(df.columns[0])
print(df.index)
print(df.index[[0, 2]])
print(df.index[0])
# reset index, drop=True is not generate "index" column
df.reset_index(drop=True, inplace=True)
print(df)

# %%
print("###### operation #########")
df['Sum'] = df['Kms Driven'] + df['Mileage']
print(df)
print()
df['Sum'] -= df['Mileage']
print(df)

# %%
print("###### iteration #########")
# Note: not modify data in iteration
# iterate by col
for col_name in df:
    print(col_name)
    print(df[col_name])
print()

# %%
# iterate by row
for row_index, row in df.iterrows():
    print(row_index)
    print(row)
print()

for row_index in df.index:
    print(row_index)
    print(df.loc[row_index])
print()

# %%
# iterate by tuple
for row in df.itertuples():
    print(row.Index)
    print(row)
print()

# %%
# iterate by row, delete given data
for row_index in df.index:
    if df.loc[row_index, "Year"] == 2019:
        df.drop(row_index, inplace=True)
df.reset_index(inplace=True)
df.drop("index", axis=1 ,inplace=True)
print(df)

# %%
print("###### sort #########")
sort = df.sort_values(ascending=False, by="Year").reset_index()
print(sort)
print()
sort = df.sort_values(by="Year").reset_index()
print(sort)
print()
# sort multiple values
sort = df.sort_values(by=["Year", "Mileage"]).reset_index()
print(sort)
print()
unsort = df.sort_values(by="Year").sort_index(ascending=False)
print(unsort)
print()

# %%
print("###### merge #########")
# https://stackoverflow.com/questions/40468069/merge-two-dataframes-by-index
# merge column by index
right = pd.DataFrame({"Country": ["China", "China", "USA", "China", "USA", "USA", "USA", "China", "USA"]})
print(right)
col_merge = pd.merge(df, right, left_index=True, right_index=True)
print(col_merge)
print()
# or join
col_join = df.join(right)
print(col_join)
print()
# or concat
col_concat = pd.concat([df, right], axis=1)
print(col_concat)
print()

# %%
# merge column by Brand, merge intersection
country = pd.DataFrame({"Brand": ["Tata", "Hyundai"], "Country": ["China", "USA"]})
merge = pd.merge(df, country, on="Brand", how="left")
print(merge)
print()
country = pd.DataFrame({"Brand": ["Tata", "Hyundai", "Maruti"], "Country": ["China", "USA", "US"]})
merge = pd.merge(df, country, on="Brand", how="left")
print(merge)
print()
# sort by brand, not how
country = pd.DataFrame({"Brand": ["Tata", "Hyundai", "Maruti"], "Country": ["China", "USA", "US"]})
merge = pd.merge(df, country, on="Brand")
print(merge)
print()
# merge union, Brand Intel not in df
country = pd.DataFrame({"Brand": ["Tata", "Hyundai", "Maruti", "Intel"], "Country": ["China", "USA", "US", "Canada"]})
merge = pd.merge(df, country, on="Brand", how="outer")
print(merge)
print()

# %%
print("###### concat #########")
# concat row, default axis = 0
new_row = {"Brand":["Tata"], "Year":[2016], "Kms Driven": [32000], "City":["Delhi"], "Mileage":[200]}
df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
print(df)
print()
# concat col
right = pd.DataFrame({"Country": ["China", "China", "USA", "China", "USA", "USA", "USA", "China", "USA"]})
col_concat = pd.concat([df, right], axis=1)
print(col_concat)
print()

# %%
print("###### groupby and aggregate #########")
# group by one condition
group = df.groupby("Brand").groups
print(group)
print()
# group by multiple conditions
group = df.groupby(["Brand", "Year"]).groups
print(group)
print()
# iterate group
for name, group in df.groupby(["Brand", "Year"]):
    print(name)
    print(group)
print()
# get one group
one_group = df.groupby(["Brand", "Year"]).get_group(("Tata", 2016))
print(one_group)
print()
one_group = df.groupby("Brand").get_group("Tata")
print(one_group)
print()
# group and aggregate
group = df.groupby("Brand").agg({
    "Mileage": ["max", "min"],
    "Kms Driven": ["max", "min"],
    })
print(group)
print()
# reset index
group = df.groupby("Brand", as_index=False).agg({
    "Mileage": ["max", "min"],
    "Kms Driven": ["max", "min"],
    })
print(group)
print()
# group to dict
print(dict(list(df.groupby(["Brand", "Year"]))))
print()

# %%
print("###### drop_duplicates #########")
# delete duplicated data
print(df)
print()
duplicated = df.drop_duplicates()
print(duplicated)
print()
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df)
print()

# %%
print("###### apply #########")
# batch column data
df['Detail'] = df.apply(lambda col: col["Brand"]+","+str(col["Year"]), axis=1)
print(df)
print()
df['Choice'] = df.apply(lambda col: "yes" if col["Year"] > 2015 else "No", axis=1)
print(df)
print()
df['Sum'] = df['Sum'].apply(lambda x: x+1)
print(df)
print()

# %%
print("###### map #########")
# convert float to string at Sum column
df['Sum'] = df['Sum'].map('{:.2f}'.format)
print(df)

# %%
print("###### dropna #########")
print(df)
print()
print(df.dropna())
print()
# filter given column
df.dropna(subset=['Sum'], inplace = True)
print(df)
print()


# %%
print("###### misc #########")
# calculate brand count
print(df.Brand.value_counts())
# return row index of max year
print(df.Year.idxmax())
# return max year
print(df.Year.max())
# return accumulation of year
print(df.Year.cumsum())
# return largest 2 year
print(df.Year.nlargest(2))
print(df.loc[df.Year.nlargest(2).index])

# %%
print("###### export or print #########")
df.to_csv('demo.csv', sep=",", index=False, header=True)
print(df.to_string())
print()
print(df.__repr__())
print()
print(df.to_string(
    index      = False,
    justify    = "center",
    formatters = {
        "Brand" : "{:>30s}".format,
        "Mileage" : "{:6,.2f}".format,
    },
))