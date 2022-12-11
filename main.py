import pandas as pd
from graphics import *
import matplotlib.pyplot as plt
from tkinter import filedialog

def clean_df(file_path):
    #Import the data set
    df = pd.read_csv(file_path)
    og_len = len(df)

    #Remove unwanted variables
    df = df.drop(columns=['uniq_id', 'manufacturer', 'customers_who_bought_this_item_also_bought','product_information','product_description','items_customers_buy_after_viewing_this_item','customer_questions_and_answers','customer_reviews','sellers'])

    #Delete rows with blank values
    df = df[(df.price.notnull())]
    df = df[(df.number_available_in_stock.notnull())]
    df = df[(df.number_of_reviews.notnull())]
    df = df[(df.number_of_answered_questions.notnull())]
    df = df[(df.average_review_rating.notnull())]
    df = df[(df.amazon_category_and_sub_category.notnull())]

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

    df["description_length"] = df["description"].str.len().astype(int)

    #Create new category variable
    df["category"] = df["amazon_category_and_sub_category"].str.split(">").str[0]
    df["category"] = df["category"].str.split("&").str[0]

    df.drop(columns=['description','amazon_category_and_sub_category'])

    return df


def interactive(pt, box1, box2, box3, box4, box5):
    if pt.getX() > 9 and pt.getX() < 11.5 and pt.getY() > 5.3 and pt.getY() < 6.5:
        return "update"
        
    elif pt.getX() > 0 and pt.getX() < 1 and pt.getY() > 0 and pt.getY() < 1:
        return "quit"

    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 3.9 and pt.getY() < 4.2:
        box1.setFill("orange")
        return "number_of_reviews"

    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 3.2 and pt.getY() < 3.5:
        box2.setFill("orange")
        return "category"

    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 2.5 and pt.getY() < 2.8:

        box3.setFill("orange")
        return "price"

    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 1.7 and pt.getY() < 2.1:
        box4.setFill("orange")
        return "description_length"

    elif pt.getX() > 9 and pt.getX() < 9.5 and pt.getY() > 1 and pt.getY() < 1.4:
        box5.setFill("orange")
        return "average_review_rating"

def get_insights(insight_text):

    #Add linebreak to insight_text every 8 words to make it fit in the window
    insight_text = insight_text.split()
    insight_text = [insight_text[i:i+8] for i in range(0, len(insight_text), 8)]
    insight_text = [" ".join(x) for x in insight_text]

    insight_text = "\n".join(insight_text)

    #Create a smaller window to display insights
    win2 = GraphWin("Insights", 600, 500)
    win2.setBackground("white")

    #Create a title for the window
    title = Text(Point(300, 20), "Insights for current graph")
    title.setSize(25)
    title.setStyle("bold")
    title.setFace("courier")
    title.setTextColor("grey")
    title.draw(win2)
    
    #Create a text box to display insights
    insight_box = Text(Point(300, 250), insight_text)
    insight_box.setSize(15)
    insight_box.setStyle("bold")
    insight_box.setFace("courier")
    insight_box.setTextColor("grey")
    insight_box.draw(win2)


    return win2


