# Chirp

This project was realised by Loïc Christen and Alexandre Venturi.
This is a minimalist version of X.

To run this project you first need to clone the repository on your device with a git clone 

```
git clone https://github.com/NotDonaldPump/Chirp.git
```

In the case you want to run the project by a console you will need to navigate a bit through the folders

```
cd Chirp
```

We assume here you already have a version of Python and so you can install some package that are listed in the *requirement.txt*

```
pip install -r requirements.txt
```

You will need to have a Redis server running, and you must add a folder named "data" at the root of the project. In this folder, you should place JSON files containing tweets in the standard Twitter format. Then you can run populate_database.py.

```
python chirp/populate_database.py
```

Finally, you can run our web app ./chirp/web_app.py

```
streamlit run ./chirp/web_app.py
```
