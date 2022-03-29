import pandas as pd


def get_meta_df():
    """
    Reads run information (SRR...) with age and tissue information
    :return: the meta_df containing the information
    """
    meta_df = pd.read_csv('SRA Extraction/SraRunTable.csv', usecols=['Run', 'Age', 'tissue'])
    # Remove samples that are unknown age (NA)
    meta_df = meta_df[False == meta_df["Age"].str.contains("NA")]
    # Remove the _number part of tissue
    meta_df['tissue'] = [(tissue.split("_")[0]) for tissue in meta_df['tissue']]
    # Change the dtype for columns
    meta_df = meta_df.astype({'Age': 'int32', 'tissue': 'category'})
    return meta_df


def write_tissue_count(tissue, meta_df):
    """
    Given a tissue, generate an Excel file containing samples at each age and their mean and std.
    :param tissue: tissue to count
    :param meta_df: the dataframe that contains the metadata of each sample (age and tissue)
    """
    # Read the quantification data
    quant_df = pd.read_csv('salmon_quants/%s_quant.csv' % tissue)
    quant_df = quant_df.rename(columns={'Unnamed: 0': 'Gene_ID'}) # Change the name of col 1 to Gene_ID
    # Tissue dataframe
    tissue_df = meta_df.loc[meta_df["tissue"] == tissue]
    # For each age, get samples and their mean & std
    ages = [1, 3, 6, 9, 12, 15, 18, 21, 24, 27]
    df_list = []
    for age in ages:
        age_df = tissue_df.loc[tissue_df["Age"] == age]
        srr = age_df.Run.to_list()
        srr.insert(0, 'Gene_ID')
        sub_df = quant_df.loc[:, srr]
        sub_df['mean'] = sub_df.mean(axis=1, numeric_only=True)
        sub_df['std'] = sub_df.std(axis=1, numeric_only=True)
        df_list.append(sub_df)
    # Write to an Excel file
    with pd.ExcelWriter('Tissue_Age_Tables/%s.xlsx' % tissue) as writer:
        for sub_df, age in zip(df_list, ages):
            sub_df.to_excel(writer, index=False, sheet_name='age = %s' % age)


def analyze_all_tissue():
    tissue_list = ['BAT', 'Bone', 'GAT', 'Heart', 'Kidney', 'Limb', 'Liver', 'Lung', 'Marrow', 'Pancreas', 'SCAT',
                   'Skin', 'Small', 'Spleen', 'WBC']
    meta_df = get_meta_df()
    for tissue in tissue_list:
        print('Processing Tissue %s -----------------------------------------------------------' % tissue)
        write_tissue_count(tissue, meta_df)
        print('Finished processing Tissue %s. \n' % tissue)


if __name__ == '__main__':
    analyze_all_tissue()
