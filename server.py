import argparse

import uvicorn


def get_server_mode() -> str:
    parser = argparse.ArgumentParser(description="Run the server in dev/prod mode.")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="dev",
        help="dev or prod",
        choices=["dev", "prod"],
    )
    args = parser.parse_args()
    return args.mode


def start_server(mode: str):
    app_import_path = "src.main:app"

    if mode == "prod":
        uvicorn.run(app_import_path, host="0.0.0.0", port=8000)
    else:
        uvicorn.run(app_import_path, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start_server(mode=get_server_mode())
