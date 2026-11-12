# API de Fluxo de Caixa

API Flask para cadastro e autenticação de usuários e registro de entradas e
saídas financeiras. Os lançamentos são associados ao identificador do usuário
presente na identidade do JWT. A aplicação cria as tabelas do banco de dados
durante a inicialização.

## Autenticação

- O login gera um token de acesso e um token de atualização JWT.
- Os tokens são enviados em cookies `HttpOnly`; os endpoints protegidos esperam
  o cookie de acesso.
- O token de acesso expira após 30 minutos. `POST /auth/refresh` exige o cookie
  com um token de atualização válido e renova o cookie de acesso.
- A configuração atual define `JWT_COOKIE_SECURE = false`; portanto, os cookies
  não são marcados como `Secure`. Configure essa opção para uso em produção com
  HTTPS.
- Os endpoints marcados como protegidos abaixo exigem autenticação JWT.

As rotas não têm um prefixo global adicional:

| Grupo | Prefixo |
|---|---|
| Autenticação | `/auth` |
| Fluxo financeiro | `/data` |
| Usuário | `/user` |

Os exemplos de JSON mostram os campos lidos pelo código. Não há validação de
campos obrigatórios, enums para forma de pagamento/categoria ou formato de data
definidos de maneira consistente nas rotas. A maioria das rotas não define
status HTTP explicitamente; mensagens de erro em JSON não garantem, por si só,
um status de erro, e handlers sem retorno de sucesso podem resultar em erro
500 do Flask.

## Autenticação — `/auth`

### POST `/auth/subscribe` — Criar conta

Recebe credenciais e o nome do usuário. O endpoint cria um registro de
autenticação e um registro de usuário com `admin` igual a `0`. A senha é
armazenada com hash bcrypt.

**Requisição**

```json
{
  "name": "Nome do usuário",
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "senha"
}
```

**Resposta de sucesso**

```json
{
  "msg": "Conta criada com sucesso"
}
```

Em caso de exceção, a rota retorna `{"erro":"Erro ao tentar criar conta"}`.

### POST `/auth/login` — Autenticar usuário

Recebe nome de usuário e senha. Na resposta, define cookies JWT de acesso e de
atualização e retorna os dados básicos da conta.

**Requisição**

```json
{
  "username": "usuario",
  "password": "senha"
}
```

**Resposta**

```json
{
  "data": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@example.com"
  }
}
```

Em caso de exceção, a rota retorna `{"erro":"Erro ao logar"}`. **Limitação
atual:** embora exista uma verificação de senha, o resultado dela não é usado
para interromper a autenticação antes da emissão dos tokens. Portanto, não
considere a validação de senha confiável até que essa implementação seja
corrigida.

### POST `/auth/refresh` — Renovar token de acesso

Exige o cookie JWT de atualização (`refresh`). Cria um novo cookie JWT de
acesso; o corpo informa os dados básicos da conta.

**Resposta**

```json
{
  "data": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@example.com"
  }
}
```

## Fluxo financeiro — `/data`

Todos os endpoints deste grupo exigem JWT. Um lançamento contém `name`,
`value`, `quantity`, `payment`, `categorie` e `type_data`; o registro também
armazena `id`, `id_user`, `create_at` e `updated_at`. `type_data` é booleano:
`false` é tratado como despesa e `true` como entrada. Categorias e formas de
pagamento são texto livre no modelo.

### POST `/data/` — Criar lançamento

Cria lançamento para o usuário identificado pelo JWT.

**Requisição**

```json
{
  "name": "Exemplo",
  "value": 25.5,
  "quantity": 1,
  "payment": "cartao",
  "categorie": "alimentacao",
  "type_data": false
}
```

**Resposta**

```json
{
  "message": "Data criado com sucesso"
}
```

Em caso de exceção, retorna `{"error":"Erro ao criar fluxo"}`.

### GET `/data/all` — Listar lançamentos do usuário

Retorna todos os lançamentos associados ao usuário autenticado. Cada item
inclui os dados abaixo; `create_at` é convertido para texto e pode ser `null`.

**Resposta**

```json
[
  {
    "id": 1,
    "name": "Exemplo",
    "value": 25.5,
    "quantity": 1,
    "payment": "cartao",
    "categorie": "alimentacao",
    "type_data": false,
    "create_at": "2026-01-31 12:00:00"
  }
]
```

Sem lançamentos, a resposta é uma lista vazia (`[]`). Em caso de exceção,
retorna `{"error":"Erro ao buscar dados do usuário"}`.

### GET `/data/month` — Consultar lançamentos por data

A rota lê `date` de um corpo JSON e pretende retornar lançamentos do usuário
cujo `create_at` corresponda à data informada.

**Corpo lido pela rota**

```json
{
  "date": "2026-01-31"
}
```

**Limitação atual:** a rota instancia a função de consulta com dois argumentos,
mas a implementação aceita apenas um; assim, não há resposta de sucesso
funcional estabelecida. A exceção é convertida em
`{"error":"Erro ao buscar dados"}`. O formato efetivamente comparado com
`create_at` também não está definido como contrato de data.

### GET `/data/categories` — Listar categorias

Retorna as categorias distintas presentes nos lançamentos do usuário.

**Resposta**

