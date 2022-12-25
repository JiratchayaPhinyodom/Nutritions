import pandas as pd


class Menu:

    """class Menu that get the all of name food in the file csv."""

    def __init__(self):
        self.nutrition = pd.read_csv('nutritions.csv')

    def get(self):
        list_name_food = []
        name_food = self.nutrition['ShortDescrip']
        for i in range(len(name_food)):
            list_name_food.append(name_food[i])
        return list_name_food

class Usrda:

    """class Usrda that get the type of food are the usrda."""

    def __init__(self):
        self.nutrition = pd.read_csv('nutritions.csv')

    def get(self):
        self.list_usrda_col = []
        nutrition_usrda = self.nutrition.drop(columns=['ID', 'FoodGroup', 'ShortDescrip', 'Descrip', 'CommonName',
                                                       'MfgName', 'ScientificName', 'Energy_kcal', 'Protein_g', 'Fat_g',
                                                       'Carb_g', 'Sugar_g', 'Fiber_g', 'VitA_mcg', 'VitB6_mg',
                                                       'VitB12_mcg', 'VitC_mg', 'VitE_mg', 'Folate_mcg', 'Niacin_mg',
                                                       'Riboflavin_mg', 'Thiamin_mg', 'Calcium_mg', 'Copper_mcg',
                                                       'Iron_mg', 'Magnesium_mg', 'Manganese_mg', 'Phosphorus_mg',
                                                       'Selenium_mcg', 'Zinc_mg'])
        col_nutrition_usrda = nutrition_usrda.columns
        for i in range(len(col_nutrition_usrda)):
            self.list_usrda_col.append(col_nutrition_usrda[i])
        return self.list_usrda_col

class Combobox:

    """class Combobox that get the all columns od the nutrition."""

    def __init__(self):
        self.nutrition = pd.read_csv('nutritions.csv')

    def get(self):
        self.list_choice_combobox = []
        choice_combobox = self.nutrition.drop(columns=['ID', 'FoodGroup', 'ShortDescrip', 'Descrip', 'CommonName',
                                                       'MfgName', 'ScientificName'])
        col_choice_combobox = choice_combobox.columns
        for i in range(len(col_choice_combobox)):
            self.list_choice_combobox.append(col_choice_combobox[i])
        return self.list_choice_combobox

class Rank:

    """class Rank that will get the top 10 of each nutrition."""

    def __init__(self):
        self.nutrition = pd.read_csv('nutritions.csv')

    def get_value(self, rows, select_combobox):
        if rows == 'ShortDescrip':
            self.nutrition_largest_name = self.nutrition.nlargest(n=10, columns=[select_combobox], keep='all')
            list_shortdescrip = []
            for short_descrip in self.nutrition_largest_name.ShortDescrip[0:10]:
                list_shortdescrip.append(short_descrip)
            return list_shortdescrip
        if rows == select_combobox:
            self.nutrition_largest_value = self.nutrition[select_combobox].nlargest(n=10)
            list_combobox_value = []
            for combobox_value in self.nutrition_largest_value:
                list_combobox_value.append(combobox_value)
            return list_combobox_value

class UsrdaValue:

    """class UsrdaValue get the value usrda of each food."""

    def __init__(self):
        self.nutrition = pd.read_csv('nutritions.csv')
        self.list_usrda_col = Usrda().get()

    def get_value(self, usrd_value):
        list_value = []
        data = self.nutrition.loc[self.nutrition.ShortDescrip.isin([usrd_value])]
        for i in range(len(self.list_usrda_col)):
            list_value.append(data.loc[data.index[0], self.list_usrda_col[i]])
        return list_value

class CompareValue:

    """class CompareValue get the value of 2 food."""

    def __init__(self):
        self.nutrition = pd.read_csv('nutritions.csv')
        self.list_choice_combobox = Combobox().get()

    def get_value(self, col_compare, name_food1, name_food2):
        list_compare_value = []
        data1 = self.nutrition.loc[self.nutrition.ShortDescrip.isin([name_food1])]
        data2 = self.nutrition.loc[self.nutrition.ShortDescrip.isin([name_food2])]
        for i in range(len(self.list_choice_combobox)):
            if self.list_choice_combobox[i] == col_compare:
                list_compare_value.append(data1.loc[data1.index[0], self.list_choice_combobox[i]])
                list_compare_value.append(data2.loc[data2.index[0], self.list_choice_combobox[i]])
            else:
                pass
        return list_compare_value

def Get(choice):
    """The design patterns function."""
    gets = {
        "Menu": Menu,
        "Usrd": Usrda,
        "Combobox": Combobox
    }

    return gets[choice]()

def Get_Value(choice):
    """The design patterns function."""
    get_values = {
        "Usrd_Value": UsrdaValue,
        "Compare_Value": CompareValue,
        "Rank": Rank
    }

    return get_values[choice]()