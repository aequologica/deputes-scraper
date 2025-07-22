#!/usr/bin/env python3
"""
Script simple pour télécharger la liste des députés français
Version rapide et minimaliste
"""

import pandas as pd
import requests

def download_deputes_simple():
    """
    Télécharge la liste des députés depuis NosDéputés.fr
    Source la plus fiable et bien documentée
    """
    print("📥 Téléchargement de la liste des députés...")
    
    # URL de l'API NosDéputés.fr (JSON)
    url = "https://www.nosdeputes.fr/deputes/json"
    
    try:
        # Télécharger les données JSON
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extraire la liste des députés 
        deputes_data = []
        for depute_info in data['deputes']:
            depute = depute_info['depute']
            deputes_data.append(depute)
        
        # Créer DataFrame
        df = pd.DataFrame(deputes_data)
        
        # Sauvegarder
        output_file = "deputes_france.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"✅ {len(df)} députés téléchargés")
        print(f"📁 Fichier sauvé: {output_file}")
        
        # Afficher les colonnes disponibles
        print(f"\n📋 Colonnes disponibles ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Aperçu des données
        print(f"\n👥 Aperçu des députés:")
        if 'nom' in df.columns:
            cols_to_show = ['nom']
            if 'parti_ratt_financier' in df.columns:
                cols_to_show.append('parti_ratt_financier')
            print(df[cols_to_show].head(10).to_string(index=False))
        
        return df
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def download_deputes_enrichi():
    """
    Télécharge les données enrichies avec statistiques depuis NosDéputés
    (Alternative car l'URL Datan n'est plus accessible)
    """
    print("\n📊 Téléchargement des données enrichies...")
    
    # URL alternative - synthèse des données depuis NosDéputés
    url = "https://www.nosdeputes.fr/synthese/data/json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Créer un DataFrame avec les statistiques disponibles
        if 'deputes' in data:
            df = pd.DataFrame(data['deputes'])
        else:
            print("⚠️ Pas de données enrichies disponibles pour le moment")
            return None
        
        output_file = "deputes_statistiques.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"✅ {len(df)} députés avec statistiques téléchargés")
        print(f"📁 Fichier sauvé: {output_file}")
        
        return df
        
    except Exception as e:
        print(f"⚠️ Données enrichies non disponibles: {e}")
        return None

def download_single_depute(slug):
    """
    Télécharge les détails d'un député spécifique
    
    Args:
        slug: Le slug du député (ex: "emmanuel-macron")
    """
    url = f"https://www.nosdeputes.fr/{slug}/json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(f"📄 Détails de {data['depute']['nom']}:")
        print(f"   Circonscription: {data['depute']['nom_circo']}")
        print(f"   Parti: {data['depute']['parti_ratt_financier']}")
        print(f"   Profession: {data['depute']['profession']}")
        
        return data
        
    except Exception as e:
        print(f"❌ Erreur pour {slug}: {e}")
        return None

if __name__ == "__main__":
    print("🏛️  Téléchargeur simple des députés français")
    print("-" * 40)
    
    # Télécharger la liste principale
    df_principal = download_deputes_simple()
    
    # Télécharger les données enrichies
    df_enrichi = download_deputes_enrichi()
    
    print("\n🎉 Téléchargement terminé!")
    print("\n💡 Utilisation:")
    print("   - deputes_france.csv : Liste complète des députés")
    print("   - deputes_statistiques.csv : Avec scores de participation, loyauté, etc.")
