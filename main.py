import client


def main():
    f = open("client_info.txt")
    client_id = f.readline()
    client_secret = f.readline()
    test_client = client.Client(client_id, client_secret)
    test_client.get_access_token()
    print(test_client.access_token)


if __name__ == '__main__':
    main()
