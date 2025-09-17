# dashboard_calculator.py

# import pandas as pd

# class DashboardDataCalculator:
#     def __init__(self, df: pd.DataFrame):
#         if df.empty:
#             raise ValueError("Le DataFrame ne peut pas être vide.")
#         self.df = df.copy()
#         self.df['polarity'] = self.df['polarity'].fillna('non mentionné')
#         if 'timestamp' in self.df.columns:
#             self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')

#     def get_all_dashboard_data(self):
#         """
#         Calcule et retourne toutes les données nécessaires pour le dashboard
#         sous forme de dictionnaire.
#         """
#         polarity_counts = self.df['polarity'].value_counts()
#         dept_sentiment = pd.crosstab(self.df['Département'], self.df['polarity'])
        
#         # ... (tous les autres calculs de votre script original)
#         self.df['Dept_Filiere'] = self.df['Département'] + ' - ' + self.df['Filière']
#         dept_filiere_positive = self.df.groupby('Dept_Filiere')['polarity'].apply(
#             lambda x: (x == 'positive').sum() / len(x) * 100 if len(x) > 0 else 0
#         ).sort_values(ascending=False)
        
#         top_users = self.df['User'].value_counts().head(8)
        
#         # Calculs pour les KPIs
#         total_feedbacks = len(self.df)
#         unique_users = self.df['User'].nunique()
#         positive_pct = (self.df['polarity'] == 'positive').mean() * 100
        
#         # Structure des données pour Chart.js (exemple)
#         pie_chart_data = {
#             'labels': polarity_counts.index.tolist(),
#             'datasets': [{
#                 'data': polarity_counts.values.tolist(),
#                 'backgroundColor': ['#2ecc71', '#e74c3c', '#f39c12', '#95a5a6', '#34495e']
#             }]
#         }
        
#         positive_by_dept_filiere_data = {
#             'labels': dept_filiere_positive.index.tolist(),
#             'datasets': [{
#                 'label': '% de Sentiments Positifs',
#                 'data': dept_filiere_positive.values.tolist(),
#                 'backgroundColor': '#3498db'
#             }]
#         }

#         # Retourner un dictionnaire JSON-sérialisable
#         return {
#             "kpis": {
#                 "total_feedbacks": total_feedbacks,
#                 "unique_users": unique_users,
#                 "positive_pct": round(positive_pct, 1),
#                 # ... autres KPIs
#             },
#             "charts": {
#                 "polarity_distribution": pie_chart_data,
#                 "positive_by_dept_filiere": positive_by_dept_filiere_data,
#                 # ... autres données de graphiques
#             },
#             "tables": {
#                 "top_users": top_users.reset_index().to_dict(orient='records'),
#                 "sentiment_by_department": dept_sentiment.reset_index().to_dict(orient='records')
#             }
#         }

import pandas as pd

class DashboardDataCalculator:
    def __init__(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("Le DataFrame ne peut pas être vide.")
        self.df = df.copy()
        self.df['polarity'] = self.df['polarity'].fillna('non mentionné')
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')

    def get_all_dashboard_data(self):
        polarity_counts = self.df['polarity'].value_counts()
        dept_sentiment = pd.crosstab(self.df['Département'], self.df['polarity'])
        self.df['Dept_Filiere'] = self.df['Département'] + ' - ' + self.df['Filière']
        dept_filiere_positive = self.df.groupby('Dept_Filiere')['polarity'].apply(
            lambda x: (x == 'positive').sum() / len(x) * 100 if len(x) > 0 else 0
        ).sort_values(ascending=False)
        top_users = self.df['User'].value_counts().head(8)
        total_feedbacks = len(self.df)
        unique_users = self.df['User'].nunique()
        positive_pct = (self.df['polarity'] == 'positive').mean() * 100
        pie_chart_data = {
            'labels': polarity_counts.index.tolist(),
            'datasets': [{
                'data': polarity_counts.values.tolist(),
                'backgroundColor': ['#2ecc71', '#e74c3c', '#f39c12', '#95a5a6', '#34495e']
            }]
        }
        positive_by_dept_filiere_data = {
            'labels': dept_filiere_positive.index.tolist(),
            'datasets': [{
                'label': '% de Sentiments Positifs',
                'data': dept_filiere_positive.values.tolist(),
                'backgroundColor': '#3498db'
            }]
        }
        return {
            "kpis": {
                "total_feedbacks": total_feedbacks,
                "unique_users": unique_users,
                "positive_pct": round(positive_pct, 1),
            },
            "charts": {
                "polarity_distribution": pie_chart_data,
                "positive_by_dept_filiere": positive_by_dept_filiere_data,
            },
            "tables": {
                "top_users": top_users.reset_index().to_dict(orient='records'),
                "sentiment_by_department": dept_sentiment.reset_index().to_dict(orient='records')
            }
        }