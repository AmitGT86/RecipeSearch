from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from fpdf import FPDF
import time

# Initialize the WebDriver
service = Service(executable_path='users/amitbarua/Downloads/chromedriver/chromedriver')

# Initialize the WebDriver with the updated method
driver = webdriver.Chrome(service=service)

def search_google(query):
    # Open Google
    driver.get("http://www.google.com")
    # Find the search box
    search_box = driver.find_element_by_name('q')
    # Type our query
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for search results to load

def fetch_recipe():
    # Assuming the first result is always the most relevant
    first_result = driver.find_element_by_css_selector('h3')
    first_result.click()
    time.sleep(2)  # Wait for the page to load

    # Now scrape the recipe details
    # Adjust selectors based on the site structure
    recipe_title = driver.find_element_by_tag_name('h1').text
    ingredients = [elem.text for elem in driver.find_elements_by_css_selector('ingredient-selector')]
    instructions = [elem.text for elem in driver.find_elements_by_css_selector('instruction-selector')]

    return recipe_title, ingredients, instructions

def create_pdf(title, ingredients, instructions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True)
    pdf.cell(200, 10, txt="Ingredients", ln=True)
    for ingredient in ingredients:
        pdf.cell(200, 10, txt=ingredient, ln=True)
    pdf.cell(200, 10, txt="Instructions", ln=True)
    for instruction in instructions:
        pdf.cell(200, 10, txt=instruction, ln=True)
    pdf.output("recipe.pdf")

if __name__ == "__main__":
    search_google("most searched recipe of the day")
    recipe_title, ingredients, instructions = fetch_recipe()
    create_pdf(recipe_title, ingredients, instructions)
    driver.close()
