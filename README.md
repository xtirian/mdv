```kotlin
pdfapp/
├── venv/                     ← ambiente virtual (não versionar)
├── main.py                   ← ponto de entrada da aplicação (Tkinter inicia aqui)
├── ui/                       ← elementos da interface (Tkinter)
│   └── app_window.py         ← janela principal da aplicação
├── pdf/                      ← lógica de leitura e extração de PDF
│   └── extractor.py          ← extrator de dados dos PDFs
├── export/                   ← exportação dos dados
│   └── excel_exporter.py     ← função para exportar para Excel
├── utils/                    ← funções auxiliares
│   └── helpers.py            ← qualquer lógica genérica ou reutilizável
├── assets/                   ← ícones, imagens ou arquivos fixos
├── requirements.txt
└── README.md                 ← descrição do projeto (opcional)

```