import os
import xml.etree.ElementTree as ET

def convert_xml_to_yolo(xml_folder, txt_folder, class_map):
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)
    
    for xml_file in os.listdir(xml_folder):
        if not xml_file.endswith('.xml'):
            continue
        
        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        image_width = int(root.find('size/width').text)
        image_height = int(root.find('size/height').text)
        
        txt_file = os.path.join(txt_folder, os.path.splitext(xml_file)[0] + '.txt')
        
        with open(txt_file, 'w') as f:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in class_map:
                    continue
                
                class_num = class_map[class_name]
                
                bbox = obj.find('bndbox')
                xmin = float(bbox.find('xmin').text)
                ymin = float(bbox.find('ymin').text)
                xmax = float(bbox.find('xmax').text)
                ymax = float(bbox.find('ymax').text)
                
                x_center = (xmin + xmax) / 2 / image_width
                y_center = (ymin + ymax) / 2 / image_height
                width = (xmax - xmin) / image_width
                height = (ymax - ymin) / image_height
                
                f.write(f"{class_num} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")



# Example class map
class_map = {
    "with_mask": 0,
    "without_mask": 1,
    "mask_weared_incorrect": 2,
    "others": 3
}

# Paths to the folders containing XML files and where to save TXT files
xml_folder = 'archive/annotations'
txt_folder = 'annotations'

convert_xml_to_yolo(xml_folder, txt_folder, class_map)
