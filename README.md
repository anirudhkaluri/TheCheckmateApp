INSTRUCTIONS TO RUN THE PROJECT:

1) Clone the repository at https://bitbucket.org/infilectassignment/chessapp/
2) Open the terminal and navigate into the chessapp directory cloned to your local machine
3) Execute the following command:
	$docker compose up -d --build

The command starts the app at 127.0.0.1:8000. Kill if any process is already running on that address.


API End Point: 127.0.0.1/chess/<string:slug>
Method: POST
Body: JSON data with chessboard positions



INSTRUCTIONS TO TEST THE PROJECT
After the App starts running, there are three ways to test:

1) UNIT TESTS: Run the following command in the terminal
		$docker compose exec web python manage.py test

    • Class ValidMovesTest: Tests get_valid_moves method in chess/utils/validMoves.py module. There are 7 unique tests to test the core logic of the application. 

    • ClassPositionViewTest: Tests PositionView that uses Django REST framework to handle API calls. One positive test and two tests with invalid request format have been tested 

    • Class PositionSerializerTest:Tests PositionSerializer that validates incoming data. One positive test and two tests with invalid request format have been tested




2) TESTING WITH CURL
    • Open CurlTests.txt file present in the directory.
    • Copy a curl command.
    • Run it in the command line on the terminal.
    • Verify the output with the expected output present in the same file.
    • Repeat for all the Curl commands testing different scenarios


3) IMPORT TESTS INTO POSTMAN

    • Open Postman desktop application
    • Click on File
    • Select import
    • Browse to the Infilect.postman_collection.json file present in the directory.
    • Add as a new collection
    • Run each request in the collection



For details regarding the project, please refer to the Documentation.pdf file.
In case of any queries and further elaborations I request you to contact me.