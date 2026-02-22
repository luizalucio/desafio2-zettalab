
from pathlib import Path

CAMINHO_BASE = Path(__file__).parent.parent

# lista dos shapefiles que vou conferir
ARQUIVOS = {
    'SICAR': CAMINHO_BASE / "dados/brutos/sicar/AREA_IMOVEL_1.shp",
    'MapBiomas': CAMINHO_BASE / "dados/brutos/mapbiomas/dashboard_alerts-shapefile.shp",
    'PRODES': CAMINHO_BASE / "dados/brutos/prodes/yearly_deforestation_biome.shp",
    'DETER': CAMINHO_BASE / "dados/brutos/deter/deter-nf-deter-public.shp",
}

# funções

def verificar_shapefile(caminho, nome):

    caminho = Path(caminho)

    print(f"\n{'='*80}")
    print(f"{nome}")
    print(f"Caminho: {caminho}")
    print('='*80)

    if not caminho.exists():
        print("ARQUIVO NÃO ENCONTRADO!")
        return

    if caminho.suffix.lower() != ".shp":
        print("O arquivo encontrado não é um shapefile (.shp)")
        return

    tamanho_mb = caminho.stat().st_size / (1024 * 1024)

    print("Shapefile encontrado com sucesso!")
    print(f"Nome do arquivo: {caminho.name}")
    print(f"Tamanho aproximado: {tamanho_mb:.2f} MB")
    print(f"Pasta: {caminho.parent}")

def main():
    print("="*80)
    print("VERIFICAÇÃO DOS DADOS BAIXADOS")
    print("="*80)

    # Passo por cada arquivo e verifico se está correto
    for nome, caminho in ARQUIVOS.items():
        verificar_shapefile(caminho, nome)

    print("\n" + "="*80)
    print("VERIFICAÇÃO CONCLUÍDA!")
    print("="*80)
    print("\nPRÓXIMOS PASSOS SUGERIDOS:")
    print("   1. Confirmar se os shapefiles são os corretos")
    print("   2. Conferir sistema de coordenadas (CRS) de cada shapefile")
    print("   3. Usar esses caminhos no script 01_preparacao_dados.py")

if __name__ == "__main__":
    main()
