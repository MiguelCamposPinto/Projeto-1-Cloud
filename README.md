# 1) Iniciar o ambiente virtual:
> 1º
```
 py -m venv venv 
```
  Ou
```
 python3 -m venv venv  

```

> 2º
```
pip install -r back/requirements.txt 
```

> 3º

``` 
 .\venv\Scripts\Activate.ps1  
```
</br>



---
---


</br>

# 2) 1º terminal.
    Rodar esses comandos para iniciar a aplicação e e o conteiner docker com o mysql:

> 1º Inicia o conteiner docker com mysql na porta 3306.
```
docker run -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=appdb -p 3306:3306 -d mysql:5.7
```

> 2º Define as variaveis de ambiente e inicializa o schema no DB
```
$env:DB_HOST = "127.0.0.1"
$env:DB_USER = "root"
$env:DB_PASS = "rootpass"
$env:DB_NAME = "appdb"

python back/scripts/init_db.py
```

> 3º Inicia o server da aplicação na porta 8085.
```
cd back/
flask run --host=0.0.0.0 --port=8085
```

</br>



---
---


</br>

# 3) 2º terminal(aberto simultaneo ao primeiro).
    OBS: Se ainda não estiver dentro do ambiente virtual, entrar! (passo 1)
    Rodar os testes:

- Testes Unitarios:
```
pytest back/tests/unit
```

- Testes de Integração:
```
pytest back/tests/integration
```


</br>



---
---


</br>

* Obs: Ao fazer o commit os testes de CI ja rodam automaticamente no workflow do github.
        Pode ser visualizado na aba "Actions" na pagina do projeto.
