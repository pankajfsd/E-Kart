from utils import dataReader, configReader, validation, mailService
# Importing necessary modules from the utils package.
# - dataReader: for reading data from files
# - configReader: for reading configuration settings
# - validation: for validating data
# - mailService: for sending emails

import shutil
# Importing the shutil module for file operations like copying files.
import datetime
# Importing the datetime module for handling date and time operations.
import os
# Importing the os module for interacting with the operating system, like file and directory operations.

if __name__ == "__main__":
    # The main entry point of the script. Code inside this block will only run if the script is executed directly.

    try:
        # Wrapping the main logic in a try block to catch and handle any exceptions.

        # print(validation.get_product_price_dict())
        # Uncommenting this line would print the product price dictionary for debugging purposes.

        email_date = datetime.date.today().strftime('%Y-%m-%d')
        # Getting today's date in the format 'YYYY-MM-DD' for use in the email subject.
        subject = f'Validation email for {email_date}'
        # Creating the email subject with the current date.

        today = configReader.get_today()
        # Getting today's date from the configuration settings.

        incoming_file_path, file_list = dataReader.get_file_list()
        # Getting the path of the incoming files and the list of files to process.

        # print(incoming_file_path)
        # print(file_list)
        # Uncommenting these lines would print the incoming file path and file list for debugging.

        success_folder = configReader.get_application_config("FILE_PATH")['success.file.path']
        rejected_folder = configReader.get_application_config("FILE_PATH")['rejected.file.path']
        incoming_folder = configReader.get_application_config("FILE_PATH")['incoming.file.path']
        # Reading the directory paths for success, rejected, and incoming files from the configuration.

        success_files_path = f'{success_folder}/{today}'
        rejected_files_path = f'{rejected_folder}/{today}'
        incoming_files_path = f'{incoming_folder}/{today}'
        # Constructing the full paths for success, rejected, and incoming files, including today's date.

        total_cnt = len(file_list)
        # Counting the total number of files to be processed.

        if total_cnt > 0:
            # Proceeding only if there are files to process.

            success_cnt = 0
            rejected_cnt = 0
            # Initializing counters for successful and rejected files.

            for file in file_list:
                # Looping through each file in the file list.

                flag = True
                header = False
                # Initializing a flag to indicate if the file processing was successful and a header flag for CSV
                # writing.

                orders = dataReader.read_orders_data(file)
                # Reading the orders data from the file and storing it as orders_list.

                print(orders)
                # Printing the orders for debugging.

                if len(orders) > 0:
                    # Proceeding if the file contains orders data.

                    for order in orders:
                        # Looping through each order in the file.

                        print(order)
                        # Printing the order for debugging.

                        rejected_reason = ''
                        pid_reject_reason = ''
                        empty_reject_reason = ''
                        date_reject_reason = ''
                        city_reject_reason = ''
                        sales_reject_reason = ''
                        order_dict = {}
                        # Initializing variables to store rejection reasons and an order dictionary to hold order
                        # details.

                        data_row = order.split(',')
                        # Splitting the order string by commas to extract individual fields.
                        order_dict['order_id'] = data_row[0]
                        order_dict['order_date'] = data_row[1]
                        order_dict['product_id'] = data_row[2]
                        order_dict['quantity'] = data_row[3]
                        order_dict['sales'] = data_row[4]
                        order_dict['city'] = data_row[5].strip()
                        # Populating the order dictionary with extracted fields.

                        # print(order_dict)
                        # Uncommenting this line would print the order dictionary for debugging.

                        prod_ids = validation.get_prod_ids()
                        # Getting the list of valid product IDs for validation.

                        val_pid = validation.validate_prod_id(order_dict['product_id'], prod_ids)
                        val_od = validation.validate_order_date(order_dict['order_date'])
                        val_city = validation.validate_city(order_dict['city'])
                        val_empty = validation.validate_emptiness(order_dict)
                        val_sales = validation.validate_sales(order_dict['product_id'], order_dict['sales'],
                                                              order_dict['quantity'])
                        # Validating various fields of the order.

                        if not val_pid:
                            pid_reject_reason = f"Invalid product id {order_dict['product_id']}"
                            rejected_reason += pid_reject_reason + ';'

                        if len(val_empty) > 0:
                            for col in val_empty:
                                empty_reject_reason += col + ','
                            empty_reject_reason = 'Columns ' + empty_reject_reason.strip(',') + ' are empty'
                            rejected_reason += empty_reject_reason + ';'

                        if not val_od:
                            date_reject_reason = f"Date {order_dict['order_date']} is a future date"
                            rejected_reason += date_reject_reason + ';'

                        if not val_city:
                            city_reject_reason = f"Invalid city {order_dict['city']}"
                            rejected_reason += city_reject_reason + ';'

                        if not val_sales and val_pid:
                            sales_reject_reason = f'Invalid Sales calculation'
                            rejected_reason += sales_reject_reason + ';'
                        # Constructing rejection reasons based on validation results.

                        if val_pid and val_od and val_city and len(val_empty) == 0 and val_sales:
                            continue

                        else:
                            flag = False

                            row_str = ''
                            if not os.path.exists(f'{rejected_files_path}'):
                                os.makedirs(f'{rejected_files_path}', exist_ok=True)
                            shutil.copy(f'{incoming_files_path}/{file}', f'{rejected_files_path}/{file}')
                            rejected_cnt += 1

                            with open(f'{rejected_files_path}/error_{file}', 'a') as f:
                                for key in order_dict.keys():
                                    row_str += order_dict[key] + ','

                                row_str += rejected_reason
                                row_str = row_str.strip(';')

                                if not header:
                                    f.write('order_id,order_date,product_id,quantity,sales,city,rejected_reason\n')
                                    header = True

                                f.write(row_str + '\n')

                        # If any validation fails, the order is rejected, and the file is copied to the rejected folder.
                        # The rejection reasons are written to a file with a header.

                    else:
                        if flag:
                            if not os.path.exists(f'{success_files_path}'):
                                os.makedirs(f'{success_files_path}', exist_ok=True)

                            shutil.copy(f'{incoming_files_path}/{file}', f'{success_files_path}/{file}')

                            success_cnt += 1

                        # If all validations pass, the file is copied to the success folder.

                else:
                    if not os.path.exists(f'{rejected_files_path}'):
                        os.makedirs(f'{rejected_files_path}', exist_ok=True)

                    shutil.copy(f'{incoming_files_path}/{file}', f'{rejected_files_path}/{file}')

                    with open(f'{rejected_files_path}/error_{file}', 'a') as f:
                        f.write("Empty file\n")
                    rejected_cnt += 1
                # If the file is empty, it is copied to the rejected folder, and an error message is written
                # by creating a file error_filename.

            else:
                body = f"""
                Total Files: {total_cnt} \n
                Successful Files: {success_cnt} \n
                Rejected Files: {rejected_cnt}
                """
                mailService.sendmail(subject, body)

                # After processing all files, an email is sent summarizing the results.

        else:
            mailService.sendmail(subject, "No file present in source folder.")
            # If no files are present to process, an email is sent indicating this.

    except Exception as e:
        print(str(e))
        # If an exception occurs, it is caught and printed.
