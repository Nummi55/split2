# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Check if there are any object annotations in the XML
        if len(root.findall('object')) == 0:
            # Negative example (no objects)
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     '',  # Empty class
                     None,  # Empty xmin
                     None,  # Empty ymin
                     None,  # Empty xmax
                     None   # Empty ymax
                     )
            xml_list.append(value)
        else:
            for member in root.findall('object'):
                try:
                    filename = root.find('filename').text
                    width = int(root.find('size')[0].text)
                    height = int(root.find('size')[1].text)
                    class_name = member[0].text if len(member) > 0 else ''
                    xmin = int(member[4][0].text) if len(member[4]) > 0 else None
                    ymin = int(member[4][1].text) if len(member[4]) > 1 else None
                    xmax = int(member[4][2].text) if len(member[4]) > 2 else None
                    ymax = int(member[4][3].text) if len(member[4]) > 3 else None
                    
                    value = (filename, width, height, class_name, xmin, ymin, xmax, ymax)
                    xml_list.append(value)
                except Exception as e:
                    print(f"Error processing file {xml_file}: {str(e)}")

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    for folder in ['train', 'validation']:
        image_path = os.path.join(os.getcwd(), ('images/' + folder))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(('images/' + folder + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')

main()
