import requests
from bs4 import BeautifulSoup

class recipe_parser:

    def __init__(self):
        self.units = ['centimeter', 'centimeters', 'centimetre', 'centimetres', 'cup', 'can', 'cups', 'fl oz', 'fluid ounce', 'fluid oz', 'g', 'gallon', 'gallons', 'gram', 'inch', 'inches', 'kg', 'kilogram', 'kilograms', 'liter', 'litre', 'mg', 'milligram', 'milliliter', 'millilitre', 'millimeter', 'millimeters', 'millimetre', 'millimetres', 'ounce', 'ounces', 'oz', 'pint', 'pints', 'pound', 'pounds', 'quart', 'quarts', 'tablespoon', 'tablespoons', 'tbsp', 'teaspoon', 'teaspoons', 'tsp']
        self.tools = ['pan', 'bowl', 'baster', 'saucepan', 'knife', 'oven', 'beanpot', 'chip pan', 'cookie sheet', 'cooking pot', 'crepe pan', 'double boiler', 'doufeu', 'dutch oven', 'food processor', 'frying pan', 'skillet', 'griddle', 'karahi', 'kettle', 'pan', 'pressure cooker', 'ramekin', 'roasting pan', 'roasting rack', 'saucepansauciersaute pan', 'splayed saute pan', 'souffle dish', 'springform pan', 'stockpot', 'tajine', 'tube panwok', 'wonder pot', 'pot', 'apple corer', 'apple cutter', 'baster', 'biscuit cutter', 'biscuit press', 'baking dish', 'bread knife', 'browning tray', 'butter curler', 'cake and pie server', 'cheese knife', 'cheesecloth', 'knife', 'cherry pitter', 'chinoise', 'cleaver', 'corkscrew', 'cutting board', 'dough scraper', 'egg poacher', 'egg separator', 'egg slicer', 'egg timer', 'fillet knife', 'fish scaler', 'fish slice', 'flour sifter', 'food mill', 'funnel', 'garlic press', 'grapefruit knife', 'grater', 'gravy strainer', 'ladle', 'lame', 'lemon reamer', 'lemon squeezer', 'mandoline', 'mated colander pot', 'measuring cup', 'measuring spoon', 'grinder', 'tenderiser', 'thermometer', 'melon baller', 'mortar and pestle', 'nutcracker', 'nutmeg grater', 'oven glove', 'blender', 'fryer', 'pastry bush', 'pastry wheel', 'peeler', 'pepper mill', 'pizza cutter', 'masher', 'potato ricer', 'pot-holder', 'rolling pin', 'salt shaker', 'sieve', 'spoon', 'fork', 'spatula', 'spider', 'tin opener', 'tongs', 'whisk', 'wooden spoon', 'zester', 'microwave', 'cylinder', 'Aluminum foil', 'steamer', 'broiler rack', 'grate', 'shallow glass dish', 'wok', 'dish', 'broiler tray', 'slow cooker']
        self.attributes = {}
        self.ingredients = []
        self.directions = []
        self.soup = ''
        self.ratio = ''
        self.transformed_directions = []
        self.transformed_ingredients = []
        self.nutrition = {}
        self.direction_tools = {}
        self.direction_ingre = {}
        self.all_tools_used = []

    def get_recipe(self, recipe_query):
        try:
            query = recipe_query.replace(" ", "-")
            find_recipe = requests.get(f'https://www.allrecipes.com/search?q={query}')
            soup = BeautifulSoup(find_recipe.content, 'html.parser')
            s = soup.find('div', class_='comp search-results__content mntl-block')
            content = s.find_all('a')
            recipe_link = content[0].get('href')
            fetch_recipe = requests.get(recipe_link)
            self.soup = BeautifulSoup(fetch_recipe.content, 'html.parser')
        except Exception as e:
            print('Error fetching the recipe:', e)

    def get_attributes(self):
        try:
            s = self.soup.find('div', class_="comp recipe-details mntl-recipe-details")
            lines = s.find_all('div')
            attributes_temp = lines[0].text.split('\n')
            attributes_raw = [i[:-1].lower() for i in attributes_temp if i != '']
            for a in range(len(attributes_raw) // 2):
                b = 2 * a
                self.attributes[attributes_raw[b]] = attributes_raw[b + 1]
        except Exception as e:
            print('Error parsing recipe attributes:', e)

    def scale_factor(self, servings_query):
        try:
            self.ratio = servings_query / int(self.attributes['servings'])
            return self.ratio
        except Exception as e:
            print('Error calculating scale factor:', e)

    def get_ingredients(self):
        try:
            s = self.soup.find('div', class_='comp mntl-structured-ingredients')
            lines = s.find_all('span')
            ingredients_raw = [line.text for line in lines]
            for a in range(len(ingredients_raw) // 3):
                b = 3 * a
                self.ingredients.append(ingredients_raw[b:b + 3])
            ratios = {'½': '0.5', '⅓': '0.33', '⅔': '0.66', '¼': '0.25', '¾': '0.75', '⅕': '0.2', '⅖': '0.4', '⅗': '0.6',
                      '⅘': '0.8', '⅙': '0.16', '⅚': '0.83', '⅛': '0.125'}
            for i in self.ingredients:
                if i[0] in ratios:
                    i[0] = ratios[i[0]]
                elif len(i[0]) == 3:
                    if i[0].split()[1] in ratios:
                        i[0] = i[0].split()[0] + ratios[i[0].split()[1]]
            return self.ingredients
        except Exception as e:
            print('Error parsing ingredients:', e)

    def get_directions(self):
        try:
            s = self.soup.find('ol', class_="comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup")
            lines = s.find_all('li')
            directions_raw = [line.text.split('.') for line in lines]
            for i in directions_raw:
                for d in i:
                    if d.strip() != '':
                        self.directions.append(d.strip())
            return self.directions
        except Exception as e:
            print('Error parsing directions:', e)

    def scaled_directions(self):
        try:
            local_ratio = {'1/2': '.5', '1/4': '.25', '3/4': '.75', '1/3': '.33', '2/3': '.66', '1/5': '.2', '2/5': '.4',
                           '4/5': '.8', '1/6': '.16', '5/6': '.83', '1/8': '.125', '½': '.5', '⅓': '.33', '⅔': '.66',
                           '¼': '.25', '¾': '.75', '⅕': '.2', '⅖': '.4', '⅗': '.6', '⅘': '.8', '⅙': '.16', '⅚': '.83',
                           '⅛': '.125'}
            local_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            for step in self.directions:
                s = step.split()
                for u in self.units:
                    for a in s:
                        if u == a:
                            x = s.index(a)
                            if s[x - 1] in local_ratio:
                                if s[x - 2] in local_numbers:
                                    z = float(s[x - 2] + local_ratio[s[x - 1]])
                                    s[x - 1] = round(z * self.ratio, 2)
                                    s.pop(x - 2)
                                elif s[x - 2] not in local_numbers:
                                    z = float(local_ratio[s[x - 1]])
                                    s[x - 1] = round(z * self.ratio, 2)
                            if s[x - 1] in local_numbers:
                                z = float(s[x - 1])
                                s[x - 1] = round(z * self.ratio, 2)
                step = " ".join(map(str, s))
                self.transformed_directions.append(step)
            return self.transformed_directions
        except Exception as e:
            print('Error scaling directions:', e)

    def scaled_ingredients(self):
        try:
            self.transformed_ingredients = self.ingredients
            for i in self.transformed_ingredients:
                if i[0] != '':
                    i[0] = round(float(i[0]) * self.scale_factor(), 2)
            return self.transformed_ingredients
        except Exception as e:
            print('Error scaling ingredients:', e)

    def get_nutrition(self):
        try:
            s = self.soup.find('table', class_="mntl-nutrition-facts-summary__table")
            lines = s.find_all('tr')
            for line in lines:
                a = line.text.strip().split('\n')
                self.nutrition[a[1]] = a[0].strip()
            return self.nutrition
        except Exception as e:
            print('Error parsing nutrition:', e)

    def get_tools(self):
        try:
            for step in self.transformed_directions:
                step_tool = [tool for tool in self.tools if tool in step]
                self.direction_tools[step] = list(set(step_tool))
            return self.direction_tools
        except Exception as e:
            print('Error extracting tools used in directions:', e)

    def get_direction_ingre(self):
        try:
            for step in self.transformed_directions:
                step_ing = []
                for ing in self.transformed_ingredients:
                    x = ing[2].split(',')[0].strip()
                    y = ing[1]
                    if x in step:
                        step_ing.append(x)
                self.direction_ingre[step] = list(set(step_ing))
            return self.direction_ingre
        except Exception as e:
            print('Error extracting ingredients used in directions:', e)

    def direction_time(self):
        try:
            dm = {}
            local_ratio = {'1/2': '.5', '1/4': '.25', '3/4': '.75', '1/3': '.33', '2/3': '.66', '1/5': '.2', '2/5': '.4',
                           '4/5': '.8', '1/6': '.16', '5/6': '.83', '1/8': '.125', '½': '.5', '⅓': '.33', '⅔': '.66',
                           '¼': '.25', '¾': '.75', '⅕': '.2', '⅖': '.4', '⅗': '.6', '⅘': '.8', '⅙': '.16', '⅚': '.83',
                           '⅛': '.125'}
            local_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            for step in self.transformed_directions:
                ss = step.split()
                if 'minutes' in ss:
                    dm[step] = [ss[ss.index('minutes') - 1], 'minutes']
                if 'hours' in ss and ss[ss.index('hours') - 1] in local_ratio:
                    if ss[ss.index('hours') - 2] in local_numbers:
                        z = float(ss[ss.index('hours') - 2] + local_ratio[ss[ss.index('hours') - 1]])
                        dm[step] = [z, 'hours']
                    if ss[ss.index('hours') - 2] not in local_numbers:
                        dm[step] = [ss[ss.index('hours') - 1], 'hours']
                if 'hours' not in ss and 'minutes' not in ss:
                    dm[step] = ['', '']
            return dm
        except Exception as e:
            print('Error extracting direction times:', e)

    def tools_used_overall(self):
        try:
            tools_used_all = []
            for tool in self.tools:
                tools_used_all.extend(tool for step in self.transformed_directions if tool in step)
            self.all_tools_used = list(set(tools_used_all))
            return self.all_tools_used
        except Exception as e:
            print('Error extracting all tools used:', e)

# For testing purposes
if __name__ == "__main__":
    rcp = recipe_parser()
    recipe_query = "biryani"
    servings_query = 4
    rcp.get_recipe(recipe_query)
    rcp.get_attributes()
    rcp.scale_factor(servings_query)
    rcp.get_directions()
    rcp.get_ingredients()
    rcp.scaled_ingredients()
    rcp.scaled_directions()
    rcp.get_nutrition()
    rcp.get_tools()
    rcp.get_direction_ingre()
    rcp.direction_time()
    rcp.tools_used_overall()
    # Print or use the parsed recipe data as needed
    print("Attributes:", rcp.attributes)
    print("Scaled Ingredients:", rcp.transformed_ingredients)
