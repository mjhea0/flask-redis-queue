import time

from project.server.main import ds
from project.server.main.utils import packing


def create_job(texts, file_names, byte_datas, webhook_endpoint, delay, tic):
    try:
        time.sleep(int(delay))
        webhook_endpoint = webhook_endpoint
        byte_data_lengths = []
        for byte_data in byte_datas:
            byte_data_lengths.append(len(byte_data))
        toc = time.time()
        output_object = ds.OutputObject(
            time=toc - tic,
            texts=texts,
            file_names=file_names,
            byte_data_lengths=byte_data_lengths,
            webhook_endpoint=webhook_endpoint,
            delay=delay,
            tic=tic,
        )
        pickled_object = packing(source_object=output_object)
        return pickled_object
    except Exception as e:
        e.webhook_endpoint = webhook_endpoint
        e.tic = tic
