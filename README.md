# Task Manager POO (RUP)
Projetode Gerenciamento de Tarefas em Python, usando POO estrita e fases do RUP.
## Estrutura
- `src/domain`: regras de negocio (entidades, value objects, erros)
- `src/application`: casos de uso (services, commands, resultados)
- `src/infrastructure`: persistencia (repositorios)
- `src/interface`: UI (CLI)
## Como rodar
```bash
python -m venv .venv
source .venv/bin/activate
python main.py
```
