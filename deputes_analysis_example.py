#!/usr/bin/env python3
"""
Exemple d'analyse des données des députés téléchargées
Montre comment exploiter les données une fois téléchargées
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def analyze_deputes_data(csv_file="deputes_france.csv"):
    """
    Analyse les données des députés téléchargées
    
    Args:
        csv_file: Fichier CSV avec les données des députés
    """
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        print(f"📊 Analyse de {len(df)} députés")
        print("-" * 40)
        
        # 1. Informations générales
        print("📋 INFORMATIONS GÉNÉRALES")
        print(f"   Nombre total de députés: {len(df)}")
        print(f"   Colonnes disponibles: {len(df.columns)}")
        
        # 2. Répartition par parti politique
        if 'parti_ratt_financier' in df.columns:
            print("\n🎨 RÉPARTITION PAR PARTI")
            parti_counts = df['parti_ratt_financier'].value_counts()
            for parti, count in parti_counts.head(10).items():
                percentage = (count / len(df)) * 100
                print(f"   {parti}: {count} députés ({percentage:.1f}%)")
        
        # 3. Répartition par sexe
        if 'sexe' in df.columns:
            print("\n👥 RÉPARTITION PAR SEXE")
            sexe_counts = df['sexe'].value_counts()
            for sexe, count in sexe_counts.items():
                percentage = (count / len(df)) * 100
                print(f"   {sexe}: {count} députés ({percentage:.1f}%)")
        
        # 4. Répartition par région
        if 'nom_circo' in df.columns:
            print("\n🗺️  TOP 10 DÉPARTEMENTS")
            # Extraire le département du nom de circonscription
            df['departement'] = df['nom_circo'].str.extract(r'(\d{2,3}[A-Z]?)')
            dept_counts = df['departement'].value_counts()
            for dept, count in dept_counts.head(10).items():
                print(f"   {dept}: {count} députés")
        
        # 5. Analyse des professions
        if 'profession' in df.columns:
            print("\n💼 TOP 10 PROFESSIONS")
            prof_counts = df['profession'].value_counts()
            for prof, count in prof_counts.head(10).items():
                print(f"   {prof}: {count} députés")
        
        # 6. Statistiques d'âge (si disponible)
        if 'age' in df.columns:
            print("\n📊 STATISTIQUES D'ÂGE")
            print(f"   Âge moyen: {df['age'].mean():.1f} ans")
            print(f"   Âge médian: {df['age'].median():.0f} ans")
            print(f"   Plus jeune: {df['age'].min():.0f} ans")
            print(f"   Plus âgé: {df['age'].max():.0f} ans")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Fichier {csv_file} non trouvé")
        print("💡 Exécutez d'abord le script de téléchargement")
        return None
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return None

def create_visualizations(df):
    """
    Crée des visualisations des données
    
    Args:
        df: DataFrame avec les données des députés
    """
    try:
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Analyse des Députés de l\'Assemblée Nationale', fontsize=16)
        
        # 1. Répartition par parti (top 10)
        if 'parti_ratt_financier' in df.columns:
            parti_counts = df['parti_ratt_financier'].value_counts().head(10)
            axes[0, 0].barh(range(len(parti_counts)), parti_counts.values)
            axes[0, 0].set_yticks(range(len(parti_counts)))
            axes[0, 0].set_yticklabels(parti_counts.index, fontsize=8)
            axes[0, 0].set_title('Top 10 Partis Politiques')
            axes[0, 0].set_xlabel('Nombre de députés')
        
        # 2. Répartition par sexe
        if 'sexe' in df.columns:
            sexe_counts = df['sexe'].value_counts()
            axes[0, 1].pie(sexe_counts.values, labels=sexe_counts.index, autopct='%1.1f%%')
            axes[0, 1].set_title('Répartition par Sexe')
        
        # 3. Distribution des âges
        if 'age' in df.columns:
            axes[1, 0].hist(df['age'].dropna(), bins=20, alpha=0.7, edgecolor='black')
            axes[1, 0].set_title('Distribution des Âges')
            axes[1, 0].set_xlabel('Âge')
            axes[1, 0].set_ylabel('Nombre de députés')
            axes[1, 0].axvline(df['age'].mean(), color='red', linestyle='--', 
                              label=f'Moyenne: {df["age"].mean():.1f}')
            axes[1, 0].legend()
        
        # 4. Top 10 professions
        if 'profession' in df.columns:
            prof_counts = df['profession'].value_counts().head(10)
            axes[1, 1].barh(range(len(prof_counts)), prof_counts.values)
            axes[1, 1].set_yticks(range(len(prof_counts)))
            axes[1, 1].set_yticklabels(prof_counts.index, fontsize=8)
            axes[1, 1].set_title('Top 10 Professions')
            axes[1, 1].set_xlabel('Nombre de députés')
        
        plt.tight_layout()
        plt.savefig('analyse_deputes.png', dpi=300, bbox_inches='tight')
        print("📈 Graphiques sauvés dans 'analyse_deputes.png'")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des graphiques: {e}")

def search_deputies(df, search_term):
    """
    Recherche des députés par nom ou critère
    
    Args:
        df: DataFrame avec les données des députés
        search_term: Terme de recherche
    """
    if 'nom' in df.columns:
        results = df[df['nom'].str.contains(search_term, case=False, na=False)]
        
        print(f"🔍 Résultats pour '{search_term}':")
        if len(results) > 0:
            for _, depute in results.iterrows():
                print(f"   - {depute['nom']}")
                if 'nom_circo' in depute:
                    print(f"     Circonscription: {depute['nom_circo']}")
                if 'parti_ratt_financier' in depute:
                    print(f"     Parti: {depute['parti_ratt_financier']}")
        else:
            print("   Aucun résultat trouvé")
    
    return results if 'nom' in df.columns else pd.DataFrame()

def export_by_party(df, party_name, output_file=None):
    """
    Exporte la liste des députés d'un parti spécifique
    
    Args:
        df: DataFrame avec les données des députés
        party_name: Nom du parti
        output_file: Fichier de sortie (optionnel)
    """
    if 'parti_ratt_financier' in df.columns:
        party_deputies = df[df['parti_ratt_financier'].str.contains(party_name, case=False, na=False)]
        
        if output_file is None:
            output_file = f"deputes_{party_name.replace(' ', '_').lower()}.csv"
        
        party_deputies.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"📋 {len(party_deputies)} députés de '{party_name}' exportés vers {output_file}")
        
        return party_deputies
    
    return pd.DataFrame()

def main():
    """Fonction principale d'analyse"""
    print("📊 Analyseur des données des députés français")
    print("=" * 50)
    
    # Analyser les données
    df = analyze_deputes_data()
    
    if df is not None:
        # Créer des visualisations
        print("\n📈 Création des graphiques...")
        create_visualizations(df)
        
        # Exemples de recherche
        print("\n🔍 EXEMPLES DE RECHERCHE")
        search_deputies(df, "Macron")
        
        # Exemple d'export par parti
        print("\n📤 EXEMPLE D'EXPORT PAR PARTI")
        if 'parti_ratt_financier' in df.columns:
            parties = df['parti_ratt_financier'].value_counts().head(3)
            for party in parties.index:
                export_by_party(df, party)
        
        print("\n🎉 Analyse terminée!")
        print("\n💡 Fonctions disponibles:")
        print("   - analyze_deputes_data(): Analyse générale")
        print("   - search_deputies(): Recherche par nom")
        print("   - export_by_party(): Export par parti")
        print("   - create_visualizations(): Graphiques")

if __name__ == "__main__":
    main()
