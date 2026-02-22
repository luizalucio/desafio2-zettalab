

import geopandas as gpd
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

CAMINHO_BASE = Path(__file__).parent.parent

# caminhos dos shapefiles brutos
CAMINHOS = {
    'sicar': CAMINHO_BASE / "dados/brutos/sicar/AREA_IMOVEL_1.shp",
    'mapbiomas': CAMINHO_BASE / "dados/brutos/mapbiomas/dashboard_alerts-shapefile.shp",
    'prodes': CAMINHO_BASE / "dados/brutos/prodes/yearly_deforestation_biome.shp",
    'deter': CAMINHO_BASE / "dados/brutos/deter/deter-nf-deter-public.shp"
}

CRS_PADRAO = "EPSG:31982"

DIR_SAIDA = CAMINHO_BASE / "dados/processados"
DIR_SAIDA.mkdir(parents=True, exist_ok=True)

# funções

def verificar_arquivo(caminho):
    """Confere se o arquivo existe"""
    if not caminho.exists():
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return False
    print(f"Arquivo encontrado: {caminho.name}")
    return True

def carregar_shapefile(caminho, nome):
    """Carrega shapefile e mostra informações básicas"""
    try:
        gdf = gpd.read_file(caminho)
        print(f"\n{nome}")
        print(f"   - Registros: {len(gdf):,}")
        print(f"   - CRS atual: {gdf.crs}")
        print(f")