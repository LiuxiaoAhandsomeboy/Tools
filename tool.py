import streamlit as st
import openpyxl

st.title("Create EOL Mapping")

def get_eol_process():
    wb = openpyxl.load_workbook(excel_file_path)
    sheet = wb[sheet_name]
    result_dict = {}
    for row in sheet.iter_rows():
        if row[column1].value is not None:
            key = row[column1].value
            value = row[column2].value if row[column2].value is not None else None
            result_dict[key] = value
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


def return_eol_process_list(mapping_diag_file_path):
    mapping_diag = {}
    for line in mapping_diag_file_path.getvalue().decode().splitlines():
        if "=> {'Request' =>" in line:
            key_value = line.split('=>')
            mapping_diag[key_value[0].replace("\t","").replace("'","").replace('"','')] = key_value[2].replace("\n", "").replace(",", "").replace("}", "").replace("'", "")
    
    processed_values = []
    for item in result_list:
        c, d = item.split(':')
        d = d.strip()
        found = False
        if not d:
            found = False
        else:
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
            st.markdown( f"        '{index}' => {item},\n")
            selected_supported_steps_in_project.append(str(index))
        else:
            for key, value in supported_all_test_steps.items():
                if value == item:
                    selected_supported_steps_in_project.append(str(key))
                    break
    st.markdown(f"'Selected_SupportedStepsInProject' => {selected_supported_steps_in_project}")



# 上传文件
excel_file_path = st.file_uploader("上传EOL输入文件", type=["xlsx"])
mapping_diag_file_path = st.file_uploader("上传 mapping diag 文件", type=["pm"])

sheet_name = st.text_input("Enter sheet name")
column1 = st.text_input("Enter column1 name")
column2 = st.text_input("Enter column2 name")


if excel_file_path and mapping_diag_file_path and sheet_name and column1 and column2:
    column1 = int(column1)
    column2 = int(column2)
    result_list = get_eol_process()
    result_list = return_eol_process_list(mapping_diag_file_path)
    convert_result_list_to_perl_form(result_list)




      



      
