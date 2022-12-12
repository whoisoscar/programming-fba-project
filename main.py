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

    print(f"Dataset successfully cleaned ({og_len} --> {len(df)} rows).")
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
    
    elif 1 <= pt.getX() <= 2 and 5 <= pt.getY() <= 5.5:
        return "edit titles"

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


def draw_graphs(graphs_window, command, titles):
    win = graphs_window.win

    if "number_of_reviews" in command and "average_review_rating" in command:
        # Scatter plot showing the relationship between the number of reviews and the average review
        plt.scatter(cleaned_df["number_of_reviews"], cleaned_df["average_review_rating"])

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Number of reviews vs average review rating")
            plt.xlabel("Number of reviews")
            plt.ylabel("Average review")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Number of reviews vs average review rating", "x_axis": "Number of reviews", "y_axis": "Average review"}
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("This plot will help you see if there is a relationship between the number of reviews a product has and its average review rating. If there is a strong positive relationship (i.e., the more reviews a product has, the higher its average review rating), this could be a good indication that the product is popular and well-liked by customers.")


    elif "number_of_reviews" in command and "price" in command:
        # Scatter plot showing the relationship between the number of reviews and the price
        plt.scatter(x=cleaned_df["number_of_reviews"], y=cleaned_df["price"])

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Number of reviews vs price")
            plt.xlabel("Number of reviews")
            plt.ylabel("Price")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Number of reviews vs price", "x_axis": "Number of reviews", "y_axis": "Price"}
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("If there is a positive relationship between the number of reviews and the price of a product, this could indicate that products with higher prices tend to have more reviews. This could be due to a variety of factors, such as the quality of the product, the popularity of the product, or the overall satisfaction of customers.")


    elif "number_of_reviews" in command and "category" in command:
        #Bar plot showing the relationship between the number of reviews and the category
        #filter any products with less than 10 reviews
        temp_df = cleaned_df[cleaned_df["number_of_reviews"] > 10]
        
        #Group by category and do average number of reviews
        temp_df = temp_df.groupby("category").agg({"number_of_reviews": "mean"}).reset_index()

        plt.bar(x=temp_df["category"], height=temp_df["number_of_reviews"])

        #add 
        plt.xticks(rotation=60, fontsize=7)

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Number of reviews vs category")
            plt.ylabel("Number of reviews")
            plt.xlabel("Category")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Number of reviews vs category", "x_axis": "Category", "y_axis": "Number of reviews"}
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("Categories that have less than 10 reviews are considered irrelevant and are removed. This could provide an overall picture of which categories of products are most popular with customers and which categories receive the most reviews.  This could provide insight into which categories of products tend to receive the most reviews on average. This information could be useful for identifying trends and patterns in customer behavior and for making decisions about which categories of products to focus on in the future.")


    elif "number_of_reviews" in command and "description_length" in command:
        # Scatter plot showing the relationship between the number of reviews and the description length
        plt.scatter(cleaned_df["number_of_reviews"], cleaned_df["description_length"])

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Number of reviews vs description length")
            plt.xlabel("Number of reviews")
            plt.ylabel("Description length")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Number of reviews vs description length", "x_axis": "Number of reviews", "y_axis": "Description length"}
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("If there is a positive relationship between the number of reviews and the description length of a product, this could indicate that products with longer descriptions tend to have more reviews. This could be because longer descriptions provide more information about the product, which can help to convince customers to leave reviews. Alternatively, it could be because products with longer descriptions tend to be of higher quality, which could make customers more likely to leave positive reviews.")

    elif "price" in command and "average_review_rating" in command:
        # Scatter plot showing the relationship between the average review and the price
        plt.scatter(x=cleaned_df["average_review_rating"], y=cleaned_df["price"])

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Average review rating vs price")
            plt.xlabel("Average review")
            plt.ylabel("Price")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Average review rating vs price", "x_axis": "Average review", "y_axis": "Price"}
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plot
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("This plot will help you see if there is a relationship between the price of a product and its average review rating. If there is a strong negative relationship (i.e., the higher the price of a product, the lower its average review rating), this could be a good indication that customers are not willing to pay a high price for a product with a low average review rating.")

    elif "average_review_rating" in command and "category" in command:
        # Bar plot showing the relationship between average review rating and the category
        temp_df = cleaned_df.groupby("category").agg({"average_review_rating": "mean"}).reset_index()
        plt.bar(x=temp_df["category"], height=temp_df["average_review_rating"])

        #add 
        plt.xticks(rotation=60, fontsize=7)

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Average review rating vs category")
            plt.ylabel("Average review rating")
            plt.xlabel("Category")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Average review rating vs category", "x_axis": "Category", "y_axis": "Average review rating"}
        
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("This shows the total number of reviews for each category of product. This could provide insight into which categories of products tend to receive the most reviews in total. This information could be useful for identifying trends and patterns in customer behavior and for making decisions about which categories of products to focus on in the future.")

    elif "average_review_rating" in command and "description_length" in command:
        # Scatter plot showing the relationship between the average review and the description length
        plt.scatter(x=cleaned_df["average_review_rating"], y=cleaned_df["description_length"])

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Average review rating vs description length")
            plt.xlabel("Average review")
            plt.ylabel("Description length")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Average review rating vs description length", "x_axis": "Average review", "y_axis": "Description length"}
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("This plot will help you see if there is a relationship between the length of the product description and the average review rating. If there is a strong positive relationship (i.e., the longer the product description, the higher the average review rating), this could be a good indication that customers find the longer product descriptions more helpful, and that this has a positive impact on the product's average review rating.")

    elif "price" in command and "category" in command:
        #Bar plot showing the relationship between price and the category
        temp_df = cleaned_df.groupby("category").agg({"price": "mean"}).reset_index()
        plt.bar(x=temp_df["category"], height=temp_df["price"])

        #add 
        plt.xticks(rotation=60, fontsize=7)

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Price vs category")
            plt.ylabel("Price")
            plt.xlabel("Category")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Price vs category", "x_axis": "Category", "y_axis": "Price"}
            
        #Save plot as "graph.png" in full size
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("This could provide an overall picture of which categories of products tend to be the most expensive. This information could be useful for identifying which categories of products are the most profitable and which categories may need to be adjusted in order to increase sales. Additionally, this information could be useful for identifying trends and patterns in customer behavior and for making decisions about which categories of products to focus on in the future.")

    elif "price" in command and "description_length" in command:
        #Scatter plot showing the relationship between the average review and the description length

        #Filter description length to be less than 5000
        temp_df = cleaned_df[cleaned_df["description_length"] > 500]
        plt.scatter(x=temp_df["price"], y=temp_df["description_length"])

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
            plt.title("Price vs description length")
            plt.xlabel("Price")
            plt.ylabel("Description length")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Price vs description length", "x_axis": "Price", "y_axis": "Description length"}
        
        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("If there is a positive relationship between the price and the description length of a product, this could indicate that products with longer descriptions tend to have higher prices. This could be because longer descriptions provide more information about the product, which can help to convince customers to pay a higher price. Alternatively, it could be because products with longer descriptions tend to be of higher quality, which could make customers willing to pay a higher price.")

    elif "category" in command and "description_length" in command:
        #Bar plot showing the relationship between description length and the category
        temp_df = cleaned_df.groupby("category").agg({"description_length": "mean"}).reset_index()

        #filter any products with less than 10 reviews
        temp_df = cleaned_df[cleaned_df["description_length"] > 500]

        plt.bar(x=cleaned_df["category"], height=cleaned_df["description_length"])
        plt.xticks(rotation=60, fontsize=7)

        if titles != None:
            plt.title(titles["title"])

            plt.xlabel(titles["x_axis"])
            plt.ylabel(titles["y_axis"])
        else:
        
            plt.title("Description length vs category")
            plt.xlabel("Category")
            plt.ylabel("Description length")

            #Save titles in graphs_window for edit use
            graphs_window.graph_titles = {"title": "Description length vs category", "x_axis": "Category", "y_axis": "Description length"}



        #Save plot as "graph.png"
        plt.savefig("graph.png", bbox_inches='tight')

        #clear plt
        plt.clf()

        if titles == None:
            graphs_window.child_insights_window = get_insights("Categories that have less than 500 reviews are considered irrelevant and are removed. This could provide an overall picture of which categories of products tend to have the longest descriptions. This information could be useful for identifying which categories of products are the most detailed and which categories may need improvement in order to provide more information to customers.")

    #Insert the graphs inside the window

    #Draw white rectangle behind the graph to cover previous graph
    rect = Rectangle(Point(1, 0.3), Point(8, 6))
    rect.setFill("white")
    #change the border color of the rectangle
    rect.setOutline("white")
    rect.draw(win)
    graph = Image(Point(5, 3), "graph.png")
    graph.draw(win)

    #Create button to edit graph titles to the top left of the graph
    edit_title = Rectangle(Point(1, 5), Point(2, 5.5))
    edit_title.setFill("grey")
    edit_title.draw(win)
    edit_title_text = Text(Point(1.5, 5.25), "Edit Title")
    edit_title_text.draw(win)


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

