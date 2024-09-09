FROM apeworx/silverback:latest

USER harambe

WORKDIR /app

RUN mkdir -p .build && chown harambe:harambe .build
COPY --chown=harambe:harambe ./bots/* ./bots/
COPY --chown=harambe:harambe ./contracts/* ./contracts/

COPY ape-config.yaml ape-config.yaml
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN ape compile

ENV WORKERS=1
ENV MAX_EXCEPTIONS=3

ENTRYPOINT silverback worker -v DEBUG -w $WORKERS \
    -x $MAX_EXCEPTIONS --account bot "bots.example:app"
