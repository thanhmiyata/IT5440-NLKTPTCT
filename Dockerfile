# Base image: Ubuntu 22.04 (ARM64 compatible)
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
# - build-essential: GCC, Make, etc.
# - cmake, ninja-build: Build systems
# - git: Version control
# - python3: Required for LLVM build scripts
# - clang, lld: Compiler and linker used to bootstrap the build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    python3 \
    clang \
    lld \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Clone the HWASanIO repository
RUN git clone https://github.com/Fraunhofer-AISEC/hwasanio-llvm-project.git

# Create build directory
WORKDIR /workspace/hwasanio-llvm-project
RUN mkdir -p build

# Configure the build using CMake
# We use the system Clang/LLD to build the custom LLVM
WORKDIR /workspace/hwasanio-llvm-project/build
RUN cmake ../llvm/ \
    -G Ninja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LLD=ON \
    -DLLVM_TARGETS_TO_BUILD='AArch64' \
    -DLLVM_ENABLE_PROJECTS='clang;lld;compiler-rt'

# Build the project (This will take a while)
RUN ninja

# Add the built binaries to PATH
ENV PATH="/workspace/hwasanio-llvm-project/build/bin:${PATH}"

# Reset working directory to project root
WORKDIR /workspace/hwasanio-llvm-project

# Default command
CMD ["/bin/bash"]
