import tkinter as tk
from tkinter import filedialog
import pyautogui
from datetime import datetime
import os
import pytesseract
from PIL import Image, ImageFilter
import requests
import re
from pynput import mouse

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot & OCR App")
        self.image_path = ''
        self.question = ''
        self.answer = 0

        # Create GUI elements
        self.screenshot_button = tk.Button(root, text="Capture Screenshot", command=self.start_capture)
        self.screenshot_button.pack(pady=10)
        
        self.result_label = tk.Label(root, text="Extracted Text:")
        self.result_label.pack(pady=10)
        
        self.extracted_text = tk.Text(root, height=5, width=50)
        self.extracted_text.pack(pady=10)

        self.answer_label = tk.Label(root, text="Answer from API:")
        self.answer_label.pack(pady=10)

        self.answer_value = tk.Label(root, text="Waiting for input...")
        self.answer_value.pack(pady=10)
        
        self.move_button = tk.Button(root, text="Move Mouse", command=self.move_mouse_action)
        self.move_button.pack(pady=10)

    def start_capture(self):
        # Get the four corner coordinates by clicking
        x1, y1, x2, y2, x3, y3, x4, y4 = self.capture_clicks_for_corners()
        
        # Take the snippet screenshot using the selected corners
        self.take_screenshot_corners(x1, y1, x2, y2, x3, y3, x4, y4)
        
        # Extract the text and update the text box
        self.extract_text_from_image(self.image_path)
        
        # Fetch and print the output, also update the label
        self.fetch_and_print_output()

    # Other methods are similar to your original functions

    def take_screenshot_corners(self, x1, y1, x2, y2, x3, y3, x4, y4):
        width = abs(x2 - x1)
        height = abs(y3 - y1)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        file_path = os.path.join("screenshots", f'screenshot_snippet_{timestamp}.png')
        screenshot.save(file_path)
        self.image_path = file_path

    def extract_text_from_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.convert('L').filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(img)
            clean_text = re.sub(r'\s+', ' ', text.strip())
            self.extracted_text.delete('1.0', tk.END)
            self.extracted_text.insert(tk.END, clean_text)
            self.question = clean_text
        except Exception as e:
            print(f"Error: {e}")

    def fetch_and_print_output(self):
        url = f"https://5nshirxic4.execute-api.us-east-1.amazonaws.com/stage1?history={requests.utils.quote(self.question)}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_data = response.json()
                message = response_data.get('body', '')
                match = re.search(r'\{\((\d)\)\}', message)
                if match:
                    self.answer = int(match.group(1))
                    self.answer_value.config(text=f"Answer: {self.answer}")
                else:
                    self.answer_value.config(text="No answer found.")
            else:
                self.answer_value.config(text="Failed to fetch answer.")
        except requests.RequestException as e:
            self.answer_value.config(text=f"Error: {e}")

    def move_mouse_action(self):
        self.move_mouse(self.answer)

    def capture_clicks_for_corners(self):
        print("Click on the screen to select the corners for the screenshot.")
        x1, y1 = self.wait_and_click("Top-left corner")
        x2, y2 = self.wait_and_click("Top-right corner")
        x3, y3 = self.wait_and_click("Bottom-left corner")
        x4, y4 = self.wait_and_click("Bottom-right corner")
        return x1, y1, x2, y2, x3, y3, x4, y4

    def wait_and_click(self, message):
        	# Function to wait for a manual click using pynput
        def wait_for_manual_click():
            print("Waiting for your manual click...")
            click_position = [None]  # To store the click position

		# This function is called when a mouse click is detected
            def on_click(x, y, button, pressed):
                if pressed and button == mouse.Button.left:
                    click_position[0] = (x, y)
                    return False  # Stop listener after the first click
		
		# Listen for the mouse click
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()

            return click_position[0]
        print(f"Click to select the {message}...")
        return wait_for_manual_click()  # Reuse your existing wait_for_manual_click logic

    def move_mouse(self, number):
        current_x, current_y = pyautogui.position()
        if number == 1:
            pyautogui.moveTo(current_x - 100, current_y - 100, duration=3)
        elif number == 2:
            pyautogui.moveTo(current_x + 100, current_y - 100, duration=3)
        elif number == 3:
            pyautogui.moveTo(current_x - 100, current_y + 100, duration=3)
        elif number == 4:
            pyautogui.moveTo(current_x + 100, current_y + 100, duration=3)

# Start the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
