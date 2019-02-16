import csv
import glob
import os


import pandas as pd
import pydicom

from config import config


def make_directory(directory_name):
    """

    :param directory_name: Name of the directory to be created
    :return:
    """
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)


def read_csv_file():
    """

    :return: The file containing the TCGA case list if it exists
    """
    try:
        input_df = pd.read_csv(config['input_csv_path'])
        return input_df
    except FileNotFoundError:
        print ('Input file {} not found'.format(config['input_csv_path']))
        # TODO: Add logger to handle this exception
        return  None


def check_folder_status(input_file):
    """

    :param input_file: The file containing the TCGA case list
    :return:
    """
    with open(os.path.join(config['output_path'], config['output_file_name']), 'w') as csvfile:
        field_names = ['Patient ID', 'Magnetization Strength', 'Scanner Manufacturer', 'Scanner Model',
                   'Echo Time', 'Repetition Time']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for idx, row in input_file.iterrows():
            try:
                folder_name = row[0]
                if not os.path.exists(os.path.join(config['input_file_path'], folder_name)):
                    #TODO: Add the particular folder name to a logger
                    continue
                subfolder_name = os.listdir(os.path.join(config['input_file_path'], folder_name))
                required_folder_names = os.listdir(os.path.join(config['input_file_path'],
                                                                folder_name, subfolder_name[0]))
                dicom_filenames = glob.glob(os.path.join(config['input_file_path'], folder_name,
                                            subfolder_name[0], required_folder_names[0], '*.dcm'))
                ds = pydicom.dcmread(dicom_filenames[0])

                magnetization_value = ds.MagneticFieldStrength
                if magnetization_value>1000:
                # Convert from Gauss to Tesla
                # 10000 Gauss = 1 Tesla
                    magnetization_value /= 10000
                manufacturer_name = ds.Manufacturer
                scanner_model = ds.ManufacturerModelName
                t_r = ds.RepetitionTime
                t_e = ds.EchoTime
                writer.writerow({'Patient ID': folder_name, 'Magnetization Strength':magnetization_value,
                          'Scanner Manufacturer': manufacturer_name, 'Scanner Model':scanner_model,
                           'Echo Time':t_e, 'Repetition Time':t_r})
            except Exception as e:
                print (' Exception {} has occurred'.format(e))

if __name__ == "__main__":

    make_directory(config['output_path'])
    input_dataframe = read_csv_file()
    check_folder_status(input_dataframe)
    print ('Program execution finished.')