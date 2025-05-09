import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog
import os

def load_file():
    """Open file dialog and return loaded DataFrame."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a CSV or Excel file",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )

    if not file_path:
        print("⚠️ No file selected.")
        return None, None

    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext == ".xlsx":
            df = pd.read_excel(file_path)
        else:
            print("⚠️ Unsupported file format.")
            return None, None
    except Exception as e:
        print(f"⚠️ Failed to load file: {e}")
        return None, None

    return df, os.path.basename(file_path)

def create_sankey(df, title="Sankey Diagram"):
    """Generate Sankey diagram from DataFrame."""
    required_cols = {'Source', 'Target', 'Value'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"⚠️ File must contain columns: {required_cols}")

    all_nodes = pd.concat([df['Source'], df['Target']]).unique()
    labels = {node: idx for idx, node in enumerate(all_nodes)}

    df['source_idx'] = df['Source'].map(labels)
    df['target_idx'] = df['Target'].map(labels)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=list(labels.keys())
        ),
        link=dict(
            source=df['source_idx'],
            target=df['target_idx'],
            value=df['Value']
        ))])

    fig.update_layout(title_text=title, font_size=12)
    fig.show()

if __name__ == "__main__":
    df, filename = load_file()
    if df is not None:
        create_sankey(df, title=f"Sankey Diagram - {filename}")