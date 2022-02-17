import argparse
import logging.config
from datetime import datetime
from config import Logger
from src.domain.usecases.scraper_doktuz import scrapper_doktuz
from src.domain.usecases.scraper_doktuz_excel import scrapper_doktuz_excel

def readParams():
    parser = argparse.ArgumentParser(description='Extract data from Doktuz web page')
    
    parser.add_argument('op', type=str, choices=['pdf','excel'], 
                   help='pdf:to get certificates and Imp values, excel:to get excel file')
    
    parser.add_argument('--initDate', '-i', dest='i', type=str,
                        help="enter init-date in format dd-mm-yyyy",default=datetime.today().strftime('%d-%m-%Y'))
    
    parser.add_argument('--endDate', '-e', dest='e', type=str,
                        help="enter end-date in format dd-mm-yyyy", default=datetime.today().strftime('%d-%m-%Y'))
    
    parser.add_argument('--days', '-d', dest='d', type=str,
                        help="parse range from init and end date taking n days parameter, required only for op=excel ", default=7)

    args = parser.parse_args()
    
    return args
def run_doktuz(init_date, end_date):
    Logger.info("La aplicación para obtener PDF empezo a las: {}".format(datetime.now()))
    scrapper_doktuz(init_date, end_date)
    Logger.info("La aplicación para obtener PDF finalizo a las: {}".format(datetime.now()))
    logging.shutdown()

def run_doktuz_excel(init_date, end_date, by):
    Logger.info("La aplicación para obtener EXCEl empezo a las: {}".format(datetime.now()))
    scrapper_doktuz_excel(init_date, end_date, by)
    Logger.info("La aplicación para obtener EXCEl finalizo a las: {}".format(datetime.now()))
    logging.shutdown()

def main():
    args = readParams()
    if(args.op== 'pdf'):
        assert args.i != None, 'init day parameter is required'
        assert args.e != None, 'end day parameter is required'
        run_doktuz(args.i, args.e)
    elif(args.op == 'excel'):
        assert args.i != None, 'init day parameter is required'
        assert args.e != None, 'end day parameter is required'
        assert args.d != None, 'days parameter is required'
        run_doktuz_excel(args.i, args.e, args.d)
    else:
        raise Exception('op parameter is required')

#main()

if __name__ == "__main__": # EJECUCION POR INTERFAZ GRAFICA
    Logger.info("La aplicación empezo a las: {}".format(datetime.now()))
    run_doktuz('13-01-2022', '13-01-2022')
    #run_doktuz_excel('25-01-2022', '08-02-2022', 7)
    Logger.info("La aplicación finalizo a las: {}".format(datetime.now()))
    logging.shutdown()
# EJECUCION POR TERMINAL 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
# scrapy runspider ./src/domain/usecases/get_data.py -o doktuz.csv -t csv 

