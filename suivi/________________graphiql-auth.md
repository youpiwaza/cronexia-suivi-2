# Ne pas se taper "errors": > "message": "Unauthorized" > "statusCode": 401

```graphql
mutation Login($data: LoginInput!) {
  login(data: $data) {
    accessToken
    refreshToken
    tokenType
  }
}
```

```json
{
  "data": {
    "login": "super.admin",
    "password": "P!zz@&T@c0$#FTW"
  }
}
```

Récupérer le header renvoyé ~

```json
{
  "data": {
    "login": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMjZhOTBjNy1hMTY2LTQ5ZTctODRkYy0zOTE2ODVjN2YwNTUiLCJzdXBpIjoiMDAwMDAwMDAtMDAwMC0wMDAwLWZmZmYtMTExMTExMTExMTExIiwic3VwYyI6IlNVUEVSX0FETUlOIiwiaWF0IjoxNzY4NDc0MzcwLCJleHAiOjE3Njg0NzUyNzB9.siyaLLp5jOhpmKny0SSJ5JyisIpq13hcFWllSjdqnDc",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMjZhOTBjNy1hMTY2LTQ5ZTctODRkYy0zOTE2ODVjN2YwNTUiLCJzdXBpIjoiMDAwMDAwMDAtMDAwMC0wMDAwLWZmZmYtMTExMTExMTExMTExIiwic3VwYyI6IlNVUEVSX0FETUlOIiwiaWF0IjoxNzY4NDc0MzcwLCJleHAiOjE3Njg3MzM1NzB9.Y3jFNFkYzNzRKDAQ4FAd60uS_OsQuVYbf-Ld_2itTR0",
      "tokenType": "Bearer"
    }
  }
}
```

Puis avec la future requête renvoyer dans les headers (en bas à côté de variables)

```json
{
  "Authorization" : "Bearer ACCESS_TOKEN"
}

~


{
  "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMjZhOTBjNy1hMTY2LTQ5ZTctODRkYy0zOTE2ODVjN2YwNTUiLCJzdXBpIjoiMDAwMDAwMDAtMDAwMC0wMDAwLWZmZmYtMTExMTExMTExMTExIiwic3VwYyI6IlNVUEVSX0FETUlOIiwiaWF0IjoxNzY4NDc0MzcwLCJleHAiOjE3Njg0NzUyNzB9.siyaLLp5jOhpmKny0SSJ5JyisIpq13hcFWllSjdqnDc"
}
```