class editTitles():
    def __init__(self):
        self.win = GraphWin("Edit Titles", 500, 500)

        self.win.setBackground("white")
        self.win.setCoords(0.0, 0.0, 12.0, 7.0)

        #Add "Edit Titles" text
        edit_titles_text = Text(Point(6, 6.5), "Edit Titles")
        edit_titles_text.draw(self.win)
        edit_titles_text.setFace("courier")
        edit_titles_text.setSize(36)
        edit_titles_text.setStyle("bold")
        edit_titles_text.setTextColor("grey")

        #Add title text and input box
        title_text = Text(Point(6, 5.5), "Title")
        title_text.draw(self.win)
        title_text.setFace("courier")
        title_text.setSize(25)
        title_text.setStyle("bold")
        title_text.setTextColor("grey")
        self.title_input = Entry(Point(6, 5), 20)
        self.title_input.draw(self.win)

        #Add x-axis text and input box
        x_axis_text = Text(Point(6, 4.5), "X-Axis")
        x_axis_text.draw(self.win)
        x_axis_text.setFace("courier")
        x_axis_text.setSize(25)
        x_axis_text.setStyle("bold")
        x_axis_text.setTextColor("grey")
        self.x_axis_input = Entry(Point(6, 4), 20)
        self.x_axis_input.draw(self.win)

        #Add y-axis text and input box
        y_axis_text = Text(Point(6, 3.5), "Y-Axis")
        y_axis_text.draw(self.win)
        y_axis_text.setFace("courier")
        y_axis_text.setSize(25)
        y_axis_text.setStyle("bold")
        y_axis_text.setTextColor("grey")
        self.y_axis_input = Entry(Point(6, 3), 20)
        self.y_axis_input.draw(self.win)

        #Add submit button
        submit = Rectangle(Point(3.5, 2.5), Point(8.5, 1.5)).draw(self.win)
        submit.setFill("orange")
        submit_text = Text(Point(6, 2), "Update Titles")
        submit_text.draw(self.win)
        submit_text.setFace("courier")
        submit_text.setSize(20)
        submit_text.setStyle("bold")
        submit_text.setTextColor("black")

    def get_inputs(self):
        #Get inputs from user
        title = self.title_input.getText()
        x_axis = self.x_axis_input.getText()
        y_axis = self.y_axis_input.getText()

        #return dictionary of inputs
        return {"title": title, "x_axis": x_axis, "y_axis": y_axis}
    
    def add_current_titles(self, titles):
        #Add current titles to input boxes
        self.title_input.setText(titles["title"])
        self.x_axis_input.setText(titles["x_axis"])
        self.y_axis_input.setText(titles["y_axis"])

