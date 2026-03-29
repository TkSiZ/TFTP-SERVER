# 📡 Servidor TFTP Assíncrono

Um servidor TFTP (Trivial File Transfer Protocol) leve e assíncrono, implementado em Python com `asyncio`. Suporta operações de download (RRQ) e upload (WRQ) de arquivos, com gerenciamento de retransmissão e proteção contra path traversal.

---

## ✨ Funcionalidades

- **I/O Assíncrono** — construído sobre `asyncio` para tratamento de requisições concorrentes e não bloqueantes
- **RRQ (Requisição de Leitura)** — serve arquivos aos clientes com retransmissão automática em caso de timeout
- **WRQ (Requisição de Escrita)** — recebe uploads de arquivos dos clientes
- **Gerenciador de Retransmissão** — lógica de tentativas configurável com timeout por bloco
- **Proteção contra Path Traversal** — restringe todo acesso a arquivos ao diretório base configurado
- **Arquitetura Modular** — separação clara entre protocolo, handlers, sessão e camadas do servidor

---

## 🗂️ Estrutura do Projeto

```
.
├── main.py                   # Ponto de entrada — inicializa o servidor UDP
├── config.py                 # Configurações do servidor (host, porta, timeouts, etc.)
│
├── protocol/
│   ├── packet.py             # Construtor e parser de pacotes TFTP
│   └── options.py            # Negociação de opções TFTP (OACK)
│
├── server/
│   ├── core.py               # DatagramProtocol do asyncio — despacha requisições
│   ├── session.py            # Sessão por cliente (socket, envio/recebimento, caminho do arquivo)
│   └── retransmit.py         # Lógica de retransmissão com tentativas configuráveis
│
├── handlers/
│   ├── base.py               # Classe base abstrata TransferHandler
│   ├── rrq.py                # Handler de Requisição de Leitura
│   └── wrq.py                # Handler de Requisição de Escrita
│
├── services/
│   └── file_service.py       # Utilitário de resolução segura de caminhos de arquivo
│
├── utils/
│   ├── file_utils.py         # Utilitário de junção de caminhos seguro contra traversal
│   └── logger.py             # Configuração básica de logging
│
└── tests/
    └── test_packet.py        # Testes unitários para parsing e construção de pacotes
```

---

## ⚙️ Configuração

Todas as configurações estão em `config.py`:

| Parâmetro     | Padrão          | Descrição                                      |
|---------------|-----------------|------------------------------------------------|
| `HOST`        | `0.0.0.0`       | Endereço de escuta                             |
| `PORT`        | `6969`          | Porta UDP                                      |
| `BLOCK_SIZE`  | `512`           | Tamanho do bloco de transferência (bytes)      |
| `TIMEOUT`     | `3`             | Segundos de espera por ACK antes de retentar   |
| `MAX_RETRIES` | `5`             | Número máximo de tentativas de retransmissão   |
| `BASE_DIR`    | `./tftp_root`   | Diretório raiz para arquivos servidos/recebidos|

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) (recomendado) ou `pip`

### Instalar dependências

```bash
uv sync
# ou
pip install -r requirements.txt
```

### Iniciar o servidor

```bash
python main.py
```

O servidor começará a escutar em `0.0.0.0:6969` e criará automaticamente o diretório `./tftp_root` caso ele não exista.

```
TFTP server running on 0.0.0.0:6969
```

---

## 🧪 Executando os Testes

```bash
pytest
```

Os testes cobrem a construção e o parsing de pacotes ACK, DATA e RRQ.

---

## 📦 Suporte ao Protocolo TFTP

| Opcode | Operação | Status       |
|--------|----------|--------------|
| 1      | RRQ      | ✅ Suportado  |
| 2      | WRQ      | ✅ Suportado  |
| 3      | DATA     | ✅ Tratado    |
| 4      | ACK      | ✅ Tratado    |
| 5      | ERROR    | ✅ Enviado    |
| 6      | OACK     | ⚙️ Construído (parsing de opções disponível) |

---

## 🔒 Segurança

- Todos os caminhos de arquivo são resolvidos com `os.path.abspath` e validados contra o `BASE_DIR` configurado antes de qualquer operação, prevenindo ataques de path traversal (ex: `../../etc/passwd`).
- Qualquer requisição que tente escapar do diretório base recebe uma resposta de **Violação de Acesso (código de erro 2)**.

---

## 🏗️ Visão Geral da Arquitetura

```
Pacote UDP do Cliente
        │
        ▼
TFTPServerProtocol (server/core.py)
  asyncio.DatagramProtocol
        │
        ▼
  TFTPSession (server/session.py)
  Socket + contexto de requisição por cliente
        │
        ├──▶ RRQHandler (handlers/rrq.py)
        │      └── RetransmissionManager
        │
        └──▶ WRQHandler (handlers/wrq.py)
```

Cada datagrama UDP recebido é despachado como uma tarefa `asyncio` independente, criando uma `TFTPSession` isolada por cliente. A sessão mantém seu próprio socket UDP, permitindo transferências simultâneas sem bloqueio.

---
