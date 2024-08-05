import pandas as pd

def read_excel(file_path):
    data = pd.read_excel(file_path)
    compounds = data[['Formula', 'Entry prototype']].to_dict(orient='records')
    return compounds

def get_element_label_lists(num_elements):
    # Define the appropriate lists of elements based on the structure type
    if num_elements == 2:
        df = pd.read_excel("data/element_labels.xlsx", sheet_name='Binary', engine='openpyxl')
    
        # Assuming the first column is 'Element_A' and the second is 'Element_B'
        A_list = df['Element_A'].dropna().tolist() 
        B_list = df['Element_B'].dropna().tolist()
        
        return A_list, B_list

    if num_elements == 3:
        df = pd.read_excel("data/element_labels.xlsx", sheet_name='Ternary', engine='openpyxl')
        
        R_list = df['Element_R'].dropna().tolist()
        M_list = df['Element_M'].dropna().tolist()
        X_list = df['Element_X'].dropna().tolist()

        return R_list, M_list, X_list

def get_mendeleev_numbers(data):
    data = "data/element_Mendeleev_numbers.xlsx"
    df = pd.read_excel(data, header=None)
    elements = df.iloc[
        :, 0
    ]  # Assuming elements are in the first column
    mendeleev_numbers = df.iloc[
        :, 1
    ]  # Assuming Mendeleev numbers are in the 6th column
    return dict(zip(elements, mendeleev_numbers))