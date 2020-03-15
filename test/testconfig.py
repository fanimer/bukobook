
if __name__ == '__main__':
    with open(r'..\flaskr\schema.sql') as f:
        string = f.read()
    query = string.split(';')[:-1]
    query = [_.replace('\r', '') for _ in query]
    query = [_.replace('\n', '') + ';' for _ in query]
    print(query)
