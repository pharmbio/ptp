# PTP Project

## Overview
> This project is designed to process and analyze molecular data using Ligand based models run with CPSign. It includes components for data storage, processing, and web-based interaction.


<img width="867" alt="Screenshot 2024-10-18 at 14 56 57" src="https://github.com/user-attachments/assets/a7518347-6969-445b-8cec-78824c536373">

## Running the project
1. Navigate to the specified serving url.
2. Upload a csv smiles file.
> Se the example in test/smiles_example.csv for valid input file format.

## Local Installation
There are two options. Docker-compose is fast to get started. The alternative and production-like alternative is skaffold. See skaffold.dev for more information on how to run.
### Usage

To use this project, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/pharmbio/ptp.git
    cd ptp
    ```

2. **Run the application**:
    ```sh
    docker-compose up --build
    ```

## Deployment

### Kubernetes Deployment
1. Modify values.yaml according to your specification.

2. **Deploy using Helm**:
    ```sh
    helm install --upgrade charts/ptp --values values.yaml
    ```
> Note: The deployment will create a Job to fetch all depdendency models before starting services. This may take some time since there are 10Gb+ downloadables.
> This is only needed on load (new version) or reload of model library.

### Docker Deployment
1. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

### Scilifelab Serve Deployment

1. Build container
    ```sh
    docker build -t ptp .
    ```
2. Push container to registry

3. Deploy
    - By default the folder /app/ext_storage/ should be mounted to outside storage to avoid ram bloat. It will contain database, media, and models.
    - Place the downloaded models (from https://huggingface.co/pharmbio/ptp) to /app/ext_storage/models/

4. Configuration
    - Currently static files are served by Django itself even with DEBUG=False
    - All defaults of environmental variables make sense for SciLifeLab Serve. Here are some environmental variables that can be changed if needed:
    - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER` etc for email settings.
    - `MAX_MODELS` to limit the number of active models (for debug purposes) .otherwise it iterates all models present (currently 800+).
    - `MEDIA_DIR` for media directory
    - `MODEL_DIR` for models directory
    - `DATABASE_DIR` for database directory
    - `SITE_URL` for generating download links in emails


## References
Model repository on Hugging Face: [pharmbio/ptp](https://huggingface.co/pharmbio/ptp)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Authors
- **Jonathan Alvarsson** - *Research, scipipe version and models* - [jonathanalvarsson](https://github.com/jonalv) 
- **Morgan Ekmefjord** - *Web service, deployment and service packaging* - [morganekmefjord](https://github.com/morganekmefjord)
