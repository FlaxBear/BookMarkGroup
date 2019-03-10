import db

base_db = db.Base_db()

base_db.startConnect()

table_info = {
    "table" : "test_sample",
    "param" : {
        "id": { "primary_key":"YES" },
        "name": { "primary_key":"NO" },
        "memo": { "primary_key":"NO" }
    }
}
result = ""

#insert_sql = base_db.createInsertSql(table_info)
insert_value = {
    "id" : "3",
    "name" : "aaaa",
    "memo" : "aaaa"
}
#result = base_db.insertExecute(insert_sql, insert_value)

# delete_value = {
#     "id": 2,
# }

# delate_sql = base_db.createDelateSql(table_info)
#result = base_db.delateExecute(delate_sql, delete_value)

# update_value = {
#     "id" : 2,
#     "name": "cccc",
#     "memo": "cccc"
# }


# sql = base_db.createUpdateSql(table_info)
# result = base_db.updateExecute(sql, update_value)


select_data = {
    "id": 2
}
sql = base_db.createSelectSql(table_info)
data, result = base_db.selectExecute(sql, select_data)
base_db.finishConnect()
print(type(data))
print(result)