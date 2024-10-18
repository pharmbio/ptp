# PTP Project

## Overview
This project is designed to process and analyze molecular data using various tools and frameworks. It includes components for data storage, processing, and web-based interaction.

## Usage
To use this project, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://huggingface.co/pharmbio/ptp
    cd ptp
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```sh
    docker-compose up
    ```

## Deployment

### Kubernetes Deployment
1. **Create a Kubernetes secret for your Scaleway S3 credentials**:
    ```sh
    kubectl apply -f scaleway-secret.yaml
    ```

2. **Deploy using Helm**:
    ```sh
    helm install --upgrade charts/ptp --generate-name
    ```

### Docker Deployment
1. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

## References
Model repository on Hugging Face: [pharmbio/ptp](https://huggingface.co/pharmbio/ptp)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors
- **Jonathan Alvarsson** - *Research, scipipe version and models* - [jonathanalvarsson](https://github.com/jonalv) 
- **Morgan Ekmefjord** - *Web service, deployment and service packaging* - [morganekmefjord](https://github.com/morganekmefjord)