```json
[
  "alimentacao",
  "transporte"
]
```

Sem categorias, retorna `[]`. Em caso de exceção, retorna
`{"error":"Error ao buscar dados"}`.

### GET `/data/percentcategories` — Consultar percentuais por categoria

Retorna uma lista com a categoria e um valor percentual calculado pelo código.
O cálculo usa despesas da categoria e o saldo líquido como base; não representa
necessariamente a participação de cada categoria no total de despesas.

**Resposta**

```json
[
  {
    "categorie": "alimentacao",
    "value": 25.0
  }
]
```

O campo `value` é arredondado para duas casas decimais. Em caso de exceção,
retorna `{"error":"Error ao buscar do usuário"}`.

### GET `/data/flowdata` — Consultar resumo do fluxo

Retorna o saldo (`amount`), a soma de despesas (`expensive`) e a soma de
entradas (`gain`) calculados para o usuário.

**Resposta**

```json
{
  "data": {
    "amount": 0.0,
    "expensive": 0.0,
    "gain": 0.0
  }
}
```

Sem valores, os totais agregados usam `0.0`. Em caso de exceção, retorna
`{"error":"Erro a buscar dados"}`. O cálculo atual multiplica uma soma por um
valor `quantity` obtido separadamente; não há regra de negócio adicional
documentada para esse cálculo.

### PUT `/data/update/<id>` — Atualizar lançamento

Atualiza os campos do lançamento indicado pelo identificador na URL.

**Requisição**

```json
{
  "name": "Exemplo atualizado",
  "value": 30.0,
  "quantity": 1,
  "payment": "pix",
  "categorie": "alimentacao",
  "type_data": false
}
```

**Resposta**

```json
{
  "message": "Dados atualizados com successo"
}
```

Em caso de exceção, retorna `{"error":"Erro ao atualizar dados"}`. O código
localiza o lançamento pelo ID, mas não confere se ele pertence ao usuário do
JWT.

### DELETE `/data/delete/<id>` — Excluir lançamento

Exclui o lançamento indicado pelo identificador na URL. Exige JWT.

**Resposta no código atual:** não há corpo de sucesso retornado pela rota.
Em caso de exceção, retorna `{"error":"Erro ao deletar dados"}`. Assim como na
atualização, a exclusão busca pelo ID sem conferir a propriedade do lançamento
pelo usuário autenticado.

## Usuário — `/user`

Todas as rotas deste grupo exigem JWT. As respostas de sucesso de algumas
rotas não estão implementadas corretamente; os detalhes abaixo descrevem o
comportamento encontrado, não um contrato presumido.

### GET `/user/` — Consultar usuário autenticado

A rota lê `username`, `email` e `password` de um corpo JSON e tenta buscar o
usuário associado à identidade do JWT.

**Corpo lido pela rota**

```json
{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "senha"
}
```

**Limitação atual:** o método de busca está declarado sem `self`, embora seja
chamado como método de instância, e seu resultado também não é retornado pela
rota. No estado atual, a chamada cai no tratamento de exceção e retorna
`{"erro":"Erro ao tentar criar conta"}`; não há corpo de sucesso funcional.

### GET `/user/users` — Listar usuários

Chama a função de consulta de usuários, mas o método está declarado sem `self`
e a paginação chamada internamente também não recebe os parâmetros exigidos.
No estado atual, a chamada cai no tratamento de exceção e retorna
`{"error":"Error ao tentar requisitar todos os usuários"}`.

### POST `/user/client/<id>` — Consultar usuário pelo ID

A rota tenta buscar o usuário indicado por `id`.

**Limitação atual:** o método chamado está declarado sem `self`, embora seja
chamado como método de instância. A execução cai no tratamento de exceção e
retorna `{"erro":"Erro ao tentar criar conta"}`. Além disso, a implementação
usa `json.dump` sobre um objeto de modelo SQLAlchemy, o que também não produz
uma resposta JSON válida.

### PUT `/user/updateuser` — Atualizar usuário autenticado

Recebe `name` e tenta atualizar o nome do usuário identificado pelo JWT.

**Requisição**

```json
{
  "name": "Novo nome"
}
```

**Limitação atual:** a operação de atualização não retorna uma resposta de
sucesso na rota. Em caso de exceção, retorna `{"error":"erro ao atualizar usuário"}`.

### DELETE `/user/deleteuser` — Excluir usuário autenticado

Exclui o usuário associado à identidade do JWT.

**Resposta de sucesso**

```json
{
  "message": "Usuário deletado com sucesso"
}
```

Em caso de exceção, retorna `{"error":"Error ao tentar deletar usuários"}` e
status HTTP `500`.

## Configuração

A aplicação carrega variáveis de ambiente para a conexão do SQLAlchemy e a
chave de assinatura JWT. O arquivo `exemple.env` indica os nomes esperados:

```dotenv
SQLALCHEMY_DATABASE_URI=
SECRET_KEY_JWT=
```

No código, o valor lido para `JWT_SECRET_KEY` usa a variável `SECRET_KEY`,
enquanto o exemplo de ambiente apresenta `SECRET_KEY_JWT`. Esses nomes precisam
ser alinhados na configuração para que o JWT funcione corretamente. Não
compartilhe nem versione valores reais de conexão ou chaves secretas.