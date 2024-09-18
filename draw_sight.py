import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog,simpledialog, messagebox
import tkinter.font as tkfont

header="crosshairHorVertSize:p2=3, 2\nrangefinderProgressBarColor1:c=0, 255, 0, 64\nrangefinderProgressBarColor2:c=255, 255, 255, 64\nrangefinderTextScale:r=0.7\nrangefinderUseThousandth:b=no\nrangefinderVerticalOffset:r=0.1\nrangefinderHorizontalOffset:r=5\ndetectAllyTextScale:r=0.7\ndetectAllyOffset:p2=4, 0.05\nfontSizeMult:r=1\nlineSizeMult:r=1\ndrawCentralLineVert:b=yes\ndrawCentralLineHorz:b=yes\ndrawSightMask:b=yes\ncrosshairColor:c=0, 0, 0, 0\ncrosshairLightColor:c=0, 0, 0, 0\ncrosshairDistHorSizeMain:p2=0.03, 0.02\ncrosshairDistHorSizeAdditional:p2=0.005, 0.003\ndistanceCorrectionPos:p2=-0.26, -0.05\ndrawDistanceCorrection:b=yes\n\ncrosshair_distances{\ndistance:p3=200, 0, 0\ndistance:p3=400, 4, 0\ndistance:p3=600, 0, 0\ndistance:p3=800, 8, 0\ndistance:p3=1000, 0, 0\ndistance:p3=1200, 12, 0\ndistance:p3=1400, 0, 0\ndistance:p3=1600, 16, 0\ndistance:p3=1800, 0, 0\ndistance:p3=2000, 20, 0\ndistance:p3=2200, 0, 0\ndistance:p3=2400, 24, 0\ndistance:p3=2600, 0, 0\ndistance:p3=2800, 28, 0\ndistance:p3=3000, 0, 0\ndistance:p3=3200, 32, 0\ndistance:p3=3400, 0, 0\ndistance:p3=3600, 36, 0\ndistance:p3=3800, 0, 0\ndistance:p3=4000, 40, 0\ndistance:p3=4200, 0, 0\ndistance:p3=4400, 44, 0\ndistance:p3=4600, 0, 0\ndistance:p3=4800, 48, 0\ndistance:p3=5000, 0, 0\ndistance:p3=5200, 52, 0\ndistance:p3=5400, 0, 0\ndistance:p3=5600, 56, 0\ndistance:p3=5800, 0, 0\ndistance:p3=6000, 60, 0\n}\n\ncrosshair_hor_ranges{}\n\nmatchExpClass {\nexp_tank:b = yes\nexp_heavy_tank:b = yes\nexp_tank_destroyer:b = yes\nexp_SPAA:b = yes\n}\n\ndrawLines{\n"


