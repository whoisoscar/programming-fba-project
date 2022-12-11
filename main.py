import pandas as pd
from graphics import *

#Test 1
#Testing
#Test 2
def clean_df():
    #Import the data set
    df = pd.read_csv("amazon_co-ecommerce_sample.csv")


    #Remove unwanted variables
    df = df.drop(columns=['uniq_id', 'manufacturer', 'amazon_category_and_sub_category', 'customers_who_bought_this_item_also_bought','product_information','product_description','items_customers_buy_after_viewing_this_item','customer_questions_and_answers','customer_reviews','sellers'])


    print(len(df))
    #Delete rows with blank values
    df = df[(df.price.notnull())]
    df = df[(df.number_available_in_stock.notnull())]
    df = df[(df.number_of_reviews.notnull())]
    df = df[(df.number_of_answered_questions.notnull())]
    df = df[(df.average_review_rating.notnull())]
    #df = df[(df.amazon_category_and_sub_category.notnull())]


    #Strip price variable of any string
    df["price"] = df["price"].str.replace("£","").str.replace(",","").astype(float)

    #Strip number available variable of any string
    df["number_available_in_stock"] = df["number_available_in_stock"].str.replace("\xa0new","").str.replace("\xa0used","").str.replace("\xa0collectible","").str.replace("\xa0refurbished","").astype(int)

    #Strip number of reviews variable of any string
    df["number_of_reviews"] = df["number_of_reviews"].str.replace(",","").astype(int)

    #Convert number of answered questions to integer
    df["number_of_answered_questions"] = df["number_of_answered_questions"].astype(int)

    #Strip average review rating variable of any string
    df["average_review_rating"] = df["average_review_rating"].str.replace(" out of 5 stars","").astype(float)


    #Create new description length variable
    df = df[(df.description.notnull())]

    df["description length"] = df["description"].str.len().astype(int)

    df.drop(columns=['description'])



    #rows before: 10000
    #rows after: 5588

    print(len(df))
    print(df.head())

def interactive(pt, win, box1, box2, box3, box4, box5):
    command = ""
    if pt.getX() > 9 and pt.getX() < 11.5 and pt.getY() > 5.3 and pt.getY() < 6.5:
        print("Update")
        update(win, box1, box2, box3, box4, box5)
    elif pt.getX() > 0 and pt.getX() < 1 and pt.getY() > 0 and pt.getY() < 1:
        print("Quit")
        win.close()
    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 3.9 and pt.getY() < 4.2:
        print("Review")
        box1.setFill("orange")
        command += "Review"
    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 3.2 and pt.getY() < 3.5:
        print("Category")
        box2.setFill("orange")
        command += "Category"
    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 2.5 and pt.getY() < 2.8:
        print("Price")
        box3.setFill("orange")
        command += "Price"
    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 1.8 and pt.getY() < 2.1:
        print("Description")
        box4.setFill("orange")
        command += "Description"
    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 1.1 and pt.getY() < 1.4:
        print("Manufacturer")
        box5.setFill("orange")
        command += "Manufacturer"
    else:
        print("Error")

def update(win, box1, box2, box3, box4, box5):
    boxes = [box1, box2, box3, box4, box5]
    close2 = False
    for i in boxes:
        i.setFill("white")
    while close2 == False:
        print("graph something now")
        pt = win.getMouse()
        interactive(pt, win, box1, box2, box3, box4, box5)


