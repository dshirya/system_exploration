import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# colors here is the list of all the possible colors
def plot_periodic_table(df, highlight_tile=(0, 0), colors=['red', 'blue', 'green']):
    # -1 because the graph looked weird otherwise
    rows = df.shape[0] - 1
    cols = df.shape[1] - 1
    fig, ax = plt.subplots(figsize=(cols, rows))

    for r in range(rows):
        for c in range(cols):
            element_symbol = df.iloc[r, c]
            if pd.notna(element_symbol):
                ax.text(c, rows - 1 - r, element_symbol, va='center', ha='center', fontsize=12)

                # Color logic
                if (r, c) == highlight_tile:
                    width = 1 / len(colors)
                    for i, color in enumerate(colors):
                        ax.add_patch(Rectangle((c - 0.5 + i * width, rows - 1 - r - 0.5), width, 1, color=color, alpha=0.5))
                        
    for r in range(rows + 1):
        ax.axhline(r - 0.5, color='black', linewidth=1)  # Horizontal lines
    for c in range(cols + 1):
        ax.axvline(c - 0.5, color='black', linewidth=1)  # Vertical lines

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.title('Periodic Table')
    plt.grid(False)

    return fig, ax


# Replace this with your Excel file path
excel_file = r"data/periodic_table.xlsx"

df = pd.read_excel(excel_file, sheet_name='Sheet1', engine='openpyxl', header=None)

highlight_tile = (0, 0)
# Edit to the colors you want to split the cell with
highlight_colors = ['red']
highlight_colors.append('blue')
#highlight_colors.append('green')

fig, ax = plot_periodic_table(df, highlight_tile=highlight_tile, colors=highlight_colors)

plt.show()
