# Mig's Bot — pacote para Silly Development

## Arquivos
- `bot.py`: bot Discord com `/script`, `/help`, `.help` e `/source`.
- `requirements.txt`: dependências Python.
- `.env.example`: nomes das variáveis necessárias; não contém segredos.
- `sillydev.conf`: lembrete de configuração, não contém tokens.

## Instalação na Silly Development
1. Extraia este ZIP no seu computador.
2. No painel Silly Development, crie um servidor/serviço com runtime **Python**.
3. Envie os arquivos extraídos usando o File Manager/SFTP ou conecte um repositório Git.
4. Na aba **Startup**, configure o arquivo principal como `bot.py` (ou o comando `python bot.py`).
5. Nas variáveis de ambiente do servidor, adicione:
   - `DISCORD_TOKEN` = token do bot Discord
   - `AUTHORIZED_USER_ID` = ID numérico do usuário autorizado a usar `/source`
6. Instale as dependências do `requirements.txt` se o painel não fizer isso automaticamente.
7. Inicie o servidor e confira o console. O log deve mostrar que os comandos slash foram sincronizados e que o bot conectou.

## Discord
Para o comando de texto `.help`, habilite **Message Content Intent** em Discord Developer Portal → Bot → Privileged Gateway Intents.

## Observações
- Não coloque o token em `bot.py`, no ZIP, em repositórios públicos ou em mensagens.
- O `/source` envia uma cópia efêmera dos arquivos atuais incluídos no pacote; não inclui tokens.
- O bot apenas exibe texto Lua cadastrado. Ele não executa loaders.
- Os links do catálogo são de terceiros e podem mudar, exigir chaves ou deixar de funcionar.
- A hospedagem contínua depende da disponibilidade e das regras atuais do provedor.
