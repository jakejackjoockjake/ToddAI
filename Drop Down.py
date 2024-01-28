from taipy import Gui, Core
page = """
Drop Down List:
<|{value}|selector|lov=background; aeroplane; bicycle; bird; boat; bottle; bus; car; cat; chair; cow; diningtable; dog; horse; motorbike; person; pottedplant; sheep;sofa; train; tvmonitor|dropdown|>
Show any of these items and/or a picture of an item on camera and we will tell a story involving the item!
"""
if __name__ == "__main__":
    ################################################################
    #            Instantiate and run Core service                  #
    ################################################################
    Core().run()

    ################################################################
    #            Instantiate and run Gui service                   #
    ################################################################

    Gui(page).run()