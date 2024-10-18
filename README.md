# PTP Project

## Overview
This project is designed to process and analyze molecular data using various tools and frameworks. It includes components for data storage, processing, and web-based interaction.

## Usage
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
