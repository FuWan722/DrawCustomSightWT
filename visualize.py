import matplotlib.pyplot as plt
import re

# Function to extract line coordinates from a given line string
def extract_coordinates(line):
    # Regex to find coordinates in the format line:p4 = x1, y1, x2, y2;
    match = re.search(r'line:p4\s*=\s*([\d.-]+),\s*([\d.-]+),\s*([\d.-]+),\s*([\d.-]+)', line)
    if match:
        return float(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4))
    return None

# Function to read and parse the file
def read_lines_from_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            coords = extract_coordinates(line)
            if coords:
                lines.append(coords)
    return lines

# Function to plot the lines
def plot_lines(lines):
    plt.figure(figsize=(10, 6))
    for x1, y1, x2, y2 in lines:
        plt.plot([x1, x2], [y1, y2], color='black')  # Plot each line with markers at ends
    plt.title('Line Visualization')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()  # Invert the Y-axis to flip the image
    plt.show()

# Main function to read the file and visualize lines
def main():
    filename = 'change_this.blk'  # Replace with your file path
    lines = read_lines_from_file(filename)
    plot_lines(lines)

if __name__ == "__main__":
    main()
