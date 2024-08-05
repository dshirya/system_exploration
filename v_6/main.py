import os
import click
from util.excel import read_excel
from util.parser import separate_formulas
from util.sort import sort_formulas
from util.plot import process_formulas

PERIODIC_TABLE_FILE = 'data/periodic_table.xlsx'
CURRENT_DIR = os.path.dirname(__file__)

@click.command()
@click.option('--directory', default=CURRENT_DIR, type=click.Path(exists=True), help='Directory to look for Excel files.')
def main(directory):
    """
    This script processes compounds from an Excel file and generates periodic table plots.
    """
    excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]
    if not excel_files:
        click.echo('No Excel files found in the specified directory.')
        return

    file_choices = {str(index + 1): file for index, file in enumerate(excel_files)}
    
    for index, file in file_choices.items():
        click.echo(f"{index}. {file}")

    choice = click.prompt('Please select the number of the file you want to process', type=click.Choice(file_choices.keys()))
    compounds_file = os.path.join(directory, file_choices[choice])

    compounds = read_excel(compounds_file)
    binary_formulas, ternary_formulas, _ = separate_formulas(compounds)

    sorted_binary_formulas = sort_formulas(binary_formulas)
    sorted_ternary_formulas = sort_formulas(ternary_formulas)

    process_formulas(sorted_binary_formulas, sorted_ternary_formulas, periodic_table_file=PERIODIC_TABLE_FILE)

if __name__ == '__main__':
    main()