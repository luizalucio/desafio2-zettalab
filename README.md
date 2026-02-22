# Desafio 2 Zettalab: Identificação de Desmatamento em Propriedades Rurais do Amapá

Este projeto foi desenvolvido como parte do Programa Zettalab - Desafio 2, um programa de seleção, desenvolvimento e integração de alunos da Universidade Federal de Lavras (UFLA), conduzido pela Agência Zetta/UFLA de Inovação, Geotecnologia e Sistemas Inteligentes. O desafio foca na aplicação de geotecnologias para a análise ambiental.

## Objetivo do Projeto

Este projeto tem como objetivo identificar propriedades rurais do estado do Amapá que apresentem áreas de desmatamento dentro de seus limites geográficos, utilizando exclusivamente dados públicos de geoinformação. Para cada propriedade afetada, são calculadas a área total do imóvel, a área desmatada sobreposta e uma indicação de potencial sujeição à suspensão de comercialização de produtos.

Este projeto tem como objetivo identificar propriedades rurais no estado do Amapá que apresentem áreas de desmatamento dentro de seus limites geográficos, utilizando exclusivamente dados públicos de geoinformação. Para cada propriedade afetada, são calculadas a área total do imóvel, a área desmatada sobreposta e uma indicação de potencial sujeição à suspensão de comercialização de produtos.

## Visão Geral do Desafio

O desafio consiste em analisar a sobreposição de dados de desmatamento com registros de propriedades rurais para:
1.  Identificar todas as propriedades rurais do Amapá com qualquer área de desmatamento.
2.  Apresentar para cada propriedade afetada:
    *   Área total do imóvel (hectares).
    *   Área desmatada sobreposta (hectares).
    *   Indicação de "sujeito à suspensão" devido a ilícito ambiental.

## Fontes de Dados

Foram utilizadas as seguintes bases de dados geoespaciais públicas:
*   Cadastro Ambiental Rural (CAR/SICAR): Representa os limites geográficos das propriedades rurais.
*   PRODES (Monitoramento da Floresta Amazônica Brasileira por Satélite): Dados anuais de desmatamento consolidado.
*   DETER (Detecção de Desmatamento em Tempo Real): Alertas diários de desmatamento.
*   MapBiomas Alerta: Mapeamento do uso e cobertura da terra com alertas de desmatamento.

## Metodologia (Scripts)

O projeto é organizado em uma série de scripts Python que executam as etapas de verificação, preparação, análise e visualização dos dados.

### `00_verificar_dados.py`
Este script verifica a existência e as informações básicas dos shapefiles brutos baixados. Ele confere se os arquivos `.shp` estão presentes nos caminhos esperados e exibe detalhes como número de registros e sistemas de coordenadas.

### `01_preparacao_dados.py`
Responsável por carregar, validar e padronizar as bases geoespaciais. As principais etapas incluem:
*   Carregamento dos shapefiles brutos.
*   Projeção para um Sistema de Coordenadas de Referência (CRS) padrão (`EPSG:31982`) para garantir compatibilidade nas análises espaciais.
*   Limpeza e filtragem dos dados, como a seleção de propriedades no Amapá para o CAR e a remoção de geometrias inválidas.
*   Salvamento das camadas processadas em `dados/processados`.

### `02_analise_intersecao.py`
Este é o coração da análise, onde os dados de desmatamento são cruzados com as propriedades do CAR:
*   **Consolidação do Desmatamento:** Combina os dados de desmatamento do MapBiomas, PRODES e DETER em uma única camada. Uma etapa de `dissolve` foi ativada para unir polígonos sobrepostos e evitar dupla contagem.
*   **Intersecção:** Realiza a operação de `overlay` entre as propriedades do CAR limpas e a camada consolidada de desmatamento para identificar as áreas de sobreposição.
*   **Cálculo de Áreas:** Calcula a área total das propriedades e a área desmatada dentro de cada propriedade, ambas em hectares.
*   **Identificação de Ilicitude:** Adiciona uma coluna `sujeito_suspensao` com "SIM" para todas as propriedades que possuem alguma área desmatada, indicando potencial ilícito ambiental.
*   **Salvamento de Resultados:** Os resultados são salvos em formato Shapefile, GeoPackage, CSV e Excel em `dados/resultados`.

### `03_visualizacao.py`
Gera visualizações dos resultados da análise:
*   **Mapa Temático:** Um mapa do Amapá mostrando as propriedades rurais com desmatamento, coloridas de acordo com o percentual de área desmatada.
*   **Gráficos Estatísticos:** Um conjunto de gráficos (histograma, top 10 propriedades, boxplot e scatter plot) para fornecer uma análise estatística do desmatamento.
*   **Resumo Estatístico:** Um arquivo de texto (`resumo_estatistico.txt`) com as principais estatísticas da análise.
Todas as visualizações são salvas em `outputs/mapas`.

## Resultados Visuais

Aqui estão as visualizações geradas pela análise do projeto, destacando as propriedades rurais com desmatamento no Amapá e estatísticas relevantes.

## Próximos Passos e Melhorias

*   Validação do CAR: Implementar validações mais robustas para os dados do CAR, como verificação de CNPJ/CPF duplicados ou inconsistências cadastrais.
*   Critérios de Suspensão: Refinar a lógica da coluna `sujeito_suspensao` com base em critérios mais detalhados (e.g., percentual de desmatamento tolerável, data do desmatamento).
*   Otimização de Performance: Para grandes volumes de dados, explorar otimizações como o uso de índices espaciais mais avançados ou processamento em paralelo.
*   Interface Gráfica: Desenvolver uma interface gráfica simples para facilitar a interação com a análise por usuários não técnicos.

Espero que este projeto demonstre minhas habilidades em geoprocessamento e análise de dados espaciais.

Luíza Helena
