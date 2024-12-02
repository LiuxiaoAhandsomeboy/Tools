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
            value = row[column2].value.replace('$','').replace('0x', '').replace('0X', '') if row[column2].value is not None else None
            result_dict[key] = value
    result_dict = process_dict_values(result_dict)
    result_list = convert_dict_to_list(result_dict)
    return result_list
    
def find_value(s):
    for i in s.split('\n'):
        if 'Send' in i:
            return i

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
column1 = st.text_input("Enter column of diag step")
column2 = st.text_input("Enter column of diag request")


if excel_file_path and mapping_diag_file_path and sheet_name and column1 and column2:
    column1 = int(column1)
    column2 = int(column2)
    result_list = ['进入扩展模式\n\nStart Diagnostic Extented\nSession:10 03', '安全认证\nSecurity Access:27 01', '读取软件件号\nRead SW Number:22 F1 88', '写入VIN\nWrite VIN: 2E F1 90', '写入ECU安装日期\nWrite ECUInstallationDate:2E F1 9D', '写入回路配置参数\nWrite ECU Configuration:2E FA 00', '写入整车配置参数\nWrite Vehicle Configuration:2E F1 97',  '写入CAN报文参数\nWrite CAN configuration:2E FB 00', 'IDF功能配置\nWrite IDF configuration:2E FC 00', '等待\nWait:', '复位\nRe set:11 03', '等待ECU初始化\nWait for ECU Initialization:', '读回路配置参数\nRead ECU Configuration:22 FA 00', '读CAN报文参数\nRead CAN configuration:22 FB 00', '读IDF功能配置\nRead IDF configuration:22 FC 00', '读整车配置参数\nRead Vehicle Configuration:22 F1 97', '读最终配置参数\nRead real ECU Configuration:22 F1 98', '读故障码\nRead Fault Memory:19 02 01', '进入扩展模式\nStart Diagnostic Extented Session:10 03', '使能ECU点火功能\nEnable Fire:2E FA 0F', '复位\nSoft Reset:11 03 ', '清除故障码\nClear DTCs:14 FF FF FF', '读故障码\nRead DTC\n:19 02 09', '读使能点火状态\nRead Enable Firing of ECU:22 FA 0F ', 'power off:', '结束\nEnd:None']
    result_list = return_eol_process_list(mapping_diag_file_path)
    convert_result_list_to_perl_form(result_list)




      



      
