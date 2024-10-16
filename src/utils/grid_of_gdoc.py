
import requests
from bs4 import BeautifulSoup
import sys


def read_table_from_google_docs(url):
    # Retrieves and parses the data in the document
    response = requests.get(url)
    bs = BeautifulSoup(response.content, 'html.parser')
    
    # Find the tag <table> in the HTML document
    table = bs.find('table')
    return table


def parse_cordinate_from_table(table):
    width, height = 0, 0
    char_cordinate = []

    # Drop the header row and get the rest of the rows
    rows = [] if table is None else table.find_all('tr')[1:]      

    # Get characters and (x,y) from each row
    for row in rows:
        # Get the columns in each row
        cols = row.find_all('td')
        if len(cols) == 3:
            x = int(cols[0].text.strip())
            char = cols[1].text.strip()
            y = int(cols[2].text.strip())
            char_cordinate.append((char, x, y))
            width = max(width, x)
            height = max(height, y)
    
    return width, height, char_cordinate

    # Initiate the grid
    # grid = [[' ' for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    # grid = []
    
    # # Fill in the characters and their (x,y) cordinates in the grid
    # for char, x, y in char_cordinate:
    #     grid[y][x] = char
    # return grid


def tranform_to_grid(x_max, y_max, char_cordinate):
    # Initiate the grid
    grid = [[' ' for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    
    # Fill in the characters and their (x,y) cordinates in the grid
    for char, x, y in char_cordinate:
        grid[y][x] = char
    return grid


def print_grid(grid):
    # Print out the grid
    for row in grid:
        print(''.join(row))


# takes in the URL of a Google Doc as an argument,
def parse_grid_from_google_docs(url):

    # Retrieves and parses the data in the document
    table = read_table_from_google_docs(url)

    if table is None:
        print("No table found in the document.")
        sys.exit(1)

    # parse the width, height of the grid and character cordinates from the table
    width, height, char_cordinate = parse_cordinate_from_table(table)
    
    # Transform the characters and their (x,y) cordinates to a grid
    grid = tranform_to_grid(width, height, char_cordinate)
    
    # Print out the grid
    print_grid(grid)


if __name__ == '__main__':
    # url = input("Enter the URL of the Google Doc: ")
    url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
    parse_grid_from_google_docs(url)

# Usage
# sample_url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
# parse_grid_from_google_docs(sample_url)
# print()
# print('*********')
