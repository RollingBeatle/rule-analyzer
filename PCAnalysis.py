import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def main():
        
    df = pd.read_excel('./data/categories.xlsx', sheet_name="Sheet1", engine="openpyxl")
    df.set_index('State')
    num_components = 2  # You can adjust this value as needed
    print(df)
    pca = PCA(n_components=num_components)
    dfnums =df.iloc[:, 1:] 
    pca.fit(dfnums)

    reduced_data = pca.transform(dfnums)

    reduced_df = pd.DataFrame(reduced_data, columns=[f'PC{i+1}' for i in range(num_components)])

    explained_variance_ratio = pca.explained_variance_ratio_
    plt.scatter(reduced_df['PC1'], reduced_df['PC2'])
    
    names = [col for col in df.columns]
    for i, row in df.iterrows():
        
        label = ', '.join(names)
        plt.annotate(names[i], (reduced_df['PC1'][i], reduced_df['PC2'][i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA Result')
    plt.show()

if __name__ == "__main__":
    main()
    