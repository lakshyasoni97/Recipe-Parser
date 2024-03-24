recipe_query = input('enter recipe name: ')
servings_query = int(input('enter the number of person you want to cook the recipe for: '))

from old_code.allrecipe_scraper import recipe_parser

try:
    rcp = recipe_parser()
    rcp.get_recipe(recipe_query)
    rcp.get_attributes()
    rcp.scale_factor()
    rcp.get_directions()
    rcp.get_ingredients()
    rcp.scaled_ingredients()
    rcp.scaled_directions()
    rcp.get_nutrition()
    rcp.get_tools()
    rcp.get_direction_ingre()
    rcp.direction_time()
    rcp.tools_used_overall()
except:
    print('Recipe not found, refer web instead: ')
    # print(ddg(recipe_query)[0])