class graphsWindow():
    def __init__(self):
        self.win = GraphWin("Amazon FBA Product Finder", 1200, 700)
        self.win.setBackground("white")
        self.win.setCoords(0.0, 0.0, 12.0, 7.0)

        #Creating Title
        title = Text(Point(4.3, 6.5), "Amazon Product Finder")
        title.draw(self.win)
        title.setFace("courier")
        title.setSize(36)
        title.setStyle("bold")
        title.setTextColor("grey")

        #Insert amazon logo before title
        logo = Image(Point(1.5, 6.5), "amazon2.png")
        
        logo.draw(self.win)

        #Creating Variables
        variables = Text(Point(10.5, 5), "Select Variables")
        variables.draw(self.win)
        variables.setFace("courier")
        variables.setSize(28)
        variables.setStyle("bold")
        variables.setTextColor("grey")
        maximum = Text(Point(10.2, 4.7), "Maximum 2 Variables")
        maximum.draw(self.win)
        maximum.setFace("courier")
        maximum.setSize(18)
        maximum.setStyle("bold")
        maximum.setTextColor("grey")

        #Creating Boxes for clicking on variables
        box1 = Rectangle(Point(9.2, 3.9), Point(9.5, 4.2)).draw(self.win)
        box1.setFill("white")
        text1 = Text(Point(10.2, 4.05), "# Reviews")
        text1.draw(self.win)
        text1.setFace("courier")
        text1.setSize(25)
        text1.setStyle("bold")
        text1.setTextColor("grey")

        box2 = box1.clone()
        box2.move(0, -0.75)
        box2.draw(self.win)
        text2 = text1.clone()
        text2.move(0.15, -0.75)
        text2.setText("Category")
        text2.draw(self.win)

        box3 = box2.clone()
        box3.move(0, -0.75)
        box3.draw(self.win)
        text3 = text2.clone()
        text3.move(-0.2, -0.75)
        text3.setText("Price")
        text3.draw(self.win)

        box4 = box3.clone()
        box4.move(0, -0.75)
        box4.draw(self.win)
        text4 = text3.clone()
        text4.move(0.45, -0.7)
        text4.setText("Description\nLength")
        text4.draw(self.win)

        box5 = box4.clone()
        box5.move(0, -0.7)
        box5.draw(self.win)
        text5 = text4.clone()
        text5.move(0.1, -0.8)
        text5.setText("Average\nReview Rating")
        text5.draw(self.win)

        #Creating Update Button
        update = Rectangle(Point(9.2, 5.5), Point(11.5, 6.5)).draw(self.win)
        update.setFill("orange")
        update_text = Text(Point(10.35, 6), "Update")
        update_text.draw(self.win)
        update_text.setFace("courier")
        update_text.setSize(25)
        update_text.setStyle("bold")
        update_text.setTextColor("black")

        #Creating Quit Button
        quit = Rectangle(Point(0, 0), Point(0.8, 0.8)).draw(self.win)
        quit.setFill("grey")
        quit_text = Text(Point(0.4, 0.4), "Quit")
        quit_text.draw(self.win)
        quit_text.setFace("courier")
        quit_text.setSize(25)
        quit_text.setStyle("bold")
        quit_text.setTextColor("black")

        self.box1 = box1
        self.box2 = box2
        self.box3 = box3
        self.box4 = box4
        self.box5 = box5

        self.variables_for_edit = []
        self.graph_variables = []
        self.graph_titles = {"title": "", "x_axis": "", "y_axis": ""}
        self.child_insights_window = None
        self.editable_status = False

