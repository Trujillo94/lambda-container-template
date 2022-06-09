# Define function directory
ARG FUNCTION_DIR="/function"

FROM python:3.10-slim

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    pkg-config \
    python-dev \
    g++ \
    make \
    cmake

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY . ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install \
    --target ${FUNCTION_DIR} \
    awslambdaric

WORKDIR ${FUNCTION_DIR}

# Install requirements
RUN pip3 --no-cache-dir install -r requirements.txt

# Copy in the build image dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "main.handler" ]