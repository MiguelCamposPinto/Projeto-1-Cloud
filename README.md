# Guia de Execução do Projeto
Aqui será descrito como configurar o ambiente, iniciar a aplicação Flask integrada ao MySQL e executar os testes unitários e de integração exigidos

</br>

# 1) Preparar o Ambiente Virtual:
### 1. Criar o ambiente virtual. Utilize o seguinte comando
```
 py -m venv venv 
```
  Ou
```
 python3 -m venv venv  

```

### 2. - Instalar as dependências
```
pip install -r back/requirements.txt 
```

### 3. - Ativar o ambiente

``` 
 .\venv\Scripts\Activate.ps1  
```

---
---


</br>

# 2) Subir MySQL + Inicializar Banco + Rodar Aplicação
Todas as etapas abaixo devem ser executadas no **1º terminal**, com o ambiente virtual ativado.

### 1. Inicia o conteiner docker com mysql na porta 3306.
```
docker run -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=appdb -p 3306:3306 -d mysql:5.7
```

### 2. Exportar variáveis de ambiente e inicializar o schema:
```
$env:DB_HOST = "127.0.0.1"
$env:DB_USER = "root"
$env:DB_PASS = "rootpass"
$env:DB_NAME = "appdb"

python back/scripts/init_db.py
```

### 3. Iniciar o servidor Flask (porta 8085):
```
cd back/
flask run --host=0.0.0.0 --port=8085
```
A API estará disponível em:

👉 http://localhost:8085

---
---

</br>

# 3) Executar os Testes (Unitários e Integração)
Os testes devem ser executados em um **2º terminal** simultâneo ao primeiro, com o ambiente virtual também ativado.

### Ativar ambiente virtual (caso não esteja ativo):
```
.\venv\Scripts\Activate.ps1
```

### ✔ Testes Unitários:
```
pytest back/tests/unit/
```

### ✔ Testes de Integração:
```
pytest back/tests/integration/
```
### ✔ Rodar todos os testes:
```
pytest
```

---
---

</br>


# 4) Pipeline Automático no GitHub
Sempre que um **commit** ou **pull request** é feito para a branch `main`,
o workflow do GitHub Actions é acionado automaticamente:

- Sobe container MySQL  
- Instala dependências  
- Inicializa o banco  
- Executa todos os testes  

Você pode acompanhar os resultados em:

👉 Aba “Actions” no GitHub do projeto

--- 
