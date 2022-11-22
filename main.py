import pandas as pd
from graphics import *

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

    """# Draw the interface
    Text(Point(1, 3.2), " Message:").draw(win)
    Text(Point(1, 2.8), " Encryption Key:").draw(win)
    Text(Point(1, 1), "Encrypted Message:").draw(win)
    inputText = Entry(Point(2.25, 3.2), 5)
    inputText.setText("hello")
    inputText.draw(win)

    inputKey = Entry(Point(2.25, 2.8), 5)
    inputKey.setText("2")
    inputKey.draw(win)

    outputText = Text(Point(2.25, 1),"")
    outputText.draw(win)
    button = Text(Point(1.5, 2.0), "Encrypt It")
    button.draw(win)
    Rectangle(Point(1, 1.5), Point(2, 2.5)).draw(win)

    # wait for a mouse click
    win.getMouse()

    # convert inputs
    original_message = str(inputText.getText())
    encryption_key = int(inputKey.getText())
    encrypted_message = encryptor(original_message, encryption_key)

    # display output and change button
    outputText.setText(encrypted_message)
    button.setText("Close")"""

    # wait for click and then quit
    win.getMouse()
    win.close()


gui()