✅ Project Structure Recap
Your Flask project directory looks like this:

vbnet
Copy
Edit
project/
│
├── static/
│   ├── assets/
│   ├── forms/
│   └── uploads/
│
├── templates/
│   ├── blog-single.html
│   ├── blog.html
│   ├── index.html
│   └── portfolio-details.html
│
├── app.py                  ← Flask application
├── healthy_vs_rotten.h5   ← Trained model
├── ipython.html            ← Optional/not typical in Flask
└── Readme.txt              ← Documentation
✅ Kaggle API Setup (on Google Colab)
Get kaggle.json:

Go to your Kaggle Account Settings.

Click “Create New API Token” → This downloads kaggle.json.

In Colab: