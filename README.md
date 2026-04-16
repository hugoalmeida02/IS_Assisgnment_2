# Student-Course Management System (MCP + LangChain)

## Descrição

Este projeto implementa um sistema de gestão de estudantes e cursos, exposto através de:

- **REST API (FastAPI)**
- **Model Context Protocol (MCP)**
- **Agente com LangChain**

O sistema permite interação em **linguagem natural**, onde um agente interpreta pedidos e executa operações através do MCP.

---

## Contexto Académico

Universidade de Coimbra  
Mestrado em Engenharia Informática (MEI)  
Disciplina: Integração de Sistemas (2025/2026)

---

## Arquitetura

UI (Browser)
↓
FastAPI (/chat)
↓
LangChain Agent
↓
MCP Server
↓
Services (lógica de negócio)
↓
SQLite Database

---

## Funcionalidades

### Students
- Criar, listar, atualizar e remover estudantes

### Courses
- Criar, listar, atualizar e remover cursos
- Capacidade limitada

### Enrollments
- Inscrição de estudantes em cursos
- Inscrição por:
  - ID
  - Email

---

## Regras de Negócio

- Email de estudante é único  
- Nome de curso é único  
- Capacidade do curso deve ser > 0  
- Não é possível duplicar inscrições  
- Não é possível inscrever em cursos cheios  

---

## MCP Server

### Tools
- create_student
- create_course
- enroll_student
- list_students
- list_courses

### Resources
- school://schema
- school://report/courses
- school://report/students

### Prompts
- academic_assistant_prompt
- enrollment_help_prompt

---

## Agente (LangChain)

- Interpreta pedidos em linguagem natural  
- Decide automaticamente que tools usar  
- Usa prompt e resources para contexto  
- Mantém memória de interação  

---

## Como executar

#### 1. Criar ambiente virtual
```bash
python -m venv venv
```

#### 2. Ativar ambiente virtual
```bash
venv\Scripts\activate
```

#### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 4. Configurar variável de ambiente
Criar ficheiro `.env` na raiz do projeto:
```text
OPENAI_API_KEY=your_api_key_here
```

#### 5. (Opcional) Popular base de dados
```bash
python -m app.seed
```

#### 6. Executar aplicação
```bash
uvicorn app.main:app --reload
```

## Aceder à aplicação

- API Docs: http://127.0.0.1:8000/docs  
- Interface Web: http://127.0.0.1:8000/ui  


---

## Exemplos de uso

List all students  
Create a student named João with email joao@example.com  
Create a course called Security with capacity 1  
Enroll joao@example.com in course 1  

---

## Autor

- Hugo Almeida — 2021234629  