class DrawingApp:
    def __init__(self, image_path='apple.jpeg'):
        self.image = cv2.imread(image_path)
        #if self.image is None:
            #raise ValueError(f"Error: Unable to load image from path '{image_path}'")
        try:
            self.original_image = self.image.copy()
        except:
            pass
        self.drawing = False
        self.start_point = None
        self.lines = []
        self.zoom_scale = 1.0
        self.window_name = "Image"
        self.blk_file_path = 'drawing.blk'  # Default path to save the .blk file
        self.keybinds={
            "Save": "s",
            "Undo": "z",
            "Zoom in": "]",
            "Zoom out": "[",
            "Save and quit": "q"
        }

        # Initialize Tkinter for file dialog
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

                # Ask for the image file path
        self.image_path = self.ask_for_image_path()
        if not self.image_path:
            raise ValueError("No image file selected. Exiting the program.")
        
        # Load the image
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"Error: Unable to load image from path '{self.image_path}'")
        self.original_image = self.image.copy()

        #ask for scale
        self.ask_for_scale()

        # Show keybinds in a persistent window
        self.show_keybinds()

    def ask_for_image_path(self):
        """ Display a file dialog to select the image file. """
        self.root.deiconify()  # Show the root window to enable the dialog
        
        # Open the file dialog to select an image
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", ["*.png","*.jpg","*.jpeg",".bmp"]), ("All Files", "*.*")]
        )
        self.root.withdraw()  # Hide the root window after selection
        return image_path
    
    def ask_for_scale(self):
        # """ Display a pop-up window that asks for a number. """
        # self.root.deiconify()  # Show the root window to enable the pop-up
        img_s=[self.original_image.shape[1],self.original_image.shape[0]]
        rec_s=60
        mul=rec_s/img_s[1]
        proposed_s=[img_s[0]*mul,img_s[1]*mul]
        text="Image has size: "+str(img_s)+"\nEnter a scale multiplier to resize the image.\
                                    \n(It is recommended to have the new size (width and height) below "+str(rec_s)+")\
                                    \nA good number to try: "+str(rec_s/img_s[1])+"     (proposed size: "+str(proposed_s)+")"

        # tk.messagebox.showinfo("",text)  # Show a greeting message

        # # Ask the user to enter a number
        self.scale = simpledialog.askfloat("Input Required", text,initialvalue=mul)
        if self.scale is None:
            raise ValueError("No number was entered. Exiting the program.")

        print(f"Number entered: {self.scale}")
        self.root.withdraw()  # Hide the root window again

    def show_keybinds(self):
        """ Show a persistent window with keybind information. """
        self.keybind_window = tk.Toplevel(self.root)
        self.keybind_window.title("Keybinds")
        self.keybind_window.geometry("300x150")  # Set a size for the window
        keybinds = "Keybinds:\n"

        for key, value in self.keybinds.items():
            keybinds+=(f"{key}: {value}\n")
        
        label = tk.Label(self.keybind_window, text=keybinds, padx=20, pady=20, font=tkfont.Font(family="Helvetica", size=12))
        label.pack(fill=tk.BOTH, expand=True)

        # Ensure the window is on top
        self.keybind_window.lift()
        self.keybind_window.attributes('-topmost', True)

        self.keybind_window.update_idletasks()
        
        # Bind the window close event to ensure it doesn't block the OpenCV window
        self.keybind_window.protocol("WM_DELETE_WINDOW", self.keybind_window.destroy)
        
        # Update keybinds window to make sure it's visible
        self.root.after(100, self.keybind_window.update)

    def zoom_in(self, factor=1.2):
        """ Zoom in by the given factor. """
        self.zoom_scale *= factor
        self.update_display()

    def zoom_out(self, factor=1.2):
        """ Zoom out by the given factor. """
        self.zoom_scale /= factor
        self.update_display()

    def update_display(self):
        """ Update the display with the current zoom scale. """
        zoomed_image = cv2.resize(self.original_image, None, fx=self.zoom_scale, fy=self.zoom_scale, interpolation=cv2.INTER_LINEAR)
        for line in self.lines:
            scaled_line = (
                (int(line[0][0] * self.zoom_scale), int(line[0][1] * self.zoom_scale)),
                (int(line[1][0] * self.zoom_scale), int(line[1][1] * self.zoom_scale))
            )
            cv2.line(zoomed_image, scaled_line[0], scaled_line[1], (0, 255, 0), 2)
        cv2.imshow(self.window_name, zoomed_image)

    def draw_line(self, event, x, y, flags, param):
        """ Handles mouse events to draw lines, accounting for zoom level. """
        # Convert the mouse coordinates to the original image coordinates
        adjusted_x = int(x / self.zoom_scale)
        adjusted_y = int(y / self.zoom_scale)

        if event == cv2.EVENT_LBUTTONDOWN:
            # Store the start point (in original image coordinates)
            self.start_point = (adjusted_x, adjusted_y)
            self.drawing = True

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                # Copy the original image to draw the temporary lines
                temp_image = self.original_image.copy()
                zoomed_temp_image = cv2.resize(temp_image, None, fx=self.zoom_scale, fy=self.zoom_scale, interpolation=cv2.INTER_LINEAR)
                # Redraw all previously drawn lines, scaled based on the current zoom
                for line in self.lines:
                    scaled_line = (
                        (int(line[0][0] * self.zoom_scale), int(line[0][1] * self.zoom_scale)),
                        (int(line[1][0] * self.zoom_scale), int(line[1][1] * self.zoom_scale))
                    )
                    cv2.line(zoomed_temp_image, scaled_line[0], scaled_line[1], (0, 255, 0), 2)
                    
                # Draw the current dynamic line (scaled correctly for zoom)
                end_point = (adjusted_x, adjusted_y)
                cv2.line(temp_image, self.start_point, end_point, (0, 255, 0), 2)
                preview_line=(
                        (int(self.start_point[0] * self.zoom_scale), int(self.start_point[1] * self.zoom_scale)),
                        #(int(end_point[0]), int(end_point[1]))
                        (int(x),int(y))
                )
                cv2.line(zoomed_temp_image,preview_line[0],preview_line[1],(0,255,0),2)
                # Zoom the temporary image before displaying

                cv2.imshow(self.window_name, zoomed_temp_image)
        elif event == cv2.EVENT_LBUTTONUP:
            if self.drawing:
                # Finalize the line and add it to the list of lines
                end_point = (adjusted_x, adjusted_y)
                self.lines.append((self.start_point, end_point))
                self.drawing = False

                # Update the display with the finalized line
                self.update_display()



    def undo_last_line(self):
        """ Remove the last drawn line. """
        if self.lines:
            self.lines.pop()
            self.update_display()

    def save_to_blk(self):
        img_s=[self.original_image.shape[1],self.original_image.shape[0]]
        """ Open a file dialog to save the drawn lines to a .blk file. """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".blk",
            filetypes=[("BLK files", "*.blk"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as file:
                file.write(header)  # Begin War Thunder .blk file structure
                for line in self.lines:
                    x1, y1 = line[0]
                    x2, y2 = line[1]
                    y1=y1-img_s[1]
                    y2=y2-img_s[1]
                    file.write(f"\tline{{ line:p4 = {x1*self.scale:.4f}, {y1*self.scale:.4f}, {x2*self.scale:.4f}, {y2*self.scale:.4f};  "
                               f"radialMoveSpeed:r = 0.0;  thousandth:b = Yes;  move:b = No;  "
                               f"moveRadial:b = No;  radialCenter:p2 = 0, 0; }}\n")
                file.write("}\n")  # End War Thunder .blk file structure
            print(f"Drawing successfully saved to {file_path}")

    def run(self):
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.draw_line)
        self.update_display()
        #messagebox.showinfo("Hello", "Hello!")


        # Use Tkinter's after() to repeatedly check for key presses
        def check_keypress():
            key = cv2.waitKey(1)
            if key == ord(self.keybinds.get('Save and quit')):
                self.save_to_blk()
                cv2.destroyAllWindows()
                self.keybind_window.destroy()  # Close the Tkinter window too
            elif key == ord(self.keybinds.get('Zoom in')):
                self.zoom_in()
            elif key == ord(self.keybinds.get('Zoom out')):
                self.zoom_out()
            elif key == ord(self.keybinds.get('Undo')):
                self.undo_last_line()
            elif key == ord(self.keybinds.get('Save')):
                self.save_to_blk()
                
                # Re-run the function after a short delay
            self.root.after(10, check_keypress)

        # Start the keypress check loop
        self.root.after(10, check_keypress)
        self.root.mainloop()  # Start Tkinter's main event loop
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = DrawingApp()
    app.run()