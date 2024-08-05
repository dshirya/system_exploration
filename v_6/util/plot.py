import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Define color mapping
COLOR_MAP = {
    'clover': (2, 118, 8),
    'sangre': (195, 18, 30),
    'neptune': (3, 72, 161),
    'pumpkin': (255, 176, 28),
    'cerulean': (29, 172, 214),
    'cocoa': (156, 83, 0),
    'amethyst': (153, 102, 204),
    'orange red': (255, 69, 0)
}

# Convert colors to normalized RGB tuples
COLOR_MAP_NORM = {name: (r/255, g/255, b/255) for name, (r, g, b) in COLOR_MAP.items()}

def plot_periodic_table(df, highlights, title, common_element=None):
    """
    Plot the periodic table with highlighted elements.
    
    Parameters:
    - df: DataFrame containing the periodic table layout.
    - highlights: Dictionary of elements to highlight with their corresponding colors.
    - title: Title of the plot.
    - common_element: Element to display as the common element.
    """
    rows = df.shape[0]
    cols = df.shape[1]
    fig, ax = plt.subplots(figsize=(cols, rows))

    for r in range(rows):
        for c in range(cols):
            element_symbol = df.iloc[r, c]
            if pd.notna(element_symbol):
                ax.text(c, rows - 1 - r, element_symbol, va='center', ha='center', fontsize=12)

                if element_symbol in highlights:
                    colors = highlights[element_symbol]
                    width = 1 / len(colors)
                    for i, color in enumerate(colors):
                        ax.add_patch(Rectangle(
                            (c - 0.5 + i * width, rows - 1 - r - 0.5),
                            width, 1, 
                            color=COLOR_MAP_NORM[color], 
                            alpha=0.5
                        ))

    for r in range(rows + 1):
        ax.axhline(r - 0.5, color='black', linewidth=1)
    for c in range(cols + 1):
        ax.axvline(c - 0.5, color='black', linewidth=1)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    

#title it 


    plt.title(title)
    plt.grid(False)

    if common_element:
        plt.text(3, -1, f'Common element - {common_element}', fontsize=18, ha='left', va='center')

    return fig, ax

def create_periodic_table_plot(file_path, highlights, title, common_element=None):
    """
    Create a periodic table plot from the Excel data.
    
    Parameters:
    - file_path: Path to the Excel file containing the periodic table layout.
    - highlights: Dictionary of elements to highlight with their corresponding colors.
    - title: Title of the plot.
    - common_element: Element to display as the common element.
    """
    df = pd.read_excel(file_path, header=None)
    fig, ax = plot_periodic_table(df, highlights, title, common_element)
    return fig, ax

def save_plot(entry_prototype, highlights, periodic_table_file, common_element=None):
    """
    Save the plot to a PNG file.
    
    Parameters:
    - entry_prototype: Name of the entry prototype.
    - highlights: Dictionary of elements to highlight with their corresponding colors.
    - periodic_table_file: Path to the periodic table Excel file.
    - common_element: Element to display as the common element.
    """
    folder_name = entry_prototype
    os.makedirs(folder_name, exist_ok=True)
    file_name = f"{folder_name}/{entry_prototype}-{common_element}.png"
    fig, ax = create_periodic_table_plot(periodic_table_file, highlights, entry_prototype, common_element)
    fig.savefig(file_name)
    plt.close(fig)

def process_formulas(binary_formulas, ternary_formulas, periodic_table_file):
    """
    Process the binary and ternary formulas, generate highlights, and save plots.
    
    Parameters:
    - binary_formulas: List of binary formulas to process.
    - ternary_formulas: List of ternary formulas to process.
    - periodic_table_file: Path to the periodic table Excel file.
    """
    grouped_binary_formulas = group_by_entry_prototype(binary_formulas)
    grouped_ternary_formulas = group_by_entry_prototype(ternary_formulas)

    for entry_prototype, grouped in grouped_binary_formulas.items():
        print(f"\nProcessing {entry_prototype} for binary formulas:")
        highlights, common_element = get_highlights_binary(grouped)
        print("Highlights:", highlights)
        save_plot(entry_prototype, highlights, periodic_table_file, common_element)

    for entry_prototype, grouped in grouped_ternary_formulas.items():
        print(f"\nProcessing {entry_prototype} for ternary formulas:")
        highlights, common_element = get_highlights_ternary(grouped)
        print("Highlights:", highlights)
        save_plot(entry_prototype, highlights, periodic_table_file, common_element)

