
# UC01 – Adicionar Tarefa

## Table of Contents

<details>

   <summary>Contents</summary>

1. [1. Objetivo](#1-objetivo)
1. [2. Atores](#2-atores)
1. [3. Escopo](#3-escopo)
1. [4. Stakeholders e Interesses](#4-stakeholders-e-interesses)
1. [5. Pré-condições](#5-pr-condies)
1. [6. Pós-condições](#6-ps-condies)
   1. [Sucesso – Nova tarefa criada](#sucesso--nova-tarefa-criada)
   1. [Sucesso – Tarefa existente atualizada](#sucesso--tarefa-existente-atualizada)
   1. [Cancelamento](#cancelamento)
   1. [Falha](#falha)
1. [7. Fluxo Principal – Criar Nova Tarefa](#7-fluxo-principal--criar-nova-tarefa)
1. [8. Fluxos Alternativos](#8-fluxos-alternativos)
   1. [A1 – Título duplicado encontrado](#a1--ttulo-duplicado-encontrado)
   1. [A2 – Usuário não confirma atualização](#a2--usurio-no-confirma-atualizao)
   1. [A3 – Título inválido](#a3--ttulo-invlido)
   1. [A4 – Erro de persistência](#a4--erro-de-persistncia)
1. [9. Regras de Negócio](#9-regras-de-negcio)
   1. [RN-UC01-01 – Duplicidade por título normalizado](#rn-uc01-01--duplicidade-por-ttulo-normalizado)
   1. [RN-UC01-02 – Atualização em caso de duplicidade](#rn-uc01-02--atualizao-em-caso-de-duplicidade)
   1. [RN-UC01-03 – Descrição vazia não altera](#rn-uc01-03--descrio-vazia-no-altera)
   1. [RN-UC01-04 – Registro de atualização](#rn-uc01-04--registro-de-atualizao)
   1. [RN-TAR-01 – Normalização do título no domínio](#rn-tar-01--normalizao-do-ttulo-no-domnio)
1. [10. Validações](#10-validaes)
1. [11. Mensagens ao Usuário (CLI)](#11-mensagens-ao-usurio-cli)
1. [12. Observações Técnicas](#12-observaes-tcnicas)

</details>

## 1. Objetivo

Permitir que o usuário adicione uma nova tarefa ao sistema.
Caso já exista uma tarefa com o mesmo **título normalizado**, o sistema deve perguntar se o usuário deseja **atualizar a descrição** da tarefa existente.

---

## 2. Atores

* **Ator Primário:** Usuário

---

## 3. Escopo

Aplicativo de Gerenciamento de Tarefas (interface CLI na iteração atual).

---

## 4. Stakeholders e Interesses

* **Usuário:**

  * Criar tarefas rapidamente
  * Evitar duplicidade de tarefas com o mesmo objetivo
  * Manter status e histórico da tarefa ao atualizar a descrição

* **Sistema:**

  * Garantir consistência dos dados
  * Centralizar validações e regras no domínio
  * Evitar duplicidades por variação de escrita (maiúsculas, espaços)

---

## 5. Pré-condições

* O sistema está em execução.
* O repositório de tarefas está disponível.

---

## 6. Pós-condições

### Sucesso – Nova tarefa criada

* Uma nova tarefa é persistida.
* O título é normalizado internamente.
* O status inicial da tarefa é **PENDENTE**.
* O sistema informa sucesso ao usuário.

### Sucesso – Tarefa existente atualizada

* A tarefa existente é mantida (ID, título e status).
* A descrição pode ser atualizada conforme regras de negócio.
* A data de atualização (`atualizada_em`) é registrada.
* O sistema informa o resultado da atualização.

### Cancelamento

* Nenhuma tarefa é criada ou alterada.
* O sistema informa o cancelamento da operação.

### Falha

* Nenhuma tarefa é persistida.
* O sistema informa o erro de validação ao usuário.

---

## 7. Fluxo Principal – Criar Nova Tarefa

1. O usuário solicita a funcionalidade **Adicionar Tarefa**.
2. O sistema solicita o **título** da tarefa.
3. O usuário informa o título.
4. O sistema solicita a **descrição** (opcional).
5. O usuário informa a descrição ou deixa em branco.
6. O sistema solicita à entidade `Tarefa` a criação da tarefa por meio do método `criar()`, que:

   * normaliza o título,
   * valida que o título não fique vazio.
7. O sistema consulta o repositório para verificar se existe tarefa com o mesmo **título normalizado**.
8. **Não existindo duplicidade**, o sistema persiste a nova tarefa.
9. O sistema exibe a mensagem:
   **“Tarefa criada com sucesso.”**

---

## 8. Fluxos Alternativos

### A1 – Título duplicado encontrado

**Ponto de extensão:** Passo 7 do Fluxo Principal.

1. O sistema encontra uma tarefa existente com o mesmo título normalizado.
2. O sistema pergunta ao usuário:
   **“Já existe uma tarefa com o título ‘X’. Deseja atualizar a descrição da existente? (S/N)”**
3. O usuário responde **S**.
4. O sistema tenta atualizar a descrição da tarefa existente conforme RN-UC01-03.
5. O sistema registra a atualização da tarefa.
6. O sistema exibe:

   * **“Descrição atualizada com sucesso.”**, se a descrição foi alterada
   * **“Nenhuma alteração aplicada na descrição.”**, se a descrição foi preservada

---

### A2 – Usuário não confirma atualização

**Ponto de extensão:** Passo 2 do Fluxo A1.

1. O usuário responde **N**.
2. O sistema não altera nenhuma tarefa.
3. O sistema exibe:
   **“Operação cancelada. Nenhuma tarefa foi alterada.”**

---

### A3 – Título inválido

**Ponto de extensão:** Passo 6 do Fluxo Principal.

1. O título informado, após normalização, resulta em valor vazio.
2. A entidade `Tarefa` rejeita a criação.
3. O sistema exibe:
   **“Título inválido. Informe um título não vazio.”**
4. O caso de uso é encerrado sem persistência.

---

### A4 – Erro de persistência

**Ponto de extensão:** Passos 8 ou 5 do Fluxo A1.

1. O sistema falha ao persistir a tarefa.
2. O sistema exibe mensagem de erro apropriada.
3. O caso de uso é encerrado sem garantia de persistência.

---

## 9. Regras de Negócio

### RN-UC01-01 – Duplicidade por título normalizado

A verificação de duplicidade deve ser feita com base no **título normalizado**, definido e mantido pela entidade `Tarefa`.

### RN-UC01-02 – Atualização em caso de duplicidade

Quando houver título duplicado e o usuário confirmar, o sistema deve atualizar **somente a descrição** da tarefa existente, preservando o status.

### RN-UC01-03 – Descrição vazia não altera

Se a nova descrição informada for vazia ou nula, a descrição existente deve ser preservada.

### RN-UC01-04 – Registro de atualização

Mesmo quando a descrição for preservada, o sistema deve registrar a atualização da tarefa (`atualizada_em`).

### RN-TAR-01 – Normalização do título no domínio

A normalização e validação do título são responsabilidades exclusivas da entidade `Tarefa`, realizadas durante a criação via método de fábrica.

---

## 10. Validações

* Título não pode ser vazio após normalização.
* Comparação de títulos é case-insensitive.
* Descrição é opcional.

---

## 11. Mensagens ao Usuário (CLI)

* “Informe o título da tarefa:”
* “Informe a descrição (opcional):”
* “Já existe uma tarefa com o título ‘X’. Deseja atualizar a descrição da existente? (S/N)”
* “Tarefa criada com sucesso.”
* “Descrição atualizada com sucesso.”
* “Nenhuma alteração aplicada na descrição.”
* “Operação cancelada. Nenhuma tarefa foi alterada.”
* “Título inválido. Informe um título não vazio.”

---

## 12. Observações Técnicas

* O caso de uso é implementado no `AdicionarTarefaService`.
* O domínio não lança exceções para regras de negócio; utiliza controle explícito via `Resultado`.
* A interface de confirmação é desacoplada por meio de porta (`IConfirmacaoUI`).

---

📌 **Status:** UC01 **finalizado e validado em execução real**.