def draw_graphs(win, command):
    
    if "number_of_reviews" in command and "average_review_rating" in command:
        # Scatter plot showing the relationship between the number of reviews and the average review
        plt.scatter(cleaned_df["number_of_reviews"], cleaned_df["average_review_rating"])
        plt.title("Number of reviews vs average review rating")
        plt.xlabel("Number of reviews")
        plt.ylabel("Average review")
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        win2 = get_insights("This plot will help you see if there is a relationship between the number of reviews a product has and its average review rating. If there is a strong positive relationship (i.e., the more reviews a product has, the higher its average review rating), this could be a good indication that the product is popular and well-liked by customers.")


    elif "number_of_reviews" in command and "price" in command:
        # Scatter plot showing the relationship between the number of reviews and the price
        plt.scatter(x=cleaned_df["number_of_reviews"], y=cleaned_df["price"])
        plt.title("Number of reviews vs price")
        plt.xlabel("Number of reviews")
        plt.ylabel("Price")
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        win2 = get_insights("If there is a positive relationship between the number of reviews and the price of a product, this could indicate that products with higher prices tend to have more reviews. This could be due to a variety of factors, such as the quality of the product, the popularity of the product, or the overall satisfaction of customers.")


    elif "number_of_reviews" in command and "category" in command:
        #Bar plot showing the relationship between the number of reviews and the category
        #filter any products with less than 10 reviews
        temp_df = cleaned_df[cleaned_df["number_of_reviews"] > 10]
        
        #Group by category and do average number of reviews
        temp_df = temp_df.groupby("category").agg({"number_of_reviews": "mean"}).reset_index()

        plt.bar(x=temp_df["category"], height=temp_df["number_of_reviews"])

        #add 
        plt.xticks(rotation=60, fontsize=7)
        plt.title("Number of reviews vs category")
        plt.ylabel("Number of reviews")
        plt.xlabel("Category")
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        win2 = get_insights("Categories that have less than 10 reviews are considered irrelevant and are removed. This could provide an overall picture of which categories of products are most popular with customers and which categories receive the most reviews.  This could provide insight into which categories of products tend to receive the most reviews on average. This information could be useful for identifying trends and patterns in customer behavior and for making decisions about which categories of products to focus on in the future.")


    elif "number_of_reviews" in command and "description_length" in command:
        # Scatter plot showing the relationship between the number of reviews and the description length
        plt.scatter(cleaned_df["number_of_reviews"], cleaned_df["description_length"])
        plt.title("Number of reviews vs description length")
        plt.xlabel("Number of reviews")
        plt.ylabel("Description length")
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        win2 = get_insights("If there is a positive relationship between the number of reviews and the description length of a product, this could indicate that products with longer descriptions tend to have more reviews. This could be because longer descriptions provide more information about the product, which can help to convince customers to leave reviews. Alternatively, it could be because products with longer descriptions tend to be of higher quality, which could make customers more likely to leave positive reviews.")

    elif "price" in command and "average_review_rating" in command:
        # Scatter plot showing the relationship between the average review and the price
        plt.scatter(x=cleaned_df["average_review_rating"], y=cleaned_df["price"])
        plt.title("Average review rating vs price")
        plt.xlabel("Average review")
        plt.ylabel("Price")
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        win2 = get_insights("This plot will help you see if there is a relationship between the price of a product and its average review rating. If there is a strong negative relationship (i.e., the higher the price of a product, the lower its average review rating), this could be a good indication that customers are not willing to pay a high price for a product with a low average review rating.")

    elif "average_review_rating" in command and "category" in command:
        # Bar plot showing the relationship between average review rating and the category
        temp_df = cleaned_df.groupby("category").agg({"average_review_rating": "mean"}).reset_index()
        plt.bar(x=temp_df["category"], height=temp_df["average_review_rating"])

        #add 
        plt.xticks(rotation=60, fontsize=7)
        plt.title("Average review rating vs category")
        plt.ylabel("Average review rating")
        plt.xlabel("Category")
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        win2 = get_insights("This shows the total number of reviews for each category of product. This could provide insight into which categories of products tend to receive the most reviews in total. This information could be useful for identifying trends and patterns in customer behavior and for making decisions about which categories of products to focus on in the future.")

    elif "average_review_rating" in command and "description_length" in command:
        # Scatter plot showing the relationship between the average review and the description length
        plt.scatter(x=cleaned_df["average_review_rating"], y=cleaned_df["description_length"])
        plt.title("Average review rating vs description length")
        plt.xlabel("Average review")
        plt.ylabel("Description length")
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        win2 = get_insights("This plot will help you see if there is a relationship between the length of the product description and the average review rating. If there is a strong positive relationship (i.e., the longer the product description, the higher the average review rating), this could be a good indication that customers find the longer product descriptions more helpful, and that this has a positive impact on the product's average review rating.")

    elif "price" in command and "category" in command:
        #Bar plot showing the relationship between price and the category
        temp_df = cleaned_df.groupby("category").agg({"price": "mean"}).reset_index()
        plt.bar(x=temp_df["category"], height=temp_df["price"])

        #add 
        plt.xticks(rotation=60, fontsize=7)
        plt.title("Price vs category")
        plt.ylabel("Price")
        plt.xlabel("Category")
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        win2 = get_insights("This could provide an overall picture of which categories of products tend to be the most expensive. This information could be useful for identifying which categories of products are the most profitable and which categories may need to be adjusted in order to increase sales. Additionally, this information could be useful for identifying trends and patterns in customer behavior and for making decisions about which categories of products to focus on in the future.")

    elif "price" in command and "description_length" in command:
        #Scatter plot showing the relationship between the average review and the description length

        #Filter description length to be less than 5000
        temp_df = cleaned_df[cleaned_df["description_length"] > 500]
        plt.scatter(x=temp_df["price"], y=temp_df["description_length"])
        plt.title("Price vs description length")
        plt.xlabel("Price")
        plt.ylabel("Description length")
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        win2 = get_insights("If there is a positive relationship between the price and the description length of a product, this could indicate that products with longer descriptions tend to have higher prices. This could be because longer descriptions provide more information about the product, which can help to convince customers to pay a higher price. Alternatively, it could be because products with longer descriptions tend to be of higher quality, which could make customers willing to pay a higher price.")

    elif "category" in command and "description_length" in command:
        #Bar plot showing the relationship between description length and the category
        temp_df = cleaned_df.groupby("category").agg({"description_length": "mean"}).reset_index()

        #filter any products with less than 10 reviews
        temp_df = cleaned_df[cleaned_df["description_length"] > 500]

        plt.bar(x=cleaned_df["category"], height=cleaned_df["description_length"])
        plt.xticks(rotation=60, fontsize=7)
        plt.title("Description length vs category")
        plt.xlabel("Category")
        plt.ylabel("Description length")

        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        win2 = get_insights("Categories that have less than 500 reviews are considered irrelevant and are removed. This could provide an overall picture of which categories of products tend to have the longest descriptions. This information could be useful for identifying which categories of products are the most detailed and which categories may need improvement in order to provide more information to customers.")

    #Insert the graphs inside the window

    #Draw white rectangle behind the graph to cover previous graph
    rect = Rectangle(Point(1, 0.3), Point(8, 6))
    rect.setFill("white")
    #change the border color of the rectangle
    rect.setOutline("white")
    rect.draw(win)
    graph = Image(Point(5, 3), "graph.png")
    graph.draw(win)

    return win2


