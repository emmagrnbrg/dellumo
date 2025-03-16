DIGITS = "0123456789"

EXPIRATION_MINUTES = 15  # время жизни процесса (запроса на регистрацию / восстановление пароля / ...)
MAX_ATTEMPTS_COUNT = 3  # максимальное число попыток подтверждения одноразового кода
CODE_LIFE_TIME = 3  # время жизни одноразового кода в минутах

REFRESH_TOKEN_LIFETIME = 43200  # время жизни refresh-токена, 30 дней
ACCESS_TOKEN_LIFETIME = 30  # время жизни access-токена
