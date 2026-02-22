import os
import shutil
import glob

def main():
    print("Iniciando a criação da pasta de entrega...")

    entrega_dir = 'entrega'
    
    # subpastas na pasta de entrega
    entrega_dados_dir = os.path.join(entrega_dir, 'dados')
    entrega_mapas_dir = os.path.join(entrega_dir, 'mapas')
    entrega_scripts_dir = os.path.join(entrega_dir, 'scripts')
    
    # caminhos de origem
    resultados_dir = os.path.join('dados', 'resultados')
    mapas_dir = os.path.join('outputs', 'mapas')
    scripts_dir = 'scripts'

    if os.path.exists(entrega_dir):
        shutil.rmtree(entrega_dir)
        print(f"Pasta '{entrega_dir}' existente removida.")
    
    os.makedirs(entrega_dados_dir, exist_ok=True)
    os.makedirs(entrega_mapas_dir, exist_ok=True)
    os.makedirs(entrega_scripts_dir, exist_ok=True)
    print(f"Estrutura de pastas em '{entrega_dir}' criada.")

    print("
Copiando arquivos de resultados...")
    arquivos_resultados = glob.glob(os.path.join(resultados_dir, '*'))
    if not arquivos_resultados:
        print(f"Aviso: Nenhum arquivo encontrado em '{resultados_dir}'. Verifique se o script 02 foi executado.")
    else:
        for f_path in arquivos_resultados:
            shutil.copy(f_path, entrega_dados_dir)
            print(f" - Copiado: {os.path.basename(f_path)}")

    print("
Copiando mapas e gráficos...")
    arquivos_mapas = glob.glob(os.path.join(mapas_dir, '*'))
    if not arquivos_mapas:
        print(f"Aviso: Nenhum arquivo encontrado em '{mapas_dir}'. Verifique se o script 03 foi executado.")
    else:
        for f_path in arquivos_mapas:
            shutil.copy(f_path, entrega_mapas_dir)
            print(f" - Copiado: {os.path.basename(f_path)}")

    print("
Copiando scripts...")
    arquivos_scripts = glob.glob(os.path.join(scripts_dir, '*.py'))
    for f_path in arquivos_scripts:
        shutil.copy(f_path, entrega_scripts_dir)
        print(f" - Copiado: {os.path.basename(f_path)}")
            
    print("
Copiando arquivos da raiz do projeto...")
    files_to_copy_from_root = ['requirements.txt', 'README.md']
    for file_name in files_to_copy_from_root:
        if os.path.exists(file_name):
            shutil.copy(file_name, entrega_dir)
            print(f" - Copiado: {file_name}")
        else:
            print(f"Aviso: Arquivo '{file_name}' não encontrado na raiz do projeto.")

    print("
Processo de criação da pasta de entrega concluído com sucesso!")

if __name__ == '__main__':
    main()
