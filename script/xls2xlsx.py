import glob
import os
import time
import pandas as pd

class excelConvert():
    def __init__(self):
        self.path = os.getcwd()
        xlsxdirname = "xlsx"
        xlsxpath = os.path.join(self.path, xlsxdirname)

        if not os.path.exists(xlsxpath):
            print(f"create directory: {xlsxdirname}")
            os.makedirs(xlsxpath)
        self.xlsxpath = xlsxpath

    def batch_convert(self):
        xls_files = glob.glob(self.path + "/*.xls")
        if len(xls_files) != 0:
            print('xls files：')
            for file in xls_files:
                print(os.path.basename(file))

                fname, _ = os.path.splitext(file)
                basename = os.path.basename(fname)
                xlsxpathname = os.path.join(self.xlsxpath, basename)
                self.saveasxlsx(file, xlsxpathname)
        else:
            print('no xls, exit...')
            time.sleep(2)
            os._exit(0)

    def saveasxlsx(self, xlspath, xlsxpath):
        writer = pd.ExcelWriter(xlsxpath + '.xlsx')
        datas = pd.read_excel(xlspath,sheet_name=None)
        for sheetname, values in datas.items():
            data = pd.DataFrame(values)
            data.to_excel(writer, sheet_name=sheetname)
        writer.save()
        writer.close()

if __name__=='__main__':
    excel = excelConvert()
    excel.batch_convert()