def group_by_entry_prototype(formulas):
    """
    Group formulas by their entry prototype.
    
    Parameters:
    - formulas: List of formulas to group.
    
    Returns:
    Dictionary grouped by entry prototype.
    """
    grouped = {}
    for formula, entry_prototype, sorted_formula in formulas:
        if entry_prototype not in grouped:
            grouped[entry_prototype] = []
        grouped[entry_prototype].append((formula, sorted_formula))
    return grouped

def get_highlights_binary(grouped):
    """
    Generate the highlights dictionary for binary compounds.
    
    Parameters:
    - grouped: Grouped binary formulas by entry prototype.
    
    Returns:
    Tuple containing highlights dictionary and common element.
    """
    highlights = {}
    element_colors = {}
    color_idx = 0
    common_element = None

    color_keys = list(COLOR_MAP.keys())
    
    for _, sorted_formula in grouped:
        main_element = sorted_formula[0][0]
        secondary_element = sorted_formula[1][0]

        if main_element not in element_colors:
            element_colors[main_element] = color_keys[color_idx % len(COLOR_MAP)]
            color_idx += 1

        if main_element not in highlights:
            highlights[main_element] = [element_colors[main_element]]

        if secondary_element not in element_colors:
            element_colors[secondary_element] = element_colors[main_element]
        else:
            if element_colors[main_element] not in highlights[secondary_element]:
                highlights[secondary_element].append(element_colors[main_element])

        if secondary_element not in highlights:
            highlights[secondary_element] = [element_colors[secondary_element]]
        elif element_colors[main_element] not in highlights[secondary_element]:
            highlights[secondary_element].append(element_colors[main_element])

    common_element = list(element_colors.keys())[0] if element_colors else None
    print ('Binary: ' + common_element)
    return highlights, common_element

def get_highlights_ternary(grouped):
    """
    Generate the highlights dictionary for ternary compounds.
    
    Parameters:
    - grouped: Grouped ternary formulas by entry prototype.
    
    Returns:
    Tuple containing highlights dictionary and common element.
    """
    highlights = {}
    element_colors = {}
    color_idx = 0
    common_element = None

    color_keys = list(COLOR_MAP.keys())

    for _, sorted_formula in grouped:
        first_element = sorted_formula[0][0]  # First element in ternary formula
        main_element = sorted_formula[1][0]  # Second element in ternary formula
        third_element = sorted_formula[2][0]  # Third element in ternary formula
        
        # Assign color to main element if not already assigned
        if main_element not in element_colors:
            element_colors[main_element] = []
        
        if not element_colors[main_element]:
            element_colors[main_element].append(color_keys[color_idx % len(COLOR_MAP)])
            color_idx += 1

        if main_element not in highlights:
            highlights[main_element] = element_colors[main_element]
        
        # Assign color to third element if not already assigned
        if third_element not in element_colors:
            element_colors[third_element] = [color_keys[color_idx % len(COLOR_MAP)]]
            color_idx += 1

        if third_element not in highlights:
            highlights[third_element] = element_colors[third_element]
        else:
            if element_colors[third_element][0] not in highlights[third_element]:
                highlights[third_element].append(element_colors[third_element][0])

        # Assign the same color to the first element as the third element
        if first_element not in highlights:
            highlights[first_element] = element_colors[third_element]
        elif element_colors[third_element][0] not in highlights[first_element]:
            highlights[first_element].append(element_colors[third_element][0])

        # Handle case for more than one third element
        for additional_third_element in sorted_formula[2:]:
            if additional_third_element[0] not in element_colors:
                element_colors[additional_third_element[0]] = [color_keys[color_idx % len(COLOR_MAP)]]
                color_idx += 1

            if additional_third_element[0] not in highlights:
                highlights[additional_third_element[0]] = element_colors[additional_third_element[0]]
            else:
                if element_colors[additional_third_element[0]][0] not in highlights[additional_third_element[0]]:
                    highlights[additional_third_element[0]].append(element_colors[additional_third_element[0]][0])

            if first_element not in highlights:
                highlights[first_element] = element_colors[additional_third_element[0]]
            elif element_colors[additional_third_element[0]][0] not in highlights[first_element]:
                highlights[first_element].append(element_colors[additional_third_element[0]][0])

            if element_colors[additional_third_element[0]][0] not in element_colors[main_element]:
                element_colors[main_element].append(element_colors[additional_third_element[0]][0])

    common_element = list(element_colors.keys())[0] if element_colors else None
    print ('Ternary: ' + common_element)
    return highlights, common_element