def gui():
    win = GraphWin("Message Encoder", 1200, 700)
    
    win.setCoords(0.0, 0.0, 12.0, 7.0)

    # Draw vertical lines
    Line(Point(1, 0), Point(1, 7)).draw(win)
    Line(Point(2, 0), Point(2, 7)).draw(win)
    Line(Point(3, 0), Point(3, 7)).draw(win)
    Line(Point(4, 0), Point(4, 7)).draw(win)
    Line(Point(5, 0), Point(5, 7)).draw(win)
    Line(Point(6, 0), Point(6, 7)).draw(win)
    Line(Point(7, 0), Point(7, 7)).draw(win)
    Line(Point(8, 0), Point(8, 7)).draw(win)
    Line(Point(9, 0), Point(9, 7)).draw(win)
    Line(Point(10, 0), Point(10, 7)).draw(win)
    Line(Point(11, 0), Point(11, 7)).draw(win)

    # Draw horizontal lines
    Line(Point(0, 1), Point(12, 1)).draw(win)
    Line(Point(0, 2), Point(12, 2)).draw(win)
    Line(Point(0, 3), Point(12, 3)).draw(win)
    Line(Point(0, 4), Point(12, 4)).draw(win)
    Line(Point(0, 5), Point(12, 5)).draw(win)
    Line(Point(0, 6), Point(12, 6)).draw(win)

    #Creating Title
    title = Text(Point(3.3, 6.5), "Amazon Product Finder")
    title.draw(win)
    title.setFace("courier")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("grey")

    #Creating Rectangle where graph will be inserted
    box = Rectangle(Point(1, 1), Point(9, 5)).draw(win)
    box.setFill("white")

    #Creating Variables
    variables = Text(Point(10.5, 5), "Select Variables")
    variables.draw(win)
    variables.setFace("courier")
    variables.setSize(28)
    variables.setStyle("bold")
    variables.setTextColor("grey")
    maximum = Text(Point(10.2, 4.7), "Maximum 3 Variables")
    maximum.draw(win)
    maximum.setFace("courier")
    maximum.setSize(18)
    maximum.setStyle("bold")
    maximum.setTextColor("grey")

    #Creating Boxes for clicking on variables
    box1 = Rectangle(Point(9.2, 3.9), Point(9.5, 4.2)).draw(win)
    box1.setFill("white")
    text1 = Text(Point(10.2, 4.05), "Review")
    text1.draw(win)
    text1.setFace("courier")
    text1.setSize(25)
    text1.setStyle("bold")
    text1.setTextColor("grey")

    box2 = box1.clone()
    box2.move(0, -0.75)
    box2.draw(win)
    text2 = text1.clone()
    text2.move(0.15, -0.75)
    text2.setText("Category")
    text2.draw(win)

    box3 = box2.clone()
    box3.move(0, -0.75)
    box3.draw(win)
    text3 = text2.clone()
    text3.move(-0.2, -0.75)
    text3.setText("Price")
    text3.draw(win)

    box4 = box3.clone()
    box4.move(0, -0.75)
    box4.draw(win)
    text4 = text3.clone()
    text4.move(0.45, -0.7)
    text4.setText("Description")
    text4.draw(win)
    text4_1 = text4.clone()
    text4_1.move(0, -0.2)
    text4_1.setText("Length")
    text4_1.draw(win)

    box5 = box4.clone()
    box5.move(0, -0.7)
    box5.draw(win)
    text5 = text4.clone()
    text5.move(0.1, -0.8)
    text5.setText("Manufacturer")
    text5.draw(win)

    #Creating Update Button
    update = Rectangle(Point(9.2, 5.5), Point(11.5, 6.5)).draw(win)
    update.setFill("orange")
    update_text = Text(Point(10.35, 6), "Update")
    update_text.draw(win)
    update_text.setFace("courier")
    update_text.setSize(25)
    update_text.setStyle("bold")
    update_text.setTextColor("black")

    #Creating Quit Button
    quit = Rectangle(Point(0, 0), Point(0.8, 0.8)).draw(win)
    quit.setFill("grey")
    quit_text = Text(Point(0.4, 0.4), "Quit")
    quit_text.draw(win)
    quit_text.setFace("courier")
    quit_text.setSize(25)
    quit_text.setStyle("bold")
    quit_text.setTextColor("black")

    while True:
        pt = win.getMouse()
        interactive(pt, win, box1, box2, box3, box4, box5)



    #Avoing the program from closing
    win.getMouse()
    win.close()

gui()

