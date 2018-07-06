import pandas as pd


def get_df_from_csv(csv_filename):
    return pd.read_csv(csv_filename)


def get_iterable_event_group_list(hits_df):
    single_groups_df = hits_df[['eventID', 'groupID', 'rpID']] \
        .drop_duplicates() \
        .groupby(['eventID', 'groupID']) \
        .size() \
        .reset_index(name='counts')

    single_groups_df = single_groups_df.loc[(single_groups_df['counts'] == 3)]

    event_group_list = []

    for index, row in single_groups_df.iterrows():
        eventID, groupID = row['eventID'], row['groupID']

        event_group_list.append(tuple([eventID, groupID]))

    return event_group_list