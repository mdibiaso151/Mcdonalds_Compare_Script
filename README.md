# Mcdonalds_Compare_Script

This code reads in two CSV files, data/1monthback.csv and data/current_month.csv, and creates two dataframes, df1 and df2.

It then creates a new column called match_key in both dataframes using the Qid and InstanceId columns.

The code defines a function, df_diff, which compares the two dataframes based on the match_key column and returns a new dataframe containing the differences between them.

The differences between df1 and df2 are then calculated using the df_diff function and stored in a dataframe called df_difference.

Two new dataframes, remediated_df and pending_df, are created from df_difference, containing rows with the values 'left_only' and 'both' or 'right_only' in the _merge column, respectively.

The columns in remediated_df and pending_df are then renamed and unwanted columns are removed. The resulting dataframes are stored as remediations and pending, respectively.

Finally, remediations and pending are written to a new Excel file called data/remediated.xlsx, with separate sheets for each dataframe.
