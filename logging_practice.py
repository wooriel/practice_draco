import os
import logging
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

def logging_practice():
    # with logging_redirect_tqdm():
    epoch = 10
    with tqdm(range(epoch)) as pbar:
        for i in pbar:
            pbar.set_description("Epoch {}".format(i))
            if i == 4:
                record = "console logging redirected to `tqdm.write()`"
                LOG.info(record)
            pbar.set_postfix({'compressing':i})
                

if __name__ == "__main__":
    log = 'log'
    extension = '.txt'
    logfname = ''.join([log, extension])
    logpath = os.path.join(os.getcwd(), logfname)
    
    LOG = logging.getLogger('compress')
    LOG.handlers = []
    LOG.setLevel(logging.INFO)
    fhandler = logging.FileHandler(logpath)
    LOG.addHandler(fhandler)
    

    logging_practice()
    fhandler.close()