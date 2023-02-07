import sqlite3 as sq

def sq_start():
    global db, cur
    db = sq.connect('basket.db')
    cur = db.cursor()
    if db:
        print('Database connected successfully')
    db.execute("pragma foreign_keys = ON;")
    db.execute("""create table if not exists shop(
    brend text,
    catalog text,
    subcatalog text,
    item_id text primary key)
    """)
    db.execute("""create table if not exists items(
        item_id text references shop(item_id) on delete cascade,
        name text,
        size text,
        count int,
        price int,
        foreign key (item_id) references shop(item_id) on delete cascade)
        """)
    db.commit()

def add_to_shop(shop_item):
    cur.execute("insert into shop values(?,?,?,?);", shop_item)
    db.commit()

def add_to_items(item):
    size_lst = item[2].split(';')
    count_lst = item[3].split(';')
    for i in range(0, len(size_lst)-1):
        cur.execute("insert into items values(?,?,?,?,?);", (item[0], item[1], size_lst[i], int(count_lst[i]), int(item[4])))
        db.commit()
    db.commit()

def delete_brend_from_sql(brend):
    cur.execute(f"delete from shop where brend = '{brend}'")
    db.commit()

def delete_catalog_from_sql(brend, catalog):
    cur.execute(f"delete from shop where brend = '{brend}' and catalog = '{catalog}'")
    db.commit()

def delete_subcatalog_from_sql(brend, catalog, subcatalog):
    cur.execute(f"delete from shop where brend = '{brend}' and catalog = '{catalog}' and subcatalog = '{subcatalog}'")
    db.commit()

def delete_unknown_item_from_shop(brend, catalog, subcatalog):
    cur.execute(f"select item_id from shop where brend = '{brend}' and catalog = '{catalog}' and subcatalog = '{subcatalog}'")
    items = cur.fetchall()
    for item in items:
        if item[0].find("Unknown") != -1:
            cur.execute(f"delete from shop where item_id = '{item[0]}'")
            db.commit()
    db.commit()

def delete_item_from_sql(item_id):
    cur.execute(f"delete from shop where item_id = '{item_id}'")
    db.commit()

def get_brends():
    cur.execute(f"select * from shop;")
    result = cur.fetchall()
    return result

def get_catalog(name_of_brend):
    cur.execute(f"select * from shop where brend='{name_of_brend}';")
    result = cur.fetchall()
    return result

def get_subcatalog(name_of_catalog, name_of_brend):
    cur.execute(f"select * from shop where brend='{name_of_brend}' and catalog='{name_of_catalog}';")
    result = cur.fetchall()
    return result

def get_items(name_of_subcatalog, name_of_catalog, name_of_brend):
    cur.execute(f"select item_id from shop where brend='{name_of_brend}' and catalog='{name_of_catalog}' and subcatalog='{name_of_subcatalog}'")
    items = cur.fetchall()
    result = {}
    try:
        for item in items:
            cur.execute(f"select * from items where item_id='{item[0]}'")
            result[cur.fetchone()[0]] = cur.fetchone()[1]
        return result
    except:
        return result

def get_item(item_id):
    cur.execute(f"select * from items where item_id='{item_id}'")
    result = cur.fetchall()
    return result

def gen_item_msg(item_id):
    cur.execute(f"select * from items where item_id='{item_id}'")
    items = cur.fetchall()
    size= ""
    first = items[0]
    for item in items:
        size += f"{item[2]}, "
    result = f"""*{first[1]}*\n
    *Артикул*\: {first[0]}\n
    *Размеры*\: {size}\n
    *Цена*\: {first[4]} руб\."""
    return result

def change_item_price(item_id, new_price):
    cur.execute(f"update items set price={new_price} where item_id='{item_id}'")
    db.commit()

def change_size_count(size, new_count):
    cur.execute(f"update items set count={new_count} where size='{size}'")
    db.commit()

def get_row_count():
    cur.execute("select count(*) from shop")
    result = cur.fetchone()
    return  result[0]

def get_item_id_for_client(name_of_subcatalog, name_of_catalog, name_of_brend):
    cur.execute(f"select item_id from shop where brend='{name_of_brend}' and catalog='{name_of_catalog}' and subcatalog='{name_of_subcatalog}'")
    items = cur.fetchall()
    result = []
    for item in items:
        result.append(item[0])
    return result