def gui():

    
    def update_graphs(graph_variables, titles):
        if graphs_window.editable_status:
            draw_graphs(graphs_window, graphs_window.variables_for_edit, titles)

            return
        else:
            graphs_window.variables_for_edit = graphs_window.graph_variables

        try:
            graphs_window.child_insights_window.close()
        except:
            pass

        #Draw graph
        draw_graphs(graphs_window, graph_variables, None)

        #Reset boxes fill
        boxes = [graphs_window.box1, graphs_window.box2, graphs_window.box3, graphs_window.box4, graphs_window.box5]
        for i in boxes:
            i.setFill("white")

        graphs_window.graph_variables = []

    graphs_window = graphsWindow()

    while True:
        pt = graphs_window.win.getMouse()
        response = interactive(pt, graphs_window.box1, graphs_window.box2, graphs_window.box3, graphs_window.box4, graphs_window.box5)

        if response != "update" and response != "quit" and response != None != "edit titles":
            
            graphs_window.graph_variables.append(response)

        if response == "update":
            update_graphs(graphs_window.graph_variables, None)
            graphs_window.editable_status = True

        if response == "edit titles":

            edit_win = editTitles()
            edit_win.add_current_titles(graphs_window.graph_titles)

            #Wait for user to click submit
            while True:
                try:
                    pt = edit_win.win.getMouse()
                except:
                    break
                if pt.getX() >= 4.5 and pt.getX() <= 7.5 and pt.getY() >= 1.5 and pt.getY() <= 2.5:
                    #Get input title
                    inputs = edit_win.get_inputs()

                    edit_win.win.close()
                    update_graphs(graphs_window.graph_variables, inputs)
                    graphs_window.editable_status = False
                    break


        if response == "quit":
            try:
                graphs_window.child_insights_window.close()
            except:
                pass
            graphs_window.win.close()
            break

#gui()

if __name__ == "__main__":

    #selected_file_path = get_file()
    cleaned_df = clean_df("amazon_co-ecommerce_sample.csv")

    gui()