# Background
A simple graphics user interface (GUI) for Amazon FBA (Fulfillment by Amazon) sellers to help them make better decisions when it comes to their inventory. 
The app allows the user to upload a dataset of amazon products and upon variable selection, it will generate graphs and insights to help the user see which products, categories or any ther indicators drive a successful product.

<table>
  <tr>
    <td>
      <img src="https://i.imgur.com/0csr7cJ.png" alt="Lorem ipsum" title="Lorem ipsum">
    </td>
    <td>
      <img src="https://i.imgur.com/SMoCfz3.png" alt="Dolor sit" title="Dolor sit">
    </td>
   
  </tr>

  <tr>
    <td>Dataset Selection</td>
    <td>Main Screen</td>

  </tr>
  <tr>

   <td>
      <img src="https://i.imgur.com/iamOyG2.png" alt="Amet consectetur" title="Amet consectetur">
    </td>
    <td>
      <img src="https://i.imgur.com/T0vYhs3.png" alt="Amet consectetur" title="Amet consectetur">
    </td>
  </tr>
  
  <tr>
    <td>Insights Page</td>
    <td>Edit Titles Page</td>

  </tr>
</table>

<sub>*UI visualisations (click to enlarge)<sub>*


Limitations:
- The app only works if the imputted dataset is in the same format as the one provided in the repository.
    - This dataset only contains 10,000 products and is from the Amazon.co.uk marketplace (2017).

*Disclosure: the app was developped on MacOS Monterey 12.4 using Python 3.7.3*

## File Architecture
- `main.py` - The main file that runs the app.
- `amaon_co-ecommerce_sample.csv` - The dataset used for the app.
- any other files are self-explanatory.

## The Dataset


# Installation & Usage
*Note: all code below is intended to be run in the terminal/command line*
## First-time install

Clone the files:
`````
git clone https://github.com/whoisoscar/programming-fba-project
`````

**Create and activate a Virtual Environment**

Creating the venv:
`````
cd programming-fba-project
python3 -m venv ./project
`````
Activating the venv (each time you open the folder):
````
source ./project/bin/activate
````
**Install modules**

To install required modules:
`````
pip install -r requirements.txt
`````
## Usage
`````
python3 main.py
`````

# Further improvements
- [ ] Make the app more user-friendly
- [ ] Add more graphs and variables
- [ ] Make the app fetch the data from Amazon's API in real time rather than relying on a dataset.

# Resources Used


# Credits
This project was created for our Programming for Data Management & Analysis course at IE University. The project was created by:
- Duarte Barbosa
- Joaquín de Tord
- Giacomo Pedersoli
- Oscar Tluszcz
- Simão Varandas
