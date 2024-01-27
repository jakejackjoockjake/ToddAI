from taipy import Gui
def button_pressed(button):
    """
    Let's do this!
    """
page = """
#Please enter your name
Name: <|{name}|input|>

Hello <|{name}|>! Are you excited to learn?

<|YES|button|on_action=button_pressed>
    
    


"""

Gui(page = page).run(dark_mode=True)