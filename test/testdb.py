import pymysql

if __name__ == '__main__':
    conn = pymysql.connect('localhost', 'root', '123456',
                           'account', cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    post_id = 2
    cur.execute(
        'SELECT c.id, username, body, reply_to, by_reply'
        ' FROM comment c JOIN user u ON c.reviewer_id = u.id'
        ' WHERE post_id = %s ORDER BY created', (1, 2)
    )
    rv = cur.fetchall()
    print(rv)
