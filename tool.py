import pandas as pd
import streamlit as st


def get_eol_process():
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    result_dict = {row[column1]: (row[column2] if pd.notna(row[column2]) else None) for index, row in df.iterrows() if pd.notna(row[column1])}
    result_dict = process_dict_values(result_dict)
    result_list = convert_dict_to_list(result_dict)
    return result_list

def process_dict_values(dictionary):
    processed_dict = {}
    for key, value in dictionary.items():
        if value is not None and type(value) is str:
            hex_values = [x for x in value.split() if len(x) == 2 and all(c in '0123456789ABCDEF' for c in x)]
            processed_dict[key] = ' '.join(hex_values)
        else:
            processed_dict[key]=value
    return processed_dict

def convert_dict_to_list(dictionary):
    return [f"{key}:{value}" for key, value in dictionary.items()]

def return_eol_process_list():
        mapping_diag = {}
        with open(mapping_diag_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "=> {'Request' =>" in line:
                    key_value = line.split('=>')
                    mapping_diag[key_value[0].replace("\t","").replace("'","").replace('"','')] = key_value[2].replace("\n", "").replace(",", "").replace("}", "").replace("'", "")
        
        processed_values = []
        for item in result_list:
            c, d = item.split(':')
            d = d.strip()
            found = False
            for key, value in mapping_diag.items():
                #if value.strip() == d:
                if d in value.strip():
                    processed_values.append(key)
                    found = True
                    break
            if not found:
                if 'Power on ECU' in c:
                    processed_values.append('LC_ECU_On')
                    processed_values.append('WaitTime_8000')
                elif ('Wait' in c or 'wait' in c):
                    processed_values.append('WaitTime_')
                else:
                    processed_values.append(c)
        return processed_values

def convert_result_list_to_perl_form(result_list):
    supported_all_test_steps = {}
    selected_supported_steps_in_project = []
    result_string = ""
    for index, item in enumerate(result_list, start=1):
        if item not in supported_all_test_steps.values():
            supported_all_test_steps[index] = item
            result_string += f"        '{index}' => {item},\n"
        else:
            for key, value in supported_all_test_steps.items():
                if value == item:
                    selected_supported_steps_in_project.append(str(key))
                    break
    result_string += f"'Selected_SupportedStepsInProject' => {selected_supported_steps_in_project}"
    st.write(result_string)



# 上传文件
st.title("Create EOL Mapping")
excel_file_path = st.file_uploader("上传EOL输入文件", type=["xlsx"])
mapping_diag_file_path = st.file_uploader("上传 mapping diag 文件", type=["pm"])

sheet_name = st.text_input("Enter sheet name")
sheet_name = 'EOL'
column1 = 2
column2 = 4


'''
result_list = get_eol_process()
result_list = return_eol_process_list()
convert_result_list_to_perl_form(result_list)
'''



      



      
