import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def expense_clustering():
    st.title("Expense Clustering")
    data = st.session_state['uploaded_data']

    # Select features for clustering
    expense_columns = ['Electricity Bill (£)', 'Gas Bill (£)', 'Groceries (£)',
                       'Transportation (£)', 'Water Bill (£)', 'Sky Sports (£)', 'Other Expenses (£)',
                       'Monthly Outing (£)']

    # Normalize data
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data[expense_columns])

    # K-Means clustering
    n_clusters = st.sidebar.slider("Number of Clusters", 2, 10, 3)
    model = KMeans(n_clusters=n_clusters, random_state=42)

    labels = model.fit_predict(normalized_data)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(normalized_data)

    # Create DataFrame for plotting
    plot_df = pd.DataFrame({
        'Expense Dimension 1': pca_result[:, 0],
        'Expense Dimension 2': pca_result[:, 1],
        'Cluster': labels,
        'Employee': data['Employee'],
        'Monthly Income (£)': data['Monthly Income (£)']
    })

    fig = px.scatter(plot_df, x='Expense Dimension 1', y='Expense Dimension 2',
                     color='Cluster', hover_data=['Employee', 'Monthly Income (£)'])
    st.plotly_chart(fig)

    st.subheader("Cluster Descriptions")
    for cluster in np.unique(labels):
        cluster_data = data[labels == cluster]
        st.write(f"Cluster {cluster}:")
        st.write(cluster_data[expense_columns].mean().to_dict())

if __name__ == "__main__":
    expense_clustering()