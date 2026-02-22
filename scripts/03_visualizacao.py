
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

CAMINHO_BASE = Path(__file__).parent.parent
DIR_RESULTADOS = CAMINHO_BASE / "dados/resultados"
DIR_MAPAS = CAMINHO_BASE / "outputs/mapas"
DIR_MAPAS.mkdir(parents=True, exist_ok=True)

AUTOR_MAPA = "Luiza"

def criar_mapa_tematico(resultado):
    print("\nCRIANDO MAPA TEMATICO...")
    fig, ax = plt.subplots(1, 1, figsize=(15, 12))
    
    resultado.plot(
        column='perc_desmat',
        ax=ax,
        legend=True,
        cmap='YlOrRd',
        edgecolor='black',
        linewidth=0.5,
        legend_kwds={'label': "% de Desmatamento", 'orientation': "vertical", 'shrink': 0.7}
    )
    
    ax.set_title(
        f'Propriedades Rurais com Desmatamento - Amapa\nTotal: {len(resultado):,} propriedades afetadas',
        fontsize=16, fontweight='bold', pad=20
    )
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    texto = f"Fonte: CAR/SICAR, MapBiomas, PRODES, DETER\nElaboracao: {AUTOR_MAPA}\nData: {pd.Timestamp.now().strftime('%d/%m/%Y')}"
    ax.text(0.02, 0.02, texto, transform=ax.transAxes, fontsize=9, verticalalignment='bottom', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    caminho_saida = DIR_MAPAS / "mapa_desmatamento_amapa.png"
    plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
    print(f"   Mapa salvo: {caminho_saida}")
    plt.close()

def criar_graficos_estatisticos(resultado):
    print("\nCRIANDO GRAFICOS ESTATISTICOS...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Analise Estatistica - Desmatamento no Amapa', fontsize=16, fontweight='bold', y=0.995)
    
    # distribuição %
    ax1 = axes[0, 0]
    resultado['perc_desmat'].hist(bins=30, ax=ax1, color='coral', edgecolor='black')
    ax1.set_xlabel('% de Desmatamento', fontsize=11)
    ax1.set_ylabel('Frequencia', fontsize=11)
    ax1.set_title('Distribuicao do % de Desmatamento', fontsize=12, fontweight='bold')
    ax1.axvline(resultado['perc_desmat'].median(), color='red', linestyle='--', 
                label=f'Mediana: {resultado["perc_desmat"].median():.1f}%')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Top 10 propriedades
    ax2 = axes[0, 1]
    top10 = resultado.nlargest(10, 'area_desmat_ha')
    colunas_id_possiveis = ['cod_imovel', 'codigo', 'NUM_AREA', 'num_area']
    coluna_id_encontrada = next((c for c in colunas_id_possiveis if c in top10.columns), None)
    y_labels = top10[coluna_id_encontrada].astype(str).str[:15] if coluna_id_encontrada else [f'Prop {i+1}' for i in range(len(top10))]
    ax2.barh(range(len(top10)), top10['area_desmat_ha'], color='darkred')
    ax2.set_yticks(range(len(top10)))
    ax2.set_yticklabels(y_labels, fontsize=9)
    ax2.set_xlabel('Area Desmatada (ha)', fontsize=11)
    ax2.set_title('Top 10 Propriedades com Maior Desmatamento', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # boxplot
    ax3 = axes[1, 0]
    resultado.boxplot(column='area_desmat_ha', ax=ax3, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    ax3.set_ylabel('Area Desmatada (ha)', fontsize=11)
    ax3.set_title('Distribuicao da Area Desmatada', fontsize=12, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # Scatter
    ax4 = axes[1, 1]
    scatter = ax4.scatter(
        resultado['area_total_ha'], 
        resultado['area_desmat_ha'],
        c=resultado['perc_desmat'],
        cmap='YlOrRd',
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    ax4.set_xlabel('Area Total da Propriedade (ha)', fontsize=11)
    ax4.set_ylabel('Area Desmatada (ha)', fontsize=11)
    ax4.set_title('Relacao: Area Total x Area Desmatada', fontsize=12, fontweight='bold')
    ax4.grid(alpha=0.3)
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('% Desmatamento', fontsize=10)
    
    plt.tight_layout()
    caminho_saida = DIR_MAPAS / "graficos_estatisticos.png"
    plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
    print(f"   Graficos salvos: {caminho_saida}")
    plt.close()

def gerar_resumo_estatistico(resultado):
    print("\nGERANDO RESUMO ESTATISTICO...")
    resumo = f"""
{'='*80}
RELATORIO ESTATISTICO - DESMATAMENTO EM PROPRIEDADES RURAIS DO AMAPA
{'='*80}

RESUMO GERAL
   • Total de propriedades com desmatamento: {len(resultado):,}
   • Area total das propriedades afetadas: {resultado['area_total_ha'].sum():,.2f} ha
   • Area total desmatada: {resultado['area_desmat_ha'].sum():,.2f} ha
   • % medio de desmatamento por propriedade: {resultado['perc_desmat'].mean():.2f}%

{'='*80}
"""
    caminho_saida = DIR_MAPAS / "resumo_estatistico.txt"
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(resumo)
    print(resumo)
    print(f"   Resumo salvo: {caminho_saida}")

def main():
    print("="*80)
    print("VISUALIZACAO E ANALISE ESTATISTICA")
    print("="*80)
    
    print("\nCarregando resultados...")
    resultado = gpd.read_file(DIR_RESULTADOS / "propriedades_com_desmatamento.gpkg")
    print(f"   {len(resultado):,} registros carregados")
    
    criar_mapa_tematico(resultado)
    criar_graficos_estatisticos(resultado)
    gerar_resumo_estatistico(resultado)

if __name__ == "__main__":
    main()
