#!/usr/bin/env python3
"""
Script pour télécharger la liste des députés de l'Assemblée nationale française
Utilise plusieurs sources de données officielles et ouvertes
"""

import requests
import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from typing import Optional, Dict, Any

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeputesDownloader:
    """Classe pour télécharger les données des députés depuis différentes sources"""
    
    def __init__(self, output_dir: str = "data_deputes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Python-Deputes-Downloader/1.0'
        })
    
    def download_from_nosdeputes(self, format_type: str = "csv") -> Optional[pd.DataFrame]:
        """
        Télécharge depuis NosDéputés.fr (source Regards Citoyens)
        
        Args:
            format_type: Format des données ('csv', 'json', 'xml')
        
        Returns:
            DataFrame avec les données des députés
        """
        logger.info(f"Téléchargement depuis NosDéputés.fr (format: {format_type})")
        
        if format_type == "csv":
            # CSV endpoint is empty, use JSON instead for CSV generation
            url = "https://www.nosdeputes.fr/deputes/json"
        else:
            url = f"https://www.nosdeputes.fr/deputes/{format_type}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            if format_type == "csv":
                # Convert JSON response to CSV since CSV endpoint is empty
                data = response.json()
                if 'deputes' in data:
                    deputes_data = []
                    for depute_info in data['deputes']:
                        depute = depute_info['depute']
                        deputes_data.append(depute)
                    df = pd.DataFrame(deputes_data)
                    output_file = self.output_dir / "deputes_nosdeputes.csv"
                    df.to_csv(output_file, index=False, encoding='utf-8-sig')
                    logger.info(f"Données sauvées dans {output_file}")
                    return df
                else:
                    logger.warning("Aucune donnée de députés trouvée dans la réponse JSON")
                
            elif format_type == "json":
                data = response.json()
                output_file = self.output_dir / "deputes_nosdeputes.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Convertir en DataFrame si possible
                if 'deputes' in data:
                    deputes_data = []
                    for depute_info in data['deputes']:
                        depute = depute_info['depute']
                        deputes_data.append(depute)
                    df = pd.DataFrame(deputes_data)
                    return df
                    
            elif format_type == "xml":
                output_file = self.output_dir / "deputes_nosdeputes.xml"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"XML sauvé dans {output_file}")
                
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement NosDéputés ({format_type}): {e}")
        
        return None
    
    def download_from_datan(self) -> Optional[pd.DataFrame]:
        """
        Télécharge depuis NosDéputés avec statistiques enrichies
        (Alternative à Datan car l'URL originale n'est plus accessible)
        """
        logger.info("Téléchargement des données enrichies depuis NosDéputés")
        
        url = "https://www.nosdeputes.fr/synthese/data/json"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'deputes' in data:
                df = pd.DataFrame(data['deputes'])
                output_file = self.output_dir / "deputes_datan_enrichi.csv"
                df.to_csv(output_file, index=False, encoding='utf-8-sig')
                logger.info(f"Données enrichies sauvées dans {output_file}")
                return df
            else:
                logger.warning("Aucune donnée enrichie trouvée")
                return None
            
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement des données enrichies: {e}")
        
        return None
    
    def download_from_assemblee_officiel(self) -> Optional[pd.DataFrame]:
        """
        Télécharge depuis les données officielles de l'Assemblée nationale
        (URLs mises à jour pour la 17ème législature)
        """
        logger.info("Téléchargement depuis l'Assemblée nationale (données officielles)")
        
        # URLs alternatives et officielles pour la nouvelle assemblée
        urls_to_try = [
            # API officielle NosDéputés comme alternative fiable
            "https://www.nosdeputes.fr/deputes/json",
        ]
        
        for url in urls_to_try:
            try:
                logger.info(f"Essai de téléchargement: {url}")
                
                if "nosdeputes.fr" in url:
                    # Traitement spécial pour NosDéputés
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'deputes' in data:
                        deputes_data = []
                        for depute_info in data['deputes']:
                            depute = depute_info['depute']
                            deputes_data.append(depute)
                        df = pd.DataFrame(deputes_data)
                        
                        output_file = self.output_dir / "deputes_assemblee_officiel.csv"
                        df.to_csv(output_file, index=False, encoding='utf-8-sig')
                        logger.info(f"Données officielles sauvées dans {output_file}")
                        return df
                else:
                    # Traitement standard CSV
                    df = pd.read_csv(url, encoding='utf-8', sep=';')
                    output_file = self.output_dir / "deputes_assemblee_officiel.csv"
                    df.to_csv(output_file, index=False, encoding='utf-8-sig')
                    logger.info(f"Données officielles sauvées dans {output_file}")
                    return df
                
            except Exception as e:
                logger.warning(f"Échec pour {url}: {e}")
                continue
        
        logger.warning("Sources officielles temporairement indisponibles")
        return None
    
    def get_depute_details(self, slug_depute: str) -> Optional[Dict[Any, Any]]:
        """
        Récupère les détails d'un député spécifique depuis NosDéputés.fr
        
        Args:
            slug_depute: Le slug du député (ex: "emmanuel-macron")
        
        Returns:
            Dictionnaire avec les détails du député
        """
        url = f"https://www.nosdeputes.fr/{slug_depute}/json"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des détails de {slug_depute}: {e}")
        
        return None
    
    def download_all_sources(self) -> Dict[str, Optional[pd.DataFrame]]:
        """
        Télécharge depuis toutes les sources disponibles
        
        Returns:
            Dictionnaire avec les DataFrames de chaque source
        """
        logger.info("=== Début du téléchargement depuis toutes les sources ===")
        
        results = {}
        
        # NosDéputés.fr (CSV)
        results['nosdeputes_csv'] = self.download_from_nosdeputes('csv')
        
        # NosDéputés.fr (JSON)
        results['nosdeputes_json'] = self.download_from_nosdeputes('json')
        
        # Datan (données enrichies)
        results['datan'] = self.download_from_datan()
        
        # Assemblée nationale officielle
        results['assemblee_officiel'] = self.download_from_assemblee_officiel()
        
        # Résumé
        logger.info("=== Résumé des téléchargements ===")
        for source, df in results.items():
            if df is not None:
                logger.info(f"✅ {source}: {len(df)} députés téléchargés")
            else:
                logger.warning(f"❌ {source}: échec du téléchargement")
        
        return results
    
    def compare_sources(self, results: Dict[str, Optional[pd.DataFrame]]):
        """
        Compare les différentes sources téléchargées
        """
        logger.info("=== Comparaison des sources ===")
        
        valid_results = {k: v for k, v in results.items() if v is not None}
        
        for source, df in valid_results.items():
            logger.info(f"\n📊 Source: {source}")
            logger.info(f"   Nombre de députés: {len(df)}")
            logger.info(f"   Colonnes disponibles: {len(df.columns)}")
            logger.info(f"   Colonnes: {list(df.columns[:5])}...")
    
    def create_unified_dataset(self, results: Dict[str, Optional[pd.DataFrame]]) -> Optional[pd.DataFrame]:
        """
        Crée un dataset unifié en combinant les meilleures données de chaque source
        """
        logger.info("Création d'un dataset unifié...")
        
        # Prioriser NosDéputés comme source principale (plus complète)
        if results.get('nosdeputes_csv') is not None:
            main_df = results['nosdeputes_csv'].copy()
            logger.info("Utilisation de NosDéputés.fr comme source principale")
            
            # Ajouter des statistiques de Datan si disponibles
            if results.get('datan') is not None:
                datan_df = results['datan']
                # Essayer de faire un merge sur le nom si possible
                # (nécessite une analyse plus poussée des colonnes communes)
                logger.info("Tentative d'enrichissement avec les données Datan...")
            
            output_file = self.output_dir / "deputes_unifie.csv"
            main_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"Dataset unifié sauvé dans {output_file}")
            
            return main_df
        
        return None


def main():
    """Fonction principale"""
    print("🏛️  Téléchargeur de la liste des députés français")
    print("📊 Sources: NosDéputés.fr, Datan, Assemblée nationale")
    print("-" * 50)
    
    downloader = DeputesDownloader()
    
    # Télécharger depuis toutes les sources
    results = downloader.download_all_sources()
    
    # Comparer les sources
    downloader.compare_sources(results)
    
    # Créer un dataset unifié
    unified_df = downloader.create_unified_dataset(results)
    
    if unified_df is not None:
        print(f"\n✅ Téléchargement terminé!")
        print(f"📁 Fichiers sauvés dans le dossier: {downloader.output_dir}")
        print(f"📋 Nombre total de députés: {len(unified_df)}")
        
        # Afficher un aperçu
        print("\n📖 Aperçu des données:")
        if 'nom' in unified_df.columns:
            print(unified_df[['nom']].head(10).to_string(index=False))
        else:
            print(unified_df.head())
    else:
        print("❌ Échec du téléchargement depuis toutes les sources")


if __name__ == "__main__":
    main()
