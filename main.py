import client


def main():
    f = open("client_info.txt", 'r')
    client_id = f.readline().strip()
    client_secret = f.readline().strip()
    f.close()
    # print(client_id, client_secret)
    test_client = client.Client(client_id, client_secret)
    token = test_client.get_access_token()
    # print(token)


if __name__ == '__main__':
    main()
