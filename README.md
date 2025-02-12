# Stellar Data Management - Exemplo de Uso

Este repositório contém um exemplo simples de como interagir com a rede **Stellar** usando a **Stellar SDK** para adicionar e consultar dados em contas Stellar. O código usa a rede de **Testnet** para realizar operações sem risco de gastar tokens reais.

## Funcionalidades

O script realiza duas operações principais:

1. **Adicionar Dados a uma Conta Stellar**:
   - A função `add_data_to_account` permite armazenar dados arbitrários (nome/valor) associados a uma chave dentro de uma conta Stellar.
   
2. **Consultar Dados Armazenados em uma Conta Stellar**:
   - A função `query_data` permite consultar dados armazenados em uma conta Stellar pela chave associada.

## Requisitos

Certifique-se de ter o ambiente de desenvolvimento preparado com as seguintes dependências:

- **Python 3.x**
- **requests**: Usado para fazer requisições HTTP.
- **stellar-sdk**: A biblioteca oficial da Stellar para interagir com a rede Stellar.

Você pode instalar as dependências necessárias usando o `pip`:

```bash
pip install requests stellar-sdk
