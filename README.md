
# DynamoDB - Basic crud operations using python3.6



## Important
Note that the script will use credentials in : ~/.aws/credentials. 
you can run `aws configure` to generate the config.
Instructions can be found [here](https://docs.aws.amazon.com/cli/latest/reference/configure/) 

## Description

 1. Start by running `python3 write_data.py`. This will automatically
    create the database (if not created). Next it will continue by
    populating the table using data fetched from [here](https://www.breakingbadapi.com/api/characters).
 2. Run `python3 read_data.py` to search for a character by name (using
    GlobalSecondaryIndexes) and also get a character by ID.
 3. Run `python3 update_data.py` to update the nickname of the character
    as well as the occupations (dict).
 4. Run `python3 delete_data.py` to delete a character with a given ID
    and name.
