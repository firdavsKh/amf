
configObject = {
    "config_version":"001",
    "report_name":"1HK",
    "tables":[
        {
            "table_id":"БД",
            "table_type":"fixed",# varieble_rows / varieble_columns
            "nodes":[
                {
                    "id":"total_employed",
                    "address":"A1",
                    "read_ender":True, # если в этой колонке он не видел значение, он задумывается остановить чтение или нет
                    "data_tape":"int",
                    "length":7,
                    "is_empty_allowed":True,
                    "is_negative_allowed":True,
                    "attribute":[
                        {
                            "attr_type":"region",
                            "attr_value":"boxtar",
                        }
                    ]
                },
                {
                    "id":"total_employed",
                },
                {
                    "id":"total_employed",
                },
            ]
        },
    ]
    
    
    

}