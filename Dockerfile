FROM jjanzic/docker-python3-opencv

RUN mkdir -p /detection/stream

WORKDIR /detection

COPY stream/* /detection/stream/

RUN pip install image && pip install Pillow

COPY liveStreaming.py .

VOLUME ["/detection/stream"]

ENTRYPOINT ["python", "liveStreaming.py"]