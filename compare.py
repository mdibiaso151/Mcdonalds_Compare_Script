import pandas as pd

# Read in the CSV files and create the dataframes
headers=[   
    "Qid",
    "CVE",
    "Vulnerability",
    "FirstFound",
    "Hostname",
    "Environment",
    "InstanceId",
    "Platform"] 
    

df1 = pd.read_csv('data/1monthback.csv', usecols=headers)
  
df2 = pd.read_csv('data/current_month.csv', usecols=headers)
    



# %%
# Create a new column called 'match_key' in df1 and df2
df1['match_key'] = df1.apply(lambda x: f"{x['Qid']}::{x['InstanceId']}", axis=1)
df2['match_key'] = df2.apply(lambda x: f"{x['Qid']}::{x['InstanceId']}", axis=1)

# %%
def df_diff(df1, df2, which=None):
    """
    Function to find the differences between two dataframes.
    """
    comparison_df = df1.merge(df2, indicator=True, how="outer", on=['match_key'])
    if which is None:
        diff_df = comparison_df
        # diff_df = comparison_df[comparison_df["_merge"] != "both"]
    else:
        diff_df = comparison_df[comparison_df["_merge"] == which]
    return diff_df

# %%
# Find the differences between the two dataframes based on the match_key column
df_difference = df_diff(df1, df2)

# %%
# Select the rows with the value 'left_only' in the _merge column
remediated_df = df_difference[df_difference['_merge'] == 'left_only']
pending_df = df_difference.loc[(df_difference['_merge'] == 'both') | (df_difference['_merge'] == 'right_only')]


# %%
#rename and reformat clean up before writing

remediated_df.columns = remediated_df.columns.str.rstrip("_x")
pending_df.columns = pending_df.columns.str.rstrip("_y")

#remove unwanted columns x and y
headers_new=[   
    "Qid",
    "CVE",
    "Vulnerability",
    "FirstFound",
    "Hostname",
    "Environment",
    "InstanceId",
    "Platform",
    "_merge"]
    
remeadiations=pd.DataFrame(remediated_df,columns=headers_new)
pending=pd.DataFrame(pending_df,columns=headers_new)


# Write the remediated data to a new sheet in an Excel file
with pd.ExcelWriter('data/remediated.xlsx') as writer:
    remeadiations.to_excel(writer, sheet_name='remediated',index=False)
    pending.to_excel(writer, sheet_name='pending',index=False)






