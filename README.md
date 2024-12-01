# cancer-dashboard
To run streamlit app, follow the below steps:

1. pip install streamlit (if not already installed)
2. if you're working in jupyter, make changes to dashboard.ipynb and convert it to .py using "jupyter nbconvert --to script dashboard.ipynb", otherwise directly make changes to dashboard.py
3. run the app - streamlit run dashboard.py

I'm currently working on seer-analysis.py and I've saved intermediary dataframes used for creating plots as csv files. Then reading those csv files in dashboard.ipynb for the web app. While this approach works for now, this isn't ideal! We should have a smooth flow which we can achieve later after we're ready with all the plots.

**Sagorika**, please push the latest seer.csv that you've fetched.

Other helpful plotting libraries:

1. pip install streamlit-echarts (https://github.com/andfanilo/streamlit-echarts)
2. pip install streamlit-elements==0.1.* (https://github.com/okld/streamlit-elements)
3. pip install streamlit-aggrid (https://github.com/PablocFonseca/streamlit-aggrid)
