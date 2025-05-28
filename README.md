
# BioReport Auto

**BioReport Auto** é um gerador automático de relatórios científicos para experimentos com dois grupos (ex: Controle vs Tratamento).

## Estrutura de pastas

```
bio_report_auto/
├── data/               # CSVs com dados experimentais
│   └── exemplo_dados.csv
├── images/             # Gráficos gerados
├── output/             # Relatórios gerados
├── templates/          # Templates HTML (Jinja2)
├── main.py             # Script principal
└── README.md           # Instruções e explicações
```

## Como rodar

1. Instale os pacotes:

```bash
pip install pandas seaborn matplotlib scipy jinja2 weasyprint
```

2. Execute o script:

```bash
python main.py
```

## Exemplo de entrada (.csv)

```csv
Amostra,Grupo,Valor
1,Controle,5.1
2,Controle,4.9
3,Controle,5.3
4,Controle,5.0
5,Controle,5.2
6,Tratamento,6.8
7,Tratamento,6.5
8,Tratamento,6.9
9,Tratamento,7.1
10,Tratamento,6.7
```
