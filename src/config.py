import os
import typing

from fastapi_mail import ConnectionConfig
from pydantic import BaseModel, DirectoryPath, NewPath, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

GeneratedPath = NewPath | DirectoryPath
LoggingSettings = dict[typing.Any, typing.Any]


class AppSettings(BaseModel):
    name: str
    version: str


class ApiSettings(BaseModel):
    max_avatar_size: int
    min_password_length: int
    max_password_length: int


class PathSettings(BaseModel):
    logs: GeneratedPath
    media: GeneratedPath
    locales: DirectoryPath
    templates: DirectoryPath

    def model_post_init(self, _: typing.Any) -> None:
        attrs = self.__annotations__.items()
        generated_path_attrs = (attr for attr, attr_type in attrs if attr_type == GeneratedPath)
        for attr in generated_path_attrs:
            pathname = getattr(self, attr)
            os.makedirs(pathname, exist_ok=True)


class JWTSettings(BaseModel):
    secret: str
    algorithm: str
    expire_minutes: int


class OTPSettings(BaseModel):
    min: int
    max: int
    expire_minutes: int

    @computed_field
    @property
    def length(self) -> int:
        return len(str(self.max))


class RedisSettings(BaseModel):
    host: str


class PostgresSettings(BaseModel):
    username: str
    password: str
    port: int
    host: str
    path: str

    @computed_field
    @property
    def uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.path,
        )


class SMTPSettings(BaseModel):
    username: str
    password: str
    port: int
    server: str
    starttls: bool
    ssl_tls: bool
    use_credentials: bool
    validate_certs: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(yaml_file="config.yaml", extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: typing.Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> typing.Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)

    debug: bool

    app: AppSettings
    api: ApiSettings
    path: PathSettings
    jwt: JWTSettings
    otp: OTPSettings
    redis: RedisSettings
    postgres: PostgresSettings
    smtp: SMTPSettings
    logging: LoggingSettings

    @computed_field
    @property
    def MAIL_CONNECTION_CONF(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self.smtp.username,
            MAIL_PASSWORD=self.smtp.password,
            MAIL_PORT=self.smtp.port,
            MAIL_SERVER=self.smtp.server,
            MAIL_STARTTLS=self.smtp.starttls,
            MAIL_SSL_TLS=self.smtp.ssl_tls,
            MAIL_DEBUG=self.debug,
            MAIL_FROM=self.smtp.username,
            MAIL_FROM_NAME=self.app.name,
            USE_CREDENTIALS=self.smtp.use_credentials,
            VALIDATE_CERTS=self.smtp.validate_certs,
        )


settings = Settings()  # type: ignore
