from scripts import extract, save_to_csv, save_to_mysqldb



def main():
    # Extract the data
    extracted_data = extract()

    # Save the data to csv files
    save_to_csv(extracted_data)

    # Save the data to MYSQL Database
    save_to_mysqldb(extracted_data, user = 'mohamed')





if __name__ == '__main__':
    main()