# Deployment

Schedx can be run locally with Streamlit and can also be adapted for hosted notebook, Databricks, or container workflows.

## 🧭 Purpose

This page documents practical ways to run the application for development, demonstration, or analysis.

## 🖥️ Local Streamlit

Create a virtual environment:

    python -m venv .venv

Activate it in Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

Run Schedx:

    streamlit run app.py

Run on a specific port:

    streamlit run app.py --server.port 8501

Run in headless mode:

    streamlit run app.py --server.headless true

## ☁️ Google Colab

A notebook workflow can be used when analysts need a hosted environment.

Recommended sequence:

1. Open the notebook in Colab.
2. Upload the workbook or mount Google Drive.
3. Set the data path.
4. Run the notebook top-to-bottom.
5. Export charts and tables for review.

## 🧱 Databricks

Schedx workflows can be adapted to Databricks when the dataset is stored in a cloud workspace or lakehouse.

Recommended sequence:

1. Clone the repository into a Databricks workspace or repo.
2. Install dependencies in the target cluster or notebook environment.
3. Upload or mount the Schedule-X workbook.
4. Execute notebook or app-oriented workflows.
5. Persist outputs to workspace storage or cloud object storage.

## 🐳 Optional Docker Workflow

If the project includes a Dockerfile, build the image:

    docker build -t schedx:latest .

Run the container:

    docker run --rm -p 8501:8501 schedx:latest

## 🧯 Troubleshooting

| Issue                         | Correction                                                              |
|-------------------------------|-------------------------------------------------------------------------|
| Streamlit command not found   | Confirm the virtual environment is active and `streamlit` is installed. |
| Workbook not found            | Upload the workbook or set the fallback path in the sidebar.            |
| Missing sheet                 | Rename the worksheet to `Data` or allow the first-sheet fallback.       |
| Port already in use           | Run with `--server.port` and choose another port.                       |
| PowerShell activation blocked | Set the current-user execution policy to allow local scripts.           |
