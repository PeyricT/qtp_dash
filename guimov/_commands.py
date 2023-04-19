from guimov import start


def _commands_guimov_launch():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="host ip adress", default='0.0.0.0')
    parser.add_argument("-p", "--port", help="host port", default='8050')
    args = parser.parse_args()

    start(host=args.host, port=args.port)
