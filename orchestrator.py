import subprocess

def run_fastapi():
    return ["uvicorn", "api_layer.fast_api.fast_api_app:app", "--reload"]

def run_streamlit():
    return ["streamlit", "run", "application_layer/streamlit_front_end/streamlit_app.py"]

if __name__ == "__main__":
    fastapi_process = subprocess.Popen(run_fastapi(), shell=False)
    
    # Running Streamlit in another subprocess
    streamlit_process = subprocess.Popen(run_streamlit(), shell=False)
    
    # Wait for both processes to complete
    fastapi_process.wait()
    streamlit_process.wait()
