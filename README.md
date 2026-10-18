# 💅 Agenda Sheila Nail Designer

Bem-vindo ao repositório oficial do aplicativo de agendamento e controle financeiro desenvolvido especialmente para a **Sheila Nail Designer**, localizada em **Capivari - SP**! 

Este sistema foi pensado para ser extremamente leve, rápido, gratuito e fácil de usar no dia a dia do estúdio de beleza.

---

## 🌟 Funcionalidades Principais

* **🗓️ Agenda Inteligente:** Organização de horários por data e hora separados, facilitando a visualização dos próximos atendimentos.
* **👥 Cadastro de Clientes:** Armazenamento de nomes, telefones de contato e observações essenciais (como alergias, preferências por esmaltação em gel ou técnicas como fibra de vidro).
* **💰 Controle de Pagamentos:** Registro prático das formas de pagamento utilizadas em cada atendimento:
  * 📱 PIX
  * 💳 Cartão de Crédito
  * 💳 Cartão de Débito
  * 💵 Dinheiro
* **📊 Painel Financeiro:** Acompanhamento em tempo real do faturamento previsto e do total de agendamentos e clientes cadastrados.

---

## 🚀 Como Funciona?

O aplicativo foi construído com uma arquitetura moderna e portátil:
* **Frontend:** HTML5, CSS3 com **Bootstrap 5** (responsivo para celular e computador) e JavaScript puro.
* **Armazenamento:** Utiliza o `localStorage` do navegador, garantindo privacidade, velocidade e funcionamento local imediato sem necessidade de servidores complexos de banco de dados.
* **Backend:** Servidor em **Python (Flask)** para execução local e integração pronta para hospedagem gratuita na nuvem (via **Render**).

---

## 💻 Como Rodar Localmente

Se você deseja testar o sistema no seu computador:

1. Clone o repositório ou baixe os arquivos na sua máquina.
2. Crie e ative um ambiente virtual Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
