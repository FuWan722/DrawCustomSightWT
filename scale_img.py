import re

def modify_blk_y_values(input_file, output_file):
    global scale
    """
    Modify the .blk file by making all the y-values (second and fourth values in p4 lines) negative.
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if 'line:p4' in line:
            # Regular expression to match the four numbers in line:p4 = x1, y1, x2, y2
            match = re.search(r'line:p4\s*=\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', line)
            if match:
                x1, y1, x2, y2 = map(float, match.groups())

                modified_line = re.sub(r'line:p4\s*=\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)',
                                       f'line:p4 = {x1*scale:.4f}, {y1*scale:.4f}, {x2*scale:.4f}, {y2*scale:.4f}', line)
                modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    # Write the modified lines to a new file
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)

if __name__ == "__main__":
    #########EDIT THESE VARIBLES#######################
    input_file = "change_this.blk"  # Path to the original .blk file
    output_file = "change_this.blk"  # Path to save the modified .blk file
    scale=1.0 #Scale the custom sight up or down (bigger or smaller compared to the original image) 
    ##########################
    
    modify_blk_y_values(input_file, output_file)
    print(f"Modified .blk file saved to {output_file}")
    
