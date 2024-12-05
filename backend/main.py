import os

from dotenv import load_dotenv

from app import create_app, config


def main():
    load_dotenv()

    debug = get_boolean_env_var('DEBUG')
    setup_config()
    app = create_app()

    config.Config.create_temp_dirs()

    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5123))
    app.run(debug=debug, host=host, port=port)


def setup_config(debug=False):
    config.APP_CONFIG = config.Config(
        ELASTIC_URL=os.getenv('ELASTIC_URL'),
        OPENAI_API_KEY=os.getenv('OPENAI_API_KEY'),
        DEBUG=debug
    )


def get_boolean_env_var(env_var: str) -> bool:
    return os.getenv(env_var, 'False').lower() == 'true'


if __name__ == "__main__":
    main()
