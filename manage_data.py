# Importação das bibliotecas necessárias
import requests  # Biblioteca para fazer requisições HTTP
from stellar_sdk import Server, Keypair, TransactionBuilder, Network  # Importação das classes necessárias da biblioteca Stellar SDK
from stellar_sdk.operation import ManageData  # Importação da operação ManageData da biblioteca Stellar SDK
import base64 # Biblioteca para para codificar e decodificar dados usando o formato Base64

# Função para adicionar dados a uma conta na rede Stellar
def add_data_to_account(account_id: str, data_name: str, data_value: str):
    # Definindo a chave secreta da conta de origem. Esta chave é necessária para assinar a transação.
    secret = "SDMT7RM5DI6K5LKMD4OU6VZDFOU66RJ4W3L7KRNIHK3KZEV4OQUH3UFB"  # Coloque a chave secreta Stellar de sua preferência
    keypair = Keypair.from_secret(secret)  # Gerando a chave do par (pública/privada) usando a chave secreta

    # Conectando ao servidor Horizon na rede de Testnet. Horizon é o servidor da Stellar que interage com a blockchain.
    server = Server("https://horizon-testnet.stellar.org")

    # Criando a operação de adicionar dados (ManageData) na transação.
    # A operação requer o nome dos dados e o valor a ser associado.
    manage_data_op = ManageData(
        data_name=data_name,  # Nome dos dados (chave)
        data_value=data_value,  # Valor dos dados a ser armazenado
        source=keypair.public_key  # A chave pública da conta de origem, que irá enviar os dados
    )
    
    # Carregando a conta de destino (onde os dados serão adicionados) através do servidor Horizon
    account = server.load_account(account_id)  # Esta função carrega a conta do blockchain Stellar com base no ID da conta

    # Criando a transação. Uma transação no Stellar requer uma conta de origem e uma operação.
    # Aqui, a conta carregada anteriormente é usada como origem.
    transaction = TransactionBuilder(
        source_account=account,  # A conta de origem que pagará pela transação
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE  # A passphrase do Testnet, indicando que é uma rede de testes
    ).append_operation(manage_data_op).build()  # A operação ManageData é adicionada à transação e a transação é construída

    # Assinando a transação com a chave secreta da conta de origem.
    # A assinatura é necessária para autorizar a execução da transação.
    transaction.sign(keypair)

    # Enviando a transação para a rede Stellar através do servidor Horizon
    response = server.submit_transaction(transaction)

    # Exibindo a resposta da transação, que contém o status e o hash da transação
    print("Transação enviada:", response)

# Função para consultar os dados de uma conta no Stellar
def query_data(account_id: str, data_name: str):
    # Construindo a URL para consultar os dados na conta usando a API do Horizon
    url = f"https://horizon-testnet.stellar.org/accounts/{account_id}/data/{data_name}"
    
    # Enviando uma requisição HTTP GET para o servidor Horizon para obter os dados
    response = requests.get(url)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Se a resposta for bem-sucedida, convertemos o conteúdo JSON em um dicionário Python
        data = response.json()
        print(f"Dados encontrados: {data}")
    else:
        # Caso contrário, exibimos o erro com o código de status da resposta e a mensagem de erro
        print(f"Erro ao consultar dados: {response.status_code}, {response.text}")

# Exemplo de uso das funções
account_id = "GAQ3DMYZ37GE5YIYTN75N7KONOCUTOJTCSUZMIZ7SQ4L466GO77I65DM"  # ID da conta de destino para os dados
data_name = "example_key"  # Nome dos dados a serem armazenados
data_value = "example_value"  # Valor dos dados a serem armazenados

# Código de teste principal, que é executado quando o script é rodado diretamente
if __name__ == "__main__":
    # Passando os argumentos corretos para as funções dentro do __main__
    add_data_to_account(account_id, data_name, data_value)  # Chama a função para adicionar dados à conta
    query_data(account_id, data_name)  # Chama a função para consultar os dados da conta

    encoded_value = "ZXhhbXBsZV92YWx1ZQ==" # # Valor codificado em Base64
    decoded_value = base64.b64decode(encoded_value).decode('utf-8') # # Decodificar a string Base64
    print(decoded_value)
