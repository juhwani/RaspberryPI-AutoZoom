# Features
# Starting the meeting
# Ending the meeting
# Switching the meeting

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import os
from datetime import datetime
# Initializing Web Driver

class ZoomAutomation:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        try:
            m_options = webdriver.ChromeOptions()
            m_options.binary_location = "/usr/bin/chromium-browser"
            m_options.add_argument("--headless")

            self.driver = webdriver.Chrome(
                options = m_options,
            )
            print("Chrome WebDriver initialized successfully")
            return True
        except:
            print("Failed Chrome WebDriver initialization")
            return False

    def validate_zoom_connection(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'zoom')]"))
            )
            page_title = self.driver.title

            if "Zoom" in page_title:
                print("successfullly connected to Zoom PWA")
                print(f"Page Title: {page_title}")
                print(f"Current URL: {self.driver.current_url}")
            else:
                print("Connected to page but Zoom PWA not confirmed")
                return False
        except:
            print("Error Connecting to Zoom PWA")
            return False



    def start_meeting(self):
        """Start a Zoom meeting"""
        try:
            # Wait for join buttons with improved timeout
            join_buttons = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "button.main__action-btn[aria-label='Join']"
                ))
            )
            
            if join_buttons.is_displayed() and join_buttons.is_enabled():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", join_buttons)
                join_buttons.click()
                return True
        
            
            print(f"Found {len(join_buttons)} Join buttons")
            
            for i, button in enumerate(join_buttons):
                print(f"Button {i + 1}:")
                print(f"- Text: {button.text}")
                print(f"- Class: {button.get_attribute('class')}")
                print(f"- ID: {button.get_attribute('id')}")
                
            return len(join_buttons) > 0
            
        except:
            print("Timeout while waiting for join buttons")
            return False
            
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("WebDriver cleaned up successfully")
            except:
                print(f"Error during cleanup")

def main():
    zoom = ZoomAutomation()
    
    try:
        # Setup driver
        if not zoom.setup_driver():
            print("Failed to set up WebDriver")
            return
            
        # Validate connection
        zoom.validate_zoom_connection()
            
        # Start meeting
        if zoom.start_meeting():
            print("Successfully found join buttons")
        else:
            print("Failed to start meeting")
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        zoom.cleanup()

if __name__ == "__main__":
    main()



# def end_meeting():
# def switch_meeting():
