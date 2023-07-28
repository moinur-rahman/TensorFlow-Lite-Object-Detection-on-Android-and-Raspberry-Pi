# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            bndbox = member.find('bndbox')
            value = (root.find('filename').text,
                     int(root.find('size').find('width').text),
                     int(root.find('size').find('height').text),
                     member.find('name').text,
                     int(bndbox.find('xmin').text),
                     int(bndbox.find('ymin').text),
                     int(bndbox.find('xmax').text),
                     int(bndbox.find('ymax').text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main(image_path):
    for folder in ['train','validation']:
        xml_df = xml_to_csv(os.path.join(image_path, folder))
        xml_df.to_csv(os.path.join(image_path, f'{folder}_labels.csv'), index=None)
        print('Successfully converted xml to csv.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='XML to CSV converter')
    parser.add_argument('--image_path', help='Path to the image directory')
    args = parser.parse_args()

    main(args.image_path)
