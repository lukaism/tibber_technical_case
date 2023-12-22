TIBBER TECHNICAL CASE

## Getting Started

These instructions will help you set up and run the project locally.

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

To run the code inside a Docker container, use the following steps:


1. Clone the repository to your local machine:

```bash
git clone https://github.com/lukaism/tibber_technical_case.git
```

2. Navigate to the project directory:

```bash
cd tibber_tecnical_case
```
3. Build and start the Docker containers:
```bash
docker-compose up
```
This will build the necessary images and start the application. You can access the application at http://localhost:5000.

note: This will execute the tests on  aswell to check everything is in order.
    
4. From this point you should be able to interact with the endpoint locally using a tool such as postman:

POST http://localhost:5000/tibber-developer-test/enter-path
Body raw(json)
```json
{
  "start": {
    "x": 10,
    "y": 22
  },
  "commands": [
    {
      "direction": "east",
      "steps": 2
    },
    {
      "direction": "north",
      "steps": 1
    }
  ]
}
```

5. To stop the containers, press Ctrl + C in the terminal, and then run:
```bash
docker-compose down
```

As a side note, the .gitignore file, exeptionally doesn't target the .env file on purpose to make the verification easier.
Right now the code is targeting a hosted postgres database but feel free to insert your own postgres url connection in the .env file.



### Running Tests
To run tests, use the following steps:

1. Build the test container:
```bash
docker-compose build
```
2. Run the tests:
```bash
docker-compose run test
```




