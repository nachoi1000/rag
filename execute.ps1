# Create a virtual environment
python -m venv virtual_env

# Activate the virtual environment
.\virtual_env\Scripts\Activate

# Install the required packages
pip install -r requirements.txt

# Run streamlit
streamlit run rag_app.py