def get_file():

    win = GraphWin("Amazon FBA Product Finder", 800, 400)
    win.setCoords(0.0, 0.0, 8.0, 4.0)

    #Creating Title
    title = Text(Point(4, 3.5), "Amazon Product Finder")
    title.draw(win)
    title.setFace("courier")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("grey")

    #Insert amazon logo before title
    logo = Image(Point(1, 3.5), "amazon2.png")

    logo.draw(win)

    #Create a description of what the program does
    description = Text(Point(4, 2.5), "This program will take a csv file of Amazon products\n and allow you to graphically analyze the data.")
    description.setFace("courier")
    description.setSize(12)
    description.setStyle("bold")
    description.setTextColor("grey")

    description.draw(win)

    #Create a button to select a file
    button = Rectangle(Point(3, 1), Point(5, 1.5))
    button.draw(win)
    button.setFill("grey")
    button.setOutline("grey")

    #Add text to button
    buttonText = Text(Point(4, 1.25), "Select File")
    buttonText.draw(win)

    #When user clicks the button, open a file explorer
    while True:
        pt = win.getMouse()
        if pt.getX() > 2.5 and pt.getX() < 4.5 and pt.getY() > 1 and pt.getY() < 1.5:

            file = filedialog.askopenfilename()

            #Check if file ends in .csv
            if ".csv" not in file:
                #Draw error message
                error = Text(Point(4, 0.5), "Error: File must be a csv file")
                error.draw(win)
                error.setFace("courier")
                error.setSize(12)
                error.setStyle("bold")
                error.setTextColor("red")
                continue

            win.close()
            return file


def gui():
    win = GraphWin("Amazon FBA Product Finder", 1200, 700)
    win.setBackground("white")
    win.setCoords(0.0, 0.0, 12.0, 7.0)

    #Creating Title
    title = Text(Point(4.3, 6.5), "Amazon Product Finder")
    title.draw(win)
    title.setFace("courier")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("grey")

    #Insert amazon logo before title
    logo = Image(Point(1.5, 6.5), "amazon2.png")
    
    logo.draw(win)

    #Creating Variables
    variables = Text(Point(10.5, 5), "Select Variables")
    variables.draw(win)
    variables.setFace("courier")
    variables.setSize(28)
    variables.setStyle("bold")
    variables.setTextColor("grey")
    maximum = Text(Point(10.2, 4.7), "Maximum 2 Variables")
    maximum.draw(win)
    maximum.setFace("courier")
    maximum.setSize(18)
    maximum.setStyle("bold")
    maximum.setTextColor("grey")

    #Creating Boxes for clicking on variables
    box1 = Rectangle(Point(9.2, 3.9), Point(9.5, 4.2)).draw(win)
    box1.setFill("white")
    text1 = Text(Point(10.2, 4.05), "# Reviews")
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
    text4.setText("Description\nLength")
    text4.draw(win)

    box5 = box4.clone()
    box5.move(0, -0.7)
    box5.draw(win)
    text5 = text4.clone()
    text5.move(0.1, -0.8)
    text5.setText("Average\nReview Rating")
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

    graph_variables = []
    insights_window = None
    while True:
        pt = win.getMouse()
        response = interactive(pt, box1, box2, box3, box4, box5)

        if response != "update" and response != "quit" and response != None:
            
            graph_variables.append(response)

        if response == "update":
            try:
                insights_window.close()
            except:
                pass

            #Draw graph
            insights_window = draw_graphs(win, graph_variables)

            #Reset boxes fill
            boxes = [box1, box2, box3, box4, box5]
            for i in boxes:
                i.setFill("white")

            graph_variables = []

        if response == "quit":
            try:
                insights_window.close()
            except:
                pass
            win.close()
            break

#gui()

if __name__ == "__main__":

    selected_file_path = get_file()
    cleaned_df = clean_df(selected_file_path)

    gui()
