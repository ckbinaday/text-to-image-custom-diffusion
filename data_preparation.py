import urllib.request
from urllib.parse import urlparse
import pandas as pd
import os
import shutil


def download_images():
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    counter = 0
    for index, row in df_conceptual_12m_tumbler.iterrows():
        try:
            a = urlparse(row['url'])
            filename = os.path.basename(a.path)
            print(filename)
            if not os.path.isfile(dataset_folder + '/' + filename):
                urllib.request.urlretrieve(row['url'], dataset_folder + '/' + filename)
                counter += 1
        except:
            pass

    print('Total Images:', counter)


def create_regularization_dir():
    class_folder = 'tumbler_reg_samples'
    class_data_dir = main_folder + '/' + class_folder
    if not os.path.exists(class_data_dir):
        os.makedirs(class_data_dir)
    if not os.path.exists(f"{class_data_dir}/images/"):
        os.makedirs(f"{class_data_dir}/images/")

    with open(f"{class_data_dir}/caption.txt", "w") as f1, open(f"{class_data_dir}/urls.txt", "w") as f2, open(
            f"{class_data_dir}/images.txt", "w"
    ) as f3:
        total = 0
        for filename in os.listdir(dataset_folder):
            if os.path.isfile(os.path.join(dataset_folder, filename)):
                series_details = df_conceptual_12m_tumbler[df_conceptual_12m_tumbler['url'].str.contains(filename)]
                if not series_details.empty:
                    details = series_details.iloc[0]
                    shutil.copyfile(os.path.join(dataset_folder, filename), f"{class_data_dir}/images/{total}.jpg")
                    f1.write(details["caption"] + "\n")
                    f2.write(details["url"] + "\n")
                    f3.write(f"{class_folder}/images/{total}.jpg" + "\n")
                    total += 1
                else:
                    print('Not Found:', filename)

        print('Total Dataset Count:', total)


if __name__ == '__main__':
    main_folder = 'C:/Users/wizcl/PycharmProjects/download_images'
    # tsv_dataset_link = 'https://storage.googleapis.com/conceptual_12m/cc12m.tsv'
    # urllib.request.urlretrieve(tsv_dataset_link, main_folder + '/cc12m.tsv')

    df_conceptual_12m = pd.read_csv(main_folder + '/cc12m.tsv', sep='\t', names=['url', 'caption'])
    print('TSV Columns:', list(df_conceptual_12m.columns))

    df_conceptual_12m_tumbler = df_conceptual_12m[df_conceptual_12m['caption'].str.contains('tumbler')]
    print('Tumbler Rows:', len(df_conceptual_12m_tumbler))

    dataset_folder = main_folder + '/tumbler_raw_samples'
    # Download Images -> then review images | Raw: 454 -> Reviewed: 130
    # download_images()

    # Create Regularization Images -> after reviewing images | Reviewed: 130 -> Dataset: 199
    create_regularization_dir()
