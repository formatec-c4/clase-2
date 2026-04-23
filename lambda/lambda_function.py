def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": "<h1>¡Hola Clase de Cloud!</h1><p>Servidor funcionando en AWS Lambda.</p>",
    }
