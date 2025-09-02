\# API 682 Seal Selection Tool



Web application for mechanical seal selection per API 682 4th Edition (Sheets 1-10).



\[!\[Streamlit App](https://static.streamlit.io/badges/streamlit\_badge\_black\_white.svg)](https://your-username-seal-selector.streamlit.app)



\## Features

\- Determines seal category (1, 2, 3) based on operating conditions

\- Classifies fluid type (hydrocarbon, nonhydrocarbon, flashing/nonflashing)

\- Recommends seal type (A, B, C, Engineered System) based on fluid properties

\- Determines seal arrangement (1, 2, 3) using Sheet 6 decision logic

\- Provides barrier fluid recommendations for Arrangements 2 \& 3

\- Displays API 682 standard requirements for selected configuration



\## Usage

1\. Enter operating conditions (pressure, temperature, shaft speed)

2\. Select fluid properties and characteristics

3\. Configure environmental and safety requirements

4\. View recommended seal category, type, and arrangement

5\. Review standard requirements in expandable sections



\## Installation

```bash

git clone https://github.com/your-username/api-682-seal-selector.git

cd api-682-seal-selector

pip install -r requirements.txt

streamlit run app.py

