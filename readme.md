This repository contains Gate simulation examples. 
# GATE Exercices
 

## Prerequisites
- You **MUST** install the [git-lfs](https://git-lfs.github.com) extension. Download the package and use:
    ```sh
    git lfs install
    ```
- **WARNING**: There are some issues with the LFS binary data stored here. Only use HTTP (not SSH) to clone:
    ```sh
    git lfs clone https://github.com/rtmedical/gate-samples.git
    ```

## Running GATE with Docker

### Using Docker Directly
To run GATE with Docker on your computer (Unix system), assuming you already have the macro in your computer, you can do:

```sh
cd folder/containing/macFolder
docker run -i --rm -v $PWD:/APP opengatecollaboration/gate mac/main.mac
```

### Using Docker Compose
We have provided a `docker-compose.yml` file in the folder. To use it, follow these steps:

 
1. Run the Docker Compose setup:
     ```sh
     docker-compose build && docker-compose up -d
     ```

This will start the GATE environment as defined in the `docker-compose.yml` file.

## Additional Information
For more details and advanced usage, refer to the [GATE Exercices Site](https://davidsarrut.pages.in2p3.fr/gate-exercices-site/).
