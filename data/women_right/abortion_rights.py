import pandas as pd

# Data for state-wise abortion laws
abortion_laws_data = {
    'State': ['Alabama', 'Arkansas', 'Idaho', 'Indiana', 'California', 'Texas', 'Florida', 'Colorado'],
    'Abortion Law Type': ['Total Ban', 'Total Ban', 'Total Ban', 'Total Ban', 'No Restrictions', 'Gestational Limit', 'Gestational Limit', 'No Restrictions'],
    'Specifics': [
        'Abortion is banned in almost all circumstances.',
        'Abortion is banned in almost all circumstances.',
        'Abortion is banned in almost all circumstances.',
        'Abortion is banned in almost all circumstances.',
        'No gestational limits.',
        'Abortion banned after 6 weeks.',
        'Abortion banned after 15 weeks.',
        'Legal with no gestational limit.'
    ],
    'Effective Date': ['2022', '2021', '2023', '2023', 'N/A', '2021', '2023', 'N/A'],
    'Source': [
        'Guttmacher Institute',
        'Guttmacher Institute',
        'New York Times',
        'New York Times',
        'LawAtlas',
        'Statista',
        'Statista',
        'LawAtlas'
    ]
}

# Create DataFrame
abortion_laws_df = pd.DataFrame(abortion_laws_data)

# Save to CSV
csv_file_path = 'state_wise_abortion_laws_2024.csv'
abortion_laws_df.to_csv(csv_file_path, index=False)

csv_file_path
