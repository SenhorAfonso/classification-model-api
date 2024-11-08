# TrustMail 🛡️📧<br>
Projeto de Classificação de E-mails<br>
Trabalho AEP - Engenharia de Software, 6º Semestre<br>

📋 Descrição do Projeto
O TrustMail é um sistema desenvolvido para classificar e-mails entre seguros e phishing, utilizando técnicas de Machine Learning. O projeto foi desenvolvido como parte de um trabalho acadêmico (AEP) no curso de Engenharia de Software, 6º semestre.

A aplicação utiliza um modelo de classificação de e-mails construído com PyTorch para identificar possíveis e-mails de phishing. O modelo está integrado a uma API desenvolvida em Django, que expõe endpoints para realizar predições, possibilitando que outras aplicações ou serviços façam uso do classificador.
O classificador foi desenvolvida para ser consumida pelo [nosso aplicativo móvel](https://github.com/rhayssaandretto/gmail-doppelganger), desenvolvido em Flutter, que é o responsável por recolher e listar os emails dos usuários, que foram classificados com ajuda desse modelo.

# 🚀 Tecnologias Utilizadas
- Python 🐍
- PyTorch 🔥 (para a construção do modelo de Machine Learning)
- Django 🌐 (para a construção da API)
- Scikit-learn 📊 (para pré-processamento e métricas)
- TfidfVectorizer (para transformar os e-mails em representações numéricas)

# 🛠️ Como Rodar o Projeto
## Pré-requisitos
- Python 3.8+
- Pip
- Virtualenv (recomendado)
  
1. Clonar o Repositório

```
git clone https://github.com/SenhorAfonso/classification-model-api.git
cd classification-model-api
```

2. Criar e Ativar um Ambiente Virtual

```
python -m venv venv
venv/Scripts/activate
```

3. Instalar as Dependências

```
pip install -r requirements.txt
```

5. Rodar o Servidor

```
python manage.py runserver
```

A aplicação estará disponível em http://localhost:8000.

6. Testar o Modelo de Classificação
Você pode enviar uma requisição POST para o endpoint /model/predict/ com o conteúdo do e-mail para classificar. Exemplo de uso com curl:

bash
Copiar código
curl -X POST http://localhost:8000/model/predict/ \
-H "Content-Type: application/json" \
-d '{"email": "Verify your MetaMask Wallet Our system has shown that your MetaMask wallet has not yet been verified, this verification can be done easily via the button below."}'

# 📊 Resultados do Modelo
O modelo foi treinado usando um conjunto de dados com e-mails rotulados como seguros ou phishing, utilizando a técnica TF-IDF para vetorização e um classificador com rede neural em PyTorch. Após treinamento e validação, o modelo apresentou os seguintes resultados:

Acurácia: 97.5% <br>
Precisão: 92% <br>
Recall: 94% <br>


Desenvolvido por:
[Pedro Sena](https://www.linkedin.com/in/senhorafonso/) <br>
[Rhayssa Andretto](https://www.linkedin.com/in/rhayssa-andretto/) <br>
[Vinicius kenji ](https://www.linkedin.com/in/vin%C3%ADcius-kenji-439b38246/) <br>
