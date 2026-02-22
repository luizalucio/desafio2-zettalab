

import geopandas as gpd
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

CAMINHO_BASE = Path(__file__).parent.parent
DIR_PROCESSADOS = CAMINHO_BASE / "dados/processados"
DIR_RESULTADOS = CAMINHO_BASE / "dados/resultados"
DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)

def consolidar_desmatamento():
    print("\nCONSOLIDANDO CAMADAS DE DESMATAMENTO...")
    
    camadas = []
    
    mapbiomas_path = DIR_PROCESSADOS / "mapbiomas_amapa_limpo.shp"
    if mapbiomas_path.exists():
        mapbiomas = gpd.read_file(mapbiomas_path)
        mapbiomas['fonte'] = 'MapBiomas'
        camadas.append(mapbiomas[['geometry', 'fonte']])
        print(f"   MapBiomas: {len(mapbiomas):,} poligonos")
    
    prodes_path = DIR_PROCESSADOS / "prodes_amapa_limpo.shp"
    if prodes_path.exists():
        prodes = gpd.read_file(prodes_path)
        prodes['fonte'] = 'PRODES'
        camadas.append(prodes[['geometry', 'fonte']])
        print(f"   PRODES: {len(prodes):,} poligonos")
    
    deter_path = DIR_PROCESSADOS / "deter_amapa_limpo.shp"
    if deter_path.exists():
        deter = gpd.read_file(deter_path)
        deter['fonte'] = 'DETER'
        camadas.append(deter[['geometry', 'fonte']])
        print(f"   DETER: {len(deter):,} poligonos")
    
    if not camadas:
        raise FileNotFoundError("Nenhuma camada de desmatamento encontrada!")
    
    desmatamento = pd.concat(camadas, ignore_index=True)
    print(f"\n   Total consolidado: {len(desmatamento):,} poligonos")
    
    print("   Dissolvendo sobreposicoes...")
    desmatamento_unico = desmatamento.dissolve()
    desmatamento_unico = desmatamento_unico.explode(index_parts=False).reset_index(drop=True)
    print(f"   Apos dissolucao: {len(desmatamento_unico):,} poligonos unicos")
    
    caminho_saida = DIR_PROCESSADOS / "desmatamento_consolidado.shp"
    desmatamento_unico.to_file(caminho_saida)
    print(f"   Salvo em: {caminho_saida}")
    
    return desmatamento_unico

def realizar_intersecao(car, desmatamento):
    print("\nREALIZANDO INTERSECAO CAR x DESMATAMENTO...")
    print(f"   CAR: {len(car):,} propriedades")
    print(f"   Desmatamento: {len(desmatamento):,} poligonos")
    
    print("   Processando intersecao (pode demorar alguns minutos)...")
    intersecao = gpd.overlay(
        car, 
        desmatamento, 
        how='intersection',
        keep_geom_type=False
    )
    
    print(f"   {len(intersecao):,} intersecoes encontradas")
    
    return intersecao

def calcular_areas(intersecao, car):
    print("\nCALCULANDO AREAS...")
    
    intersecao['area_desmat_m2'] = intersecao.geometry.area
    intersecao['area_desmat_ha'] = intersecao['area_desmat_m2'] / 10000
    
    car_areas = car.copy()
    car_areas['area_total_m2'] = car_areas.geometry.area
    car_areas['area_total_ha'] = car_areas['area_total_m2'] / 10000
    
    colunas_id = ['cod_imovel', 'codigo', 'car', 'cod_car', 'num_area', 'NUM_AREA']
    coluna_id = None
    for col in colunas_id:
        if col in car.columns:
            coluna_id = col
            print(f"   Usando coluna de identificacao: {col}")
            break
    
    if coluna_id:
        resultado = intersecao.groupby(coluna_id).agg({
            'area_desmat_ha': 'sum'
        }).reset_index()
        
        resultado = resultado.merge(
            car_areas[[coluna_id, 'area_total_ha', 'geometry']],
            on=coluna_id,
            how='left'
        )
        
        resultado['perc_desmat'] = (
            resultado['area_desmat_ha'] / resultado['area_total_ha'] * 100
        ).round(2)
        
        resultado['sujeito_suspensao'] = 'SIM'
        
        resultado = gpd.GeoDataFrame(resultado, geometry='geometry', crs=car.crs)
        
        print(f"   Areas calculadas para {len(resultado):,} propriedades")
        print(f"\n   ESTATISTICAS:")
        print(f"      - Area total media: {resultado['area_total_ha'].mean():.2f} ha")
        print(f"      - Area desmatada media: {resultado['area_desmat_ha'].mean():.2f} ha")
        print(f"      - % desmatamento medio: {resultado['perc_desmat'].mean():.2f}%")
        print(f"      - Desmatamento total: {resultado['area_desmat_ha'].sum():.2f} ha")
        
        return resultado
    else:
        print("   Coluna de identificacao nao encontrada no CAR")
        print(f"   Colunas disponiveis: {list(car.columns)}")
        return intersecao

def main():
    print("="*80)
    print("ANALISE DE INTERSECAO - Propriedades com Desmatamento")
    print("="*80)
    
    print("\n1. CARREGANDO CAR...")
    car = gpd.read_file(DIR_PROCESSADOS / "car_amapa_limpo.shp")
    print(f"   {len(car):,} propriedades carregadas")
    
    print("\n2. CONSOLIDANDO DESMATAMENTO...")
    desmatamento = consolidar_desmatamento()
    
    print("\n3. REALIZANDO INTERSECAO...")
    intersecao = realizar_intersecao(car, desmatamento)
    
    print("\n4. CALCULANDO AREAS...")
    resultado = calcular_areas(intersecao, car)
    
    print("\n5. SALVANDO RESULTADOS...")
    
    caminho_shp = DIR_RESULTADOS / "propriedades_com_desmatamento.shp"
    resultado.to_file(caminho_shp)
    print(f"   Shapefile: {caminho_shp}")
    
    caminho_gpkg = DIR_RESULTADOS / "propriedades_com_desmatamento.gpkg"
    resultado.to_file(caminho_gpkg, driver='GPKG')
    print(f"   GeoPackage: {caminho_gpkg}")
    
    resultado_csv = resultado.drop(columns='geometry')
    caminho_csv = DIR_RESULTADOS / "relatorio_desmatamento.csv"
    resultado_csv.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
    print(f"   CSV: {caminho_csv}")
    
    caminho_xlsx = DIR_RESULTADOS / "relatorio_desmatamento.xlsx"
    resultado_csv.to_excel(caminho_xlsx, index=False, engine='openpyxl')
    print(f"   Excel: {caminho_xlsx}")
    
    print("\n" + "="*80)
    print("ANALISE CONCLUIDA!")
    print("="*80)
    
    return resultado

if __name__ == "__main__":
    resultado = main()


