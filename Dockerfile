FROM ghcr.io/darpa-askem/askem-julia:latest AS JULIA_BASE_IMAGE

FROM python:3.10

USER root

# Install custom Julia
ENV JULIA_PATH=/usr/local/julia
ENV JULIA_DEPOT_PATH=/usr/local/julia
ENV JULIA_PROJECT=/home/jupyter/.julia/environments/askem

COPY --chown=1000:1000 --from=JULIA_BASE_IMAGE /usr/local/julia /usr/local/julia
COPY --chown=1000:1000 --from=JULIA_BASE_IMAGE /ASKEM-Sysimage.so /Project.toml /Manifest.toml /home/jupyter/.julia/environments/askem/
RUN chmod -R 777 /usr/local/julia/logs
RUN ln -sf /usr/local/julia/bin/julia /usr/local/bin/julia

# Install r-lang and kernel
RUN apt update && \
    apt install -y r-base r-cran-irkernel \
        graphviz libgraphviz-dev \
        libevent-core-2.1-7 libevent-pthreads-2.1-7 && \
    apt clean -y && \
    apt autoclean -y


WORKDIR /mira

# Install Mira from github
RUN git clone https://github.com/indralab/mira.git /mira && \
    pip install --no-cache-dir /mira/"[ode,tests,dkg-client,sbml]" && \
    rm -r /mira

# Install project requirements
COPY --chown=1000:1000 pyproject.toml README.md hatch_build.py /askem_beaker/
COPY --chown=1000:1000 . /askem_beaker/

# Installs the askem specific subkernels
RUN pip install --no-cache-dir --upgrade /askem_beaker

RUN pip install --upgrade /askem_beaker/beaker_kernel-1.2.3-py3-none-any.whl

WORKDIR /askem_beaker

# Switch to non-root user. It is crucial for security reasons to not run jupyter as root user!
RUN useradd -m jupyter
USER jupyter

# Install Julia kernel (as user jupyter)
RUN /usr/local/julia/bin/julia -J /home/jupyter/.julia/environments/askem/ASKEM-Sysimage.so -e 'using IJulia; IJulia.installkernel("julia"; julia=`/usr/local/julia/bin/julia -J /home/jupyter/.julia/environments/askem/ASKEM-Sysimage.so --threads=4`)'

CMD ["python", "-m", "beaker_kernel.server.main", "--ip", "0.0.0.0"]

