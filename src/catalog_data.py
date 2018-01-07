from sqlite3 import connect
import src.catalog_errors as catalog_errors


def make_category(context, name):
    """
    Returns tuple (id, name, created_at, modified_at).
    """
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            # Write row

            insert_query = '''
                INSERT INTO category("name",
                                     "created_at", "modified_at")
                VALUES (?,
                        strftime('%s', 'now'), strftime('%s', 'now'));
            '''
            cursor.execute(insert_query, (name,))
            connection.commit()

            # Pull results

            fetch_query = '''
                SELECT id, name, created_at, modified_at
                  FROM category
                 WHERE id=?;
            '''

            cursor.execute(fetch_query, (cursor.lastrowid,))
            fetch_response = cursor.fetchone()

            cursor.close()

            return fetch_response
    except:
        raise catalog_errors.DBError()


def fetch_all_categories(context):
    """
    Returns list of tuples [(id, name, created_at, modified_at), ...].
    """
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            fetch_query = '''
                SELECT id, name, created_at, modified_at
                  FROM category;
            '''

            cursor.execute(fetch_query)
            fetch_response = cursor.fetchall()

            cursor.close()

            return fetch_response
    except:
        raise catalog_errors.DBError()


def make_item(context, name, description):
    """
    Returns tuple (id, name, description, created_at, modified_at).
    """
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            # Write row

            insert_query = '''
                INSERT INTO item ("name", "description",
                                  "created_at", "modified_at")
                VALUES (?, ?,
                        strftime('%s', 'now'), strftime('%s', 'now'));
            '''
            cursor.execute(insert_query, (name, description))
            connection.commit()

            # Pull results

            fetch_query = '''
                SELECT "id",
                       "name",
                       "description",
                       "created_at",
                       "modified_at"
                  FROM item
                 WHERE id = ?;
            '''
            cursor.execute(fetch_query, (cursor.lastrowid,))
            fetch_response = cursor.fetchone()

            cursor.close()

            return fetch_response
    except:
        raise catalog_errors.DBError()


def fetch_item(context, item_id):
    """
    Returns tuple (id, name, description, created_at, modified_at).
    """
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            fetch_query = '''
                SELECT "id",
                       "name",
                       "description",
                       "created_at",
                       "modified_at"
                  FROM item
                 WHERE id = ?;
            '''
            cursor.execute(fetch_query, (item_id,))
            fetch_response = cursor.fetchone()

            cursor.close()

            return fetch_response
    except:
        raise catalog_errors.DBError()


def update_item(context, item_id, name=None, description=None):
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            if name:
                update_name_query = '''
                    UPDATE item
                    SET name = ?
                    WHERE id = ?;
                '''
                cursor.execute(update_name_query,
                               (name, item_id))

            if description:
                update_description_query = '''
                    UPDATE item
                    SET description = ?
                    WHERE id = ?;
                '''
                cursor.execute(update_description_query,
                               (description, item_id))

            cursor.close()
            connection.commit()
    except:
        raise catalog_errors.DBError()


def delete_item(context, item_id):
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            delete_query = '''
                DELETE FROM item
                 WHERE id = ?;
            '''
            cursor.execute(delete_query, (item_id,))

            cursor.close()
    except:
        raise catalog_errors.DBError()


def fetch_all_items(context, order_by, order, limit):
    """
    Returns list of tuples
    [(id, name, description, created_at, modified_at), ...].
    """
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            order_by_arg = 'created_at' if order_by.lower() == 'age' else 'id'
            order_arg = 'DESC' if order.lower() == 'descend' else 'ASC'

            fetch_query = '''
                  SELECT id, name, description, created_at, modified_at
                    FROM item
                ORDER BY %s %s
                   LIMIT ?
            ''' % (order_by_arg, order_arg)

            cursor.execute(fetch_query, (limit,))
            fetch_response = cursor.fetchall()

            cursor.close()

            return fetch_response
    except:
        raise catalog_errors.DBError()


def add_category_item_relationship(context, category_id, item_id):
    try:
        connection = connect(context.db_uri)
        with connection:
            cursor = connection.cursor()

            # Write row

            insert_query = '''
                INSERT INTO category_item("category_id", "item_id")
                VALUES (?, ?);
            '''
            cursor.execute(insert_query, (category_id, item_id))
            connection.commit()

            cursor.close()
    except:
        raise catalog_errors.DBError()
